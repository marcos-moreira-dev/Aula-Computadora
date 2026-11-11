@echo off
setlocal
rem Todo el trabajo se ejecuta en un proceso hijo, sin dejar un PAUSE.
rem No cierra otros procesos abiertos del usuario.
pushd "%~dp0"
if errorlevel 1 exit /b 1
py scripts\c28h_auditoria_global.py
set "CODE=%ERRORLEVEL%"
popd
exit /b %CODE%
