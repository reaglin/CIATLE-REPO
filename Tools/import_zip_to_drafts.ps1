<#
.SYNOPSIS
  Import a "Download All" ZIP from Claude into the curriculum-guide workflow.

.DESCRIPTION
  Validates the ZIP's contents look like curriculum-guide JSONs, extracts them
  into .\drafts\, runs queue_mgr.py reconcile, and prints a summary of what's now
  ready to push.

  Run from: C:\Users\ronal\source\repos\CIATLE-REPO\Tools

.PARAMETER ZipPath
  Path to the ZIP file. Default: .\files.zip in the current directory.
  Pass a full path to use a ZIP elsewhere (e.g. ~\Downloads\claude_files.zip).

.PARAMETER Force
  Overwrite existing draft files without prompting.

.PARAMETER KeepZip
  Don't delete the ZIP after successful import.

.EXAMPLE
  .\import_zip_to_drafts.ps1
  # Imports .\files.zip from the current directory.

.EXAMPLE
  .\import_zip_to_drafts.ps1 ~\Downloads\claude-files.zip
  # Imports a specific ZIP elsewhere on disk.

.EXAMPLE
  .\import_zip_to_drafts.ps1 -Force -KeepZip
  # Overwrites existing drafts and keeps the ZIP after import.
#>

[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [string]$ZipPath = '.\files.zip',
    [switch]$Force,
    [switch]$KeepZip
)

$ErrorActionPreference = 'Stop'
$ToolsDir = $PSScriptRoot
$DraftsDir = Join-Path $ToolsDir 'drafts'
$QueueScript = Join-Path $ToolsDir 'queue_mgr.py'

# Ensure we're running from the right place
if (-not (Test-Path $QueueScript)) {
    Write-Error "queue_mgr.py not found in $ToolsDir. Run this script from the Tools directory."
    exit 1
}

# Ensure drafts directory exists
if (-not (Test-Path $DraftsDir)) {
    New-Item -ItemType Directory -Path $DraftsDir | Out-Null
    Write-Host "Created drafts directory: $DraftsDir" -ForegroundColor DarkGray
}

# --- Step 1: Resolve the ZIP path ------------------------------------------

# Resolve relative paths against the current working directory (where the user
# invoked the script), not against $PSScriptRoot. PowerShell's Resolve-Path
# does this correctly.
try {
    $ZipPath = (Resolve-Path -Path $ZipPath -ErrorAction Stop).ProviderPath
} catch {
    Write-Error "ZIP not found: $ZipPath`nDownload the batch from chat first, or pass a full path."
    exit 1
}

Write-Host "ZIP: $ZipPath" -ForegroundColor Cyan

# --- Step 2: Stage the contents to a temp directory for validation --------

$stagingDir = Join-Path ([System.IO.Path]::GetTempPath()) "claude_import_$(Get-Random)"
New-Item -ItemType Directory -Path $stagingDir | Out-Null

