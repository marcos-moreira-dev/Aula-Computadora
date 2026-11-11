# Estado editorial después de C23-0.1

**Fecha:** 8 de noviembre de 2026, Ecuador. Se han redactado y maquetado los capítulos numerados **22 «Un bus externo de 16 bits»** y **23 «Programación para Aula-16»**, ocho páginas cada uno, con documentos Word y PDF individuales.

## Qué contiene este lote

| Indicador | Capítulo 22 | Capítulo 23 |
| --- | ---: | ---: |
| Páginas revisadas | 8 | 8 |
| Esquemas originales SVG y PNG | 4 | 4 |
| Ecuaciones editables Word OMML | 13 | 14 |
| Ejercicios y soluciones | 12 | 12 |
| Pruebas anfitrión/documento | 142737 | 77951 |

**Capítulo 22.** Se parte del espacio direccionable de **64 KiB por byte**, con 32 KiB de RAM inicial dispuestos como dos bancos de 16 KiB × 8 bits (carril bajo D7..D0 y alto D15..D8). A0 selecciona byte par/impar; el acceso de palabra alineada usa ambos carriles, y little-endian fija el orden de bytes. Una operación de palabra en dirección impar está **rechazada por nuestra convención Aula-16 V1**, no por una ley de todos los procesadores. El controlador de vídeo existente a nivel de contrato usa registros MMIO de ocho bits, sin memoria gráfica mapeada directamente al espacio CPU. Los esquemas son **funcionales**, no un circuito eléctrico.

**Capítulo 23.** El recorrido pedagógico vuelve a resolver problemas conocidos: tres palabras almacenadas desde `0x2200` suman `0x0202`; Euclides por restas da MCD(48,18)=6; Fibonacci explica el límite de `u16`, incluido `F25=75025` truncado a `9489` cuando se opera módulo 65536. El seudoensamblador nombra **acciones** para razonar, sin atribuirles opcodes, tamaños o tiempos. La **ISA binaria Aula-16, su ABI y el compilador cruzado continúan sin definir ni implementar**.

## Auditoría acumulada

| Medida | Estado actual |
| --- | ---: |
| Capítulos numerados redactados | **23 de 24** |
| Interludios redactados | **P07B** (sin numerar) |
| Capítulos numerados pendientes | **24** (uno) |
| Páginas de documentos por capítulo e interludio | **201** |
| Figuras técnicas originales | **94** |
| Ejercicios resueltos | **288** |
| Expresiones editables OMML | **307** |
| Interludio de texto/gráficos/tipografía | **P23V planeado; no redactado** |
| Libro maestro, índice y auditoría editorial integral | **Pendientes** |
| CPU, firmware, hardware de vídeo, simulador JavaFX | **No implementados** |

Para reproducir los esquemas se dispone de `scripts/generar_diagramas_capitulos_22_23.py` (Python con Inkscape instalado). Las pruebas independientes son `scripts/verificar_capitulo_22.py` y `scripts/verificar_capitulo_23.py` (Python y herramientas Poppler para revisar PDF). La lógica de referencia se ejecuta en el **ordenador anfitrión**, no en el hardware propuesto. Véanse los límites de diagramas en [guía de fidelidad](GUIA_DE_FIDELIDAD_DE_FIGURAS.md) y la especificación de vídeo congelada en [contrato V1](../simulador-javafx/CONTRATO_VIDEO_AULA_V1.md).

**Próximo paso editorial:** el capítulo 24 cierra la comparación de máquinas y enuncia con claridad los límites, problemas no resueltos, etapas de implementación y pruebas futuras. El interludio P23V se elaborará por separado conforme al plan, sin renumerar capítulos.
