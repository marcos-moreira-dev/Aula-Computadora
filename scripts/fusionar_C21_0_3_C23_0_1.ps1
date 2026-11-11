# Combina dos ZIP guardados en Descargas. No borra ni sobreescribe los originales.
$ErrorActionPreference = 'Stop'
$descargas = Join-Path $env:USERPROFILE 'Downloads'
$zipBase = Join-Path $descargas 'Aula_Computadora_C21_0_3_GLOBAL.zip'
$zipParche = Join-Path $descargas 'Aula_Computadora_C21_0_3_A_C23_0_1_PATCH.zip'
$zipSalida = Join-Path $descargas 'Aula_Computadora_C23_0_1_FUSIONADO.zip'

foreach ($archivo in @($zipBase, $zipParche)) {
    if (-not (Test-Path -LiteralPath $archivo -PathType Leaf)) {
        throw "Falta el archivo: $archivo"
    }
}
if (Test-Path -LiteralPath $zipSalida) {
    throw "La salida ya existe y no se reemplazará: $zipSalida"
}

$trabajo = Join-Path ([IO.Path]::GetTempPath()) ('FusionAulaC23_' + [guid]::NewGuid().ToString('N'))
$carpetaBase = Join-Path $trabajo 'base'
$carpetaParche = Join-Path $trabajo 'patch'
New-Item -ItemType Directory -Path $carpetaBase, $carpetaParche -Force | Out-Null
Write-Host "Carpeta temporal de trabajo: $trabajo"
Expand-Archive -LiteralPath $zipBase -DestinationPath $carpetaBase
Expand-Archive -LiteralPath $zipParche -DestinationPath $carpetaParche

$raizBase = Join-Path $carpetaBase 'Aula-Computadora'
$raizParche = Join-Path $carpetaParche 'Aula-Computadora'
if (-not (Test-Path -LiteralPath $raizBase -PathType Container) -or
    -not (Test-Path -LiteralPath $raizParche -PathType Container)) {
    throw 'Los dos ZIP deben contener la carpeta Aula-Computadora en la raíz.'
}
Copy-Item -Path (Join-Path $raizParche '*') -Destination $raizBase -Recurse -Force

foreach ($obligatorio in @(
    'libro/capitulos/22_un_bus_externo_de_16_bits.pdf',
    'libro/capitulos/23_programacion_para_aula_16.pdf',
    'simulador-javafx/VIDEO_AULA_V1_CONTRATO.json')) {
    if (-not (Test-Path -LiteralPath (Join-Path $raizBase $obligatorio))) {
        throw "Falta el archivo esperado en la fusión: $obligatorio"
    }
}
Compress-Archive -LiteralPath $raizBase -DestinationPath $zipSalida -CompressionLevel Optimal
Write-Host "Fusión lista: $zipSalida"
Write-Host 'Los ZIP de entrada no se eliminaron. La carpeta temporal se conservó para inspección.'
Write-Host 'Para probar (después de descomprimir el ZIP resultante):'
Write-Host '  py -3 scripts/verificar_capitulo_22.py'
Write-Host '  py -3 scripts/verificar_capitulo_23.py'
