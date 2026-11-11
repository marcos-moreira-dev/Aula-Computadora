# Estado editorial después de C18-0.1

**Corte:** 8 de noviembre de 2026 (Ecuador). El capítulo 18 «Hablar con la máquina» está redactado y maquetado: **8 páginas, 4 figuras originales SVG/PNG, 14 expresiones OMML y 12 ejercicios resueltos**. La obra tiene 18 de 24 capítulos numerados más P07B, con **6 capítulos pendientes (19–24)**.

## Qué demuestra el texto

- Diferencia entre salida física, pantalla, terminal, teclado, E/S mapeada y servicios de firmware.
- Registros de ejemplo `DATA=C000` y `STATUS=C002`, comparados con el retorno de `FW_STATUS`; **no** supone que el registro físico y la API usan el mismo mapa de bits.
- Tabla pública ROM candidata: `FW_PUTC=FF00`, `FW_GETC=FF04`, `FW_PUTS=FF08`, `FW_STATUS=FF0C`; se explica cómo leer una llamada con `CALL` pero **no se afirma que haya firmware operativo**.
- Escalera concreta: imprimir `A`, eco de un carácter, guardar el eco en `RAM[6F00]`, emitir `HOLA` con terminador cero, y distinguirlo del programa monitor.
- Cuatro esquemas vectoriales generados con [script reproducible](../scripts/generar_diagramas_tecnicos_aula8.py), sin copiar figuras de fuentes externas.

## Auditoría

`python3 scripts/verificar_capitulo_18.py` aprobó **646 comprobaciones** de bytes, contratos, Word y PDF; revisión visual de las ocho páginas completada. La regeneración de figuras requiere Python e Inkscape en el equipo. No se ejecutaron instrucciones en Aula-8, terminal de hardware, CPU, ROM ni circuito eléctrico.

**Próximo capítulo:** 19 «Guardar y recuperar programas». La progresión general hasta Euclides/Fibonacci figura en [ESCALERA_DE_PROGRAMAS_AULA8.md](ESCALERA_DE_PROGRAMAS_AULA8.md).
