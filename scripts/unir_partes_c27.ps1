# Une las 12 partes descargadas y extrae C27 sin sobrescribir carpetas existentes.
# Ejecutar desde PowerShell (no requiere Python ni 7-Zip):
# & "$env:USERPROFILE\Downloads\unir_partes_c27.ps1"
$ErrorActionPreference = 'Stop'
$Descargas = Join-Path ([Environment]::GetFolderPath('UserProfile')) 'Downloads'
$Nombre = 'Aula_Computadora_C27_GLOBAL.zip'
$Salida = Join-Path $Descargas $Nombre
$Destino = Join-Path $Descargas 'Aula_Computadora_C27_EXTRAIDO'
if (Test-Path -LiteralPath $Salida) { throw "Ya existe $Salida. Muevelo o cambiale el nombre antes de ejecutar." }
if (Test-Path -LiteralPath $Destino) { throw "Ya existe $Destino. No se sobreescribira." }
$Partes = @(1..12 | ForEach-Object { Join-Path $Descargas ('{0}.part{1:d2}' -f $Nombre, $_) })
foreach ($Parte in $Partes) {
    if (-not (Test-Path -LiteralPath $Parte -PathType Leaf)) { throw "Falta la parte: $Parte" }
}
$FlujoSalida = [System.IO.File]::Open($Salida, [System.IO.FileMode]::CreateNew)
try {
    foreach ($Parte in $Partes) {
        $FlujoEntrada = [System.IO.File]::OpenRead($Parte)
        try { $FlujoEntrada.CopyTo($FlujoSalida) }
        finally { $FlujoEntrada.Dispose() }
    }
} finally { $FlujoSalida.Dispose() }
Write-Host 'SHA256 del ZIP unido:' -ForegroundColor Cyan
$Huella = (Get-FileHash -LiteralPath $Salida -Algorithm SHA256).Hash
Write-Host $Huella
$RutaManifiesto = Join-Path $Descargas 'MANIFIESTO_ENTREGA_C27.json'
if (Test-Path -LiteralPath $RutaManifiesto -PathType Leaf) {
    $Esperada = (Get-Content -LiteralPath $RutaManifiesto -Raw -Encoding UTF8 | ConvertFrom-Json).global.sha256
    if ($Huella -ne $Esperada) { throw "El SHA256 no coincide con el manifiesto. No se extraera el archivo." }
    Write-Host 'Integridad validada contra el manifiesto.' -ForegroundColor Green
} else {
    Write-Warning 'Descarga tambien MANIFIESTO_ENTREGA_C27.json para contrastar automaticamente el SHA256.'
}
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($Salida, $Destino)
Write-Host "Extraido en: $Destino" -ForegroundColor Green
Start-Process explorer.exe -ArgumentList $Destino
