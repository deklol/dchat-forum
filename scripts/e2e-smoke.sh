#!/usr/bin/env sh
set -eu

docker compose up -d --build
docker compose exec -T web python manage.py migrate --noinput
docker compose exec -T web python manage.py test apps.core.tests apps.forum.tests
curl -fsS http://localhost:8000/health/live/ >/dev/null
curl -fsS http://localhost:8000/health/ready/ >/dev/null
echo "E2E smoke checks passed"
