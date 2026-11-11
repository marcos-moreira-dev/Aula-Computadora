# C28-J · Primera auditoría transversal del LIBRO

Fecha: 9 de noviembre de 2026.

## Resultado reproducible

- **26/26 capítulos** con fuente Markdown y fascículos Word/PDF presentes.
- **115 referencias de figuras** con PNG de cabecera correcta y SVG XML
  analizables; **0 errores estructurales** registrados.
- **20/26 capítulos** con sección titulada «Construimos Aula…».
- **6/26** sin ese encabezado: 01, 02, 04, 7B, 23 y 24. En el texto
  sí existen pasos de práctica o síntesis; requieren lectura causal, no
  una etiqueta automática de fallo.
- **9 SVG adicionales** producidos por pilotos C28, conservados fuera
  de las 115 referencias maestras. No presentarlos como ya publicados.
- Reejecución del auditor visual: **115 pares PNG/SVG verificables**,
  **10 hojas de contacto** y **0 alertas geométricas automáticas**.

## Material nuevo

- `scripts/c28j_auditar_progresion_libro.py`: inventario repetible.
- `libro/AUDITORIA_PROGRESION_C28J.md`: matriz por capítulo.
- `libro/AUDITORIA_PROGRESION_C28J.json`: resultados legibles por máquina.
- `PLAN_CONSERVACION_LIBRO_Y_GITHUB_FUTURO.md`: preservar la futura edición
  final, después practicar ramas, revisión y pull requests con Marcos.

Se corrigió la suposición antigua de `scripts/c28_auditar_figuras.py`
que impedía tener imágenes suplementarias sin declararlas defectuosas.
El auditador global incluye ahora `LIBRO_C28J_PROGRESION` como control.

## Aún no certificado

Esta pasada **no** revisó toda la prosa, la lógica de cada una de las 115
figuras ni sus posibles problemas de cableado. Una cifra de cero colisiones
geométricas no prueba que el circuito funcione. El suplemento secuencial
C28-H sigue separado del Word/PDF maestro C28-G de 248 páginas; las
políticas del PC no se han elegido.

**Avance global del LIBRO:** permanece en **77 % estimado**, porque se
completó inventario y localización de riesgos, no toda la lectura humana
ni la cobertura HDL de los circuitos didácticos.

## Próximo tramo

1. Revisar semánticamente los cierres/aperturas de los capítulos 01–07B.
2. Auditar primero esquemas de NAND, XOR, latch, registro y buses, uniendo
   figura, tabla y testbench.
3. Corregir solo problemas reales; regenerar fascículos Word/PDF si cambia
   texto de un capítulo y, al finalizar, el maestro completo.

No se modificó ni publicó ningún repositorio GitHub.
