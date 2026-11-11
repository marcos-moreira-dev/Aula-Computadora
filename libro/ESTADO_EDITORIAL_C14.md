# Estado editorial después de C14-0.1

**Corte:** 8 de noviembre de 2026 (Ecuador). El libro contiene **14 de 24 capítulos numerados** redactados en Markdown, Word y PDF, más el interludio P07B. Faltan **10 capítulos numerados (15–24)** y la edición integral.

## Capítulo 14: De números a instrucciones

- **Nueve páginas** Word/PDF, **12 expresiones OMML editables**, **4 figuras originales** SVG/PNG con texto alternativo y **12 ejercicios resueltos**.
- Conversión de `42` decimal a `00101010` binario y `0x2A` hexadecimal. Se distingue el byte numérico de los dos caracteres «42».
- **Codificación candidata:** `LDI R0,42` se traduce a `11 00 2A`; `ST [0x6F00],R0` a `13 00 00 6F` (dirección de 16 bits **little-endian**); `HALT` a `01`. En total se depositarían **8 bytes en RAM `0x6000–0x6007`**.
- Explicación de opcode, selectores R0–R3, modo absoluto, relativo a X y a SP, desplazamiento con signo `0xFF=−1`, salto `JNZ` propuesto y longitud variable de instrucciones.
- Procedimiento didáctico de **panel con CPU detenida**, posesión única del bus y botones conceptuales DEPOSIT/EXAMINE. Se diferencia de un monitor de ROM, que requeriría **firmware funcional**, y del reset por vector `0xFFFC–0xFFFD`.
- Diferencia entre **HALT**, que detendría la CPU, y **RET**, que podría volver a un monitor después de un `CALL` válido. La expectativa de R0=`0x2A`, RAM[`0x6F00`]=`0x2A`, PC=`0x6008` es **una deducción de la propuesta**, no una ejecución medida.
- **132.993 comprobaciones de modelos y documentos**: conversión de los 256 valores de byte, división y recomposición de 65.536 direcciones, selectores/modos, desplazamientos firmados, depósito/examen ideal, lectura estática del programa, figuras, Word y texto/PDF. El verificador no contiene una CPU.

## Acumulado

| Indicador | Valor |
| --- | ---: |
| Capítulos numerados redactados | **14/24** |
| Interludios | **1** (P07B) |
| Capítulos numerados pendientes | **10** (15–24) |
| Páginas acumuladas, incluido P07B | **129** |
| Figuras originales SVG/PNG | **58** |
| Ejercicios resueltos | **180** |
| Expresiones OMML en Word | **183** |
| Comprobaciones del capítulo 14 | **132.993** |
| Libro maestro Word/PDF, cubierta, índice, glosario | Pendiente |
| CPU física, firmware, panel, ensamblador y simulador | Sin implementar |

## Próximo trabajo y límites

1. Capítulo 15 **«La instrucción en movimiento»**: narrar *fetch–decode–execute* con PC, IR, MAR/MDR, selectores y cambios ideales de RAM y registros; distinguir siempre una traza en papel de ciclos físicos.
2. Continuar los capítulos **16–24** sin renumerar el interludio P07B.
3. Tras el capítulo 24, preparar revisión editorial global, portada, bibliografía/glosario, tabla de contenidos y el **Word/PDF maestro**.
4. **R1 técnico sigue abierto**: aceptar o rectificar ISA, diseñar arbitraje, temporización, panel y micro-ROM, implementar firmware/CPU y someter circuitos a pruebas reales antes de declarar ejecución o validación eléctrica.

## Reproducción

```bash
python3 scripts/generar_figuras_capitulo_14.py
python3 scripts/generar_capitulo_14.py
# Exportar DOCX a PDF con LibreOffice o el renderizador editorial y revisar las nueve páginas.
python3 scripts/verificar_capitulo_14.py
python3 scripts/verificar_contexto.py
```

**Fuentes internas:** `simulador-javafx/ISA_AULA8_CANDIDATA.md`, `simulador-javafx/ISA_AULA8_CANDIDATA.json`, `simulador-javafx/PROGRAMACION_DESDE_CERO.md` y `simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.md`. Su estado sigue siendo **provisional**.
