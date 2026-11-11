# Aula-Computadora — seis maquetas representativas de UX/UI

**Estado:** diseño de interfaz **propuesto**, 11 de noviembre de 2026.
Estas imágenes **no** son capturas de una aplicación JavaFX implementada,
una PCB fabricable, una simulación SPICE ni una CPU ya ejecutable.

## Inventario visual

| ID | PNG | SVG | Propósito |
| --- | --- | --- | --- |
| IM-01 | `IM-01_AULA_UX_V1.png` | `IM-01_AULA_UX_V1.svg` | Inicio: Aula-8 y Aula-16 con avances independientes. |
| IM-02 | `IM-02_AULA_UX_V1.png` | `IM-02_AULA_UX_V1.svg` | Placa didáctica 3D conceptual de Aula-8. |
| IM-03 | `IM-03_AULA_UX_V1.png` | `IM-03_AULA_UX_V1.svg` | NAND2 estática: dos PMOS en paralelo y dos NMOS en serie. |
| IM-04 | `IM-04_AULA_UX_V1.png` | `IM-04_AULA_UX_V1.svg` | Error de prueba: observado contra esperado, sin causa raíz inventada. |
| IM-05 | `IM-05_AULA_UX_V1.png` | `IM-05_AULA_UX_V1.svg` | Editor y monitor de texto 32 × 16 en una única vista. |
| IM-06 | `IM-06_AULA_UX_V1.png` | `IM-06_AULA_UX_V1.svg` | Aula-16: bancos par/impar y ejemplo de palabra little-endian. |

`AULA_UX_SEIS_VISTAS_CONTACTO_V1.png` reúne las seis vistas para su
revisión visual.

## Qué es exacto y qué no

- La gramática de ventana coincide con
  `simulador-javafx/CONTRATO_UX_COMANDOS_Y_CAPTURAS_V1_PROPUESTA.md`:
  menú superior, toolbar contextual, sidebar, workspace/tabs, inspector,
  dock inferior y statusbar.
- La NAND de IM-03 usa la topología lógica del plano
  `c28_ac/activos_app/CMOS_NAND2_4_MOS.svg`; los bloques son una
  **abstracción gráfica**, no símbolos de encapsulado o pines reales.
- IM-04 muestra un conjunto de vectores didáctico hipotético y deja la
  causa del error sin determinar.
- El texto de IM-05 es **pseudocódigo ilustrativo**, no un ensamblador
  Aula-8 aprobado ni una compilación que se haya ejecutado.
- IM-06 presenta organización lógica candidata y **no presupone**
  64 KiB de RAM físicamente instalados. El ejemplo
  `RAM[0x6000]=0x34`, `RAM[0x6001]=0x12` reconstruye `0x1234`.
- Aula-16 no tiene vista 3D en V1. Las vistas comparten un futuro
  estado lógico, pero ninguna imagen prueba que ese motor esté construido.
- El objetivo de finalizar cada recorrido en cinco horas sigue siendo una
  meta por comprobar mediante pruebas de uso.

## Regeneración

Con Python y `svgwrite`:

```bash
python scripts/generar_mockups_ux_im01_im06.py
```

El generador conserva el archivo histórico IM-02 V1, cuyo SVG y script
original están también en `docs/ux/mockups/` y `scripts/`. Los otros
cinco SVG se convierten a PNG con Inkscape; todos los SVG son editables.

**Pendiente:** validar estos diseños con Marcos y después implementar las
vistas reales en JavaFX. Los colores, posiciones y medidas de la interfaz
son propuestas; no constituyen todavía un sistema de diseño congelado.
