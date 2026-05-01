#!/usr/bin/env bash
# Redeploy updated binaries to an existing VPS installation.
# Run from the repo root on your build machine, or adapt for CI.
set -euo pipefail

REMOTE_USER="root"
REMOTE_HOST="yourserver"
APP_DIR="/opt/presemaker-repo/app"
RELEASE_DIR="/tmp/presemaker-release"

# 1. Publish
dotnet publish PreseMakerRepo.Api -c Release -r linux-x64 --self-contained false -o "$RELEASE_DIR"

# 2. Stop service, swap binaries, run migrations, restart
ssh "$REMOTE_USER@$REMOTE_HOST" bash <<EOF
set -euo pipefail
systemctl stop presemaker-repo
cp -r "$RELEASE_DIR"/. "$APP_DIR/"
cd "$APP_DIR"
sudo -u presemaker dotnet PreseMakerRepo.Api.dll --run-migrations
systemctl start presemaker-repo
systemctl status presemaker-repo --no-pager
EOF

rsync -a --delete "$RELEASE_DIR/" "$REMOTE_USER@$REMOTE_HOST:$RELEASE_DIR/"
echo "Update complete."
