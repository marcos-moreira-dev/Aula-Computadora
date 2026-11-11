# Informe de integración C28-H global completo

**Fecha de integración:** 9 de noviembre de 2026.

La distribución global C28-G se copió íntegramente y sin cambios en sus
archivos originales. Se añadieron exclusivamente los archivos nuevos del
piloto C28-H, su suplemento de lectura y un comprobador global con resultados
recuperables. No se borraron los históricos ni los fascículos del libro.

## Prueba de preentrega ejecutada en el entorno de construcción

- **7 controles aprobados**, **0 fallidos**, **1 pendiente**.
- Integridad estructural de los **26 fascículos** (`.md`, `.docx`, `.pdf`) y
  de los dos volúmenes maestros C28-G (`.docx`, `.pdf`).
- Modelos Python C28-A, C28-D, C28-E, C28-F, C28-G y C28-H: aprobados.
- Icarus Verilog: pendiente aquí por ausencia del simulador. El script
  `PROBAR_TODO_GLOBAL_C28H.cmd` intentará ejecutar C28-F y C28-H en Windows.
- La comparación entre la copia global y la base C28-G no encontró cambios
  de contenido en los archivos heredados.

## Advertencias de alcance

### Corrección C28-I: renderizado opcional y evidencia separada

Tras la retroalimentación de Marcos en Windows, se separaron dos comprobaciones:

- `C28_G_LECTURA`: ejecuta las comparaciones lógicas; la falta de Inkscape
  ya **no invalida** su resultado.
- `C28_G_RENDER_PNG`: certifica solamente que se consiguió exportar el PNG;
  si no se encuentra Inkscape queda **PENDIENTE** sin ocultar el aviso.

Se buscan rutas habituales de Inkscape en Windows, además de `PATH`. La
figura vectorial SVG se conserva incluso si la exportación a PNG falla.
El progreso y el plan editorial están en
`libro/PLAN_CIERRE_EDITORIAL_C28I.md`. Los 10 controles correctos y el
único error de exportación informados en Windows **no equivalen** a una
revisión exhaustiva de las 26 lecciones ni certifican hardware físico.

**Pruebas de la corrección en entorno de construcción:** se comprobó el
script sin Inkscape (`8.360` vectores correctos, PNG pendiente, salida 0)
y con Inkscape (`8.360` vectores correctos, PNG exportado, salida 0). La
auditoría global resultó en **8 aprobados, 0 fallidos, 1 pendiente**; la
única prueba pendiente en ese entorno es Icarus Verilog, que **sí figura
ejecutado** en el registro Windows previo de Marcos. Esta diferencia
no se debe presentar como una regresión del HDL.

**Retroalimentación de Marcos (9-nov-2026, 14:32):** se verificó el
ZIP `Retroalimentacion_GLOBAL_C28H_20261109_143202.zip`: **12 controles
aprobados, 0 fallidos y 0 pendientes**. Entre ellos, la compilación y
simulación C28-F y C28-H con Icarus (12.124 vectores por cada política
secuencial). La figura C28-G se exportó con Inkscape; C28-H generó sus SVG
pero informó que no localizaba Inkscape. Se corrigió su búsqueda y se
añadió un control independiente `C28_H_RENDER_PNG`. El resultado 12/12 es
histórico de la ejecución recibida, no un sustituto de la nueva reejecución.

**Verificación posterior de las figuras C28-H:** el script corregido
se ejecutó con y sin Inkscape. Sin él mantiene ambos SVG y señala PNG
pendiente sin fallar el modelo; con él exporta los dos PNG y verifica
sus cabeceras. Ambas imágenes fueron inspeccionadas visualmente a nivel
funcional: la explicación de PC/MAR/MDR y la comparación tabular se leen
completas y tienen los límites del modelo indicados. La auditoría global
posterior registró **9 aprobados, 0 fallidos, 1 pendiente local de Icarus**.
La retroalimentación Windows ya demostró Icarus para el RTL anterior, pero
esta corrección de imágenes aún no se ha reejecutado allí.

El Word y el PDF maestros corresponden a **C28-G**; C28-H todavía es un
suplemento separado, no una edición maestra regenerada. La política de
avance del PC no se ha decidido. Los esquemas PNG/SVG representan el
protocolo funcional, no una prueba eléctrica. No se ha construido CPU
integrada, firmware, ensamble ni programa JavaFX.

## Cómo probar

Usar `LEEME_C28_H_GLOBAL_COMPLETO.md` y ejecutar desde `Descargas` el
bloque PowerShell completo allí incluido. Produce
`Retroalimentacion_GLOBAL_C28H_*.zip` con informes y trazas.
