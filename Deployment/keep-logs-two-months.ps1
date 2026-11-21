# keep-logs-two-months.ps1 -- keep about two months of Nginx logs on the web server (plan 9.2)
#
# Ubuntu's Nginx rotates its logs daily and keeps 14 (/etc/logrotate.d/nginx: "rotate 14").
# This sets it to keep 62 days, so the monthly visitor report (visitor-report.cmd -LastMonth)
# always has the whole of the month before, whenever in the month it is run.
#
# Run it once, from the CIATLE-REPO folder. It asks for the server password (ssh), keeps a copy
# of the old file as /root/logrotate-nginx.bak, and shows the result. Safe to run again.
# The logs hold IP addresses; they stay on the server and the report deletes its copy.
#
#   .\Deployment\keep-logs-two-months.ps1
#   .\Deployment\keep-logs-two-months.ps1 -KeepDays 90

[CmdletBinding()]
param(
    [string]$RemoteUser = "root",
    [string]$RemoteHost = "129.121.101.162",
    [ValidateRange(14, 400)][int]$KeepDays = 62
)

$ErrorActionPreference = "Stop"

# daily, so "rotate N" means N days (it would mean N weeks under "weekly").
# No double quotes inside: Windows PowerShell 5.1 would mangle them on the way to ssh.
$remote = @"
set -e
f=/etc/logrotate.d/nginx
test -f `$f || { echo No `$f on this server.; exit 2; }
[ -f /root/logrotate-nginx.bak ] || cp `$f /root/logrotate-nginx.bak
# The check runs on the whole configuration (logrotate.conf holds settings, such as su, that the nginx
# file alone lacks), before and after the edit; only an error the edit adds counts against it.
logrotate -d /etc/logrotate.conf >/tmp/lr-before.txt 2>&1 || true
grep -i 'error' /tmp/lr-before.txt | sort -u >/tmp/lr-before-errors.txt || true
sed -i -E 's/^([[:space:]]*)(daily|weekly|monthly)[[:space:]]*$/\1daily/; s/^([[:space:]]*)rotate[[:space:]]+[0-9]+/\1rotate $KeepDays/' `$f
grep -qE '^[[:space:]]*rotate[[:space:]]+$KeepDays' `$f || { echo Could not set rotate in `$f:; cat `$f; exit 3; }
logrotate -d /etc/logrotate.conf >/tmp/lr-after.txt 2>&1 || true
grep -i 'error' /tmp/lr-after.txt | sort -u >/tmp/lr-after-errors.txt || true
if comm -13 /tmp/lr-before-errors.txt /tmp/lr-after-errors.txt | grep -q .; then
  echo logrotate reports new errors after the change, so the old file is put back:
  comm -13 /tmp/lr-before-errors.txt /tmp/lr-after-errors.txt | head -20
  cp /root/logrotate-nginx.bak `$f
  exit 4
fi
if [ -s /tmp/lr-after-errors.txt ]; then
  echo Note: logrotate already reported these before the change, and still does. The change did not cause them:
  head -10 /tmp/lr-after-errors.txt
fi
rm -f /tmp/lr-before.txt /tmp/lr-after.txt /tmp/lr-before-errors.txt /tmp/lr-after-errors.txt
echo --- `$f now:
cat `$f
echo --- log files on the server now:
ls -1 /var/log/nginx/access.log* | wc -l
"@ -replace "`r", ""

Write-Host "Setting Nginx to keep $KeepDays days of logs on $RemoteHost (ssh may ask for the server password)..." -ForegroundColor Cyan
& ssh "$RemoteUser@$RemoteHost" $remote
if ($LASTEXITCODE -ne 0) { throw "The change did not go through (exit $LASTEXITCODE); see above." }

Write-Host ""
Write-Host "Done. The server now keeps $KeepDays days of logs. The extra days build up from today:" -ForegroundColor Green
Write-Host "the full two months are there in about $KeepDays days. Nothing older than 14 days can be recovered."
