#!/usr/bin/env sh
set -eu

TMP_DIR="./backups/restore-test"
mkdir -p "$TMP_DIR"

./scripts/backup.sh "$TMP_DIR"
LATEST_SQL="$(ls -t "$TMP_DIR"/db-*.sql | head -n 1)"
LATEST_MEDIA="$(ls -t "$TMP_DIR"/media-*.tar.gz | head -n 1)"
./scripts/restore.sh "$LATEST_SQL" "$LATEST_MEDIA"

echo "Restore test finished"
