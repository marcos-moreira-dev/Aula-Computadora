# C28-L · Entrega global con auditoría de circuitos iniciales

**9 de noviembre de 2026.** Esta entrega es un **ZIP global**, no un
parche ni un repositorio nuevo; conserva los 26 capítulos y la edición
maestra C28-G, el piloto C28-H, las figuras y las herramientas existentes.

## Evidencia recibida de Windows

La retroalimentación `Retroalimentacion_GLOBAL_C28H_20261109_150543.zip`
registró **14 controles APROBADOS, cero FALLIDOS y cero PENDIENTES**.
Incluyó simulaciones Icarus de C28-F y de las dos políticas C28-H y las
exportaciones PNG de C28-G y C28-H. Son pruebas de los prototipos digitales,
**no** certificación del hardware real ni de una computadora terminada.

## Trabajo nuevo C28-L

- Se inspeccionó la progresión de los capítulos 1–7B hacia la computadora.
- Se contrastaron fórmulas y tablas NAND, XOR, latch y selección LOAD.
- La herramienta `scripts/c28l_verificar_logica_inicial.py` verificó
  **131.144 comparaciones** y dejó JSON reproducible en `c28_l/auditoria`.
- El archivo `scripts/c28h_auditoria_global.py` incorpora un nuevo control
  `LIBRO_C28L_LOGICA_INICIAL`.
- El informe `libro/AUDITORIA_LOGICA_C28L_01_A_07B.md` explica alcances
  y advertencias. La imagen XOR se inspeccionó visualmente, pero todavía
  no se transcribió automáticamente cada cable a una netlist.

## Estado y rumbo editorial

**Libro: 77 % (estimación ponderada; sin variación ficticia por el aumento
de pruebas).** El detalle de siete frentes y cinco fases de cierre está
en `libro/PLAN_CIERRE_EDITORIAL_C28I.md`.

Lo próximo: cotejar los diagramas lógicos prioritarios con sus conexiones
reales, proseguir lectura técnica de los capítulos 8–24, reconciliar los
pilotos PC/MAR/memoria con el texto, actualizar el Word/PDF maestro e
inspeccionar las páginas y las licencias. El proyecto GitHub/PR permanece
deliberadamente **aplazado** hasta después de cerrar el libro.

En Windows, usar el bloque PowerShell completo de
`LEEME_C28_H_GLOBAL_COMPLETO.md`. La suite deja un ZIP de retroalimentación
y vuelve a `Descargas`, sin retener una sesión de PowerShell dentro de la
carpeta que Marcos desee eliminar.
