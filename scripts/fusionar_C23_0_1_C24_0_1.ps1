# Fusionar en Descargas un ZIP base C23 y un parche C24. No borrar originales.
$ErrorActionPreference = 'Stop'
$downloads = Join-Path $env:USERPROFILE 'Downloads'
$baseZip = Join-Path $downloads 'Aula_Computadora_C23_0_1_GLOBAL.zip'
$patchZip = Join-Path $downloads 'Aula_Computadora_C23_0_1_A_C24_0_1_PATCH.zip'
$resultZip = Join-Path $downloads 'Aula_Computadora_C24_0_1_FUSIONADO.zip'

foreach ($item in @($baseZip, $patchZip)) {
    if (-not (Test-Path -LiteralPath $item -PathType Leaf)) {
        throw "No se encontró el ZIP esperado: $item"
    }
}
if (Test-Path -LiteralPath $resultZip) {
    throw "La salida ya existe; no se reemplazará: $resultZip"
}

$work = Join-Path ([IO.Path]::GetTempPath()) ('Aula_C24_' + [guid]::NewGuid().ToString('N'))
$baseDir = Join-Path $work 'base'
$patchDir = Join-Path $work 'patch'
New-Item -ItemType Directory -Path $baseDir,$patchDir -Force | Out-Null
Write-Host "Trabajo temporal: $work"
Expand-Archive -LiteralPath $baseZip -DestinationPath $baseDir
Expand-Archive -LiteralPath $patchZip -DestinationPath $patchDir

$project = Join-Path $baseDir 'Aula-Computadora'
$change = Join-Path $patchDir 'Aula-Computadora'
foreach ($folder in @($project, $change)) {
    if (-not (Test-Path -LiteralPath $folder -PathType Container)) {
        throw "Paquete inválido: no contiene la carpeta Aula-Computadora: $folder"
    }
}

# Superposición ARCHIVO A ARCHIVO. Evita anidar directorios que ya existen.
# -Force incluye configuración de CI bajo .github y otras rutas ocultas.
$prefixLength = $change.Length + 1
foreach ($item in (Get-ChildItem -LiteralPath $change -Recurse -File -Force)) {
    $relative = $item.FullName.Substring($prefixLength)
    $target = Join-Path $project $relative
    $parent = Split-Path -Parent $target
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    Copy-Item -LiteralPath $item.FullName -Destination $target -Force
}

foreach ($required in @(
    'libro/capitulos/23v_de_mapas_de_caracteres_a_escritorio_grafico.pdf',
    'libro/capitulos/24_una_computadora_que_podemos_explicar.pdf',
    'scripts/verificar_entrega_c24.py',
    'simulador-javafx/VIDEO_AULA_V1_CONTRATO.json')) {
    if (-not (Test-Path -LiteralPath (Join-Path $project $required) -PathType Leaf)) {
        throw "Archivo obligatorio faltante después de fusionar: $required"
    }
}

Compress-Archive -LiteralPath $project -DestinationPath $resultZip -CompressionLevel Optimal
Write-Host "FUSIÓN TERMINADA: $resultZip"
Write-Host 'No se borraron los ZIP de entrada. Se conserva la carpeta temporal.'
Write-Host 'Para probar: expande el ZIP resultante, abre su carpeta Aula-Computadora y ejecuta:'
Write-Host '  py -3 scripts/verificar_entrega_c24.py'
