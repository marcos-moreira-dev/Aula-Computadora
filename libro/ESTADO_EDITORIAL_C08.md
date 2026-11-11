# Estado editorial después de C08-0.1

**Fecha de corte:** 6 de noviembre de 2026. Hay **8 capítulos numerados redactados** de los 24 previstos, más el interludio P07B entre los capítulos 7 y 8. Faltan **16 capítulos (9–24)** y la edición maestra integrada.

## Qué se entregó

- **Capítulo 8, «Direcciones y buses»**: diferencia entre dirección y dato, decodificador de dos bits para cuatro posiciones, bus de direcciones, datos y control, lectura/escritura, triestado, multiplexor y conflictos de bus.
- Ejemplo numérico completo: `0x1200 = 0001 0010 0000 0000₂ = 4 608₁₀`. El espacio direccionable por bytes de 16 bits posee `65 536 = 64 KiB` posiciones, desde `0x0000` hasta `0xFFFF`; ello no promete 64 KiB de RAM instalada.
- Secuencia conceptual: leer `RAM[0x1200] = 0x41`, escribir `0x53` en `0x1201`, releer y comprobar que la primera posición no cambia. El mapa de memoria definitivo no está aprobado.
- Comparación explícita: Aula-8 usa **16 bits de dirección y 8 de dato**, Aula-16 **16 bits de dirección y 16 de dato**, memoria por bytes con dos bancos de 8 bits, little-endian y palabras alineadas en el diseño inicial.
- **Cuatro diagramas originales** en SVG y PNG, **9 páginas** Word/PDF, **12 ecuaciones editables OMML** y **12 ejercicios resueltos**. No se renumeró el currículo.
- `scripts/verificar_capitulo_08.py` realizó **459379 controles matemáticos y documentales** incluyendo las 65536 direcciones, conservación de bytes, conducción exclusiva de bus y 65536 palabras little-endian. También inspecciona el Word, el PDF y los dibujos. La maqueta se revisó visualmente tras exportar.
- Hojas de datos de **Texas Instruments SN74HC138** y **Alliance Memory AS6C62256**: referencias de decodificación y SRAM respectivamente, no un esquema probado de Aula.

**Límites:** no se midieron corrientes, retardos, capacidad de conducción o señales eléctricas; no hay CPU Aula ejecutable ni memoria montada. El protocolo CS_n/RD_n/WR_n es un modelo pedagógico y no puede copiarse como secuencia de temporización comercial. El diseño detallado de bancos Aula-16 se desarrollará en el capítulo 22.

## Acumulado comprobado

| Indicador | Estado C08-0.1 |
|---|---|
| Capítulos numerados del currículo | 24 |
| Capítulos numerados con Word/PDF | **8** |
| Interludios con Word/PDF | **1** (P07B) |
| Capítulos numerados pendientes | **16** (9–24) |
| Páginas Word/PDF acumuladas | **79** (70 previas + 9) |
| Figuras originales | **34 SVG y 34 PNG** |
| Ejercicios con solucionario | **108** |
| Ecuaciones editables OMML | **103** |
| Comprobaciones del capítulo 8 | **459379** |
| Word/PDF maestro, portada e índice | **Pendientes** |
| CPU, firmware, componentes físicos probados y aplicación | **No implementados** |

## Qué falta

1. Redactar **capítulo 9 «RAM y ROM reales»**, con SRAM/ROM comerciales, chip select, organización, expansión y relaciones con el bus. Después, escribir los capítulos 10–24.
2. Auditar transversalmente los capítulos 1–8 y P07B para comprobar ritmo pedagógico, consistencia de notación, remisiones, precisión y ejercicios.
3. Antes de los capítulos de instrucciones y programas, contrastar y concretar ISA, datapath, señales, mapa de memoria, ROM, seguridad de buses y pruebas de Aula-8/Aula-16; las propuestas R0.14 siguen sin ser circuitos o ejecutables.
4. Preparar el **libro maestro** Word/PDF: portada, índice navegable, paginación continua, glosario, bibliografía, créditos, accesibilidad y revisión tipográfica final. Resolver derechos de materiales de referencia.
5. Realizar validaciones de hardware **solo cuando haya un diseño eléctrico real**, hojas de datos concretas, esquema, medición y pruebas; ninguna ilustración actual equivale a esa validación.

## Regenerar desde el repositorio

Se requiere Python con `python-docx`, Inkscape, LibreOffice y Poppler:

```bash
python3 scripts/generar_figuras_capitulo_08.py
python3 scripts/generar_capitulo_08.py
# Convertir el DOCX a PDF con LibreOffice.
python3 scripts/verificar_capitulo_08.py
```
