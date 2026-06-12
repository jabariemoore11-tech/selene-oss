# Reference Inventory

This document records behavior-level lessons from existing self-hosted AI workspaces. It is not source code and should not be used to copy implementation details.

## Observed surfaces worth rebuilding as first-class Selene primitives

| Surface | Behavior lesson | Selene primitive |
|---|---|---|
| Model/provider setup | Users need endpoint records, provider probes, defaults, and fallbacks. | ModelRegistry |
| Local model serving | Users need cached model scan, running task state, and failure logs. | ModelWorld / CookbookBridge |
| Memory | Memory needs owner, scope, source, relevance, and import/export. | MemoryGraph |
| Skills | Skills need structured files, trigger rules, testing, and injection budgets. | SkillCapsules |
| Settings/prefs | Settings need defaults, user prefs, schema migrations, and safe export. | SettingsStore |
| Agent tools | Tools need side-effect declarations and policy below the model. | ToolContracts + ActionFirewall |
| Logs | Logs exist in app, data, model-serve, Docker, and browser surfaces. | LogRegistry |
| Diagnostics | Health should be proof-producing, not random admin output. | Doctor / Health Receipts |
| Shell/cockpit bridge | UI should call real runtime state, not branding-only static data. | Runtime State API |

## Known log roots for compatibility adapters

- `logs/*.log` for app/runtime logs
- `data/logs/*.log` for feature/provider logs
- temp model-serve logs, commonly `/tmp/odysseus-tmux/*.log`
- Docker/service-manager logs when running under containers
- optional browser/client error ring buffer
