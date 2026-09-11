# Back up the production database and download a verified copy.
#
# Run from the repo root:
#   .\Deployment\backup-db.ps1                     # timestamped backup, downloaded and verified
#   .\Deployment\backup-db.ps1 -Label before-import
#   .\Deployment\backup-db.ps1 -NoDownload         # server copy only
#   .\Deployment\backup-db.ps1 -DbPath /var/presemaker-repo/data/repo.db   # when the path cannot be found
#
# What it does, in one ssh call:
#   1. reads the database path from /etc/presemaker-repo/environment;
#   2. takes a consistent copy with SQLite's online backup (`sqlite3 .backup`) — safe while the site runs,
#      WAL included — and checks it with PRAGMA integrity_check. If sqlite3 is not installed it stops the
#      service for the few seconds a plain copy takes (and always restarts it);
#   3. keeps the newest -KeepOnServer backups in /var/presemaker-repo/backups and deletes older ones;
#   4. reports the path, size and SHA-256.
# Then it downloads the file with scp to -LocalDir and checks the SHA-256 matches.
#
# deploy-update.ps1 runs this automatically before every deploy (-Label predeploy).
# Prompts for the server password twice (ssh, then scp) unless key auth is set up — see DATABASE_BACKUPS.md.

[CmdletBinding()]
param(
    [string]$RemoteUser   = "root",
    [string]$RemoteHost   = "129.121.101.162",
    [string]$EnvFile      = "/etc/presemaker-repo/environment",
    # Set this when the database is not where the environment file says (the script reports what it found).
    [string]$DbPath       = "",
    [string]$BackupDir    = "/var/presemaker-repo/backups",
    [string]$ServiceName  = "presemaker-repo",
    [string]$Label        = "",
    [int]$KeepOnServer    = 30,
    [string]$LocalDir     = (Join-Path $env:USERPROFILE "floridacourserepo-backups"),
    [switch]$NoDownload
)

$ErrorActionPreference = "Stop"
$target = "$RemoteUser@$RemoteHost"
$suffix = if ($Label) { "-" + ($Label -replace '[^A-Za-z0-9_-]', '') } else { "" }

# The remote script travels base64-encoded and is decoded into bash on the server, so no quoting survives
# PowerShell -> ssh -> bash, and there are no CR line endings (see the note in deploy-update.ps1).
$remoteScript = @'
set -euo pipefail
DB='__DBPATH__'
if [ -z "$DB" ]; then DB=$(grep -ihs DefaultConnection '__ENVFILE__' /etc/systemd/system/presemaker-repo.service | tr -d '\r' | sed -n 's/.*[Dd]ata[ _]*[Ss]ource *= *\([^;"]*\).*/\1/p' | sed 's/[[:space:]]*$//' | head -n 1); fi
if [ -z "$DB" ]; then DB=$(grep -ihs DefaultConnection '__ENVFILE__' /etc/systemd/system/presemaker-repo.service | tr -d '\r' | sed -n 's/.*[Ff]ilename *= *\([^;"]*\).*/\1/p' | sed 's/[[:space:]]*$//' | head -n 1); fi
if [ -z "$DB" ]; then for GUESS in /var/presemaker-repo/data/repo.db /var/presemaker-repo/repo.db /opt/presemaker-repo/app/repo.db; do if [ -f "$GUESS" ]; then DB="$GUESS"; break; fi; done; fi
if [ -z "$DB" ] || [ ! -f "$DB" ]; then
  echo "Could not find the database file. Looked for a Data Source= path in __ENVFILE__ and the systemd unit, then in the usual locations." >&2
  echo "-- lines mentioning DefaultConnection (secrets masked):" >&2
  grep -ihs DefaultConnection '__ENVFILE__' /etc/systemd/system/presemaker-repo.service | sed -E 's/(Password|SecretKey|Pwd)=[^;"]*/\1=***/Ig' >&2 || true
  echo "-- *.db files under /var and /opt:" >&2
  find /var /opt -maxdepth 5 -name '*.db' -size +0 2>/dev/null | head -n 10 >&2 || true
  echo "-- then re-run with the path, e.g.:  .\\Deployment\\backup-db.ps1 -DbPath /var/presemaker-repo/data/repo.db" >&2
  exit 1
