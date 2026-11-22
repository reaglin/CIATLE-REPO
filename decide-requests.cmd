@echo off
rem Decide the guide requests on hold for floridacourserepo.com (see Tools\guide_requests.py).
rem Shows each held request with the reason it could not be written, then:
rem   A  decline all, each with its reason (shown publicly; visitors may request again)
rem   O  one at a time: decline, edit the reason, or send it back to be written
cd /d "%~dp0Tools"
python guide_requests.py decide
echo.
pause
