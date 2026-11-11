@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0EJECUTAR_Y_CAPTURAR.ps1"
if errorlevel 1 echo Se encontro un problema. El ZIP de retroalimentacion contiene los detalles.
pause
endlocal
