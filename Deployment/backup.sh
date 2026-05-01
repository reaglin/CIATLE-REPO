#!/usr/bin/env bash
# Database backup — run via cron as root or presemaker user.
# Suggested crontab: 0 2 * * * /opt/presemaker-repo/backup.sh
set -euo pipefail

DB_PATH="/var/presemaker-repo/data/repo.db"
BACKUP_DIR="/var/presemaker-repo/backups"
RETAIN_DAYS=30
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

sqlite3 "$DB_PATH" ".backup '$BACKUP_DIR/repo_$TIMESTAMP.db'"
gzip "$BACKUP_DIR/repo_$TIMESTAMP.db"

# Remove backups older than RETAIN_DAYS
find "$BACKUP_DIR" -name "repo_*.db.gz" -mtime +"$RETAIN_DAYS" -delete

echo "Backup complete: $BACKUP_DIR/repo_$TIMESTAMP.db.gz"
