# Flujo único para Windows: pruebas Maven -> GUI -> capturas F12 -> ZIP.
# No captura el escritorio completo ni sube información a ningún servidor.
$ErrorActionPreference = 'Continue'
$started = Get-Date
$stamp = $started.ToString('yyyyMMdd_HHmmss')
$temp = Join-Path ([System.IO.Path]::GetTempPath()) "AULA_GUI_FEEDBACK_$stamp"
$zip = Join-Path $PSScriptRoot "Retroalimentacion_AULA_GUI_$stamp.zip"
$returnCode = 0

New-Item -ItemType Directory -Path $temp -Force | Out-Null
try {
    $logs = Join-Path $temp 'logs'
    New-Item -ItemType Directory -Path $logs | Out-Null

    $tools = @(
        @{ Command = 'java'; Argument = '-version'; File = 'java_version.txt' },
        @{ Command = 'javac'; Argument = '-version'; File = 'javac_version.txt' },
        @{ Command = 'mvn'; Argument = '-version'; File = 'maven_version.txt' }
    )
    foreach ($item in $tools) {
        $commandName = $item.Command
        $destination = Join-Path $logs $item.File
        if (Get-Command $commandName -ErrorAction SilentlyContinue) {
            & $commandName $item.Argument 2>&1 | Out-File -FilePath $destination -Encoding utf8
        } else {
            "No disponible: $commandName" | Out-File -FilePath $destination -Encoding utf8
        }
    }

    if (-not (Get-Command mvn -ErrorAction SilentlyContinue)) {
        'ERROR: Maven no está disponible en PATH.' |
            Out-File (Join-Path $logs 'maven_test.txt') -Encoding utf8
        $returnCode = 2
    } else {
        Push-Location $PSScriptRoot
        try {
            Write-Host '1/3 Verificando el proyecto JavaFX con Maven...' -ForegroundColor Cyan
            & mvn clean test 2>&1 | Out-File (Join-Path $logs 'maven_test.txt') -Encoding utf8
            $testExit = $LASTEXITCODE
            if ($testExit -ne 0) {
                Write-Host 'Fallaron las pruebas; revisa el log del ZIP.' -ForegroundColor Yellow
                $returnCode = 3
            } else {
                Write-Host '2/3 Abriendo Aula Computadora...' -ForegroundColor Cyan
                Write-Host '  Interactúa con Montaje 2D, Placa 3D e Interior NAND2.'
                Write-Host '  Pulsa F12 en la ventana cada vez que quieras una captura.'
                Write-Host '  Cierra la ventana de Aula para generar el ZIP automáticamente.'
                & mvn javafx:run 2>&1 | Out-File (Join-Path $logs 'javafx_run.txt') -Encoding utf8
                if ($LASTEXITCODE -ne 0) { $returnCode = 4 }
            }
        } finally {
            Pop-Location
        }
    }

    $shots = Join-Path $PSScriptRoot 'capturas'
    $dest = Join-Path $temp 'capturas'
    New-Item -ItemType Directory -Path $dest | Out-Null
    if (Test-Path -LiteralPath $shots) {
        Get-ChildItem -LiteralPath $shots -Filter '*.png' -File |
            Where-Object { $_.LastWriteTime -ge $started } |
            ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $dest }
    }

    @'
AULA COMPUTADORA — RETROALIMENTACIÓN DE LA VENTANA REAL
1. ¿La barra de herramientas usa iconos nítidos y cuadrados?
2. ¿RECORRIDO e INSPECTOR ocupan el ancho completo, sin franjitas?
3. ¿Se puede acercar, alejar y panear en Montaje 2D e Interior NAND2?
4. ¿Se puede orbitar y desplazar la placa 3D sin confundirlo con colocar piezas?
5. ¿Dentro de la cucarachita blanca se ven P1/P2, N1/N2 y los cables a A/B/Y/VDD/GND?
6. ¿Se pudieron colocar piezas por clic/arrastre? ¿Cómo quedó la tabla de verdad?
7. ¿Qué elemento visual todavía se ve demasiado primitivo?
8. Si la aplicación falló, ¿en qué momento y con qué mensaje?
9. ¿Las redes VDD/A/B/Y/MID/GND se ven conectadas al molde en 2D y 3D?
10. ¿Han desaparecido las diagonales espurias de los rectángulos 3D?
11. ¿Se pueden plegar/desplegar ambos laterales y se libera el espacio?
12. ¿El diálogo Ayuda muestra el mensaje completo sin truncarlo con '...'?
13. ¿Las etiquetas P1/P2/N1/N2 y PMOS/NMOS se leen sin espejo en Placa 3D?
14. ¿Se distinguen exactamente tres patas metálicas salientes por transistor
    en la vista 2D y en la 3D, desde una cámara oblicua?

Nota: F12 guarda la ventana JavaFX en la carpeta capturas. Este ZIP
solo incluye las capturas tomadas durante esta ejecución.
'@ | Out-File (Join-Path $temp 'RESPUESTAS.txt') -Encoding utf8

    Write-Host '3/3 Empaquetando logs y capturas...' -ForegroundColor Cyan
    Compress-Archive -Path (Join-Path $temp '*') -DestinationPath $zip
    Write-Host "Retroalimentación lista: $zip" -ForegroundColor Green
} catch {
    Write-Host "No pudo completarse el proceso: $($_.Exception.Message)" -ForegroundColor Red
    $returnCode = 5
    try {
        "Error: $($_.Exception.Message)" | Out-File (Join-Path $temp 'ERROR.txt') -Encoding utf8
        Compress-Archive -Path (Join-Path $temp '*') -DestinationPath $zip
        Write-Host "Paquete de diagnóstico: $zip"
    } catch { Write-Host 'Tampoco pudo empaquetarse el diagnóstico.' }
} finally {
    if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Recurse -Force }
}
exit $returnCode
