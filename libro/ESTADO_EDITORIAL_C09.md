# Estado editorial después de C09-0.1

**Fecha de corte:** 6 de noviembre de 2026. Con el capítulo 9 existen **9 capítulos numerados** en Word/PDF, más el interludio P07B. El currículo conserva **24 capítulos numerados**; quedan por redactar **15 (10–24)**. No hay edición maestra del libro ni máquina Aula implementada.

## Trabajo entregado

- **Capítulo 9, «RAM y ROM reales»**: paso del registro a la memoria comercial, SRAM volátil, celda de realimentación 6T explicada por bloques, matriz y dirección interna, lectura/escritura y pines activos en bajo.
- Hojas de datos primarias: **Alliance Memory AS6C62256** (`32K × 8`, quince direcciones internas, ocho líneas de datos, CE#/OE#/WE#) y **Microchip AT28C64B** (`8K × 8`, trece direcciones internas, EEPROM no volátil, escritura interna de duración y procedimientos específicos). Se diferencian tiempos de acceso de lectura de los de programación y no se extrapolan valores a otras memorias.
- Ejemplo transparente de mapa de **64 KiB**: `0x0000–0x7FFF` SRAM 32 KiB; `0x8000–0xDFFF` sin asignación 24 KiB; `0xE000–0xFFFF` EEPROM 8 KiB usada como ROM. **Es ilustrativo**, no aprobación del mapa real de Aula.
- Dirección `0xE123`: selección de ROM con `A15:A13=111`, desplazamiento interno `0x0123 = 291`. Se explica que 16 bits de dirección CPU no implican 16 pines de dirección en cada chip.
- Expansión de profundidad `2 × (32K × 8) → 64K × 8` frente a expansión de anchura `2 × (32K × 8) → 32K × 16`. No se atribuye el segundo circuito al cableado definitivo de Aula-16.
- **Cuatro figuras originales SVG/PNG**, **8 páginas Word/PDF**, **10 ecuaciones editables OMML**, **12 ejercicios** con solucionario.
- El verificador `scripts/verificar_capitulo_09.py` realizó **368752 controles matemáticos y documentales** de las 65536 direcciones, tabla de señales, capacidad, selección, little-endian aritmético, archivos Word/PDF y figuras. Se incluye en CI y se revisó visualmente la exportación.

**Limitaciones:** no hay una celda SRAM construida, chips conectados, pruebas de decodificación electrónica, temporización medida, PCB, firmware grabado ni CPU que arranque. La referencia a SRAM 6T es conceptual; no es un esquema de transistores apto para construir. La imagen y tabla de memoria no convierten un mapa provisional en un compromiso de implementación.

## Estado acumulado

| Indicador | C09-0.1 |
|---|---|
| Capítulos numerados del plan | **24** |
| Capítulos numerados con Word/PDF | **9** |
| Interludios terminados | **1** (P07B) |
| Capítulos numerados pendientes | **15** (10–24) |
| Páginas de capítulos e interludio | **87** (79 + 8) |
| Figuras originales | **38 SVG y 38 PNG** |
| Ejercicios resueltos | **120** |
| Ecuaciones Word OMML | **113** |
| Controles nuevos específicos de C09 | **368752** |
| Word/PDF maestro, portada, índices | **Pendientes** |
| CPU, firmware, memoria montada y simulador | **No implementados** |

## Qué falta para concluir

1. Escribir el **capítulo 10, «El circuito que suma»**, seguido de los capítulos 11–24, con ejemplos completos, esquemas originales y ejercicios comprobados.
2. Auditar juntas las 87 páginas: conceptos previos, notación decimal/binario/hexadecimal, correspondencia imagen-texto, pasos de problemas, español y fuentes.
3. Precisar y comprobar los diseños Aula-8 y Aula-16 cuando lleguemos a instrucciones, control, mapa definitivo, firmware, monitor y programación. Las propuestas técnicas actuales **no** equivalen a CPU ejecutable o circuito certificado.
4. Componer el **Word maestro y PDF maestro** con portada, índice navegable, paginación global, glosario, bibliografía, créditos y control de accesibilidad/derechos.
5. Reservar la verificación eléctrica y temporal para cuando existan un esquema concreto y componentes seleccionados, con documentación y mediciones apropiadas.

## Reproducción

```bash
python3 scripts/generar_figuras_capitulo_09.py
python3 scripts/generar_capitulo_09.py
# Convertir libro/capitulos/09_ram_y_rom_reales.docx a PDF con LibreOffice.
python3 scripts/verificar_capitulo_09.py
```
