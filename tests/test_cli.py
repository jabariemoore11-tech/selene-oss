from __future__ import annotations

import json
from pathlib import Path

from selene_oss.cli import main


def test_logs_list_cli_outputs_json_for_registered_root(tmp_path: Path, capsys):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "app.log").write_text("ready\n", encoding="utf-8")

    exit_code = main(["logs", "list", "--root", str(logs)])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["name"] == "app.log"
    assert payload[0]["source_name"] == "custom"


def test_logs_tail_cli_redacts_output(tmp_path: Path, capsys):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "app.log").write_text("token=secret-value\n", encoding="utf-8")

    exit_code = main(["logs", "tail", "app", "--root", str(logs), "--lines", "5"])

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "secret-value" not in out
    assert "[REDACTED]" in out
