# dChat

Open source Discord/forum hybrid with public read access and member-only interaction.

Current release baseline: `v1.2`

Live example:

- `https://forum.dek.cx/`

## What dChat ships with

- Public-readable topics and threads
- Member-only posting, replying, voting, and profile customization
- Built-in math CAPTCHA with no external API dependency
- Optional email verification, disabled by default
- Discord-inspired, forum-structured UI with real-time thread updates
- Nested replies, post permalinks, `@mentions`, and inbox notifications
- Direct messages with markdown/link embeds, image uploads, moderation queue, reports, soft delete, restore, and action logs
- Theme branding controls, including full color customization and the optional `dekcx` preset
- First-run setup wizard
- GDPR export/delete flows
- Backup, restore, and smoke-test scripts

## Default stack

The default install is intentionally small:

- Django
- PostgreSQL
- WhiteNoise for static assets
- Docker Compose

Optional full profile:

- Redis for shared cache
- Caddy for reverse proxy and TLS termination

There is no required worker process in the default release.

Tracked source footprint:

- `120` tracked files
- about `0.39 MB` before dependencies, media, and generated static output

## Quick start

Linux/macOS:

```bash
cp .env.example .env
docker compose up -d --build
```

PowerShell:

```powershell
Copy-Item .env.example .env
docker compose up -d --build
```

Open `http://localhost:8000` and complete `/setup`.

Optional full profile:

```bash
docker compose --profile full up -d --build
```

That adds Redis and Caddy. With the full profile, the app is served on `http://localhost` and `https://localhost`.

## First-run behavior

- If no users exist, dChat redirects to `/setup`
- The first created account becomes the initial admin
- The first created account is also user `id=1`
- The email on user `id=1` is used as the default public legal contact on the Terms, Privacy, and Cookies pages

Choose that first email accordingly.

## Public repo safety

This repo is safe to publish only if you keep local/operator data out of version control.

Do not commit:

- `.env`
- local databases
- uploaded media
- backups
- generated static output
- local editor/IDE files

The provided `.gitignore` is set up for that split.

## Operations

Useful scripts:

- `scripts/backup.sh` / `scripts/backup.ps1`
- `scripts/restore.sh` / `scripts/restore.ps1`
- `scripts/restore-test.sh` / `scripts/restore-test.ps1`
- `scripts/e2e-smoke.sh` / `scripts/e2e-smoke.ps1`

Runtime pages:

- Changelog: `/changelog/`
- Docs: `/docs/readme/`, `/docs/install/`, `/docs/faq/`

## Notes

- Guest users can read but cannot interact
- Uploads are limited to PNG, JPEG, and GIF up to 8 MB
- Markdown is sanitized
- Video upload is disabled
- Redis cache and metrics are opt-in

## License

MIT. See `LICENSE`.
