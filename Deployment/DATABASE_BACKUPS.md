# Database backups — floridacourserepo.com

Production is one SQLite file (path in `/etc/presemaker-repo/environment`, normally
`/var/presemaker-repo/data/repo.db`). Courses, guides, requests and resources all live in it.

## Take a backup (one command)

From the repo root, in PowerShell:

```powershell
.\Deployment\backup-db.ps1
```

It makes a timestamped copy on the server with SQLite's online backup (safe while the site runs), checks
its integrity, keeps the newest 30 on the server (`/var/presemaker-repo/backups/`), downloads it to
**`%USERPROFILE%\floridacourserepo-backups\`** and verifies the SHA-256. It ends with
`Backup complete and verified: <file>`.

| Option | Use |
|---|---|
| `-Label before-import` | adds a label to the file name |
| `-NoDownload` | server copy only |
| `-KeepOnServer 60` | keep more server copies |
| `-LocalDir D:\backups` | download somewhere else (keep it off synced college OneDrive folders) |

**`deploy-update.ps1` runs a backup automatically before every deploy** (label `predeploy`); pass
`-SkipBackup` only when you have just taken one.

If the server has no `sqlite3`, the script falls back to stopping the site for a few seconds while it copies.
Install it once to avoid that: `ssh root@129.121.101.162 "apt install -y sqlite3"`.

## Stop typing the password (recommended)

Each run asks for the server password twice (ssh, then scp); a deploy asks several more times. An SSH key
removes the prompts and lets backups run on a schedule. Once, in PowerShell:

```powershell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\id_ed25519"        # press Enter for no passphrase, or set one
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | ssh root@129.121.101.162 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
ssh root@129.121.101.162 "echo key login works"                     # should not ask for a password
```

With the key in place a weekly scheduled backup is one Task Scheduler action:
`powershell.exe -NoProfile -File C:\Users\ronal\source\repos\CIATLE-REPO\Deployment\backup-db.ps1 -Label weekly`.

## Restore a backup

Restoring replaces everything written since the backup (courses, guides, requests, resources). The backup
must match the code's migrations: restoring a backup taken **before** a deploy means redeploying the code
from before that deploy too, or the new code will migrate the restored file again on start.

```powershell
# 1. Copy the backup up (skip if restoring a server copy from /var/presemaker-repo/backups)
scp "$env:USERPROFILE\floridacourserepo-backups\repo-YYYYMMDD-HHMMSS.db" root@129.121.101.162:/var/presemaker-repo/backups/
# 2. Swap it in with the site stopped
ssh root@129.121.101.162
systemctl stop presemaker-repo
cp -p /var/presemaker-repo/data/repo.db /var/presemaker-repo/backups/repo-before-restore.db
rm -f /var/presemaker-repo/data/repo.db-wal /var/presemaker-repo/data/repo.db-shm
cp /var/presemaker-repo/backups/repo-YYYYMMDD-HHMMSS.db /var/presemaker-repo/data/repo.db
chown presemaker:presemaker /var/presemaker-repo/data/repo.db
systemctl start presemaker-repo && systemctl is-active presemaker-repo
exit
```
