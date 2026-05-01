#!/usr/bin/env bash
# Initial deployment to a fresh Ubuntu 22.04/24.04 LTS VPS.
# Run as root or with sudo. Replace DOMAIN with your actual domain.
set -euo pipefail

DOMAIN="yourdomain.com"
APP_DIR="/opt/presemaker-repo/app"
DATA_DIR="/var/presemaker-repo"
ETC_DIR="/etc/presemaker-repo"

# 1. Create service user
useradd -r -s /usr/sbin/nologin presemaker || true

# 2. Create directories
mkdir -p "$DATA_DIR"/{data,storage/modules,logs}
mkdir -p "$APP_DIR"
mkdir -p "$ETC_DIR"
chown -R presemaker:presemaker "$DATA_DIR"
chown -R presemaker:presemaker "$APP_DIR"

# 3. Install .NET 8 Runtime (Ubuntu — follow Microsoft docs if this fails)
if ! command -v dotnet &>/dev/null; then
    wget https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O /tmp/packages-microsoft-prod.deb
    dpkg -i /tmp/packages-microsoft-prod.deb
    apt-get update
    apt-get install -y dotnet-runtime-8.0
fi

# 4. Place taxonomy.json (copy from source repo or provide separately)
# cp /path/to/taxonomy.json "$ETC_DIR/taxonomy.json"
# chown presemaker:presemaker "$ETC_DIR/taxonomy.json"

# 5. Place and secure environment secrets
# cp environment.template "$ETC_DIR/environment"
# nano "$ETC_DIR/environment"   # fill in all placeholders
chmod 600 "$ETC_DIR/environment"
chown presemaker:presemaker "$ETC_DIR/environment"

# 6. Publish application (run from repo root on build machine, then rsync)
# dotnet publish PreseMakerRepo.Api -c Release -r linux-x64 --self-contained false -o /tmp/presemaker-release
# rsync -a /tmp/presemaker-release/ root@yourserver:"$APP_DIR/"

# 7. Run migrations (seeds taxonomy and creates admin account)
cd "$APP_DIR"
sudo -u presemaker dotnet PreseMakerRepo.Api.dll --run-migrations

# 8. Install and start systemd service
cp /path/to/presemaker-repo.service /etc/systemd/system/presemaker-repo.service
systemctl daemon-reload
systemctl enable presemaker-repo
systemctl start presemaker-repo

# 9. Install Nginx and Certbot
apt-get install -y nginx certbot python3-certbot-nginx

# 10. Place Nginx config
cp /path/to/nginx-site.conf /etc/nginx/sites-available/presemaker-repo
# Edit the file to replace yourdomain.com with $DOMAIN
sed -i "s/yourdomain.com/$DOMAIN/g" /etc/nginx/sites-available/presemaker-repo
ln -sf /etc/nginx/sites-available/presemaker-repo /etc/nginx/sites-enabled/presemaker-repo
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# 11. Obtain TLS certificate
certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN"

echo "Deployment complete. Visit https://$DOMAIN"
