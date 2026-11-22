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
  4. A request Claude cannot write is put ON HOLD on the site with a reason worded for the public.
     At the end you are shown every held request with its reason and asked what to do
     (Tools\guide_requests.py decide): decline all, one at a time, or leave them. A declined
     request shows its reason publicly, and visitors can request the course again if that changes.
     decide-requests.cmd in the repo root does step 4 on its own.

  Run it from check-requests.cmd in the repo root (double-click it, or run it in a terminal).

.PARAMETER Batch
  The most requests to work in one run (default 10). The rest wait for the next run.

.PARAMETER CheckOnly
  List what is waiting, offer the held decisions, and stop. Claude is not started.

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

# Held = waiting for Ron's decision, not for Claude.
$work = @($guides.items | Where-Object { $_.status -ne 'Held' })
$held = @($guides.items | Where-Object { $_.status -eq 'Held' })

function Invoke-HeldDecisions {
    if ($held.Count -eq 0) { return }
    Push-Location $Tools
    try { python guide_requests.py decide } finally { Pop-Location }
}

Write-Host ""
Write-Host "Curriculum-guide requests to work:  $($work.Count)" -ForegroundColor Cyan
foreach ($i in $work) {
    Write-Host ("  {0,3}. {1,-10} {2}  ({3} request(s))" -f $i.rank, $i.courseId, $i.title, $i.requestCount)
}
if ($held.Count -gt 0) {
    Write-Host "On hold for your decision:          $($held.Count)  ($((@($held | ForEach-Object { $_.courseId })) -join ', '))" -ForegroundColor Yellow
}
Write-Host "Career-path requests waiting:      $($careers.waiting)" -ForegroundColor Cyan
foreach ($i in $careers.items) { Write-Host "       $($i | ConvertTo-Json -Compress -Depth 2)" }
Write-Host ""

if ($CheckOnly) { Invoke-HeldDecisions; exit 0 }

if ($work.Count -eq 0 -and $careers.waiting -eq 0) {
    Write-Host "Nothing to work. No Claude session needed." -ForegroundColor Green
    Invoke-HeldDecisions
    exit 0
}

# ---- 2. Claude does the work ------------------------------------------------------------
$prompt = @"
This is the scheduled request check for floridacourserepo.com, run by Tools\check_requests.ps1 with
no one watching. Ron has approved this run ahead of time, so do NOT stop to ask for confirmation of
the batch. Where you would normally need his decision, skip that item and list it in the report.

Use the guide skill (.claude/skills/guide/SKILL.md) and follow Tools/CLAUDE.md and Tools/SOURCES.md
as you do in an ordinary session. Work from Tools/.

1. Run python review_lookup.py --requests first (Tools/CLAUDE.md requires it). Requests already ON
   HOLD on the site are Ron's to decide: leave them alone. Read the open ones with
   python guide_requests.py list --status open: a course declined before and requested again shows the
   old reason and what the requester says has changed; write it if the change makes it writable.
2. Take up to $Batch of the waiting requests in rank order. For each, as in earlier batches (see the git log, e.g.
   "Batches 243-244"): research and draft the guide, send the course's base data where it is
   missing, or decline a shell course (special topics, independent study and the like) with a public
   reason, as earlier runs did.
   Any course you cannot write for another reason (no readable description, a course the college
   no longer teaches, a course a REVIEW_QUEUE item marks HELD - ASK RON) is put ON HOLD for Ron with
   python guide_requests.py hold <ID> "<reason>". The reason is shown to the public if Ron declines,
   so write one to three plain sentences about the course: what is missing and what would let it be
   written (for example "Florida Poly, the only college that offers EEL4448, does not publish a
   description or syllabus for it, so there is nothing to base a guide on. If one is published, the
   course can be requested again."). Never name Ron, a REVIEW_QUEUE item, or the visitor. Also add
   the REVIEW_QUEUE item as before.
3. Validate (python validate_drafts.py on the batch). Never push past a FAIL: fix it or skip it.
4. Reconcile and push, then confirm each guide is live with /api/v1/courses/{id}/guide.
5. Also read the career-path requests (python career_paths.py requests). Do not write career
   paths in this run; just report what is waiting.
6. Update the docs earlier batches updated (Tools/NEXT_SESSION.md, Tools/SOURCES.md,
   Tools/REVIEW_QUEUE.md as needed). Commit only the files this run changed, with a message in the
   repo's style, and git push.
7. End with a short report: a table of guides published (course, credits, contact hours), the
   requests declined and why, the requests put on hold and their reasons, how many requests are
   still waiting, and the career-path requests waiting. (Ron decides the held ones right after.)
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

# The run may have put more on hold: re-read, then offer the decisions.
try {
    $guides = (Invoke-RestMethod "$Base/queue/guides?status=waiting" -TimeoutSec 30).data
    $held = @($guides.items | Where-Object { $_.status -eq 'Held' })
} catch { }
Invoke-HeldDecisions
exit $code
