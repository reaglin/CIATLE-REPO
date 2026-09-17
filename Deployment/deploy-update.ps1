# Redeploy updated binaries to an existing VPS installation.
# PowerShell equivalent of deploy-update.sh, for Windows hosts without bash
# on PATH. Uses native Windows OpenSSH (ssh/scp) and the dotnet CLI.
#
# Run from the repo root:
#   .\Deployment\deploy-update.ps1
#
# Code-only change (no migration, no taxonomy edit):
#   .\Deployment\deploy-update.ps1 -CodeOnly
# That skips the taxonomy copy and the database backup, and REFUSES to run if
# the repo holds a migration production has not applied.
#
# Backs up the production database first (Deployment\backup-db.ps1) — migrations
# change the schema in place. Pass -SkipBackup only when you have just taken one.
#
# You will be prompted for the server password by ssh and scp several times
# (six with the backup), unless you have key auth set up — see DATABASE_BACKUPS.md.

[CmdletBinding()]
param(
    [string]$RemoteUser = "root",
    [string]$RemoteHost = "129.121.101.162",
    [string]$AppDir     = "/opt/presemaker-repo/app",
    [string]$EtcDir     = "/etc/presemaker-repo",
    [string]$ReleaseDir = "$env:TEMP\presemaker-release",
    [switch]$SkipMigrations,
    [switch]$SkipTaxonomy,
    [switch]$SkipBackup,
    # Ship binaries only: no taxonomy copy, no database backup. Refuses to run if
    # the repo holds a migration production has not applied, because that would
    # not be a code-only deploy -- the app applies pending migrations at startup
    # whatever this script does. See Test-PendingMigrations below.
    [switch]$CodeOnly
)

$ErrorActionPreference = "Stop"

$target = "$RemoteUser@$RemoteHost"

