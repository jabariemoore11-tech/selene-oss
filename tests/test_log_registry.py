from __future__ import annotations

from pathlib import Path

import pytest

from selene_oss.log_registry import LogNotFoundError, LogRegistry, Redactor


def test_registry_lists_app_data_and_model_logs_with_source_labels(tmp_path: Path):
    app_logs = tmp_path / "logs"
    data_logs = tmp_path / "data" / "logs"
    model_logs = tmp_path / "tmux"
    app_logs.mkdir()
    data_logs.mkdir(parents=True)
    model_logs.mkdir()
    (app_logs / "app.log").write_text("app online\n", encoding="utf-8")
    (data_logs / "search_engine_error.log").write_text("search failed\n", encoding="utf-8")
    (model_logs / "llama-serve.log").write_text("model loaded\n", encoding="utf-8")

    registry = LogRegistry()
    registry.register_source("app", app_logs, source_type="app")
    registry.register_source("data", data_logs, source_type="feature")
    registry.register_source("model", model_logs, source_type="model-serve")

    entries = registry.list_logs()

    assert {entry.name for entry in entries} == {
        "app.log",
        "search_engine_error.log",
        "llama-serve.log",
    }
    by_name = {entry.name: entry for entry in entries}
    assert by_name["app.log"].source_name == "app"
    assert by_name["search_engine_error.log"].source_type == "feature"
    assert by_name["llama-serve.log"].source_type == "model-serve"


def test_tail_log_redacts_secret_like_values(tmp_path: Path):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "app.log").write_text(
        "ok\n"
        "openai=sk-abc...3456\n"
        "auth=Bearer abcdefghijklmnopqrstuvwxyz.1234567890.token\n"
        "password=super-secret-value\n",
        encoding="utf-8",
    )
    registry = LogRegistry(redactor=Redactor())
    registry.register_source("app", logs)

    tail = registry.tail_log("app", lines=10)

    assert "sk-abc...3456" not in tail.text
    assert "Bearer abcdef" not in tail.text
    assert "super-secret-value" not in tail.text
    assert "[REDACTED]" in tail.text


def test_resolve_uses_exact_stem_or_substring_and_prefers_newest(tmp_path: Path):
    logs = tmp_path / "logs"
    logs.mkdir()
    old = logs / "first-worker.log"
    new = logs / "second-worker.log"
    old.write_text("old\n", encoding="utf-8")
    new.write_text("new\n", encoding="utf-8")
    old_mtime = 1000
    new_mtime = 2000
    import os

    os.utime(old, (old_mtime, old_mtime))
    os.utime(new, (new_mtime, new_mtime))
    registry = LogRegistry()
    registry.register_source("app", logs)

    assert registry.resolve("second-worker").name == "second-worker.log"
    assert registry.resolve("worker").name == "second-worker.log"


def test_missing_log_raises_clear_error(tmp_path: Path):
    registry = LogRegistry()
    registry.register_source("app", tmp_path / "missing")

    with pytest.raises(LogNotFoundError, match="no log matching"):
        registry.resolve("../secret")


def test_registered_paths_are_confined_to_source_root(tmp_path: Path):
    root = tmp_path / "logs"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (outside / "secret.log").write_text("password=hunter2\n", encoding="utf-8")
    registry = LogRegistry()
    registry.register_source("app", root)

    assert registry.list_logs() == []
    with pytest.raises(LogNotFoundError):
        registry.tail_log(str(outside / "secret.log"))
