# Entrega editorial C26-0.1 — Aula Computadora

**Fecha:** 8 de noviembre de 2026. **Naturaleza:** revisión y maquetación de un manuscrito didáctico, no validación electrónica de una computadora.

## Qué se modificó

1. Los anteriores interludios se integran como **capítulos 7B y 23B**, sin desplazar la numeración histórica de los capítulos 1–24.
2. Se repararon el rótulo de la corriente en el primer esquema, la superposición en el recorrido de microcontrol del capítulo 13 y la composición tipográfica de potencias como `16⁰` en el capítulo 8. Se inspeccionaron hojas de contacto de los esquemas y páginas focales del PDF.
3. El capítulo 1 añade una **protoboard funcional explicativa**: rieles, contactos de una misma fila, resistencia, LED, polaridad y retorno. La vista no pretende identificar pines ni capacidades de una marca de placa en particular.
4. El capítulo 22 muestra los **dos carriles de ocho bits** de Aula-16, los bancos alto/bajo, la decodificación y el reparto de direcciones; el texto explica qué seleccionan `A14..A1`, `A15` y `A0`.
5. La **edición maestra de lectura** contiene seis ejercicios seleccionados y resueltos por capítulo, **156** en total. Los **312** originales se mantienen en los 26 manuscritos y sus volúmenes individuales para práctica exhaustiva. El filtrado no elimina el desarrollo teórico.
6. Se retiraron apéndices repetitivos de fuentes y autoverificación del cuerpo de los primeros capítulos. La bibliografía figura una sola vez al final del volumen, con ampliación organizada en `FUENTES_CONSULTADAS.txt`.
7. Se simplificó la introducción del libro para enseñar su contenido, sin explicar ni defender el proceso de producción.

## Archivos principales

- `libro/Aula_Computadora_C26_0_1_MAESTRO.pdf`: libro para lectura.
- `libro/Aula_Computadora_C26_0_1_MAESTRO.docx`: original editable, ecuaciones OfficeMath.
- `libro/INDICE_C26_0_1.json`: paginación medida en el PDF final.
- `FUENTES_CONSULTADAS.txt`: fuentes externas separadas de la narrativa.
- `libro/capitulos/*.md`: 26 fuentes didácticas completas.
- `libro/capitulos/*.docx` y `*.pdf`: 26 fascículos con sus 12 ejercicios originales por capítulo.
- `libro/figuras/*.svg`: figuras editables por código; los PNG se incrustan en el Word.

## Reproducir y comprobar

Se requieren Python 3, `python-docx`, LibreOffice y Poppler (`pdfinfo`, `pdftotext`); para regenerar SVG/PNG se requiere Inkscape. Desde la raíz:

```bash
python3 scripts/generar_figuras_capitulo_01.py
python3 scripts/generar_figuras_capitulo_13.py
python3 scripts/generar_diagramas_capitulos_22_23.py
python3 scripts/generar_libro_maestro.py --pages-json libro/INDICE_C26_0_1.json
python3 scripts/verificar_libro_maestro.py
python3 scripts/verificar_contrato_video_aula_v1.py
```

El índice debe volverse a medir después de una modificación que afecte saltos de página. Las pruebas de documentos no sustituyen una revisión visual detallada de una nueva exportación.

En Windows, la fusión conservadora de la base anterior y el parche se realiza con `scripts/fusionar_C25_0_1_C26_0_1.ps1`; **no borra los ZIP de entrada**.

## Rastro hacia el futuro taller virtual

- El montaje de LED/resistencia y las posiciones del protoboard serán **lecciones de exploración** del simulador cuando exista una fuente de verdad de nodos/conexiones.
- Las líneas y el arbitraje del bus serán **vistas de señales**; la selección de bancos es un contrato funcional, aún no un circuito físico.
- La ROM de caracteres, la VRAM indirecta, los registros MMIO y los modos exclusivos de texto/gráfico se mantienen según `simulador-javafx/CONTRATO_VIDEO_AULA_V1.md`.
- No hay todavía una CPU, ROM, controlador, compilador ni aplicación JavaFX ejecutándose. Las figuras y las pruebas de cálculo **no certifican hardware**.

## Fuera de esta revisión

La portada ilustrada, las fotografías/ilustraciones históricas, los derechos de reproducción y una edición final de publicación quedan para la etapa gráfica posterior. Esta revisión no ha pretendido resolver el esquemático de construcción ni prometer una placa física.
