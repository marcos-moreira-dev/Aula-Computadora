# C28-P · Entrega y pruebas de la siguiente auditoría

**Base:** `Aula_Computadora_C28_H_GLOBAL_COMPLETO.zip`, que ya incluye
los 26 capítulos, Word/PDF C28-G, suplemento C28-H y atlas histórico C28-O.

Este avance añade la auditoría C28-P y sus informes. No altera el maestro
Word/PDF, la ISA, el mapa de memoria, el contrato de vídeo ni las políticas
de PC. Progreso editorial estimado: **84 %**; siguiente meta de Windows:
**19 controles**, uno adicional respecto a los 18 ya aprobados.

## A. Si descargas el nuevo ZIP global completo

Guarda `Aula_Computadora_C28_P_GLOBAL_COMPLETO.zip` en Descargas.
Abre PowerShell en Descargas y ejecuta **todo este bloque**:

```powershell
$ErrorActionPreference = 'Stop'
$descargas = Join-Path $env:USERPROFILE 'Downloads'
$zip = Join-Path $descargas 'Aula_Computadora_C28_P_GLOBAL_COMPLETO.zip'
if (-not (Test-Path -LiteralPath $zip -PathType Leaf)) {
    throw "Falta $zip"
}
$destino = Join-Path $descargas ('Aula_C28P_PRUEBA_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
Expand-Archive -LiteralPath $zip -DestinationPath $destino
$comprobador = Join-Path $destino 'Aula-Computadora\PROBAR_TODO_GLOBAL_C28H.cmd'
if (-not (Test-Path -LiteralPath $comprobador -PathType Leaf)) {
    throw 'No se encontró el comprobador global en el ZIP'
}
try {
    & $comprobador
    $codigo = $LASTEXITCODE
} finally {
    Set-Location -LiteralPath $descargas
}
$resultado = Get-ChildItem -LiteralPath (Join-Path $destino 'Aula-Computadora') -Filter 'Retroalimentacion_GLOBAL_C28H_*.zip' -File |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $resultado) { throw 'No se generó el ZIP de retroalimentación' }
Write-Host ('RETROALIMENTACIÓN: ' + $resultado.FullName) -ForegroundColor Cyan
Write-Host ('CÓDIGO FINAL: ' + $codigo)
```

Envíame el ZIP de retroalimentación que aparezca al final. Los modelos
Python no necesitan red; Icarus e Inkscape siguen siendo necesarios
para los respectivos controles de simulación y renderizado. La recolección
auxiliar de fotos puede requerir Wikimedia Commons, pero las cinco fotos
ya están incluidas en el global.

## B. Si prefieres descargar solo el parche pequeño

Coloca en Descargas **ambos** archivos:

- `Aula_Computadora_C28_H_GLOBAL_COMPLETO.zip` anterior.
- `Aula_Computadora_C28_P_PARCHE.zip` nuevo.

Ejecuta primero el bloque siguiente para generar el global actualizado,
**sin borrar el ZIP anterior**, y luego ejecuta el bloque del apartado A:

```powershell
$ErrorActionPreference = 'Stop'
$descargas = Join-Path $env:USERPROFILE 'Downloads'
$anterior = Join-Path $descargas 'Aula_Computadora_C28_H_GLOBAL_COMPLETO.zip'
$parche = Join-Path $descargas 'Aula_Computadora_C28_P_PARCHE.zip'
$nuevo = Join-Path $descargas 'Aula_Computadora_C28_P_GLOBAL_COMPLETO.zip'
foreach ($archivo in @($anterior, $parche)) {
    if (-not (Test-Path -LiteralPath $archivo -PathType Leaf)) {
        throw "Falta $archivo"
    }
}
if (Test-Path -LiteralPath $nuevo) {
    throw "Ya existe el ZIP destino: $nuevo. No se sobrescribe."
}
$temporal = Join-Path $descargas ('Aula_C28P_FUSION_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
New-Item -ItemType Directory -Path $temporal | Out-Null
Expand-Archive -LiteralPath $anterior -DestinationPath $temporal
Expand-Archive -LiteralPath $parche -DestinationPath $temporal -Force
Compress-Archive -Path (Join-Path $temporal 'Aula-Computadora') -DestinationPath $nuevo
Write-Host ('GLOBAL ACTUALIZADO: ' + $nuevo) -ForegroundColor Green
```

El bloque no elimina el original ni la carpeta temporal. No se altera la
política de ejecución de PowerShell, ni se cierran procesos ajenos.

## Resultado esperado

- Nuevo control: `LIBRO_C28P_TRAMO_FINAL`.
- Si todo pasa, el resumen debe mostrar **19/19** y **0 fallidos**.
- Se conservan las trazas de HDL, los hashes maestros y el detalle de
  cualquier fallo; no se certifica hardware ni una CPU integrada.
