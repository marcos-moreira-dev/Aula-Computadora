# Aula-Computadora C28-H · Global completo para pruebas

Este ZIP incluye **todos los archivos recibidos de C28-G** (libro Word/PDF,
26 fascículos Word/PDF/Markdown, figuras, código, pilotos y scripts) **más**
el piloto secuencial C28-H y los complementos editoriales hasta C28-O.
No requiere fusionar parches anteriores. **La edición maestra sigue siendo
C28-G; el atlas histórico no la sustituye ni altera su contenido.**

**Ajuste C28-I:** la revisión lógica de C28-G y la exportación opcional
de PNG con Inkscape se registran por separado. El plan para terminar el
libro está en `libro/PLAN_CIERRE_EDITORIAL_C28I.md`.

**Ajuste posterior a la retroalimentación Windows:** se añadieron búsqueda
de Inkscape en rutas habituales y un control separado para las dos láminas
de C28-H. La falta de un renderizador no invalida ni los modelos Python ni
la simulación Icarus; sus resultados figuran en controles diferentes.

**Avance del LIBRO C28-J:** se incorpora
`libro/AUDITORIA_PROGRESION_C28J.md` con matriz de los 26 capítulos,
115 figuras y los seis capítulos sin sección «Construimos» explícita.
La prueba reproducible, `scripts/c28j_auditar_progresion_libro.py`, usa
solamente Python estándar y forma parte de `PROBAR_TODO_GLOBAL_C28H.cmd`.
`libro/PLAN_CIERRE_EDITORIAL_C28I.md` conserva el progreso ponderado
estimado; el nuevo archivo `PLAN_CONSERVACION_LIBRO_Y_GITHUB_FUTURO.md`
documenta un flujo de ramas y pull requests **sin crear repositorio**.

**Avance C28-L (fundamentos):** se incluye la lectura parcial de los capítulos
1–7B en `libro/AUDITORIA_LOGICA_C28L_01_A_07B.md` y la prueba
`scripts/c28l_verificar_logica_inicial.py`, con **131.144 comparaciones
correctas de lógica ideal** (predominan las combinaciones del registro8).
El comprobador se ejecuta ahora como **control adicional** del global.
La retroalimentación anterior confirmó 14/14 controles aprobados en Windows;
con C28-L, la nueva ejecución puede completar **15/15**, sujeto a prueba.
Esto no certifica planos eléctricos ni modifica el Word/PDF maestro.

**Nuevo C28-M:** la retroalimentación Windows de C28-L confirmó **15/15
controles APROBADOS**. Se ha incorporado
`scripts/c28m_verificar_alu_mapa_y_programa.py` con **196.620 vectores**
de memoria, sumador, resta/ALU y el intérprete limitado al ejemplo LDI/ST/HALT.
También se añadió como control separado el comprobador de los **36 opcodes
candidatos** `scripts/verificar_isa_aula8_borrador.py`. El próximo lote
puede alcanzar **17/17 controles**, pendiente de verificar en Windows.
La lectura técnica de capítulos 8–14, sus límites y las cuatro figuras
inspeccionadas constan en
`libro/AUDITORIA_C28M_MEMORIA_ALU_ISA_08_A_14.md`. El plan editorial
sube justificadamente de **77 % a 80 %**; todavía no se modifica el PDF/Word
maestro ni se declara real la CPU.

**Nuevo C28-N (fotografías históricas):** Marcos confirmó en Windows
**17/17 controles APROBADOS, ninguno fallido ni pendiente**. Para la siguiente
retroalimentación se suma una **recogida auxiliar de cinco fotografías
auténticas** de Wikimedia Commons (Altair 8800, placa Apple II, DEC VT100,
Intel 8086 e IBM PC 5150). El script consulta las licencias de cada foto y
las descarga **desde tu computadora** directamente a la carpeta de pruebas.
Todas las fotos, créditos, páginas fuente, SHA-256 y errores de conexión se
incluyen automáticamente en el ZIP de retroalimentación. No se instalan
programas adicionales, no se modifica Word/PDF y estas imágenes son solo
**candidatas para revisión**. Consulta
`libro/PLAN_FOTOGRAFIAS_HISTORICAS_C28N.md`.

**Nuevo C28-O (atlas histórico):** la última retroalimentación de Marcos
confirma cinco de cinco fotografías descargadas, además de los 17/17
controles globales anteriores. Las cinco fueron examinadas visualmente,
incorporadas al repositorio con sus SHA-256 y convertidas en un **atlas
complementario de siete páginas**, que enlaza Altair 8800, Apple II, DEC
VT100, Intel 8086 e IBM PC 5150 con piezas concretas de Aula. Ve
`libro/ediciones/C28_O/Aula_Computadora_Atlas_Historico_C28_O.pdf`.
Se registra una prueba adicional de integridad de los cinco JPG, metadatos
y PDF; **el nuevo objetivo son 18/18 controles y aún falta confirmarlo
en el Windows de Marcos**. Generar o revisar el atlas no comprueba un circuito
físico ni finaliza la revisión de los 26 capítulos. El avance editorial
ponderado aumenta justificadamente a **82 %**.

