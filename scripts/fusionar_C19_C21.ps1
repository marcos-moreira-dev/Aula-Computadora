# Fusión conservadora: C19 original + parche C19->C21.
# Conservar los dos ZIP fuente; generar un tercer ZIP con todos los archivos.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem

$descargas = Join-Path $env:USERPROFILE 'Downloads'
$base = Join-Path $descargas 'Aula_Computadora_C19_0_1_GLOBAL.zip'
$parche = Join-Path $descargas 'Aula_Computadora_C19_a_C21_PATCH.zip'
$salida = Join-Path $descargas 'Aula_Computadora_C21_0_1_FUSIONADA.zip'
$temporal = Join-Path $descargas ('Aula_Computadora_C21_TEMP_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff'))

foreach ($archivo in @($base, $parche)) {
    if (-not (Test-Path -LiteralPath $archivo -PathType Leaf)) {
        throw "No se encontró el archivo requerido: $archivo"
    }
}
if (Test-Path -LiteralPath $salida) {
    throw "Ya existe $salida. Se detuvo para no sobrescribirlo."
}

New-Item -ItemType Directory -Path $temporal | Out-Null
Expand-Archive -LiteralPath $base -DestinationPath $temporal
Expand-Archive -LiteralPath $parche -DestinationPath $temporal -Force
[System.IO.Compression.ZipFile]::CreateFromDirectory($temporal, $salida)

$archivoFinal = [System.IO.Compression.ZipFile]::OpenRead($salida)
try {
    $rutas = @($archivoFinal.Entries | ForEach-Object { $_.FullName })
    foreach ($necesaria in @(
        '.gitignore', '.github/workflows/documentacion.yml',
        'libro/capitulos/20_programar_un_pequeno_sistema.pdf',
        'libro/capitulos/21_que_implica_ampliar_la_palabra.pdf',
        'scripts/ensamblador_dos_pasadas_aula8_educativo.py'
    )) {
        if ($rutas -notcontains $necesaria) { throw "Falta $necesaria en el ZIP fusionado" }
    }
}
finally {
    $archivoFinal.Dispose()
}

Write-Host "ZIP C21 fusionado y comprobado: $salida" -ForegroundColor Green
Write-Host "Las fuentes y la carpeta temporal siguen intactas: $temporal"
explorer.exe /select,$salida
