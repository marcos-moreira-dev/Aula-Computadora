# C28-R/S · Aritmética desde NAND y revisión de las 248 páginas

**Fecha:** 9 de noviembre de 2026, Ecuador.
**Estado previo confirmado:** **24/24 controles aprobados en Windows** y
cinco de cinco fotos históricas descargadas, según
`Retroalimentacion_GLOBAL_C28H_20261109_200941.zip`.

## C28-R: 134 NAND, no solo una fórmula de ALU

Se construyó una **red de compuertas NAND de dos entradas, sin relojes**:

- Ocho XOR controladas sobre B (`B_i XOR SUB`), de cuatro NAND cada una.
- Ocho sumadores completos en cascada, de nueve NAND por etapa.
- Salidas de acarreo (`Cout`) y de préstamo/acarreo según modo (`Cflag`).
- Desbordamiento con signo `V=C7 XOR C8`, negativo `N=S7` y cero `Z`.

**Total: 134 NAND.** La red estructurada se serializó en
`c28_r/netlists/alu8_addsub_134nand.json` y a partir de esa misma
definición se generó `c28_r/rtl/alu8_addsub_134nand.v`.
`scripts/c28r_generar_alu8_nand.py --check` detecta discrepancias entre
fuente, JSON y RTL. El comprobador independiente
`scripts/c28r_verificar_alu8_nand.py` recorre **65.536 ADD y 65.536 SUB**
calculando las puertas efectivas del JSON, y compara resultado, C7,
Cout, Cflag, V, N y Z con aritmética externa al netlist.

| Ejemplo | Resultado de 8 bits | C | V | Z | N |
| --- | --- | ---: | ---: | ---: | ---: |
| `13 + 9` | `0x16` | 0 | 0 | 0 | 0 |
| `250 + 10` | `0x04` | 1 | 0 | 0 | 0 |
| `127 + 1` | `0x80` | 0 | 1 | 0 | 1 |
| `13 - 9` | `0x04` | 0 | 0 | 0 | 0 |
| `9 - 13` | `0xFC` | 1 | 0 | 0 | 1 |
| `0x80 - 0x01` | `0x7F` | 0 | 1 | 0 | 0 |

Las banderas aquí solo tienen sentido de **ADD y SUB**. No se decidió
el efecto de AND, OR, XOR o NOT sobre las flags ni se implementó el
MUX de toda la ALU. Los cuatro SVG cotejados son diagramas funcionales,
no conexiones físicas detalladas. El testbench Icarus de **131.072
vectores** espera su primera ejecución en Windows.

## C28-S: examen técnico y visual del volumen C28-G

Se examinó el PDF maestro A4 **sin editarlo** usando PyMuPDF y Pillow.

| Evidencia | Resultado |
| --- | ---: |
| Páginas analizadas | 248 |
| Fragmentos de texto | 17.216 |
| Bloques de imagen | 127 |
| Páginas vacías | 0 |
| Cajas de texto/imagen fuera de página (1 pt de tolerancia) | 0 |
| Caracteres de reemplazo U+FFFD | 0 |
| Hojas de contacto revisadas a escala de composición | 8 |
| Entradas de índice que coinciden con las aperturas reales | 26/26 |
| Folios de páginas interiores coincidentes | 247/247 |

El informe detallado es `c28_s/revision_pdf/C28_S_REPORTE_PAGINAS.json`.
Las ocho hojas JPEG están en `c28_s/revision_pdf/hojas_contacto/`.
Se revisaron visualmente sus miniaturas para localizar problemas grandes
de composición. Todavía **no equivale a corregir y leer el PDF página
por página a resolución de lectura**; tampoco sustituye la inspección
eléctrica del significado de cada dibujo. El script Windows C28-S
comprueba solamente la integridad de esa evidencia y el SHA del maestro.

## Suite próxima, límites y progreso

La suite Windows pasa de **24 a 28 controles**:

1. `LIBRO_C28R_ALU8_NAND_ADD_SUB` (nuevo Python).
2. `LIBRO_C28S_EVIDENCIA_PDF_248` (nuevo Python).
3. `HDL_C28_R_ALU8_NAND_ADD_SUB_COMPILACION` (nuevo Icarus).
4. `HDL_C28_R_ALU8_NAND_ADD_SUB_SIMULACION` (nuevo Icarus).

**Meta: 28/28; aún sin retroalimentación de Windows.** La madurez
editorial estimada cambia de **85 a 87,3 %**, según el desglose
ponderado de `libro/PLAN_CIERRE_EDITORIAL_C28I.md`.

Se respetaron las restricciones: **Word/PDF C28-G sin modificar**;
C28-H/C28-O todavía suplementos; PC anticipado y diferido continúan
alternativas candidatas; ISA, ABI, bus Aula-16 y vídeo V1 intactos;
sin afirmar hardware construido, CPU completa ni firmware ejecutable.
No se conectó ni creó ningún GitHub remoto.
