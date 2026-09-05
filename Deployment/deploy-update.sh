#!/usr/bin/env bash
# Redeploy updated binaries to an existing VPS installation.
# Run from the repo root on your build machine.
#
# Manual steps this script automates:
#   PowerShell: dotnet publish ...
#   Server:     systemctl stop / rm binary
#   PowerShell: scp ...
#   Server:     chmod / chown / systemctl start
set -euo pipefail

REMOTE_USER="root"
REMOTE_HOST="129.121.101.162"
APP_DIR="/opt/presemaker-repo/app"
ETC_DIR="/etc/presemaker-repo"
RELEASE_DIR="/tmp/presemaker-release"

# 1. Publish
dotnet publish PreseMakerRepo.Api -c Release -r linux-x64 --self-contained false -o "$RELEASE_DIR"

# 2. Stop service and remove locked binary
ssh "$REMOTE_USER@$REMOTE_HOST" "systemctl stop presemaker-repo && rm -f $APP_DIR/PreseMakerRepo.Api"

# 3. Copy new binaries
scp -r "$RELEASE_DIR/." "$REMOTE_USER@$REMOTE_HOST:$APP_DIR/"

# 3b. Copy taxonomy.json to the config directory
# Production reads Taxonomy:ConfigPath = /etc/presemaker-repo/taxonomy.json (appsettings.json);
# only appsettings.Development.json uses the Data/Seed copy that ships in the publish output.
# Copying binaries alone therefore leaves the seeded taxonomy stale, and TaxonomySeed reports
# success against the old file with no error -- the same silent no-op as the CJK/DENTISTRY bug.
scp PreseMakerRepo.Api/Data/Seed/taxonomy.json "$REMOTE_USER@$REMOTE_HOST:$ETC_DIR/taxonomy.json"

# 4. Fix permissions, run migrations, restart
ssh "$REMOTE_USER@$REMOTE_HOST" bash <<EOF
set -euo pipefail
chmod +x "$APP_DIR/PreseMakerRepo.Api"
chown -R presemaker:presemaker "$APP_DIR"
chown presemaker:presemaker "$ETC_DIR/taxonomy.json" || true
cd "$APP_DIR"
sudo -u presemaker dotnet PreseMakerRepo.Api.dll --run-migrations
systemctl start presemaker-repo
systemctl status presemaker-repo --no-pager
EOF

echo "Update complete."
