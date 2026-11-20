<#
.SYNOPSIS
  The twice-weekly request check for floridacourserepo.com, in one command.

.DESCRIPTION
  1. Asks the live site how many curriculum-guide (and career-path) requests are waiting.
     This step uses no AI. If nothing is waiting, it says so and stops.
  2. Otherwise starts Claude Code with no chat window (claude -p) and the /guide skill. Claude
     drafts or declines up to -Batch requests, validates, pushes, checks they are live,
     commits, pushes to git and writes a report.
  3. The report is shown here and kept in Tools\logs\check-<date>.log.

  Run it from check-requests.cmd in the repo root (double-click it, or run it in a terminal).

.PARAMETER Batch
  The most requests to work in one run (default 10). The rest wait for the next run.

.PARAMETER CheckOnly
  List what is waiting and stop. Claude is not started.

.EXAMPLE
  .\check_requests.ps1                 # the normal check
  .\check_requests.ps1 -Batch 5
  .\check_requests.ps1 -CheckOnly
#>
param(
    [int]$Batch = 10,
    [switch]$CheckOnly
)

$ErrorActionPreference = 'Stop'
$Base  = 'https://floridacourserepo.com/api/v1'
$Tools = $PSScriptRoot
$Repo  = Split-Path $Tools -Parent

# ---- 1. What is waiting (no AI) -------------------------------------------------------
try {
    $guides  = (Invoke-RestMethod "$Base/queue/guides?status=waiting"  -TimeoutSec 30).data
    $careers = (Invoke-RestMethod "$Base/queue/careers?status=waiting" -TimeoutSec 30).data
} catch {
    Write-Host "Could not reach floridacourserepo.com: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Curriculum-guide requests waiting: $($guides.waiting)" -ForegroundColor Cyan
foreach ($i in $guides.items) {
    Write-Host ("  {0,3}. {1,-10} {2}  ({3} request(s))" -f $i.rank, $i.courseId, $i.title, $i.requestCount)
}
Write-Host "Career-path requests waiting:      $($careers.waiting)" -ForegroundColor Cyan
foreach ($i in $careers.items) { Write-Host "       $($i | ConvertTo-Json -Compress -Depth 2)" }
Write-Host ""

if ($CheckOnly) { exit 0 }

if ($guides.waiting -eq 0 -and $careers.waiting -eq 0) {
    Write-Host "Nothing is waiting. No Claude session needed." -ForegroundColor Green
    exit 0
}

# ---- 2. Claude does the work ------------------------------------------------------------
$prompt = @"
This is the scheduled request check for floridacourserepo.com, run by Tools\check_requests.ps1 with
no one watching. Ron has approved this run ahead of time, so do NOT stop to ask for confirmation of
the batch. Where you would normally need his decision, skip that item and list it in the report.

Use the guide skill (.claude/skills/guide/SKILL.md) and follow Tools/CLAUDE.md and Tools/SOURCES.md
as you do in an ordinary session. Work from Tools/.

1. Run python review_lookup.py --requests first (Tools/CLAUDE.md requires it). Any course it marks
   HELD - ASK RON BEFORE WRITING is skipped in this run and reported with its REVIEW_QUEUE item.
2. Take up to $Batch of the other waiting requests in rank order. For each, as in earlier batches (see the git log, e.g.
   "Batches 243-244"): research and draft the guide, send the course's base data where it is
   missing, or decline it (shell courses and the like) with a public reason, as earlier runs did.
3. Validate (python validate_drafts.py on the batch). Never push past a FAIL: fix it or skip it.
4. Reconcile and push, then confirm each guide is live with /api/v1/courses/{id}/guide.
5. Also read the career-path requests (python career_paths.py requests). Do not write career
   paths in this run; just report what is waiting.
6. Update the docs earlier batches updated (Tools/NEXT_SESSION.md, Tools/SOURCES.md,
   Tools/REVIEW_QUEUE.md as needed). Commit only the files this run changed, with a message in the
   repo's style, and git push.
7. End with a short report: a table of guides published (course, credits, contact hours), the
   requests declined and why, the items skipped for Ron and why, how many requests are still
   waiting, and the career-path requests waiting.
"@

$logDir = Join-Path $Tools 'logs'
New-Item -ItemType Directory -Force $logDir | Out-Null
$log = Join-Path $logDir ("check-{0:yyyy-MM-dd_HHmm}.log" -f (Get-Date))

$allowed = @(
    'Read', 'Write', 'Edit', 'Glob', 'Grep', 'WebFetch', 'WebSearch', 'Skill', 'Agent',
    'Bash(python *)', 'Bash(curl *)', 'Bash(git *)', 'Bash(ls *)', 'Bash(cat *)', 'Bash(head *)',
    'Bash(grep *)', 'Bash(cd *)',
    'PowerShell(python *)', 'PowerShell(curl *)', 'PowerShell(git *)', 'PowerShell(Get-ChildItem *)',
    'PowerShell(Get-Content *)', 'PowerShell(Invoke-RestMethod *)'
)

Write-Host "Starting Claude Code (this usually takes a while; the report appears when it finishes)..."
Write-Host "Log: $log"
Write-Host ""

Push-Location $Repo
try {
    $prompt | claude -p --permission-mode acceptEdits --allowedTools $allowed 2>&1 |
        Tee-Object -FilePath $log
    $code = $LASTEXITCODE
} finally {
    Pop-Location
}

Write-Host ""
if ($code -eq 0) { Write-Host "Done. Report saved to $log" -ForegroundColor Green }
else             { Write-Host "Claude exited with code $code. See $log" -ForegroundColor Red }
exit $code