# --- Is production missing any migration this repo carries? ------------------
#
# The honest basis for a "code only" deploy. Note what this is guarding against:
# Program.cs runs MigrateAsync() and every seed on EVERY startup, so the service
# restart at the end of this script applies pending migrations regardless of any
# flag here. -CodeOnly therefore cannot PREVENT a migration; it can only refuse
# to proceed when one is pending, which is what makes the name truthful.
#
# Compares the migration ids in the repo against __EFMigrationsHistory in the
# production SQLite file. If sqlite3 is not installed on the server the check
# cannot run; that is reported loudly and the deploy continues, matching how
# backup-db.ps1 degrades rather than blocking on a missing tool.
function Test-PendingMigrations {
    param([string]$Target, [string]$RepoRoot)

    $migDir = Join-Path $RepoRoot "PreseMakerRepo.Infrastructure\Migrations"
    if (-not (Test-Path $migDir)) {
        Write-Host "    No Migrations folder found; skipping the check." -ForegroundColor DarkYellow
        return
    }
    # A migration file is <timestamp>_<Name>.cs; its Designer partner is not one.
    $local = Get-ChildItem $migDir -Filter "*.cs" |
        Where-Object { $_.Name -notlike "*.Designer.cs" -and $_.Name -match "^\d{14}_" } |
        ForEach-Object { $_.BaseName } | Sort-Object

    if (-not $local) {
        Write-Host "    No migrations in the repo; nothing to compare." -ForegroundColor DarkYellow
        return
    }

    $dbPath = "/var/presemaker-repo/data/repo.db"
    $query  = "SELECT MigrationId FROM __EFMigrationsHistory;"
    $applied = ssh $Target "command -v sqlite3 >/dev/null 2>&1 && sqlite3 '$dbPath' '$query' || echo __NO_SQLITE3__" 2>$null

    if (-not $applied -or ($applied -join "`n") -match "__NO_SQLITE3__") {
        Write-Host ""
        Write-Host "    !! COULD NOT VERIFY: sqlite3 is not installed on the server, so the" -ForegroundColor Yellow
        Write-Host "       pending-migration check did not run. If a migration IS pending it" -ForegroundColor Yellow
        Write-Host "       will still be applied when the service restarts." -ForegroundColor Yellow
        Write-Host "       Install it once:  ssh $Target `"apt install -y sqlite3`"" -ForegroundColor Yellow
        Write-Host ""
        return
    }

    $appliedSet = @($applied | ForEach-Object { $_.Trim() } | Where-Object { $_ })
    $pending = @($local | Where-Object { $appliedSet -notcontains $_ })

    if ($pending.Count -gt 0) {
        Write-Host ""
        Write-Host "    Production is missing $($pending.Count) migration(s):" -ForegroundColor Red
        $pending | ForEach-Object { Write-Host "      $_" -ForegroundColor Red }
        throw ("-CodeOnly refused: this is not a code-only change. Run the deploy " +
               "without -CodeOnly (and keep the database backup) so the schema change " +
               "is applied deliberately.")
    }

    Write-Host "    $($local.Count) migration(s) in the repo, all applied in production." -ForegroundColor Green
    $global:LASTEXITCODE = 0
}

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

# 0. Back up the database ----------------------------------------------------
# Migrations run against the live file, so take a verified copy first. backup-db.ps1 throws on any
# failure, which stops the deploy before anything is changed.
if ($CodeOnly) {
    # -CodeOnly implies both skips. The backup exists to protect against a schema
    # change, and the guard above has established there is none.
    $SkipTaxonomy = $true
    $SkipBackup   = $true
    Write-Host ""
    Write-Host "==> CodeOnly: verifying that no migration is pending" -ForegroundColor Cyan
    Test-PendingMigrations -Target $target -RepoRoot $repoRoot
    Write-Host "==> CodeOnly: skipping taxonomy.json and the database backup." -ForegroundColor DarkYellow
}

if ($SkipBackup) {
    Write-Host ""
    Write-Host "==> Skipping database backup (-SkipBackup)." -ForegroundColor DarkYellow
} else {
    & (Join-Path $PSScriptRoot "backup-db.ps1") -RemoteUser $RemoteUser -RemoteHost $RemoteHost -Label "predeploy"
}

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

# 3b. Copy taxonomy.json to the config directory -----------------------------
# Production reads Taxonomy:ConfigPath = /etc/presemaker-repo/taxonomy.json (see
# appsettings.json), NOT the copy that ships in the publish output -- only
# appsettings.Development.json points at Data/Seed/taxonomy.json. Copying the
# binaries alone therefore leaves the seeded taxonomy untouched, and TaxonomySeed
# reports success against the stale file with no error anywhere. That is the same
# silent-no-op failure mode as the CJK/DENTISTRY defect. Ship the file explicitly.
$taxonomySrc = Join-Path $apiProj "Data\Seed\taxonomy.json"
if ($SkipTaxonomy) {
    Write-Host ""
    Write-Host "==> Skipping taxonomy.json (-SkipTaxonomy)." -ForegroundColor DarkYellow
} elseif (-not (Test-Path $taxonomySrc)) {
    throw "Cannot find $taxonomySrc"
} else {
    # Fail fast on a malformed file rather than shipping one the seeder cannot parse.
    Invoke-Step "Validating taxonomy.json" {
        $json = Get-Content $taxonomySrc -Raw | ConvertFrom-Json
        $disciplines = $json.tree.Count
        $prefixes = ($json.tree | ForEach-Object { $_.children.Count } | Measure-Object -Sum).Sum
        $dupes = $json.tree | Group-Object key | Where-Object Count -gt 1
        if ($dupes) { throw "Duplicate discipline keys: $($dupes.Name -join ', ')" }
        Write-Host "    $disciplines disciplines, $prefixes prefixes, no duplicate keys"
        $global:LASTEXITCODE = 0
    }
    Invoke-Step "Copying taxonomy.json to $EtcDir" {
        scp $taxonomySrc "${target}:$EtcDir/taxonomy.json"
    }
}

# 4. Permissions, migrations, restart ---------------------------------------
# !! -SkipMigrations DOES NOT GIVE YOU A MIGRATION-FREE DEPLOY.
# It skips only this explicit pre-start pass. Program.cs runs MigrateAsync() and
# every seed on EVERY startup, so `systemctl start` below applies anything
# pending anyway -- the flag just moves that into service startup, where a
# failure takes the site down instead of stopping the deploy. Prefer -CodeOnly,
# which refuses when a migration is pending rather than hiding one.
if ($SkipMigrations) {
    Write-Host ""
    Write-Host "    !! -SkipMigrations skips only the pre-start pass. The service restart" -ForegroundColor Yellow
    Write-Host "       still applies any pending migration, and a failure there takes the" -ForegroundColor Yellow
    Write-Host "       site down rather than stopping this deploy." -ForegroundColor Yellow
}
$migrationCmd = if ($SkipMigrations) {
    "echo 'Skipping the pre-start migration pass (-SkipMigrations); startup will still migrate.'"
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
    "chown presemaker:presemaker $EtcDir/taxonomy.json || true"
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