**Nuevo C28-P (auditoría de capítulos 15–24):** la retroalimentación
`Retroalimentacion_GLOBAL_C28H_20261109_162945.zip` confirmó **18/18**
controles APROBADOS y **5/5** fotos auténticas descargadas. Se creó
`scripts/c28p_auditar_tramo_final.py` con once lecciones, cincuenta
figuras, contratos de pila/PC, RAM/ROM/MMIO, bloques, programas y vídeo.
El control agregado `LIBRO_C28P_TRAMO_FINAL` lleva la siguiente suite a
**19 controles previstos**, todavía sin retroalimentación Windows.
Detalles: `INFORME_C28_P_AUDITORIA_FINAL.md`. La madurez editorial estimada
subió a **84 %** sin alterar el Word/PDF maestro C28-G ni decidir entre
las políticas PC. El paquete mantiene exactamente el mismo comando
de prueba global de más abajo.

**Nuevo C28-Q (trazabilidad digital):** la retroalimentación Windows
`Retroalimentacion_GLOBAL_C28H_20261109_194334.zip` confirmó **19/19**
controles APROBADOS. Se añadieron topologías serializadas para XOR
de cuatro NAND y latch SR de dos NAND; un verificador comprueba sus
tablas, rutas SVG y el esquema de pines, además de las 51 NAND del
selector C28-D y 177 NAND de PC/MAR C28-F. También se incorporan
compilación y simulación Icarus de los HDL existentes de registro8
C28-A y PC16 C28-E. El objetivo de la próxima retroalimentación es
**24/24 controles**, no confirmado todavía. Informe completo:
`INFORME_C28_Q_RED_NAND_Y_RTL.md`. Madurez editorial **85 % estimada**.

**Nueva entrega acumulativa C28-S (sin nuevas decisiones de arquitectura):**
la retroalimentación `Retroalimentacion_GLOBAL_C28H_20261109_200941.zip`
confirma **24/24 controles Windows aprobados**, incluidos los HDL C28-A
y C28-E y las cinco fotografías. C28-R añade el netlist de **134 NAND**
para ADD/SUB de ocho bits, su Verilog derivado y un testbench exhaustivo;
en Python se verificaron **131.072 vectores**. C28-S examina la geometría
de **248 páginas** del maestro C28-G con ocho hojas de contacto JPEG,
sin modificar el libro. La nueva ronda contiene **28 controles previstos**:
dos Python y compilación/simulación Icarus C28-R adicionales. Todavía
**no se han ejecutado esos cuatro controles nuevos en Windows**.
Ver `INFORME_C28_S_ALU_Y_REVISION_PDF.md`. Progreso editorial **87,3 %
estimado**, sin hardware/firmware/CPU terminados.

**Entrega C28-T — documentación sin pruebas:** dos esquemas originales
SVG+PNG, un suplemento desde nueve NAND hasta ADD/SUB de ocho bits y un
mapa para integrar el material en los capítulos 4, 10 y 11. Consultar
`INFORME_C28_T_DOCUMENTACION_Y_DIAGRAMAS.md` y
`libro/SUPLEMENTO_C28T_DEL_BIT_A_134_NAND.md`. La estimación editorial
pasa a **88,5 %**. No hay nuevas comprobaciones de Windows ni cambios
en el maestro. **El ejemplo de PowerShell que figura más abajo corresponde
a la entrega histórica C28-S; no se solicita ejecutarlo en esta ronda.**

## No se ha cambiado silenciosamente la arquitectura

- Ambas políticas de PC siguen candidatas: C28-F anticipado, C28-G diferido.
- El libro maestro Word/PDF sigue siendo la **edición C28-G**. El suplemento
  C28-H está en `libro/SUPLEMENTO_C28H_CAP15.md` y se integrará al maestro
  después de confirmar el HDL y decidir la política de PC.
- El nuevo diagrama 2D es funcional, no un plano eléctrico de puertas.
- No hay CPU integrada, RAM física, reloj con temporización validada ni
  ejecutable JavaFX. El contrato de vídeo V1 no se altera.

## Probar el conjunto completo en Windows

Necesario: Python 3 con comando `py`. Opcionales, ya instalados por Marcos:
Inkscape para regenerar PNG e Icarus Verilog (`iverilog` y `vvp`) para HDL.
**No** requiere cambiar políticas de ejecución de PowerShell ni instalar Java.
Para el recolector auxiliar se necesita conexión a Wikimedia Commons;
los 28 controles digitales/editoriales propuestos funcionan sin ella porque
las cinco fotos ya se incluyen dentro de este ZIP.

