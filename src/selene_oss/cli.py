from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .log_registry import LogNotFoundError, LogRegistry


def _registry_from_args(args: argparse.Namespace) -> LogRegistry:
    registry = LogRegistry()
    root = getattr(args, "root", None)
    if root:
        registry.register_source("custom", Path(root), source_type="custom")
    else:
        registry = LogRegistry.for_project(Path.cwd(), temp_model_log_root=Path("/tmp/selene-model-logs"))
    return registry


def _cmd_logs_list(args: argparse.Namespace) -> int:
    registry = _registry_from_args(args)
    sys.stdout.write(json.dumps([entry.to_dict() for entry in registry.list_logs()], indent=2) + "\n")
    return 0


def _cmd_logs_tail(args: argparse.Namespace) -> int:
    registry = _registry_from_args(args)
    try:
        tail = registry.tail_log(args.name, lines=args.lines)
    except LogNotFoundError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1
    sys.stdout.write(tail.text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="selene", description="Selene OSS command OS utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    logs = sub.add_parser("logs", help="inspect registered logs")
    logs_sub = logs.add_subparsers(dest="logs_command", required=True)

    logs_list = logs_sub.add_parser("list", help="list logs")
    logs_list.add_argument("--root", help="custom log root; defaults to project log roots")
    logs_list.set_defaults(func=_cmd_logs_list)

    logs_tail = logs_sub.add_parser("tail", help="tail a log by exact name, stem, or substring")
    logs_tail.add_argument("name")
    logs_tail.add_argument("--root", help="custom log root; defaults to project log roots")
    logs_tail.add_argument("--lines", type=int, default=80)
    logs_tail.set_defaults(func=_cmd_logs_tail)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
