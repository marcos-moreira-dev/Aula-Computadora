# Estado editorial después de C11-0.1

**Corte:** 8 de noviembre de 2026 (Ecuador). El libro tiene **11 capítulos numerados de 24** redactados en Markdown, Word y PDF, junto al interludio P07B. Quedan **13 capítulos numerados (12–24)**, revisión global, índice y edición maestra.

## Capítulo 11: La unidad aritmético-lógica

- Ocho páginas en Word/PDF; **21 ecuaciones nativas OMML**, **4 figuras originales SVG y PNG**, **12 ejercicios desarrollados y resueltos**.
- Resta de ocho bits con `A + NOT(B) + 1`, ejemplos **13−9=4** y **9−13=−4**, detallando los ocho pasos y la señal de acarreo interno.
- Diferencia importante de **C** en la ISA candidata Aula-8: **acarreo para ADD; préstamo para SUB**. Al restar, `C_préstamo=1−Cout_sumador`. La definición de banderas para operaciones lógicas sigue pendiente.
- Explicación de **Z/N/C/V** con overflow firmado `−128−1`, funciones lógicas AND/OR/XOR/NOT por columnas, máscaras y comparación sin almacenar la resta.
- Comparaciones **con y sin signo**: `0xFF` puede ser 255 o −1; el criterio sin signo lee préstamo C y el firmado usa `N XOR V`.
- Un multiplexor selecciona una ruta funcional de ALU. La selección de resultado no equivale a habilitar la captura de un registro. Componentes TI CD74HC283, SN74HC86 y SN74HC157 sirven como referencias, no como esquema eléctrico terminado.
- **786524 verificaciones matemáticas/documentales**: todas las 65536 parejas de bytes, 12 propiedades cada una, casos de frontera, artefactos, OMML y texto del PDF. No son mediciones de hardware ni simulación de CPU.

## Acumulado

| Indicador | Valor |
| --- | ---: |
| Capítulos numerados redactados | **11/24** |
| Interludios terminados | **1** (P07B) |
| Capítulos numerados restantes | **13** (12–24) |
| Páginas de capítulos e interludio | **103** |
| Figuras originales SVG/PNG | **46** |
| Ejercicios resueltos | **144** |
| Ecuaciones editables Word OMML | **151** |
| Verificaciones del capítulo 11 | **786524** |
| Word/PDF maestro con portada y glosario | Pendiente |
| CPU, firmware, aplicación y montaje | Sin implementar |

## Pendientes para cerrar el proyecto

1. **Capítulos 12–24**, empezando por «Arquitectura Aula-8»; preservar como **candidatas** las decisiones de ISA, memoria, microarquitectura y banderas no aprobadas.
2. **Revisión editorial integral** de 103 páginas: continuidad, signos, precisión de figuras, citas, ejercicios, navegación y accesibilidad.
3. **Word y PDF maestros** con portada, índice, glosario, referencias, créditos y paginación de volumen.
4. **Validación posterior** del modelo eléctrico/temporal, diseño de CPU y desarrollo de firmware y simulador, etapas distintas de la escritura del libro.

## Reproducción

```bash
python3 scripts/generar_figuras_capitulo_11.py
python3 scripts/generar_capitulo_11.py
# Exportar Word a PDF y revisarlo visualmente antes de distribuir.
python3 scripts/verificar_capitulo_11.py
```
