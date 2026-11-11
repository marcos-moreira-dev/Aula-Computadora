# Estado editorial después de C17-0.1

**Corte:** 8 de noviembre de 2026 (Ecuador). Se encuentran redactados **17 de los 24 capítulos numerados** más el interludio P07B. Quedan **7 capítulos (18–24)** y la revisión editorial y maquetación del volumen maestro.

## Capítulo 17 — Encender una computadora

- **Ocho páginas en Word/PDF**, **12 ecuaciones OMML editables**, **4 diagramas originales SVG/PNG** y **12 ejercicios con soluciones**.
- Distingue encendido físico, RESET, contenido de ROM, firmware y micro-ROM; reconoce que RAM no queda automáticamente inicializada. Propone el vector `FFFC=00`, `FFFD=E0` para saltar al arranque ilustrativo `E000`.
- Explica el mapa de direcciones de 64 KiB y la ventana ROM `E000–FFFF` (8.192 bytes), la tabla pública `FF00–FF7F` (32 ranuras de 4 bytes, solo 4 definidas) y sus servicios `FW_PUTC`, `FW_GETC`, `FW_PUTS`, `FW_STATUS`.
- Introduce la gramática conceptual de `HELP`, `MEM`, `POKE`, `RUN` y sus límites: `MEM 6000 10` lee 16 bytes hexadecimales; `POKE` y `RUN` se limitan a `6000–6FFF`; `REG` y `LOAD` siguen indisponibles.
- Diferencia retorno al monitor por `RET` y detención por `HALT`. **196.727 comprobaciones documentales**, incluidos los 65.536 puntos del espacio de direcciones, revisan contratos y artefactos: **no se ejecuta firmware ni una CPU**.

## Acumulado

| Indicador | Valor |
| --- | ---: |
| Capítulos numerados | **17/24** |
| Interludios | **1** (P07B) |
| Pendientes | **7** (18–24) |
| Páginas Word/PDF | **152** |
| Figuras originales SVG/PNG | **70** |
| Ejercicios resueltos | **216** |
| Expresiones OMML | **219** |
| Comprobaciones C16 | **184.283** |
| Comprobaciones C17 | **196.727** |
| Libro maestro Word/PDF, portada, índice y glosario | Pendiente |
| Circuito, firmware, ensamblador y simulador | Sin implementar |

## Límites y próximos hitos

1. Capítulo 18 de acuerdo con `libro/CURRICULO.md`; no anticipar un intérprete o firmware funcionando.
2. Capítulos 19–24 con revisión cruzada y ejercicios propios.
3. Tras completar los 24 capítulos: índice, glosario, bibliografía, portada, estilo común, Word y PDF maestros.
4. Línea técnica R1 aparte: aprobación de ISA/ROM/ABI, verificación digital, temporización, memoria, circuitos reales y pruebas físicas.

```bash
python3 scripts/generar_figuras_capitulo_17.py
python3 scripts/generar_capitulo_17.py
python3 scripts/verificar_capitulo_17.py
python3 scripts/verificar_contexto.py
```

**Fuentes internas candidatas:** `simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.json`, `simulador-javafx/ISA_AULA8_CANDIDATA.json`, `simulador-javafx/MICROFLUJO_AULA8_R0_6_BORRADOR.json`. Ningún borrador representa firmware grabado, ni procesador ni ROM de control construidos.
