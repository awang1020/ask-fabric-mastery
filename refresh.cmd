@echo off
rem One double-click to refresh the Ask Fabric Mastery index from the latest
rem Substack edition. Opens a console window so you can watch progress.
pushd "%~dp0"
pwsh -NoProfile -ExecutionPolicy Bypass -File "scripts\refresh.ps1" %*
set EXITCODE=%ERRORLEVEL%
popd
echo.
echo Press any key to close...
pause >nul
exit /b %EXITCODE%
