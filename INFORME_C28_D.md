# Aula-Computadora: avance C28-D del programa en memoria y del PC

Edición de trabajo preparada a partir de C28-C. No sustituye la portada ni los maestros anteriores.

## Avance didáctico

1. El capítulo 14 muestra el **mismo arreglo de 13 posiciones de memoria contiguas** con dos recorridos, uno para `Z=0` y otro para `Z=1`. Los dos dibujos conservan los mismos bytes de la **ISA Aula-8 candidata**. Las flechas indican cambios del **PC**, no conductores eléctricos.
2. El programa de demostración empieza con `JNZ 0x6009`; con `Z=0` carga `R1=0x09` y con `Z=1` carga `R1=0x07` antes de HALT. El PC final después de buscar HALT es `0x600D` en ambos recorridos.
3. El capítulo 15 enseña una parte del **circuito combinacional de selección de PC**. Muestra la tabla de verdad de `JNZ`, `Z` y `TAKE`, con `PC_SEQ` y `TARGET` como entradas de un selector de dieciséis bits. La celda se construye con **tres NAND por bit** más **tres NAND compartidas**; 51 puertas NAND en total.

## Evidencia automática

- `python scripts/c28d_salto_y_selector_pc.py` repite **160.144 comparaciones** de la red de NAND frente a la función esperada del MUX, además de los dos recorridos del ejemplo.
- El generador escribe una **netlist JSON con 51 nodos** y dos trazas JSON; de esos mismos datos se derivan las láminas SVG. Las figuras PNG se producen a partir de SVG mediante Inkscape cuando está instalado.
- El Word contiene **124 imágenes**, incluidas las tres láminas nuevas; el PDF maestro exportado tiene **242 páginas A4** y la paginación se actualizó después del primer render.
- El test existente de C28-A sigue cubriendo NAND, LOAD, flancos, HOLD, triestado y estado inicial `X` con **509.268 comparaciones**.

**Límite importante:** la netlist es solamente combinacional. No contiene el contador PC como registro completo, `PC_LOAD`, reloj ni señalización de memoria. `JMP`, CALL y RET están fuera del selector JNZ; el programa de ejemplo los interpreta un modelo de anfitrión estrictamente limitado. No hay Verilog ejecutado, hardware físico, prueba eléctrica ni CPU completa.

## Siguientes verificaciones

1. Diseñar el contrato de captura de PC (flanco, carga, prioridad de RESET y retención) y comprobarlo primero como celda digital de prueba, sin aprobar aún una microarquitectura completa.
2. Conectar el selector con el recorrido del bus y los latches de dirección y validar que no se pierdan operandos cuando PC se actualiza.
3. Continuar la auditoría de figuras antiguas a tamaño de lectura, corregir colisiones confirmadas y comparar el PDF contra sus diagramas fuente.
4. Fijar mediante revisión con Marcos los detalles pendientes de ISA, control y mapa antes de convertir la CPU candidata en un circuito de implementación.
5. Dejar para después el diseño concreto de UX/UI de la aplicación y la integración de capturas; el libro presente no menciona JavaFX.

El objetivo sigue siendo un libro que **construya la máquina gradualmente**, con evidencia digital repetible y sin confundir esa evidencia con mediciones de un montaje.
