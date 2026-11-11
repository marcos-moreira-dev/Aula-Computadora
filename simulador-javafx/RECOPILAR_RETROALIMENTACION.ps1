$ErrorActionPreference = 'Stop'
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$output = Join-Path $PSScriptRoot "Retroalimentacion_AULA_NAND2_$stamp.zip"
$work = Join-Path ([System.IO.Path]::GetTempPath()) "AULA_NAND2_FEEDBACK_$stamp"
New-Item -ItemType Directory -Path $work | Out-Null

try {
    try {
        & java -version 2>&1 | Out-File -FilePath (Join-Path $work 'java_version.txt') -Encoding utf8
    } catch {
        "No disponible: $($_.Exception.Message)" | Out-File (Join-Path $work 'java_version.txt')
    }
    try {
        & javac -version 2>&1 | Out-File -FilePath (Join-Path $work 'javac_version.txt') -Encoding utf8
    } catch {
        "No disponible: $($_.Exception.Message)" | Out-File (Join-Path $work 'javac_version.txt')
    }
    try {
        & mvn -version 2>&1 | Out-File -FilePath (Join-Path $work 'maven_version.txt') -Encoding utf8
        Push-Location $PSScriptRoot
        try {
            & mvn test 2>&1 | Out-File -FilePath (Join-Path $work 'maven_test.txt') -Encoding utf8
            "Exit code: $LASTEXITCODE" | Add-Content (Join-Path $work 'maven_test.txt')
        } finally {
            Pop-Location
        }
    } catch {
        "No disponible: $($_.Exception.Message)" | Out-File (Join-Path $work 'maven_test.txt')
    }

    @'
AULA COMPUTADORA — PRIMER TALLER NAND2
1. ¿Se abrió la ventana? (sí/no; describe el error)
2. ¿Se ve la placa/moldes sin cortar el área de trabajo?
3. ¿El botón, las pestañas y los paneles tienen esquinas cuadradas?
4. ¿Pudiste arrastrar o elegir PMOS y NMOS y encajarlos?
5. ¿Las cuatro pruebas mostraron 1,1,1,0 para un montaje correcto?
6. ¿El doble clic o clic derecho abrió el interior del encapsulado NAND2?
7. ¿Al cerrar y reabrir se conserva el avance?
8. ¿La rueda acerca/aleja y Shift + arrastre realiza paneo en 2D?
9. ¿La pestaña 3D muestra el montaje? ¿Puedes orbitar, acercar y desplazar?
10. ¿El inspector y el recorrido tienen cabeceras que llenan su ancho?
11. ¿Los iconos y botones se ven sobrios y completamente cuadrados?
12. ¿Qué cambiarías primero del aspecto o la interacción?
13. ¿Se ven claramente las redes del NAND2 en el molde y la placa 3D?
14. ¿Puedes plegar ambos paneles y siguen visibles los botones triangulares?
15. ¿El mensaje de Ayuda aparece completo sin puntos suspensivos?

Presiona F12 dentro de la aplicación para guardar capturas de su ventana.
'@ | Out-File -FilePath (Join-Path $work 'PREGUNTAS.txt') -Encoding utf8

    $screenshots = Join-Path $PSScriptRoot 'capturas'
    if (Test-Path -LiteralPath $screenshots) {
        Copy-Item -LiteralPath $screenshots -Destination (Join-Path $work 'capturas') -Recurse
    }

    Compress-Archive -Path (Join-Path $work '*') -DestinationPath $output
    Write-Host "ZIP generado: $output"
} finally {
    Remove-Item -LiteralPath $work -Recurse -Force
}
