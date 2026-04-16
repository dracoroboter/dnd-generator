#!/bin/bash
# backup.sh — Crea un backup del progetto dungeonandragon (escluso legacy/)
# Uso: bash tech/scripts/backup.sh
# Output: ~/dungeonandragon_backup_<data_ora>.zip

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECT_NAME="$(basename "$PROJECT_DIR")"
TIMESTAMP=$(date +%Y-%m-%d_%H%M)
BACKUP_FILE="$HOME/${PROJECT_NAME}_backup_${TIMESTAMP}.zip"

echo "=== Backup $PROJECT_NAME ==="
echo "Destinazione: $BACKUP_FILE"

cd "$(dirname "$PROJECT_DIR")"
zip -r "$BACKUP_FILE" "$PROJECT_NAME/" \
    --exclude "${PROJECT_NAME}/legacy/*" \
    -x "*.log" > /dev/null

echo "=== Fatto ==="
ls -lh "$BACKUP_FILE"
