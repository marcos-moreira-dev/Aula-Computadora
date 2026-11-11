# Estado editorial después del interludio P07B-0.1

**Fecha de corte:** 6 de noviembre de 2026. **Alcance:** siete capítulos numerados y un interludio independiente, todos en manuscrito, Word y PDF. El currículo sigue teniendo **24 capítulos numerados**, de los cuales faltan **17 (8–24)**.

## Qué aporta «Del bit al significado»

- Explica la diferencia entre la **tensión real**, los umbrales válidos y los estados lógicos. La semántica del hardware depende de la función y de la polaridad de las señales, no de una equivalencia universal «0 = 0 V, 1 = 5 V».
- Interpreta `01000001` como 65, como carácter ASCII `A` y como máscara con b6 y b0 activos; la lectura de una instrucción requiere una ISA que aquí no se finge aprobada.
- Expande `11111111` como 255 sin signo y -1 en complemento a dos de ocho bits; demuestra la regla de restar 256 cuando b7 = 1.
- Distingue un carácter Unicode y su representación UTF-8: `A` -> `41` y `é` -> `C3 A9`; el formato importa incluso cuando no se altera ningún bit de la memoria.
- Introduce la diferencia entre dirección de memoria, byte almacenado y tipo; contextualiza variable, estructura de datos, función y POO sin enseñar clases ni alterar el alcance de MiniC-Aula.
- Añade **4 figuras originales SVG y PNG**, **9 ecuaciones OMML**, **12 ejercicios con solucionario**, **Word editable y PDF de 8 páginas**.
- El verificador `scripts/verificar_puente_07b.py` efectuó **1383 comprobaciones**: todas las lecturas con y sin signo de los 256 patrones de un byte, máscaras, ASCII/UTF-8, NAND y contenido de los archivos. Se añadió a CI.

**Límite:** los cálculos representan reglas matemáticas y codificaciones conocidas. No se ha ejecutado una CPU Aula, probado ROM, montado circuitos, caracterizado voltajes ni certificado un simulador físico.

## Estado acumulado

| Indicador | Resultado |
|---|---|
| Capítulos numerados previstos | **24** |
| Capítulos numerados con Word/PDF | **7** |
| Capítulos numerados por redactar | **17** |
| Interludios realizados | **1**, entre capítulos 7 y 8 |
| Páginas Word/PDF acumuladas | **70** (62 + 8) |
| Figuras propias | **30 SVG y 30 PNG** |
| Ejercicios con solución | **96** |
| Ecuaciones OMML | **91** |
| Comprobaciones específicas interludio | **1383** |
| Word/PDF maestro, portada e índice integral | **Pendientes** |
| CPU, firmware y simulador educativo | **No implementados** |

## Qué falta después de este hito

1. Escribir el **capítulo 8, «Direcciones y buses»**, y luego los capítulos 9–24. Antes de tratar instrucciones y programación como implementadas, estabilizar los contratos de Aula-8 y Aula-16 con evidencia técnica.
2. Releer capítulos 1–7 y este interludio juntos para comprobar transición de vocabulario, numeración de figuras y remisiones, supuestos de electricidad y correlación entre ilustraciones y explicaciones.
3. Producir **Word y PDF maestros**, índice navegable, glosario, bibliografía consolidada, créditos, referencias cruzadas y paginación continua.
4. Revisar tipografía, accesibilidad, ortografía, derechos de imágenes/textos, formatos finales y cualquier compatibilidad que todavía no tenga prueba real, incluida DocuPodcast.
5. Crear la **portada** en la etapa de cierre. Los 17 capítulos pendientes y la edición integral son el trabajo principal restante incluso sin portada.

No se renumeró el currículo. Convertir este interludio en un capítulo 8 formal que desplace el resto sigue siendo una **decisión editorial de Marcos**, no una modificación que se haga por cuenta propia.

## Reproducción

Con Python 3, `python-docx`, Inkscape, LibreOffice y Poppler:

```bash
python3 scripts/generar_figuras_puente_07b.py
python3 scripts/generar_puente_07b.py
# Exportar el Word a libro/capitulos/07b_del_bit_al_significado.pdf
python3 scripts/verificar_puente_07b.py
```
