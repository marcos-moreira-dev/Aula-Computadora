# Aula-Computadora C28-E · El PC ya puede conservar su dirección

**Estado: piloto lógico de laboratorio, no CPU ni esquema eléctrico apto para montaje.**

La edición incremental C28-E continúa las láminas del salto condicional C28-D.
La nueva sección del capítulo 15 incorpora una tabla de transición de estado:
sin flanco ascendente no se captura nada; con flanco ascendente, CLEAR_TEST
tiene prioridad, LOAD captura PC_NEXT y la ausencia de ambos conserva PC_Q.
El Word maestro lleva **125 imágenes integradas**; la edición de lectura
resultante ocupa **244 páginas A4**, con índice paginado.

## Construcción

- Un banco de **16 flip-flops D ideales**, porque el PC guarda direcciones de
  dieciséis bits tanto en Aula-8 como en Aula-16.
- Una red combinacional comprobable de **82 puertas NAND**:
  dos inversores compartidos para LOAD y CLR_TEST, y cinco NAND por cada bit.
- Realimentación desde Q al selector de retención. No se ha dibujado un
  transistor de reloj, ni se han atribuido tiempos, voltajes ni consumo.
- Dos nuevas figuras SVG/PNG: red con una celda NAND detallada (integrada al
  libro) y registro de doce observaciones de flanco, retención, carga, X y
  limpieza (material ampliable de apoyo). La selección de eventos del libro
  es una **tabla nativa**, para que los valores sean legibles en tamaño A4.
- Un contrato/netlist en JSON y un calendario de eventos JSON. Se genera
  Verilog y un testbench desde **la misma netlist** que gobierna las figuras.

## Evidencia

- **110.176 comparaciones** correctas del circuito NAND, estado inicial
  desconocido, flancos y referencia independiente de estado.
- Dos secuencias de integración toman la salida del selector JNZ del piloto
  C28-D y muestran que PC_Q no cambia hasta LOAD y el siguiente flanco.
- Se distingue expresamente **CLR_TEST síncrono, exclusivo de este banco**
  del RESET auténtico de CPU: la máquina real leerá el vector de ROM, que
  todavía necesita unidad de control, memoria y temporización implementadas.

**No se ha ejecutado Icarus Verilog** ni hay simulación con retardos,
validación física, compatibilidad con integrados, diseño de PCB, CPU funcional
o control completo de memoria. Verilog queda como material reproducible para
una prueba posterior en Windows, no como evidencia ya obtenida.

## Próximo hito

Unir la selección de dirección (incluido JMP y fetch secuencial) con el
arbitraje del PC y la formación de MAR; diseñar el RESET por vector de ROM
sin convertir CLR_TEST en RESET real; aplicar pruebas con una herramienta HDL
y revisar esquema de reloj/tiempos antes de hablar de integrados concretos.
Continúa pendiente la auditoría de las figuras heredadas y la revisión humana
integral del libro. La UX/UI del taller visual se conversará más adelante.
