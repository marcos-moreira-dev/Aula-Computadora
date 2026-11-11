# Revisión visual R0.3 — primer taller NAND de dos entradas

Fuente: cuatro capturas de la interfaz real R0.2 enviadas por Marcos el
11-nov-2026. Este archivo describe cambios de **código**, no ilustraciones IA.

## Contrato implementado

| Observación | Cambio verificable | Límite de ingeniería |
| --- | --- | --- |
| Placa vacía sin buses | Redes VDD, A, B, Y, MID, GND visibles como trazos de placa en 2D y 3D | Son **redes de un bit**; no un bus CPU o PCB fabricable. |
| 3D con diagonales falsas | Contornos construidos por aristas, no `Box` con malla en `DrawMode.LINE` | La silueta 3D es didáctica, no modelo de componente comercial. |
| Diálogos con `...` | Texto envuelto, tamaño mínimo controlado y tema de esquinas rectas | Validar DPI/escala en Windows. |
| Paneles fijos | Botón triangular para plegar/desplegar Recorrido e Inspector, liberando lienzo | Comprobar proporciones al redimensionar ventana. |
| Denominación NAND2 confusa | El rótulo visual dice «NAND de dos entradas» | `NAND2` sigue siendo el nombre técnico del modelo. |
| Archivos mezclados | Documentación de ejecución trasladada a `docs/`; README como índice de onboarding | No mover decenas de borradores históricos sin reparar referencias. |

## Comprobar en Windows

1. Abrir `Montaje 2D`, seleccionar PMOS y NMOS, colocar piezas por clic y arrastre.
2. Ver las seis etiquetas de red y sus trazos alrededor de los cuatro moldes.
3. Abrir `Placa 3D`; revisar que **no haya diagonales blancas espurias**;
   orbitar, acercar, desplazar y encajar una pieza.
4. Plegar y desplegar los dos paneles de forma independiente. Confirmar que
   el lienzo central recupera ancho y que no hay franjas laterales.
5. Pulsar `Ayuda > Controles de montaje`: comprobar que el texto es completo,
   legible y sin puntos suspensivos, también con escalado de Windows.
6. Inspeccionar el interior blanco del encapsulado, la topología PMOS en
   paralelo y NMOS en serie y el camino A/B/Y/VDD/GND.
7. Probar un montaje de cuatro componentes, guardar y reabrir para verificar
   continuidad. Capturar los estados principales con F12.

El asistente `EJECUTAR_Y_CAPTURAR.cmd` comprueba primero Maven y produce un
ZIP con resultados y capturas tomadas por F12 al cerrar el programa.

**Estado:** diseño R0.3 implementado; validación gráfica y compilación Maven
pendientes de Windows. Los 21 controles del modelo no sustituyen dicha prueba.
