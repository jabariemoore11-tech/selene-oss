# Selene Vision Draft

Status: draft, based on JB's selected direction. This is a product north star, not a finished spec.

## One-line picture

Selene is an Odysseus-inspired, clean-room command OS for local AI agents: a living cockpit for models, skills, memory, tools, logs, receipts, and real work.

The first public wedge is a developer/local-agent cockpit. The full product grows into a personal life OS with voice, projects, approvals, receipts, and safe autonomy.

## Identity stack

Selene is all four, in this order:

1. **Developer / agent cockpit** — repos, models, logs, tools, tests, failures, receipts.
2. **Personal life OS** — tasks, email drafts, calendar, notes, mobile commands, project lanes.
3. **Operator OS** — gets work done, proves it, stays quiet until needed.
4. **Living companion layer** — voice/personality after the operating spine is trustworthy.

## What Selene is not

- Not a generic chatbot.
- Not a fake dashboard.
- Not a prompt library with buttons.
- Not an agent swarm fantasy.
- Not automation without proof or stop controls.
- Not an Odysseus source copy. Odysseus is a reference point; Selene core is clean-room.

## Product principles

1. **State is visible.** If something is not wired, show `not configured`, `offline`, or `unknown`.
2. **Actions produce receipts.** Meaningful work should show command, scope, files touched, tools used, logs read, tests run, and rollback hints.
3. **Local-first, cloud-aware.** Prefer local models/tools when possible. Escalate intentionally.
4. **Autonomy needs rails.** Low-risk work can run. Safe writes are allowed. High-risk work needs exact approval. STOP must always work.
5. **Projects are lanes.** Each project defines allowed paths, test commands, proof rules, default skills, and risk boundaries.
6. **Logs are first-class.** Selene indexes, redacts, tails, and connects logs to failures and receipts.
7. **Motion must mean state.** Animation is allowed to be bold, but it cannot lie.

## Visual identity

Selene should feel like a dark command room with a living cortex.

The visual identity is not a tiny orb. It is a full cortex/world map:

- center: Selene cortex / command brain
- orbit: project lane, WorkOrders, models, skills, memory, receipts, logs, voice, STOP
- drawers: details, approvals, receipt browser, model world, skill loads, logs, doctor/autopsy

Visual direction:

- black/navy/graphite base
- moon-metal silver and cyan accents
- green only for verified/proof
- amber for approval/risk
- red for STOP/blocked
- readable technical type
- no gamer neon, no fake metrics

Cortex states:

- idle
- wake detected
- listening
- transcribing
- thinking
- executing
- approval needed
- blocked
- speaking
- stopped

## Voice direction

Target voice: warm British governess/operator energy.

Traits:

- precise
- calm
- competent
- a little magical
- politely bossy when needed
- never bubbly
- never corporate
- never fake-friendly

Implementation should still audition actual voices before locking it. The chosen voice must survive long sessions without getting annoying.


## Real-time voice requirement

Selene should stay armed for wake detection, not full ambient transcription.

Wake paths:

- name wake: `Selene`, with common mishearings like `Celine` normalized
- clap-clap wake: two local amplitude spikes inside a tuned timing window

Privacy rule:

- armed mode can detect wake locally
- full transcription starts only after wake/listen mode
- ambient speech before wake is not sent to STT/model, not stored, and not shown

After wake, speech should stream into an editable command text box as words are spoken.

Example target flow:

> "Selene, search and find cute dog pictures."

Selene should create a safe browser WorkOrder, open/reuse a browser, visibly type the query, submit the search, and produce a receipt. CDP/selector automation is primary; GUI fallback requires leases, previews, red-zone checks, STOP, and receipts.

## Core primitives

- LogRegistry
- SettingsStore
- ModelRegistry
- MemoryGraph
- SkillCapsules
- WorkOrders
- RunLedger
- CapabilityVault
- ProofReceipts
- ActionFirewall
- ProjectLanes
- VoiceStateMachine
- Blackbox / Autopsy / ReplayLab

## First public audience

Long-term audience is broad, but the first useful wedge should serve people who already feel the pain:

- solo devs running local agents on repos
- homelab/local-model users
- AI creators/operators running browser/model/content workflows
- productivity users later, after the rails are proven

## First public wedge

Reliability for local AI-agent work:

- inspect logs
- manage model endpoints and local model health
- show selected skills/memory
- create WorkOrders
- run tasks with receipts
- block unsafe actions
- recover from failures through blackbox records and replay tests

## Differentiator

Most agent tools either chat, run workflows, or show dashboards. Selene's difference is the control plane: visible state, explicit risk boundaries, receipts, STOP controls, and replayable failure recovery.

The promise:

> Selene turns local AI agents into an operating system you can trust — and a proof layer for autonomous work.

## System optimization, VPS, email, and automatic routing

Selene should eventually manage the machine it runs on, not just chat about work.

Safe optimizer target:

- read-only diagnosis first
- ranked optimization plans
- receipts and rollback notes
- no reckless cleanerware behavior
- no disabling security, backups, firewall, drivers, registry, BIOS, or user files without exact approval

Local VPS target:

- WSL2/Docker/systemd/Tailscale health
- service status, logs, backups, start/stop/restart plans
- private access first
- no public bind by default

Email/account target:

- per-user or per-install mailbox identities
- verification-code reading after authorization
- legitimate account setup workflows with approvals
- no shared global mailbox secret
- no spam, ban evasion, or account farming

Automatic routing target:

- skills selected from task/project/risk context
- models selected from task + hardware fit
- decisions shown before execution
- missing required skills or unsafe model authority blocks the run
