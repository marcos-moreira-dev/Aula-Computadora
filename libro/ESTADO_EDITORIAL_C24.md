# Estado editorial vigente — C24-0.1

**Fecha:** 8 de noviembre de 2026 (Ecuador). **Naturaleza:** conclusión de **los 24 manuscritos numerados**, no declaración de que el libro maestro o la computadora física están terminados.

## Lo añadido en este lote

| Entregable | Ubicación | Páginas | Figuras | OMML | Ejercicios |
| --- | --- | ---: | ---: | ---: | ---: |
| Interludio P23V «De los mapas de caracteres al escritorio gráfico» | Entre C23 y C24 | 10 | 7 | 13 | 12 |
| Capítulo 24 «Una computadora que podemos explicar» | Cierre numerado | 9 | 4 | 13 | 12 |
| **Total nuevo** | | **19** | **11** | **26** | **24** |

P23V enseña el viaje de un carácter ASCII `41` a un glifo **original** 8×8, del mapa de texto 32×16 a un mapa de bits 256×128 de **2bpp**, y de las fuentes de píxeles a las formas vectoriales. Explica la diferencia entre **modo de direccionamiento de ISA**, **dirección de CPU/MMIO** y **offset interno VRAM**. Incluye el contraste hipotético de 1/4/8bpp **sin introducir nuevos modos** al contrato V1.

El capítulo 24 cierra la trayectoria desde el transistor hasta el monitor de una microcomputadora: mapa de 64 KiB, separación de Aula-8 y Aula-16, progresión de problemas (variable, suma, arreglos, Euclides, Fibonacci, consola) y los niveles de prueba. No atribuye un opcode de Aula-16, una ROM operativa ni mediciones a hardware que no existe.

## Auditoría de estado acumulado

| Medida | Estado C24-0.1 |
| --- | ---: |
| Capítulos numerados redactados | **24 de 24** |
| Interludios independientes | **2: P07B y P23V** |
| Páginas individuales en Word/PDF | **220** |
| Figuras originales con fuentes SVG y exportación PNG | **105** |
| Ejercicios con solucionario | **312** |
| Expresiones matemáticas OMML editables | **333** |
| Comprobaciones en este lote | **66576** |
| Word/PDF **maestro** con índices y referencias consolidadas | **Pendiente** |
| CPU Aula, simulador, firmware y vídeo físico | **No implementados** |

Los 66.576 controles verifican consistencia del **modelo en anfitrión**: todos los 32.768 píxeles de 2bpp, el direccionamiento de la comparación 1bpp, matriz de glifo bit a bit, las 512 celdas de texto, los 11 SVG/PNG y estructura de los DOCX/PDF. Estas comprobaciones **no son 66.576 instrucciones de CPU ejecutadas**, ni certifican tensión, ciclos, sincronía o reloj.

Reproducir desde la raíz:

```bash
python3 scripts/verificar_contexto.py
python3 scripts/verificar_contrato_video_aula_v1.py
python3 scripts/verificar_entrega_c24.py
```

Para regenerar las figuras: `python3 scripts/generar_diagramas_c24_p23v.py` con Inkscape. Para generar Word: `python3 scripts/generar_interludio_p23v.py` y `python3 scripts/generar_capitulo_24.py` con python-docx. Para convertir Word a PDF se usa LibreOffice; para inspección, `pdfinfo` y `pdftotext` de Poppler. El ZIP ya incluye las versiones resultantes.

## Qué permanece congelado

- Arquitectura de bus: Aula-8 8 bits de datos, Aula-16 **16 bits externos**, ambos con **16 bits de direcciones byte**.
- Vídeo V1: una pantalla, **modo texto o gráfico**, sin superposición. Registros `C020–C02A`; memoria de caracteres **512 B** y bitmap **8192 B**, RAM de vídeo separada de RAM de CPU; ROM de glifos **2 KiB reservada**.
- Cuatro índices de color del bitmap: negro, verde, ámbar y blanco. No hay controlador físico, GPU ni salida VGA comprometidos.
- La tabla completa de glifos, firmware monitor, ISA/ABI definitivas, temporización y protocolos de entrada aún deben implementarse y comprobarse.

## Próxima fase editorial

1. Preparar una **edición maestra única** (Word y PDF), incluyendo los 24 capítulos y ambos interludios en sus posiciones, con índice y referencias normalizadas.
2. Auditoría transversal de términos, fórmulas, referencias cruzadas, autoría, contraste y legibilidad de todas las figuras. La verificación de paginación de capítulos sueltos **no sustituye** esta lectura global.
3. Aprobar portada, créditos y requisitos de publicación con el propietario; solo entonces etiquetar una edición estable.

La futura **implementación del taller técnico** es un frente diferente. No ampliar el libro a nuevos modos de vídeo ni introducir sin decisión un conjunto de instrucciones de gráficos. La edición puede enseñar conceptos modernos en un interludio sin exigir que el hardware Aula los reproduzca.
