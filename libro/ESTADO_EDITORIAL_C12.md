# Estado editorial después de C12-0.1

**Corte:** 8 de noviembre de 2026 (Ecuador). El libro contiene **12 de 24 capítulos numerados** en Markdown, Word y PDF, más el interludio P07B. Quedan **12 capítulos numerados (13–24)**, además de la edición maestra y la revisión editorial completa.

## Capítulo 12: Arquitectura Aula-8

- **Nueve páginas** en PDF y Word editable; **12 ecuaciones OMML**, **4 diagramas originales SVG/PNG**, **12 ejercicios con soluciones**.
- Vincula registros `R0–R3`, `PC`, `SP`, `X`, `MAR`, `MDR`, `IR`, `SEL`, `TMP` y `FLAGS`; separa el bus interno de datos de 8 bits del bus externo de direcciones de 16 bits.
- Explica la propiedad exclusiva del bus de datos, la lectura/escritura mediante `MAR`/`MDR` y el papel de la unidad de control.
- Lee **en papel** los bytes `11 00 2A` de `LDI R0,42` desde `0x6000`, con `PC=0x6003`, según la **ISA candidata**, no aprobada ni ejecutada.
- Resuelve la dirección `X=0x12FF+2=0x1301` en dos pasadas con ALU de 8 bits y `ADDR_CARRY` separado de la bandera visible `FLAGS.C`.
- **2.752.599 verificaciones aritméticas/documentales**: se recorrieron 65536 direcciones, siete desplazamientos con signo y ambos estados de C, con tres propiedades por caso; se revisaron la traza candidata, imágenes, XML Office y el PDF. **No** se simularon ciclos, firmware, tensión, tiempo ni funcionamiento de CPU.

## Acumulado

| Indicador | Valor |
| --- | ---: |
| Capítulos numerados redactados | **12/24** |
| Interludios redactados | **1** (P07B) |
| Capítulos numerados restantes | **12** (13–24) |
| Páginas acumuladas | **112** |
| Figuras originales SVG/PNG | **50** |
| Ejercicios resueltos | **156** |
| Ecuaciones OMML Word | **163** |
| Verificaciones del capítulo 12 | **2.752.599** |
| Word/PDF maestro con portada, índice y glosario | Pendiente |
| CPU, firmware, simulador JavaFX y montaje físico | No implementados |

## Siguiente trabajo y límites

1. Redactar **capítulos 13–24**, comenzando por «La unidad de control»: estados, señales lógicas, secuenciación y diferencia entre propuesta microprogramada y circuito probado.
2. Al cerrar los 24, realizar revisión editorial transversal: consistencia del vocabulario, diagramas, unidades, referencias, navegación, accesibilidad y solucionarios.
3. Construir **Word/PDF maestro**, con portada definitiva, créditos, índice, glosario y bibliografía.
4. Por separado, concretar esquemas eléctricos, temporización, microcódigo, firmware y simulador; las cifras documentales **no certifican** estas etapas.

## Reproducción

```bash
python3 scripts/generar_figuras_capitulo_12.py
python3 scripts/generar_capitulo_12.py
# Exportar el Word a PDF y revisar visualmente el resultado.
python3 scripts/verificar_capitulo_12.py
```

**Fuentes internas usadas:** `simulador-javafx/MICROARQUITECTURA_AULA8_BORRADOR.md`, `simulador-javafx/UNIDAD_CONTROL_AULA8_BORRADOR.md` y `simulador-javafx/ISA_AULA8_CANDIDATA.md`. Ninguna de ellas constituye una arquitectura congelada.
