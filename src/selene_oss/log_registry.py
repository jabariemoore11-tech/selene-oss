from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Iterable, Sequence


class LogNotFoundError(LookupError):
    """Raised when a requested log cannot be resolved from registered sources."""


@dataclass(frozen=True)
class LogSource:
    """A trusted directory of log files.

    The registry only resolves logs discovered inside registered roots. Caller
    supplied paths are treated as names, not filesystem access grants.
    """

    name: str
    root: Path
    source_type: str = "app"
    pattern: str = "*.log"


@dataclass(frozen=True)
class LogEntry:
    name: str
    path: Path
    source_name: str
    source_type: str
    bytes: int
    modified: str
    modified_ts: float

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["path"] = str(self.path)
        return data


@dataclass(frozen=True)
class LogTail:
    entry: LogEntry
    text: str
    lines: int
    redacted: bool


class Redactor:
    """Redact common secret shapes before logs are shown to humans or agents."""

    SECRET_PATTERNS: Sequence[re.Pattern[str]] = (
        re.compile(r"sk-[A-Za-z0-9._-]{6,}"),
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{12,}"),
        re.compile(r"xox[baprs]-[A-Za-z0-9-]{12,}"),
        re.compile(r"AIza[0-9A-Za-z_-]{12,}"),
        re.compile(r"Bearer\s+[A-Za-z0-9._~+/-]{12,}", re.IGNORECASE),
        re.compile(
            r"\b(password|passwd|token|api[_-]?key|secret)\s*=\s*([^\s]+)",
            re.IGNORECASE,
        ),
    )

    def redact(self, text: str) -> tuple[str, bool]:
        redacted = False
        out = text or ""
        for pattern in self.SECRET_PATTERNS:
            if pattern.search(out):
                redacted = True
                if pattern.groups >= 2:
                    out = pattern.sub(lambda m: f"{m.group(1)}=[REDACTED]", out)
                elif pattern.pattern.lower().startswith("bearer"):
                    out = pattern.sub("Bearer [REDACTED]", out)
                else:
                    out = pattern.sub("[REDACTED]", out)
        return out, redacted


class LogRegistry:
    """Source-aware log discovery and safe reading.

    Register every root explicitly. Missing roots are ignored so fresh installs
    can report an empty log set instead of crashing.
    """

    def __init__(self, *, redactor: Redactor | None = None) -> None:
        self._sources: list[LogSource] = []
        self._redactor = redactor or Redactor()

    def register_source(
        self,
        name: str,
        root: str | Path,
        *,
        source_type: str = "app",
        pattern: str = "*.log",
    ) -> LogSource:
        source = LogSource(
            name=str(name),
            root=Path(root).expanduser(),
            source_type=str(source_type),
            pattern=str(pattern or "*.log"),
        )
        self._sources.append(source)
        return source

    @classmethod
    def for_project(
        cls,
        project_root: str | Path,
        *,
        temp_model_log_root: str | Path | None = None,
        redactor: Redactor | None = None,
    ) -> "LogRegistry":
        root = Path(project_root).expanduser()
        registry = cls(redactor=redactor)
        registry.register_source("app", root / "logs", source_type="app")
        registry.register_source("data", root / "data" / "logs", source_type="feature")
        if temp_model_log_root is not None:
            registry.register_source("model", temp_model_log_root, source_type="model-serve")
        return registry

    def list_logs(self) -> list[LogEntry]:
        entries: list[LogEntry] = []
        for source in self._sources:
            entries.extend(self._entries_for_source(source))
        entries.sort(key=lambda entry: (entry.modified_ts, entry.source_name, entry.name), reverse=True)
        return entries

    def resolve(self, name: str) -> LogEntry:
        if not isinstance(name, str) or not name.strip():
            raise LogNotFoundError("no log matching empty name")
        query = name.strip()
        matches = [
            entry
            for entry in self.list_logs()
            if entry.name == query or Path(entry.name).stem == query or query in entry.name
        ]
        if not matches:
            raise LogNotFoundError(f"no log matching {query!r}")
        return matches[0]

    def tail_log(self, name: str, *, lines: int = 80) -> LogTail:
        entry = self.resolve(name)
        raw = self._read_text(entry.path)
        count = max(0, int(lines))
        selected = raw.splitlines()[-count:] if count else []
        text = "\n".join(selected)
        if raw.endswith("\n") and text:
            text += "\n"
        text, redacted = self._redactor.redact(text)
        return LogTail(entry=entry, text=text, lines=count, redacted=redacted)

    def read_log(self, name: str) -> LogTail:
        entry = self.resolve(name)
        text, redacted = self._redactor.redact(self._read_text(entry.path))
        return LogTail(entry=entry, text=text, lines=len(text.splitlines()), redacted=redacted)

    def _entries_for_source(self, source: LogSource) -> Iterable[LogEntry]:
        root = source.root
        if not root.is_dir():
            return []
        root_resolved = root.resolve()
        entries: list[LogEntry] = []
        for path in sorted(root.glob(source.pattern)):
            if not path.is_file():
                continue
            try:
                resolved = path.resolve()
                resolved.relative_to(root_resolved)
                stat = path.stat()
            except (OSError, ValueError):
                continue
            entries.append(
                LogEntry(
                    name=path.name,
                    path=resolved,
                    source_name=source.name,
                    source_type=source.source_type,
                    bytes=stat.st_size,
                    modified=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                    modified_ts=stat.st_mtime,
                )
            )
        return entries

    @staticmethod
    def _read_text(path: Path) -> str:
        return path.read_text(encoding="utf-8", errors="replace")
