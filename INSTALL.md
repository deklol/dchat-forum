# INSTALL

## Requirements

- Docker Engine
- Docker Compose plugin
- 2 GB RAM minimum
- 4 GB RAM recommended

## Minimal install

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

Open:

- `http://localhost:8000`

## Optional full profile

If you want shared Redis cache and a fronting reverse proxy:

```bash
docker compose --profile full up -d --build
```

That profile adds:

- Redis
- Caddy

Open:

- `http://localhost`
- `https://localhost`

## First run

1. Visit `/setup`
2. Create the first account
3. That account becomes the initial admin and user `id=1`
4. The email on user `id=1` is shown publicly on the Terms, Privacy, and Cookies pages by default
5. Pick `default` or `dekcx` as the initial theme preset

After setup, use `/admin` to:

- adjust branding and color tokens
- configure footer links
- review permissions and moderation settings
- edit legal documents if needed

## Common commands

View logs:

```bash
docker compose logs -f web
```

Run migrations manually:

```bash
docker compose exec web python manage.py migrate --noinput
```

Stop the stack:

```bash
docker compose down
```

## Backups

Linux/macOS:

```bash
./scripts/backup.sh
./scripts/restore-test.sh
```

PowerShell:

```powershell
.\scripts\backup.ps1
.\scripts\restore-test.ps1
```

## Smoke test

Linux/macOS:

```bash
./scripts/e2e-smoke.sh
```

PowerShell:

```powershell
.\scripts\e2e-smoke.ps1
```
