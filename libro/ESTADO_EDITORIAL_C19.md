# Estado editorial después de C19-0.1

**Corte:** 8 de noviembre de 2026 (Ecuador). El capítulo 19 «Guardar y recuperar programas» está redactado y maquetado: **8 páginas, 4 diagramas originales SVG/PNG, 15 expresiones OMML y 12 ejercicios resueltos**.

## Qué demuestra el texto

- Distinción entre byte de RAM, permanencia de un bloque de almacenamiento y archivo con estructura.
- Modelo R0.12 de bloques crudos de **256 bytes**: número de bloque, offset, comandos, estados, recuento y error. Registros `C010–C01F` candidatos.
- Ejemplo verificable de escritura de 256 bytes y persistencia en la **imagen temporal del anfitrión**; no se simulan fallos eléctricos ni recuperación tras pérdida de energía.
- `LOAD` crudo y `LOADX` AEX1: sintaxis, tamaños, zonas RAM de carga y cabecera de 32 bytes, distinguiendo claramente **comandos aún no disponibles**.
- El ejemplo `11 00 41 35 00 FF 02` se almacena en un bloque de 256 bytes, pero su conservación no significa que sea ejecutable en hardware construido.
- Cuatro esquemas SVG/PNG obtenidos con [generador común](../scripts/generar_diagramas_tecnicos_aula8.py); ver [guía de fidelidad](GUIA_DE_FIDELIDAD_DE_FIGURAS.md).

## Auditoría y acumulado

`python3 scripts/verificar_capitulo_19.py` aprobó **205.037 comprobaciones** de límites de bloques, modelo anfitrión, contratos, Word y PDF. `python3 scripts/verificar_escalera_programas_aula8.py` aprobó **4.113 pruebas matemáticas** (sumas, MCD y Fibonacci) que no se presentan como ejecución de Aula-8. Las 8 páginas finales de este capítulo se revisaron visualmente.

| Indicador | Estado |
| --- | ---: |
| Capítulos numerados redactados | **19/24** |
| Interludios | **1 (P07B)** |
| Capítulos por redactar | **5 (20–24)** |
| Páginas Word/PDF | **168** |
| Figuras técnicas originales | **78** |
| Ejercicios resueltos | **240** |
| Expresiones OMML editables | **248** |
| Volumen maestro Word/PDF, índice, bibliografía, glosario, portada | Pendientes |
| CPU, firmware nativo, almacenamiento físico y simulador | Sin implementar |

**Siguiente:** capítulo 20, de acuerdo con el currículo; después 21–24 y auditoría editorial completa. Los diagramas actuales explican **bloques funcionales**, no certifican flip-flops, SRAM, señales temporales ni netlists físicos. Antes de afirmar fidelidad de circuitos reales se necesitarán esquemas, simulaciones digitales/eléctricas y pruebas de componentes concretos.
