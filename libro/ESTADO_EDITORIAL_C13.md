# Estado editorial después de C13-0.1

**Corte:** 8 de noviembre de 2026 (Ecuador). El libro dispone de **13 de 24 capítulos numerados** en Markdown, Word y PDF, más el interludio P07B. Quedan **11 capítulos numerados (14–24)** y el trabajo editorial de integración.

## Capítulo 13: La unidad de control

- **Ocho páginas** Word/PDF, **8 expresiones OMML editables**, **4 figuras originales** SVG/PNG con descripción alternativa y **12 ejercicios con solucionario**.
- Distingue instrucción, microoperación y microsecuencia; separa la ROM de control interna de la ROM de firmware accesible en el mapa de la máquina.
- Descompone la macro `READ_PC_TO_IR` en dependencias de MAR, petición RD, captura MDR, transferencia IR y avance PC, **sin prometer un ciclo por estado**.
- Explica despacho de opcodes candidatos `11` (LDI), `13` (ST) y `01` (HALT); distingue `FAULT` de `PENDING_ROUTE` para instrucciones previstas pero aún sin secuencia descrita.
- Muestra la **validación del selector antes de `LDI_COMMIT`** y la secuencia segura de `ST [0x6F00],R0`: capturar `ADDR_LO/HI`, construir MAR, ejecutar `ST_STAGE_DATA` para sustituir el byte `6F` que quedó en MDR por `R0=2A`, y solo entonces solicitar `WR`.
- Calcula un recuento **ilustrativo** de **8 lecturas y 1 escritura** del programa `11 00 2A 13 00 00 6F 01`, con PC final `0x6008`; el recuento **no equivale** a ciclos de reloj ni a transacciones observadas en una máquina real.
- **196.771 comprobaciones** del modelo/documento: los 256 valores de selector × 256 inmediatos, recomposición de las 65.536 direcciones, orden de estados y reglas del bus, integridad y contenido de los cuatro diagramas, Word y PDF. **Sin CPU ejecutada, microcódigo codificado ni pruebas físicas.**

## Acumulado

| Indicador | Valor |
| --- | ---: |
| Capítulos numerados | **13/24** |
| Interludios | **1** (P07B) |
| Capítulos numerados pendientes | **11** (14–24) |
| Páginas acumuladas, incluido P07B | **120** |
| Figuras originales SVG/PNG | **54** |
| Ejercicios resueltos | **168** |
| Expresiones OMML en Word | **171** |
| Comprobaciones del capítulo 13 | **196.771** |
| Word/PDF maestro, portada, índice, glosario | Pendiente |
| CPU, firmware, micro-ROM, JavaFX y montaje físico | Sin implementar |

## Siguientes trabajos y límites

1. Redactar el capítulo 14 **«De números a instrucciones»**: opcodes, formatos de instrucción, direcciones, cargas manuales y límites de la ISA candidata.
2. Continuar el resto del currículo numerado **15–24** sin añadir capítulos por sorpresa.
3. Tras el capítulo 24, realizar revisión editorial general, bibliografía, glosario, portada, índice y **edición maestra Word/PDF**. Todos los capítulos actuales son **borradores revisables**, no edición final.
4. Por otra vía, diseñar y comprobar micro-ROM, temporización eléctrica, esquemas y hardware antes de afirmar que alguna instrucción se ejecutó en Aula-8. El simulador sigue sin iniciar.

## Reproducción

```bash
python3 scripts/generar_figuras_capitulo_13.py
python3 scripts/generar_capitulo_13.py
# Exportar Word a PDF con LibreOffice y revisar visualmente la paginación.
python3 scripts/verificar_capitulo_13.py
```

**Fuentes internas:** `simulador-javafx/UNIDAD_CONTROL_AULA8_BORRADOR.md`, `simulador-javafx/MICROARQUITECTURA_AULA8_BORRADOR.md`, `simulador-javafx/ISA_AULA8_CANDIDATA.md` y `simulador-javafx/MICROSECUENCIAS_AULA8_BORRADOR.json`. Todas son propuestas, no arquitectura congelada.
