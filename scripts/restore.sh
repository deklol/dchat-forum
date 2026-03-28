#!/usr/bin/env sh
set -eu

SQL_FILE="$1"
MEDIA_ARCHIVE="$2"

if [ ! -f "$SQL_FILE" ]; then
  echo "Missing SQL file: $SQL_FILE"
  exit 1
fi
if [ ! -f "$MEDIA_ARCHIVE" ]; then
  echo "Missing media archive: $MEDIA_ARCHIVE"
  exit 1
fi

cat "$SQL_FILE" | docker compose exec -T postgres psql -U "${POSTGRES_USER:-dchat}" "${POSTGRES_DB:-dchat}"
tar -xzf "$MEDIA_ARCHIVE"

echo "Restore complete"
