# Security Policy

Selene OSS is intended as a local-first command OS for trusted users. Treat it like an admin console.

Do not expose it publicly without authentication, HTTPS, and a private access layer.

Never commit:

- `.env` files
- API keys or tokens
- local databases
- runtime logs
- receipts/artifacts containing private content
- uploaded files
- model provider credentials

Before publishing, run:

```bash
git status --short
git grep -n -I -E "(sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}|xox[baprs]-|AIza[0-9A-Za-z_-]{20,}|Bearer [A-Za-z0-9._~+/-]{20,})" -- . ':!LICENSE'
```
