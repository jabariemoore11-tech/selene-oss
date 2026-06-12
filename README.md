# Selene OSS

Clean-room command-OS primitives for local AI agents.

Selene OSS is not an Odysseus copy/paste. Odysseus is a useful reference for what a self-hosted AI workspace needs, but this repo rebuilds the control plane around original, testable primitives:

- WorkOrders
- RunLedger
- CapabilityVault
- ProofReceipts
- LogRegistry
- ModelRegistry
- MemoryGraph
- SkillCapsules
- typed Settings/Profile state
- state-driven cockpit UI contracts

## Current status

Pre-alpha. Slice 1 is LogRegistry: list, resolve, tail, and redact logs from known runtime surfaces.

## Design rule

If state is not wired, show `unknown`, `offline`, or `not configured`. Do not fake dashboard metrics.

## Development

```bash
python -m pytest -q
```

## Safety

Local runtime data, `.env`, logs, databases, receipts, and artifacts are git-ignored by default.
