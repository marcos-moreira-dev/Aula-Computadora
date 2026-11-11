@echo off
setlocal
cd /d "%~dp0"
where java >nul 2>nul
if errorlevel 1 (
  echo ERROR: instala Java 21 y configuralo en PATH.
  pause
  exit /b 1
)
where mvn >nul 2>nul
if errorlevel 1 (
  echo ERROR: necesitas Maven 3.9 o posterior en PATH.
  echo Consulta docs\PRIMER_TALLER_EJECUCION.md
  pause
  exit /b 1
)
echo Verificando pruebas del taller NAND2...
call mvn test
if errorlevel 1 (
  echo FALLARON las pruebas; no se iniciara la interfaz.
  pause
  exit /b 1
)
echo Abriendo Aula Computadora...
call mvn javafx:run
if errorlevel 1 (
  echo La aplicacion finalizo con un error. Revisa la consola.
)
pause
endlocal
