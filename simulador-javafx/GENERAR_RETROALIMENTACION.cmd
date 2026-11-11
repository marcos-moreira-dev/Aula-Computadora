@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0RECOPILAR_RETROALIMENTACION.ps1"
if errorlevel 1 echo No se pudo generar el ZIP. Revisa el error anterior.
pause
endlocal
