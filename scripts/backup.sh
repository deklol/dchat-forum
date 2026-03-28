#!/usr/bin/env sh
set -eu

STAMP="$(date +%Y%m%d-%H%M%S)"
DEST="${1:-./backups}"
mkdir -p "$DEST"

docker compose exec -T postgres pg_dump -U "${POSTGRES_USER:-dchat}" "${POSTGRES_DB:-dchat}" > "$DEST/db-$STAMP.sql"
tar -czf "$DEST/media-$STAMP.tar.gz" media

echo "Backup created in $DEST"