Abre PowerShell desde cualquier carpeta y pega **un solo bloque**:

```powershell
$ErrorActionPreference = 'Stop'
$descargas = Join-Path $env:USERPROFILE 'Downloads'
$zip = Join-Path $descargas 'Aula_Computadora_C28_S_GLOBAL_COMPLETO.zip'
if (-not (Test-Path -LiteralPath $zip -PathType Leaf)) {
    throw ('No se encuentra el ZIP global C28-S en ' + $descargas)
}
$destino = Join-Path $descargas ('Aula_C28S_PRUEBAS_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff'))
Expand-Archive -LiteralPath $zip -DestinationPath $destino -ErrorAction Stop
$proyecto = Join-Path $destino 'Aula-Computadora'
$comprobador = Join-Path $proyecto 'PROBAR_TODO_GLOBAL_C28H.cmd'
if (-not (Test-Path -LiteralPath $comprobador -PathType Leaf)) {
    throw 'No aparece PROBAR_TODO_GLOBAL_C28H.cmd'
}
$codigo = -1
try {
    & $comprobador
    $codigo = $LASTEXITCODE
} catch {
    Write-Warning ('La ejecucion produjo un error: ' + $_.Exception.Message)
}
$resultado = Get-ChildItem -LiteralPath $proyecto -Filter 'Retroalimentacion_GLOBAL_C28H_*.zip' -File |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($resultado) {
    Write-Host ('RETROALIMENTACION: ' + $resultado.FullName) -ForegroundColor Cyan
}
if (-not $resultado) {
    Write-Warning 'No se genero el ZIP; revisa el resultado de Python arriba.'
}
Write-Host ('CODIGO FINAL: ' + $codigo)
Start-Process explorer.exe -ArgumentList ('"{0}"' -f $proyecto)
```

Al finalizar, PowerShell conserva su carpeta inicial; el `.cmd` no deja
procesos de prueba abiertos ni hace `pause`. No cerrar arbitrariamente
`python.exe`, `Code.exe`, `explorer.exe` ni otras aplicaciones: pueden
estar haciendo trabajo no relacionado.

## Alcance de la auditoría automática

1. Integridad estructural de los **26** fascículos Word/PDF/Markdown y los
   dos maestros C28-G; no pretende validar toda la semántica del libro.
2. Modelos digitales Python de C28-A (registro), C28-D, C28-E, C28-F,
   C28-G y C28-H, más los contrastes del libro C28-L (capítulos 3–7)
   y C28-M (capítulos 8–14) y la codificación ISA aún en borrador.
3. Icarus para C28-A, C28-E, C28-F y **dos políticas** del secuencial C28-H, cuando
   ambos ejecutables estén instalados y accesibles.
4. ZIP de retroalimentación con registros, resumen JSON/Markdown, hashes
   de Word/PDF y, si se ejecuta, traza VCD para GTKWave.
5. Como tarea **auxiliar** separada, hasta cinco fotos históricas con
   procedencia y licencia en `FOTOS_HISTORICAS_C28N/`. Un corte de Internet
   no se convierte en fallo de las pruebas lógicas; revisa su informe aparte.
6. Nuevo control `LIBRO_C28O_ATLAS_HISTORICO`: presencia de cinco JPEG,
   licencias/fuentes, huellas SHA-256, texto de acompañamiento y siete páginas
   del PDF. No verifica estilo visual: esa revisión fue humana en esta etapa.
7. Nuevo control `LIBRO_C28Q_NETLIST_Y_FIGURAS`, con topología NAND
   serializada, tres rutas SVG cotejadas y una matriz de diez circuitos.
8. Nuevo control `LIBRO_C28R_ALU8_NAND_ADD_SUB`: evalúa 134 puertas NAND
   efectivamente listadas, 131.072 combinaciones ADD/SUB y flags;
   dos controles Icarus adicionales compilan y simulan el mismo RTL.
9. Nuevo control `LIBRO_C28S_EVIDENCIA_PDF_248`: coteja hash del maestro,
   informe de las 248 páginas y ocho hojas de contacto. Su análisis geométrico
   original se hizo localmente; Windows verifica las evidencias, no las rerenderiza.

Si quieres comprobar **solo el descargador sin Internet**, desde la raíz
`Aula-Computadora` ejecuta:

```powershell
py .\scripts\c28n_autoprueba_descargas.py
```

Una verificación fallida **se conserva como evidencia** y no se reporta
como aprobada. Si Icarus no está en PATH ni en rutas estándar se registra
como **PENDIENTE**. Una prueba completa de la computadora física sigue
fuera del alcance de esta entrega.
