@echo off
rem How many people visit floridacourserepo.com: a report from the server logs.
rem Double-click it, or run it from any folder. Extra arguments go to the script, e.g. -Days 7
pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0Deployment\visitor-report.ps1" %* -Open
echo.
pause