fi
mkdir -p '__BACKUPDIR__'
DEST="__BACKUPDIR__/repo-$(date -u +%Y%m%d-%H%M%S)__SUFFIX__.db"
if command -v sqlite3 >/dev/null 2>&1; then
  sqlite3 "$DB" ".backup '$DEST'"
  CHECK=$(sqlite3 "$DEST" 'PRAGMA integrity_check;')
  if [ "$CHECK" != "ok" ]; then echo "Integrity check failed on $DEST: $CHECK" >&2; exit 1; fi
  echo "METHOD=sqlite3 online backup, integrity ok"
else
  trap 'systemctl start __SERVICE__' EXIT
  systemctl stop __SERVICE__
  cp -p "$DB" "$DEST"
  for EXT in wal shm; do if [ -f "$DB-$EXT" ]; then cp -p "$DB-$EXT" "$DEST-$EXT"; fi; done
  systemctl start __SERVICE__
  trap - EXIT
  echo "METHOD=plain copy with the service stopped (install sqlite3 for online backups)"
fi
ls -1t '__BACKUPDIR__'/repo-*.db | tail -n +$((__KEEP__ + 1)) | while read -r OLD; do rm -f -- "$OLD" "$OLD-wal" "$OLD-shm"; done
echo "BACKUP=$DEST"
echo "BYTES=$(stat -c %s "$DEST")"
echo "SHA256=$(sha256sum "$DEST" | cut -d ' ' -f 1)"
'@

$remoteScript = $remoteScript.
    Replace('__DBPATH__', $DbPath).
    Replace('__ENVFILE__', $EnvFile).
    Replace('__BACKUPDIR__', $BackupDir).
    Replace('__SUFFIX__', $suffix).
    Replace('__SERVICE__', $ServiceName).
    Replace('__KEEP__', [string]$KeepOnServer) -replace "`r", ""
$encoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($remoteScript))

Write-Host ""
Write-Host "==> Backing up the production database on $RemoteHost" -ForegroundColor Cyan
$output = ssh $target "echo $encoded | base64 -d | bash"
if ($LASTEXITCODE -ne 0) { throw "Backup failed on the server (exit code $LASTEXITCODE)." }

$info = @{}
foreach ($line in $output) {
    if ($line -match '^([A-Z0-9]+)=(.*)$') { $info[$Matches[1]] = $Matches[2] }
}
if (-not $info.ContainsKey("BACKUP")) {
    throw "The server did not report a backup path. Output:`n$($output -join "`n")"
}
$sizeMb = [math]::Round([int64]$info["BYTES"] / 1MB, 1)
Write-Host "    Server copy: $($info["BACKUP"]) ($sizeMb MB; $($info["METHOD"]))"

if ($NoDownload) {
    Write-Host "Backup complete (server copy only)." -ForegroundColor Green
    return
}

New-Item -ItemType Directory -Force $LocalDir | Out-Null
$localFile = Join-Path $LocalDir (Split-Path $info["BACKUP"] -Leaf)

Write-Host "==> Downloading to $localFile" -ForegroundColor Cyan
scp "${target}:$($info["BACKUP"])" "$localFile"
if ($LASTEXITCODE -ne 0) {
    throw "Download failed (scp exit code $LASTEXITCODE). The server copy is still at $($info["BACKUP"])."
}

$hash = (Get-FileHash $localFile -Algorithm SHA256).Hash.ToLowerInvariant()
if ($hash -ne $info["SHA256"]) {
    throw "The downloaded file does not match the server copy (SHA-256 differs). Server copy: $($info["BACKUP"])."
}
Write-Host "Backup complete and verified: $localFile" -ForegroundColor Green
