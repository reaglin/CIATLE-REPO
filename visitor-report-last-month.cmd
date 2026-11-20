@echo off
rem The monthly visitor check: a report on last month from the server logs.
rem Double-click it in the first days of each month. Saved as Deployment\visitor-reports\visitors-month-YYYY-MM.md
pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0Deployment\visitor-report.ps1" -LastMonth
echo.
pause
