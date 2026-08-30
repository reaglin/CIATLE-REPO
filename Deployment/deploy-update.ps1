# Redeploy updated binaries to an existing VPS installation.
# PowerShell equivalent of deploy-update.sh, for Windows hosts without bash
# on PATH. Uses native Windows OpenSSH (ssh/scp) and the dotnet CLI.
#
# Run from the repo root:
#   .\Deployment\deploy-update.ps1
#
# You will be prompted for the server password by ssh and scp (three times
# total, unless you have key auth set up).

[CmdletBinding()]
param(
    [string]$RemoteUser = "root",
    [string]$RemoteHost = "129.121.101.162",
    [string]$AppDir     = "/opt/presemaker-repo/app",
    [string]$ReleaseDir = "$env:TEMP\presemaker-release",
    [switch]$SkipMigrations
)

$ErrorActionPreference = "Stop"

$target = "$RemoteUser@$RemoteHost"

function Invoke-Step {
    param([string]$Name, [scriptblock]$Action)
    Write-Host ""
    Write-Host "==> $Name" -ForegroundColor Cyan
    & $Action
    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE"
    }
}

# Resolve the repo root from this script's location, so the publish path is
# correct no matter where the script is invoked from.
$repoRoot = Split-Path -Parent $PSScriptRoot
$apiProj  = Join-Path $repoRoot "PreseMakerRepo.Api"
if (-not (Test-Path $apiProj)) {
    throw "Cannot find PreseMakerRepo.Api under $repoRoot"
}

Write-Host "Deploying to $target$AppDir" -ForegroundColor Yellow
Write-Host "Publishing from $apiProj"
Write-Host "Staging in      $ReleaseDir"

# 1. Publish -----------------------------------------------------------------
if (Test-Path $ReleaseDir) {
    Remove-Item -Recurse -Force $ReleaseDir
}
Invoke-Step "Publishing Release build (linux-x64)" {
    dotnet publish $apiProj -c Release -r linux-x64 --self-contained false -o $ReleaseDir
}

# 2. Stop the service and remove the locked binary ---------------------------
Invoke-Step "Stopping service and clearing old binary" {
    ssh $target "systemctl stop presemaker-repo && rm -f $AppDir/PreseMakerRepo.Api"
}

# 3. Copy new binaries -------------------------------------------------------
# Trailing '\.' copies directory *contents*, matching the bash script's "$RELEASE_DIR/."
Invoke-Step "Copying binaries to the server" {
    scp -r "$ReleaseDir\." "${target}:$AppDir/"
}

# 4. Permissions, migrations, restart ---------------------------------------
$migrationCmd = if ($SkipMigrations) {
    "echo 'Skipping migrations (-SkipMigrations).'"
} else {
    "sudo -u presemaker dotnet PreseMakerRepo.Api.dll --run-migrations"
}

# Build the remote script as ONE single-line argument, joined with ';'.
#
# Do NOT pipe a multi-line string to `ssh "bash -s"`: PowerShell appends its
# own CRLF when writing to a native command's stdin, so the final line arrives
# with a trailing CR and bash runs e.g. `--no-pager\r`. (That produced
# "'ystemctl: unrecognized option '--no-pager" -- the CR wraps the cursor back
# over the line, which is also why the 's' appears to be missing.) Passing the
# script as an argument avoids stdin, and therefore the translation, entirely.
$remoteCommands = @(
    "set -euo pipefail"
    "chmod +x $AppDir/PreseMakerRepo.Api"
    "chown -R presemaker:presemaker $AppDir"
    "cd $AppDir"
    $migrationCmd
    "systemctl start presemaker-repo"
    # `systemctl status` exits non-zero for a non-running unit, which would trip
    # `set -e` on a report-only command. Report health explicitly instead.
    "systemctl is-active presemaker-repo"
    "systemctl status presemaker-repo --no-pager --lines=0 || true"
)
$remoteScript = $remoteCommands -join "; "

Invoke-Step "Setting permissions, running migrations, restarting" {
    ssh $target $remoteScript
}

Write-Host ""
Write-Host "Update complete." -ForegroundColor Green
Write-Host "Verify with: curl.exe -s -o NUL -w '%{http_code}' https://floridacourserepo.com/"
