# Aula-Computadora C28-G · La lectura de memoria no ocurre por arte de magia

**Estado:** prueba temporal ideal en un anfitrión, SIN circuito físico ni
simulador Icarus ejecutado en este entorno.

Esta etapa amplía el capítulo 15 con un problema que los circuitos
puramente combinacionales no resuelven: ¿cuándo es seguro capturar
un byte de memoria? El piloto propone la siguiente secuencia alternativa:

1. **PREPARAR:** MAR captura la dirección, RD se activa y PC permanece.
2. **ESPERAR:** si READY=0, MAR, MDR y PC retienen su contenido; RD sigue.
3. **ACEPTAR:** cuando READY=1, MDR recibe el dato; si era un fetch, PC
   incrementa una sola vez. RD deja de estar activo.

READY es una **abstracción de disponibilidad en el banco de pruebas**,
no un pin de una memoria elegida. El piloto C28-F capturaba MAR y
adelantaba PC en el mismo flanco; la secuencia C28-G prueba el
**avance diferido**, sin aprobar todavía una de las dos variantes.

## Evidencia ejecutada

- El archivo Verilog combinacional generado en C28-F se analizó
  **como texto de un subconjunto explícito**: asignaciones NAND de dos
  entradas y asignaciones de salidas. Un evaluador separado interpretó
  las **177 NAND** de ese archivo y contrastó **8.360 vectores**
  con las fórmulas matemáticas.
- La tabla de señales PREPARAR/ESPERAR/ACEPTAR se probó con un
  modelo de dos registros ideales de 16 bits y un MDR de 8 bits.
- Se recorrieron las dos rutas del programa de trece bytes:
  7 lecturas con Z=0 y 10 con Z=1; cada una usó esperas variables.
  El PC terminó en 600D y MAR en 600C sin cambiar la memoria.
- Se contrastó la retención durante **cien esperas** seguidas,
  las lecturas sin espera, los incrementos 60FF→6100 y FFFF→0000,
  la lectura de datos 6F00 sin alterar PC y los rechazos de
  doble solicitud y READY sin una lectura pendiente.
- Lámina original SVG/PNG generada a partir de la traza probada,
  con tabla nativa de señales en el texto del libro.

**No se ha compilado ni ejecutado el HDL con un simulador general.**
Interpretar las expresiones Verilog de nuestro módulo no prueba la
semántica completa de Verilog, los flancos de un diseño integrado,
los retardos, la alimentación o el arbitraje de un bus real.

## Entregables

- Edición maestra Word y PDF C28-G. Se conservan C28-F y anteriores.
- `scripts/c28g_auditar_hdl_y_memoria.py`: prueba de protocolos,
  rutas y parser/auditor del subconjunto Verilog.
- `c28_g/piloto_lectura/auditoria_y_trazas.json`: contrato, trazas y
  evidencias legibles por máquinas.
- `libro/figuras/c28g_lectura_con_espera.svg` y PNG.
- `scripts/c28g_probar_windows.ps1`: una sola ejecución desde
  PowerShell; si Icarus está instalado compila y corre el testbench
  combinacional previo y crea un ZIP de retroalimentación. Si no lo
  está, deja constancia de la parte HDL que sigue pendiente.

## Siguiente hito propuesto

Construir un **contrato de control más completo** para lecturas de
operandos y datos, escrituras, fases de CALL/RET y RESET por vector de
ROM. Mantener la ISA y la micro-ROM candidatas hasta que la integración
de memoria y reloj haya sido contrastada en simulación HDL completa.
La auditoría integral de diagramas heredados y el debate de UX/UI de
la futura aplicación quedan abiertos.
