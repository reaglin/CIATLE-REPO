# visitor-report.ps1 -- how many people are visiting floridacourserepo.com
#
# Runs Deployment\visitor_report.py on the web server over ssh (one password prompt, or none
# with key auth -- see DATABASE_BACKUPS.md). It counts visitors, page views, the most-visited
# courses and where visitors came from in the server's Nginx access logs, with crawlers and
# bots left out, and only the report comes back: the logs (gigabytes, with IP addresses) stay
# on the server. Needs python3 on the server (Ubuntu has it).
#
# The report is shown here and saved to Deployment\visitor-reports\visitors-<date>.md.
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
    [string]$LogFile,
    [switch]$Open          # open the saved report in Notepad (the .cmd files pass it)
)

$ErrorActionPreference = "Stop"
$here   = $PSScriptRoot
$outDir = Join-Path $here "visitor-reports"
New-Item -ItemType Directory -Force $outDir | Out-Null
if ($LastMonth) { $Month = (Get-Date).AddMonths(-1).ToString("yyyy-MM") }
if ($Month -and $Month -notmatch '^\d{4}-\d{2}$') { throw "-Month must look like 2026-11." }
$out = if ($Month) { Join-Path $outDir "visitors-month-$Month.md" }
       else        { Join-Path $outDir ("visitors-{0:yyyy-MM-dd}.md" -f (Get-Date)) }

$filter = @()
if ($Days -gt 0) { $filter += @("--days", "$Days") }
if ($Month)      { $filter += @("--month", $Month) }

if ($LogFile) {
    # A log already on this computer: count it here.
    & python -I "$here\visitor_report.py" $LogFile --out $out @filter
    if ($LASTEXITCODE -ne 0) { throw "visitor_report.py failed (exit $LASTEXITCODE)." }
} else {
    # Count on the server and bring back only the report (a few KB). The logs are gigabytes, and
    # downloading them took close to an hour; this way the IP addresses never leave the server either.
    # The script travels gzipped and base64-encoded on the command line (stdin is left to ssh's password prompt).
    $bytes = [IO.File]::ReadAllBytes("$here\visitor_report.py")
    $ms = New-Object IO.MemoryStream
    $gz = New-Object IO.Compression.GZipStream($ms, [IO.Compression.CompressionMode]::Compress)
    $gz.Write($bytes, 0, $bytes.Length); $gz.Close()
    $b64 = [Convert]::ToBase64String($ms.ToArray())
    $remote = "f=`$(mktemp); echo $b64 | base64 -d | gunzip > `$f; " +
              "command -v python3 >/dev/null || { echo python3 is not installed on the server >&2; exit 90; }; " +
              "zcat -f /var/log/nginx/access.log* 2>/dev/null | python3 -I `$f - $($filter -join ' '); " +
              "rc=`$?; rm -f `$f; exit `$rc"

    Write-Host "Counting visitors on $RemoteHost (ssh may ask for the server password)." -ForegroundColor Cyan
    Write-Host "The server reads all its logs, millions of lines; this usually takes one to five minutes..." -ForegroundColor Cyan
    $prevEnc = [Console]::OutputEncoding
    [Console]::OutputEncoding = [Text.Encoding]::UTF8
    try {
        $report = & ssh "$RemoteUser@$RemoteHost" $remote
        $rc = $LASTEXITCODE
    } finally {
        [Console]::OutputEncoding = $prevEnc
    }
    if ($rc -ne 0) { throw "The report did not run on $RemoteHost (exit $rc); see the message above." }
    $text = ($report -join "`n") + "`n"
    [IO.File]::WriteAllText($out, $text, (New-Object Text.UTF8Encoding($false)))
    Write-Host $text
}

Write-Host ""
Write-Host "Saved: $out" -ForegroundColor Green
if ($Open) { Start-Process notepad.exe -ArgumentList "`"$out`"" }
