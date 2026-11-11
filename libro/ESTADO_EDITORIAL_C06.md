# Estado editorial después de C06-0.1

**Fecha de corte:** 6 de noviembre de 2026. **Alcance:** seis capítulos numerados del libro redactados y maquetados. La arquitectura técnica R0.14 sigue siendo candidata; no hay CPU ejecutable ni prototipo físico verificado.

## Entrega del capítulo 6

- **«Memorizar en el tiempo»**: explica cómo un latch D combina un dato y una habilitación para aceptar un valor o conservar el anterior; su transformación booleana desde un latch SR con NAND está desarrollada con una tabla.
- Diferencia el **latch D sensible a nivel alto** (Q sigue D mientras LE = 1) del **flip-flop D sensible al flanco ascendente** (captura D en CLK 0 → 1 y lo conserva entre flancos).
- Dos secuencias resueltas: cinco instantes del latch transparente y siete instantes del flip-flop, sin confundir los estados ideales con tiempos eléctricos.
- Incluye **reset y preset asíncronos**, preparación y mantenimiento de datos (**setup/hold**), retardo clock-to-Q y advertencia sobre metastabilidad sin inventar medidas.
- Referencias oficiales **Texas Instruments SN74HC373** (ocho latches D, LE y OE independientes) y **SN74HC74** (dos flip-flops D de flanco ascendente, preset y clear asíncronos).
- **Cuatro figuras originales SVG/PNG**, Word editable y PDF de **ocho páginas**, nueve ecuaciones OMML y **12 ejercicios resueltos**.
- **171 controles automáticos**: tablas y secuencias booleanas, reset/preset, cálculos de frecuencia, integridad Word/PDF y figuras. Incorporados al workflow documental.

**Límites:** no se ha realizado protoboard, osciloscopio, simulación analógica, medición de setup/hold ni certificación de una frecuencia de reloj. Las especificaciones de hojas de datos se citan como referencia y no demuestran un montaje.

## Continuidad del puente semántico

La propuesta [«Del bit al significado»](PROPUESTA_PUENTE_BITS_Y_SIGNIFICADO.md) permanece reservada **después del capítulo 7, antes del 8**, sin renumerar el currículo de 24. La señal de LE, CLK o CLR_n ya tiene semántica lógica según el circuito. El valor de un byte y su interpretación como número, carácter, dirección, instrucción o estructura de software se explicará en el puente. La POO se menciona solo como una abstracción posterior, no como requisito de MiniC-Aula.

## Estado acumulado

| Indicador | C06-0.1 |
| --- | --- |
| Capítulos numerados del currículo | **24** |
| Capítulos con manuscrito, Word y PDF | **6** (1–6) |
| Capítulos numerados pendientes | **18** (7–24) |
| Páginas acumuladas | **54** (9 + 10 + 10 + 9 + 8 + 8) |
| Figuras originales | **22 SVG + 22 PNG** |
| Ejercicios con respuestas | **72** |
| Ecuaciones OMML | **73** (13 + 13 + 14 + 13 + 11 + 9) |
| Verificación específica C06 | **171 controles** |
| Puente de interpretación semántica | Propuesto, sin redactar ni renumerar |
| Portada y Word/PDF maestro | Pendientes |
| CPU, firmware, simulador y hardware físico | No implementados |

## Qué falta para cerrar el libro, sin contar la portada

1. Desarrollar los **18 capítulos numerados restantes**, con figuras, demostraciones, ejercicios y verificaciones. El siguiente es el **capítulo 7, «Del bit al registro»**: carga, retención, byte, señal enable, salidas triestado y buses.
2. Tras el capítulo 7, decidir con Marcos si el puente semántico será interludio o nuevo capítulo numerado. La incorporación como capítulo numerado elevaría el currículo a 25.
3. Revisar transversalmente los capítulos 1–6 para asegurar progresión pedagógica, esquemas correctos, redacción consistente y complejidad adecuada a principiantes.
4. Verificar hojas de datos y condiciones de ejemplos físicos; no presentar un esquema conceptual como circuito construido. Añadir evidencias materiales solamente si se realizan pruebas reales.
5. Consolidar arquitectura/ISA, firmware y pruebas antes de declarar ejecutables los programas que se enseñarán en capítulos avanzados.
6. Integrar Word maestro, PDF maestro, índice, glosario, bibliografía, créditos, referencias cruzadas y paginación unificada; revisar lectura e impresión.
7. Auditar ortografía, accesibilidad, derechos y compatibilidad con destinos adicionales solo cuando existan pruebas de esos destinos.

## Reproducir la entrega

En un entorno con Python 3, `python-docx`, Inkscape, LibreOffice y Poppler:

```bash
python3 scripts/generar_figuras_capitulo_06.py
python3 scripts/generar_capitulo_06.py
# Exportar el DOCX como libro/capitulos/06_memorizar_en_el_tiempo.pdf
python3 scripts/verificar_capitulo_06.py
```

**Próximo:** capítulo 7; después podrá abordarse el puente semántico sin interrumpir la ruta de construcción del libro.
