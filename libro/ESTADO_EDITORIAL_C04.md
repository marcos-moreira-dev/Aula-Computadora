# Estado editorial después de C04-0.1

**Fecha de corte:** 6 de noviembre de 2026. **Alcance:** cuatro capítulos introductorios redactados y maquetados. El contrato técnico R0.14 sigue siendo una propuesta de diseño, no una CPU ejecutable.

## Entregable del capítulo 4

- «**Construir funciones con compuertas**»: capítulo original de la Parte II que explica OR, NOR, XOR, suma de productos, composición de XOR con cuatro NAND y simplificación con prueba de equivalencia.
- Un caso de tres entradas `Y = A ∧ (B ∨ C)` con las ocho filas, para enseñar cómo traducir una frase funcional a ecuaciones y señales.
- **Cuatro ilustraciones originales en SVG y PNG:** OR frente a NOR, discrepancia XOR, red de cuatro NAND y función simplificada.
- **Word editable de nueve páginas** con trece expresiones OMML, tablas y cuatro dibujos insertados con texto alternativo; **PDF de nueve páginas** con texto seleccionable y páginas revisadas visualmente.
- **Doce ejercicios resueltos**, desde tablas de verdad a recorrido interno de NAND y explicación del retardo de propagación.
- **146 comprobaciones automáticas** de funciones booleanas, señales intermedias, simplificación, escritura, figuras, Word/PDF y presencia del plan de semántica. Integradas en el workflow documental.

Las tablas describen estados **ideales y estables**. No se montó el circuito, no se midieron retardos y no hay ejecución de CPU. El SN74HCT00 sirve como referencia de cuatro NAND, no como certificación de un montaje.

## Idea nueva registrada: del bit al significado

Marcos planteó el paso gradual desde niveles físicos y bits hasta números, caracteres, instrucciones y construcciones de lenguaje. Se documenta en [PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md](PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md) con ejemplos reproducibles y advertencias técnicas:

- Una tensión lógica depende de umbrales, no de que 0 sea siempre 0 V o 1 sea siempre 5 V.
- `01000001` puede ser el entero 65, el carácter ASCII `A` o una máscara con `b6` y `b0` activos; no adquiere un opcode sin ISA.
- `11111111` puede ser 255 sin signo o −1 en complemento a dos de ocho bits.
- **Ubicación sugerida:** después del capítulo 7, antes del 8; código provisional `PUENTE-07B`. No altera por ahora los 24 capítulos. Cuando se cierre el índice, Marcos podrá aprobar una incorporación formal (que daría 25 capítulos) o un interludio sin numeración.

## Estado acumulado

| Indicador | C04-0.1 |
| --- | --- |
| Capítulos del currículo numerado | 24 |
| Borradores Word/PDF | **4** (capítulos 1–4) |
| Capítulos numerados aún sin redactar | **20** (5–24) |
| Páginas de los cuatro capítulos | **38** (9 + 10 + 10 + 9) |
| Figuras propias | **14 SVG + 14 PNG** |
| Ejercicios con respuestas | **48** |
| Expresiones OMML en Word | **53** (13 + 13 + 14 + 13) |
| Verificación del capítulo 4 | **146 controles** |
| Capítulo sobre interpretación semántica | **Planificado, no redactado** |
| Portada | Pendiente |
| Libro maestro integrado con índice global | Pendiente |
| Prototipo físico, firmware, simulador | No implementados |

## Para terminar el libro, sin contar la portada

1. Redactar, ilustrar y comprobar los **20 capítulos numerados que faltan**. Sigue el capítulo 5 «La realimentación conserva información».
2. Confirmar si «Del bit al significado» se convertirá en un capítulo numerado nuevo o en un interludio, tras preparar el capítulo 7. Si pasa a ser el 25.º capítulo, aumentará en uno el trabajo pendiente.
3. Revisar con Marcos los capítulos 1–4: profundidad, continuidad, ejercicios, terminología, densidad visual y correcciones.
4. Vincular los circuitos a referencias verificadas de componentes reales y, si se desean prácticas materiales, reunir mediciones genuinas sin presentarlas como ya realizadas.
5. Cerrar la especificación de CPU, firmware, ISA y memorias antes de describir como *ejecutados* los programas de los capítulos avanzados.
6. Integrar libro maestro Word/PDF, índice, glosario, bibliografía, referencias cruzadas, créditos de figuras y revisión completa de las páginas.
7. Comprobar lectura e impresión, fidelidad de ecuaciones y, solo si se decide, compatibilidad con DocuPodcast. Revisar originales y derechos antes de publicar.

## Generación y prueba reproducibles

Desde la raíz del repositorio, con Python 3, `python-docx`, Inkscape, LibreOffice y Poppler disponibles:

```bash
python3 scripts/generar_figuras_capitulo_04.py
python3 scripts/generar_capitulo_04.py
# Exportar el Word a PDF como libro/capitulos/04_construir_funciones_con_compuertas.pdf
python3 scripts/verificar_capitulo_04.py
```

**Próximo paso:** capítulo 5, sobre realimentación y latch SR, sin saltar el capítulo 7 para escribir todavía el puente semántico.
