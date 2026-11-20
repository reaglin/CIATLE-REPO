@echo off
rem The twice-weekly request check for floridacourserepo.com (see Tools\check_requests.ps1).
rem   check-requests              the normal check: Claude works up to 10 requests
rem   check-requests -Batch 5     work up to 5
rem   check-requests -CheckOnly   just list what is waiting (no Claude)
pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0Tools\check_requests.ps1" %*
echo.
pause
