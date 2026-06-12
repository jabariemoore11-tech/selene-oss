# Contributing

Keep changes small and test-first.

Rules:

1. Write failing tests first.
2. Keep runtime control-plane primitives separate from UI.
3. Do not add fake dashboard state.
4. Do not hardcode private paths, users, projects, or credentials.
5. Mention exact verification commands in PRs.

Run:

```bash
python -m pytest -q
```
