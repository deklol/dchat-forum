$ErrorActionPreference = "Stop"

docker compose up -d --build
docker compose exec -T web python manage.py migrate --noinput
docker compose exec -T web python manage.py test apps.core.tests apps.forum.tests
Invoke-WebRequest -UseBasicParsing http://localhost:8000/health/live/ | Out-Null
Invoke-WebRequest -UseBasicParsing http://localhost:8000/health/ready/ | Out-Null
Write-Host "E2E smoke checks passed"