try {
    Write-Host "Extracting to staging area..." -ForegroundColor DarkGray
    Expand-Archive -Path $ZipPath -DestinationPath $stagingDir -Force

    # Recursively find all *_guide.json files (in case Claude nested them in a folder)
    $guideFiles = Get-ChildItem -Path $stagingDir -Filter '*_guide.json' -File -Recurse
    if (-not $guideFiles) {
        Write-Error "No *_guide.json files found in $ZipPath. Wrong ZIP?"
        exit 1
    }

    # --- Step 3: Validate each file is parseable JSON with required fields --

    $required = @('title', 'html_content', 'credits', 'contact_hours', 'prerequisites', 'version')
    $validated = @()
    $invalid = @()

    foreach ($f in $guideFiles) {
        $courseId = $f.BaseName -replace '_guide$', ''
        try {
            $json = Get-Content -Path $f.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
            $missing = $required | Where-Object { -not ($json.PSObject.Properties.Name -contains $_) }
            if ($missing) {
                $invalid += [pscustomobject]@{
                    CourseId = $courseId
                    Reason = "Missing required field(s): $($missing -join ', ')"
                    Path = $f.FullName
                }
            } else {
                $validated += [pscustomobject]@{
                    CourseId = $courseId
                    Title = $json.title
                    Credits = $json.credits
                    ContactHours = $json.contact_hours
                    Path = $f.FullName
                }
            }
        } catch {
            $invalid += [pscustomobject]@{
                CourseId = $courseId
                Reason = "Invalid JSON: $($_.Exception.Message)"
                Path = $f.FullName
            }
        }
    }

    if ($invalid) {
        Write-Host ""
        Write-Host "INVALID FILES (will be skipped):" -ForegroundColor Red
        foreach ($i in $invalid) {
            Write-Host "  - $($i.CourseId): $($i.Reason)" -ForegroundColor Red
        }
        Write-Host ""
    }

    if (-not $validated) {
        Write-Error "No valid guide files to import."
        exit 1
    }

    # --- Step 4: Check for conflicts in drafts/ ----------------------------

    $conflicts = @()
    foreach ($v in $validated) {
        $dest = Join-Path $DraftsDir "$($v.CourseId)_guide.json"
        if (Test-Path $dest) {
            $conflicts += $v.CourseId
        }
    }

    if ($conflicts -and -not $Force) {
        Write-Host "These drafts already exist in drafts\ :" -ForegroundColor Yellow
        foreach ($c in $conflicts) { Write-Host "  - $c" -ForegroundColor Yellow }
        $resp = Read-Host "Overwrite? [y/N]"
        if ($resp -notmatch '^[yY]') {
            Write-Host "Aborted. Use -Force to skip this prompt." -ForegroundColor DarkGray
            exit 0
        }
    }

    # --- Step 5: Move validated files into drafts/ -------------------------
    # If anything fails partway, roll back any moves we already did.

    $moved = @()
    try {
        foreach ($v in $validated) {
            $dest = Join-Path $DraftsDir "$($v.CourseId)_guide.json"
            Copy-Item -Path $v.Path -Destination $dest -Force
            $moved += [pscustomobject]@{ CourseId = $v.CourseId; Dest = $dest }
        }
    } catch {
        Write-Host "Move failed mid-batch -- rolling back..." -ForegroundColor Red
        foreach ($m in $moved) { Remove-Item -Path $m.Dest -ErrorAction SilentlyContinue }
        throw
    }

    # --- Step 6: Reconcile the queue ---------------------------------------

    Write-Host ""
    Write-Host "Imported $($moved.Count) draft(s) into drafts\ :" -ForegroundColor Green
    foreach ($v in $validated) {
        $tag = if ($v.CourseId -in $conflicts) { ' (overwrote)' } else { '' }
        Write-Host ("  + {0,-12} {1}{2}" -f $v.CourseId, $v.Title, $tag) -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "Reconciling queue..." -ForegroundColor Cyan
    & python $QueueScript reconcile
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "queue_mgr.py reconcile returned exit code $LASTEXITCODE"
    }

    # --- Step 7: Show what's ready to push ---------------------------------

    Write-Host ""
    Write-Host "Current queue status:" -ForegroundColor Cyan
    & python $QueueScript status

    # --- Step 8: Clean up the ZIP ------------------------------------------

    if (-not $KeepZip) {
        Remove-Item -Path $ZipPath -Force
        Write-Host ""
        Write-Host "Deleted ZIP: $ZipPath" -ForegroundColor DarkGray
    }

    Write-Host ""
    Write-Host "Done. Review the drafts, then push with:" -ForegroundColor Green
    Write-Host "  python generate_guide.py --push-from-queue --yes" -ForegroundColor White

} finally {
    # Always clean up staging
    if (Test-Path $stagingDir) {
        Remove-Item -Path $stagingDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
