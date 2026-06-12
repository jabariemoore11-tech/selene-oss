"""Selene OSS clean-room command OS primitives."""

from .log_registry import LogEntry, LogNotFoundError, LogRegistry, LogSource, LogTail, Redactor

__all__ = [
    "LogEntry",
    "LogNotFoundError",
    "LogRegistry",
    "LogSource",
    "LogTail",
    "Redactor",
]

__version__ = "0.1.0"
