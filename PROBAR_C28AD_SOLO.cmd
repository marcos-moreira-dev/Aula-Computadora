@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo.
echo =============================================================
echo  AULA-COMPUTADORA C28-AD / LIBRO + VISTAS FISICA Y DIGITAL
echo =============================================================
where py >nul 2>nul
if not errorlevel 1 (
    py -3 scripts\c28ac_verificar_modelo_app.py
    if errorlevel 1 exit /b 1
    py -3 scripts\c28ad_verificar_vistas.py
) else (
    python scripts\c28ac_verificar_modelo_app.py
    if errorlevel 1 exit /b 1
    python scripts\c28ad_verificar_vistas.py
)
if errorlevel 1 exit /b 1
echo.
echo [APROBADO] Modelo digital y correspondencia entre recursos.
echo [AVISO] Esto NO valida simulacion electrica, 3D ni PCB.
echo.
echo Para ver el ejemplo de placa, abre:
echo c28_ad\figuras\AULA8_MAINBOARD_CONCEPTUAL_8_BITraces.png
exit /b 0
