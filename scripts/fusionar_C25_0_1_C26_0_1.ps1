# Fusionar base C25 + parche C26 desde Descargas; no elimina originales.
$ErrorActionPreference = 'Stop'
$downloads = Join-Path $env:USERPROFILE 'Downloads'
$baseZip = Join-Path $downloads 'Aula_Computadora_C25_0_1_GLOBAL.zip'
$patchZip = Join-Path $downloads 'Aula_Computadora_C25_0_1_A_C26_0_1_PATCH.zip'
$resultZip = Join-Path $downloads 'Aula_Computadora_C26_0_1_FUSIONADO.zip'

foreach ($item in @($baseZip, $patchZip)) {
    if (-not (Test-Path -LiteralPath $item -PathType Leaf)) {
        throw "ZIP de entrada ausente: $item"
    }
}
if (Test-Path -LiteralPath $resultZip) {
    throw "No se sobrescribe la salida existente: $resultZip"
}

$work = Join-Path ([IO.Path]::GetTempPath()) ('Aula_C26_' + [guid]::NewGuid().ToString('N'))
$baseDir = Join-Path $work 'base'
$patchDir = Join-Path $work 'patch'
New-Item -ItemType Directory -Path $baseDir,$patchDir -Force | Out-Null
Expand-Archive -LiteralPath $baseZip -DestinationPath $baseDir
Expand-Archive -LiteralPath $patchZip -DestinationPath $patchDir

$project = Join-Path $baseDir 'Aula-Computadora'
$change = Join-Path $patchDir 'Aula-Computadora'
foreach ($folder in @($project, $change)) {
    if (-not (Test-Path -LiteralPath $folder -PathType Container)) {
        throw "Paquete sin carpeta Aula-Computadora: $folder"
    }
}

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
    'libro/Aula_Computadora_C26_0_1_MAESTRO.docx',
    'libro/Aula_Computadora_C26_0_1_MAESTRO.pdf',
    'libro/INDICE_C26_0_1.json',
    'FUENTES_CONSULTADAS.txt',
    'scripts/verificar_libro_maestro.py')) {
    if (-not (Test-Path -LiteralPath (Join-Path $project $required) -PathType Leaf)) {
        throw "Falta archivo necesario: $required"
    }
}

Compress-Archive -LiteralPath $project -DestinationPath $resultZip -CompressionLevel Optimal
Write-Host "FUSIÓN TERMINADA: $resultZip"
Write-Host 'Los ZIP de entrada permanecen intactos.'
Write-Host 'Comprobar al extraer el ZIP: py -3 scripts/verificar_libro_maestro.py'
