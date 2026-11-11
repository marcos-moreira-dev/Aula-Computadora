# Pruebas C28-G para ejecutar desde PowerShell 5.1 o superior.
# Si no hay Icarus, conserva el resultado Python y registra HDL pendiente.
$ErrorActionPreference = "Stop"
$raiz = Split-Path -Parent $PSScriptRoot
$marca = Get-Date -Format "yyyyMMdd_HHmmss"
$salida = Join-Path $raiz ("_PRUEBAS_C28G_" + $marca)
New-Item -Path $salida -ItemType Directory -Force | Out-Null
Push-Location $raiz
try {
    "Aula-Computadora C28-G - evidencia de anfitrion" |
        Set-Content (Join-Path $salida "RESUMEN_C28G.txt") -Encoding UTF8
    & py .\scripts\c28f_incremento_mary_saltos.py 2>&1 |
        Tee-Object -FilePath (Join-Path $salida "C28F_PYTHON.txt")
    if ($LASTEXITCODE -ne 0) { throw "Fallo del piloto C28-F" }
    & py .\scripts\c28g_auditar_hdl_y_memoria.py 2>&1 |
        Tee-Object -FilePath (Join-Path $salida "C28G_PYTHON.txt")
    if ($LASTEXITCODE -ne 0) { throw "Fallo del piloto C28-G" }

    $hdl = Get-Command iverilog -ErrorAction SilentlyContinue
    $vvp = Get-Command vvp -ErrorAction SilentlyContinue
    if ($null -ne $hdl -and $null -ne $vvp) {
        & iverilog -g2012 -o (Join-Path $salida "pc_mar_tb.vvp") `
            .\c28_f\piloto_pc_mar\pc_mar_c28f.v `
            .\c28_f\piloto_pc_mar\tb_pc_mar_c28f.v 2>&1 |
            Tee-Object -FilePath (Join-Path $salida "COMPILACION_IVERILOG.txt")
        if ($LASTEXITCODE -ne 0) { throw "Compilacion Icarus incorrecta" }
        & vvp (Join-Path $salida "pc_mar_tb.vvp") 2>&1 |
            Tee-Object -FilePath (Join-Path $salida "EJECUCION_VVP.txt")
        if ($LASTEXITCODE -ne 0) { throw "Simulacion Icarus incorrecta" }
        "HDL: Icarus Verilog ejecutado correctamente en ESTE equipo." |
            Add-Content (Join-Path $salida "RESUMEN_C28G.txt")
    } else {
        "HDL: no ejecutado. Icarus Verilog (iverilog y vvp) no disponible." |
            Add-Content (Join-Path $salida "RESUMEN_C28G.txt")
    }
    Get-FileHash .\c28_f\piloto_pc_mar\pc_mar_c28f.v -Algorithm SHA256 |
        Format-List | Out-File (Join-Path $salida "HASH_HDL.txt")
    Get-FileHash .\c28_g\piloto_lectura\auditoria_y_trazas.json -Algorithm SHA256 |
        Format-List | Out-File (Join-Path $salida "HASH_TRAZAS.txt")
    $zip = Join-Path $raiz ("Retroalimentacion_C28G_" + $marca + ".zip")
    Compress-Archive -Path (Join-Path $salida "*") -DestinationPath $zip -Force
    Write-Host "Pruebas terminadas. Adjunta el siguiente ZIP:" -ForegroundColor Green
    Write-Host $zip
    Start-Process explorer.exe -ArgumentList $raiz
} finally {
    Pop-Location
}
