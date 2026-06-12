from __future__ import annotations

from pathlib import Path


def test_public_docs_define_clean_room_boundary():
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    inventory = (root / "docs" / "REFERENCE_INVENTORY.md").read_text(encoding="utf-8")

    assert "clean-room" in readme.lower()
    assert "not an Odysseus copy/paste" in readme
    assert "not source code" in inventory
    assert "LogRegistry" in inventory


def test_gitignore_blocks_private_runtime_state():
    root = Path(__file__).resolve().parents[1]
    gitignore = (root / ".gitignore").read_text(encoding="utf-8")

    for pattern in (".env", "data/", "logs/", "*.db", "receipts/"):
        assert pattern in gitignore
