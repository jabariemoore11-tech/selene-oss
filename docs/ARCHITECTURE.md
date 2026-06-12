# Architecture

Selene OSS is a clean-room command OS spine.

```text
User / Voice / API
  -> Command Gateway
  -> WorkOrder
  -> Policy + Capability gates
  -> Tool adapters
  -> Proof receipts + logs
  -> State-driven cockpit
```

## Core primitives

- **LogRegistry**: source-aware log discovery, tailing, and redaction.
- **SettingsStore**: typed config + per-user prefs. Pending.
- **ModelRegistry**: local/cloud endpoint records + probes + lanes. Pending.
- **MemoryGraph**: scoped memory with trust/source labels. Pending.
- **SkillCapsules**: reusable procedures with trigger rules and verification receipts. Pending.
- **RunLedger**: durable WorkOrder lifecycle. Pending.
- **CapabilityVault**: scoped grants/leases. Pending.
- **ProofReceipts**: checksummed evidence of actions. Pending.

## UI rule

Every cockpit node must be backed by real state. Unknown state is rendered honestly.
