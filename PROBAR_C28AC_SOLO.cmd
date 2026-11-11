@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo.
echo =============================================================
echo    AULA-COMPUTADORA C28-AC  /  MODELO DIGITAL PARA EL APP
echo =============================================================
echo.
where py >nul 2>nul
if not errorlevel 1 (
    py -3 scripts\c28ac_verificar_modelo_app.py
) else (
    python scripts\c28ac_verificar_modelo_app.py
)
set "RESULTADO=%ERRORLEVEL%"
echo.
if not "%RESULTADO%"=="0" (
    echo [FALLIDO] Revisar Python y el informe de C28-AC.
    exit /b %RESULTADO%
)
echo [APROBADO] Modelo digital, conectividad y archivos de figuras.
echo [NOTA] No se han simulado tensiones ni retardos electricos.
echo.
echo Abre el visor de pasos con doble clic en:
echo c28_ac\activos_app\Visor_PASO_A_PASO_C28W.html
echo.
echo Reporte: c28_ac\auditoria\C28_AC_RESULTADOS.json
exit /b 0
