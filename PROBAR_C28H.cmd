@echo off
setlocal
rem El proceso vuelve a su directorio original y se cierra automaticamente.
rem Si el PowerShell que lo invoca ESTA dentro de una carpeta antigua,
rem el propio PowerShell seguira alli: salir con Set-Location ..
pushd "%~dp0"
if errorlevel 1 exit /b 1
set "RESULTADO=0"
echo ===== C28-H: referencia Python =====
if not exist c28_h\piloto mkdir c28_h\piloto
py scripts\c28h_piloto.py > c28_h\piloto\RESULTADO_PYTHON.txt 2>&1
if errorlevel 1 goto :python_fail
type c28_h\piloto\RESULTADO_PYTHON.txt
rem El instalador winget puede dejar Icarus fuera del PATH actual.
if exist "C:\iverilog\bin\iverilog.exe" set "PATH=C:\iverilog\bin;%PATH%"
if exist "%ProgramFiles%\Icarus Verilog\bin\iverilog.exe" set "PATH=%ProgramFiles%\Icarus Verilog\bin;%PATH%"
if exist "%ProgramFiles(x86)%\Icarus Verilog\bin\iverilog.exe" set "PATH=%ProgramFiles(x86)%\Icarus Verilog\bin;%PATH%"
where iverilog >nul 2>nul
if errorlevel 1 goto :noicarus
where vvp >nul 2>nul
if errorlevel 1 goto :noicarus
echo ===== C28-H: compilacion Icarus =====
iverilog -g2012 -s tb_lectura_c28h -o c28_h\piloto\c28h.vvp c28_h\rtl\lectura_c28h.v c28_h\rtl\tb_lectura_c28h.v > c28_h\piloto\RESULTADO_COMPILACION.txt 2>&1
if errorlevel 1 goto :hdl_fail
echo ===== C28-H: ejecucion Icarus =====
vvp c28_h\piloto\c28h.vvp > c28_h\piloto\RESULTADO_IVERILOG.txt 2>&1
if errorlevel 1 goto :hdl_fail
type c28_h\piloto\RESULTADO_IVERILOG.txt
goto :package
:noicarus
echo Icarus no aparece en PATH. Se entrega evidencia de Python sin certificar HDL.
echo Icarus NO ENCONTRADO > c28_h\piloto\RESULTADO_IVERILOG.txt
set "RESULTADO=2"
:package
echo ===== C28-H: crear retroalimentacion =====
powershell.exe -NoProfile -Command "$z='Retroalimentacion_C28H_'+(Get-Date -Format yyyyMMdd_HHmmss)+'.zip'; Compress-Archive -Path 'c28_h\piloto\*' -DestinationPath $z; Write-Host ('ENTREGAR: '+$z)"
if errorlevel 1 goto :package_fail
echo.
echo Terminado. Adjunta el ZIP Retroalimentacion_C28H generado en esta carpeta.
if "%RESULTADO%"=="2" echo ATENCION: la simulacion HDL quedo pendiente.
if "%RESULTADO%"=="1" echo ATENCION: fallo una prueba. Revisar archivos RESULTADO_* del ZIP.
echo El comprobador se cerrara y liberara su directorio.
popd
exit /b %RESULTADO%
:hdl_fail
echo Icarus fallo: se conservaran sus registros en el ZIP.
if exist c28_h\piloto\RESULTADO_COMPILACION.txt type c28_h\piloto\RESULTADO_COMPILACION.txt
if exist c28_h\piloto\RESULTADO_IVERILOG.txt type c28_h\piloto\RESULTADO_IVERILOG.txt
set "RESULTADO=1"
goto :package
:python_fail
echo ERROR: fallo el modelo Python. Se conservara su salida en el ZIP.
type c28_h\piloto\RESULTADO_PYTHON.txt
set "RESULTADO=1"
goto :package
:package_fail
echo.
echo ERROR: no se pudo crear el ZIP. Copia esta salida para diagnostico.
popd
exit /b 1
