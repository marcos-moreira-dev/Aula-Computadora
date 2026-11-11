# Estado editorial después de C15-0.1

**Corte:** 8 de noviembre de 2026 (Ecuador). Están redactados **15 de los 24 capítulos numerados** más el interludio P07B, cada uno en Markdown, Word y PDF. Quedan **9 capítulos numerados (16–24)** y la edición integral del libro.

## Capítulo 15: La instrucción en movimiento

- **Ocho páginas Word/PDF**, **12 ecuaciones OMML editables**, **4 diagramas originales SVG/PNG** con texto alternativo y **12 ejercicios resueltos**.
- Sigue, como traza de papel, los **ocho bytes** `11 00 2A 13 00 00 6F 01` depositados previamente en `0x6000–0x6007`: fetch compartido, decode y acciones funcionales de `LDI`, `ST` y `HALT`.
- Enseña los roles de **PC, MAR, MDR, IR, SEL, TMP**, los latches **ADDR_LO/ADDR_HI**, la validación de operandos y la escritura de R0 en memoria.
- Resuelve una sutileza crítica: tras leer el byte alto `6F` de la dirección, **MDR contiene `0x6F`**, por lo que `ST_STAGE_DATA` debe reemplazarlo por **`0x2A`** antes de ejecutar `WR` en `0x6F00`.
- Resultado **esperado**: R0=`0x2A`, RAM[`0x6F00`]=`0x2A`, PC=`0x6008`, IR=`0x01`; las banderas no se modifican. **Ocho lecturas y una escritura** son transacciones externas previstas, no nueve ciclos de reloj.
- **143.464 comprobaciones de modelo/documento**: 4.096 combinaciones de estado inicial FLAGS/R0, recomposición de las 65.536 direcciones, rutas de microacciones declaradas, integridad de figuras y verificación de Word/PDF. Ninguna ejecuta una CPU construida.

## Acumulado

| Indicador | Valor |
| --- | ---: |
| Capítulos numerados redactados | **15/24** |
| Interludios | **1** (P07B) |
| Capítulos numerados pendientes | **9** (16–24) |
| Páginas acumuladas, incluido P07B | **137** |
| Figuras originales SVG/PNG | **62** |
| Ejercicios resueltos | **192** |
| Expresiones OMML en Word | **195** |
| Comprobaciones del capítulo 15 | **143.464** |
| Libro maestro Word/PDF, cubierta, índice, glosario | Pendiente |
| CPU física, firmware, panel, ensamblador y simulador | Sin implementar |

## Próximo trabajo y límites

1. Capítulo 16, **«Subrutinas y pila»**: explicar CALL/RET, retornos y cambios de PC, conservando la diferencia entre contrato candidato y circuito real.
2. Completar capítulos **17–24** siguiendo el currículo original; conservar el interludio P07B sin renumeración.
3. Tras el capítulo 24, preparar revisión editorial global, portada, bibliografía, glosario, tabla de contenidos y **Word/PDF maestro**.
4. **R1 técnico sigue abierto:** congelar o revisar ISA, control, temporización, buses, panel, firmware y hardware físico. Ni los diagramas ni Python acreditan la ejecución sobre una computadora construida.

## Reproducción

```bash
python3 scripts/generar_figuras_capitulo_15.py
python3 scripts/generar_capitulo_15.py
# Renderizar el DOCX a PDF; inspeccionar visualmente sus ocho páginas.
python3 scripts/verificar_capitulo_15.py
python3 scripts/verificar_contexto.py
```

**Fuentes internas:** `simulador-javafx/ISA_AULA8_CANDIDATA.json`, `simulador-javafx/MICROSECUENCIAS_AULA8_BORRADOR.json`, `simulador-javafx/UNIDAD_CONTROL_AULA8_BORRADOR.md`, `simulador-javafx/MICROTRAZA_AULA8_BORRADOR.json`; todos son **borradores sin validación física**.
