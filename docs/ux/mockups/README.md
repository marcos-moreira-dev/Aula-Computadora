# Aula-Computadora — maquetas representativas de UX/UI

**Estado:** diseño de interfaz **propuesto**, tercera revisión semántica V3.
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

## Segunda tanda: diez vistas V2 con iconos vectoriales

La V2 conserva las primeras seis situaciones y añade cuatro escenas de
navegación que faltaban. Las diez incorporan una **barra de herramientas
con iconos y texto**, dibujada en SVG para que sus etiquetas sean
verificables y editables, sin depender de una imagen generada por IA.

| ID | Situación en V2 | Decisión de interfaz que ilustra |
| --- | --- | --- |
| IM-01 | Inicio y elección de recorrido. | Los avances de Aula-8 y Aula-16 son independientes; no hay gestor de proyectos. |
| IM-02 | Montaje de la placa de Aula-8. | El kit y la secuencia guiada acompañan un lienzo de placa conceptual. |
| IM-03 | Detalle de NAND2. | Se mantiene la separación entre pieza física, símbolo y prueba de lógica. |
| IM-04 | Prueba con resultado distinto al esperado. | Los problemas se localizan en un dock inferior, con un diagnóstico honesto. |
| IM-05 | Programación y pantalla. | Editor, herramientas de simulación y salida de texto conviven en una vista. |
| IM-06 | Aula-16 en 2D. | Una computadora más ancha no requiere modelado 3D. |
| IM-07 | Explorar referencia Aula-8. | La máquina terminada se puede inspeccionar sin modificar el avance. |
| IM-08 | Profundizar registro A → celda del bit 0. | Una misma entidad admite vista de símbolo y, cuando exista un diseño validado, vista de transistores. |
| IM-09 | Preferencias de escritorio. | Los ajustes están en un diálogo modal con navegación propia, no en el inspector. |
| IM-10 | Menú Ver y modo concentración. | Sidebar, inspector y dock se pueden ocultar para ampliar el área de dibujo. |

Para cada `IM-XX` hay dos archivos `IM-XX_AULA_UX_V2.svg` y
`IM-XX_AULA_UX_V2.png`. La lámina
`AULA_UX_DIEZ_VISTAS_CONTACTO_V2.png` permite revisar las diez de un vistazo.

## Tercera tanda: dieciséis situaciones V3

La V3 incorpora la auditoría semántica de las diez escenas anteriores y
seis situaciones adicionales de interacción. **Es la referencia visual
preferente para discutir UX/UI**; V1 y V2 permanecen para conservar el
historial de decisiones. Todos los archivos `IM-XX_AULA_UX_V3.svg` tienen
su correspondiente PNG. El código fuente está en
`scripts/generar_mockups_ux_v3.py`.

| ID | Situación de la V3 | Contrato semántico ilustrado |
| --- | --- | --- |
| IM-01 | Inicio. | Recorridos finitos y progreso independiente, sin proyectos arbitrarios. |
| IM-02 | Placa de Aula-8. | Construcción guiada con puntos de colocación; montaje aún no probado. |
| IM-03 | Construcción NAND2. | NAND2 es **objetivo**, mientras que el kit ofrece 2 PMOS y 2 NMOS; todavía no es un módulo listo para usar. |
| IM-04 | Falla en prueba. | Distingue resultado esperado y observado; evita adivinar la causa. |
| IM-05 | Editor y pantalla. | Separa editor **anfitrión** de pantalla **de la CPU**, sin atribuir al firmware un editor que no tiene. |
| IM-06 | Aula-16 2D. | Banco par/impar, palabra little-endian y dirección de 16 bits. |
| IM-07 | Arquitectura Aula-8. | R0–R3 de 8 bits, PC/SP/X de 16 bits; mapa de módulos, **no** netlist. |
| IM-08 | Registro R0. | Inspección del mismo objeto entre símbolo, detalle y estado lógico. |
| IM-09 | Preferencias. | Diálogo independiente del inspector contextual. |
| IM-10 | Menú Ver. | Visibilidad de sidebar, inspector, dock y modo concentración. |
| IM-11 | Arrastre activo de transistor. | Fantasma de colocación, región admisible, acción cancelar y pista contextual. |
| IM-12 | Compuerta aprobada. | Tabla de verdad comprobada → promover NAND2 a módulo reutilizable; ejemplo ilustrativo. |
| IM-13 | CPU Aula-8 pausada. | Inspección de buses, señales, bits, registro y pulso único; instantánea hipotética. |
| IM-14 | Panel manual. | Depositar un byte en RAM con CPU detenida y bus exclusivo; herramientas anfitrionas separadas. |
| IM-15 | Finalización Aula-8. | Recorrido finito, progreso conservado y acceso posterior a Aula-16. |
| IM-16 | Vídeo gráfico. | **Una sola pantalla** con modo gráfico alternativo exclusivo, 256 × 128, 2 bpp y cuatro colores. |

`AULA_UX_DIECISEIS_VISTAS_CONTACTO_V3.png` permite auditar el conjunto
en una lámina; `AULA_UX_NUEVAS_ESCENAS_CONTACTO_V3.png` agrupa IM-11 a
IM-16. Las barras de herramientas contextuales poseen iconos vectoriales
y etiquetas; los controles son **maquetas estáticas**.

La V3 deja expresamente **sin resolver** el circuito físico completo de
los registros, los encapsulados definitivos, el repertorio de instrucciones
y el aspecto final de una aplicación JavaFX real. La verificación y los
estados representados en IM-12 a IM-16 son **hipotéticos** y no un registro
de pruebas del motor. El diseño de información se conserva independiente
del motor de simulación y de sus posibles representaciones 2D/3D.

En esta tanda las vistas y los valores son **escenas de diseño**, no una
prueba de funcionamiento de la CPU. Por ejemplo, la pantalla IM-07 usa
un bus de bits ilustrativo; IM-08 no inventa la topología interna de
un registro cuyo circuito no haya sido aprobado. Los controles dibujados
todavía no responden a interacciones reales.

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
python scripts/generar_mockups_ux_v2.py
python scripts/generar_mockups_ux_v3.py
```

El generador conserva el archivo histórico IM-02 V1, cuyo SVG y script
original están también en `docs/ux/mockups/` y `scripts/`. Los otros
cinco SVG se convierten a PNG con Inkscape; todos los SVG son editables.
El generador V2 crea los diez SVG; sus PNG pueden rasterizarse con
Inkscape y agruparse en una lámina de contacto.

**Pendiente:** validar estos diseños con Marcos y después implementar las
vistas reales en JavaFX. Los colores, posiciones y medidas de la interfaz
son propuestas; no constituyen todavía un sistema de diseño congelado.
