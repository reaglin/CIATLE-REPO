# visitor-report.ps1 -- how many people are visiting floridacourserepo.com
#
# Reads the web server's Nginx access logs over ssh (one password prompt, or none with key
# auth -- see DATABASE_BACKUPS.md), then counts visitors, page views, the most-visited
# courses and where visitors came from, with crawlers and bots left out
# (Deployment\visitor_report.py does the counting).
#
# The report is shown here and saved to Deployment\visitor-reports\visitors-<date>.md.
# The downloaded logs hold IP addresses, so they are deleted as soon as the report is made.
#
# The server keeps about two months of logs (set by Deployment\keep-logs-two-months.ps1; 14 days
# before that), so a report made any time in a month can still cover the whole month before.
#
#   .\Deployment\visitor-report.ps1              # everything the server still has
#   .\Deployment\visitor-report.ps1 -LastMonth   # last calendar month: the monthly check
#   .\Deployment\visitor-report.ps1 -Month 2026-11
#   .\Deployment\visitor-report.ps1 -Days 7      # the last 7 days only
#   .\Deployment\visitor-report.ps1 -LogFile x   # a log file already on this computer

[CmdletBinding()]
param(
    [string]$RemoteUser = "root",
    [string]$RemoteHost = "129.121.101.162",
    [int]$Days = 0,
    [string]$Month,
    [switch]$LastMonth,
    [string]$LogFile
)

$ErrorActionPreference = "Stop"
$here   = $PSScriptRoot
$outDir = Join-Path $here "visitor-reports"
New-Item -ItemType Directory -Force $outDir | Out-Null
if ($LastMonth) { $Month = (Get-Date).AddMonths(-1).ToString("yyyy-MM") }
if ($Month -and $Month -notmatch '^\d{4}-\d{2}$') { throw "-Month must look like 2026-11." }
$out = if ($Month) { Join-Path $outDir "visitors-month-$Month.md" }
       else        { Join-Path $outDir ("visitors-{0:yyyy-MM-dd}.md" -f (Get-Date)) }

$raw = $LogFile
$downloaded = $false
if (-not $raw) {
    $raw = Join-Path $env:TEMP "fcr-nginx-access.log"
    $downloaded = $true
    Write-Host "Reading the Nginx access logs from $RemoteHost (ssh may ask for the server password)..." -ForegroundColor Cyan
    $remote = "cat /var/log/nginx/access.log /var/log/nginx/access.log.1 2>/dev/null; " +
              "zcat -f /var/log/nginx/access.log.*.gz 2>/dev/null; true"
    & ssh "$RemoteUser@$RemoteHost" $remote > $raw
    if ($LASTEXITCODE -ne 0) {
        Remove-Item $raw -ErrorAction SilentlyContinue
        throw "ssh to $RemoteHost failed (exit $LASTEXITCODE)."
    }
}

try {
    $pyArgs = @("$here\visitor_report.py", $raw, "--out", $out)
    if ($Days -gt 0) { $pyArgs += @("--days", "$Days") }
    if ($Month)      { $pyArgs += @("--month", $Month) }
    & python -I @pyArgs
    if ($LASTEXITCODE -ne 0) { throw "visitor_report.py failed (exit $LASTEXITCODE)." }
} finally {
    if ($downloaded) { Remove-Item $raw -ErrorAction SilentlyContinue }
}

Write-Host ""
Write-Host "Saved: $out" -ForegroundColor Green
