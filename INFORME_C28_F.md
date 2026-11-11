# Aula-Computadora C28-F · Seguir, saltar y recordar la dirección

**Estado:** piloto de lógica ideal en anfitrión. No es una CPU operativa,
una placa fabricable, una ISA aprobada ni una simulación eléctrica.

La edición C28-F amplía la sección del capítulo 15 dedicada al registro PC.
El PC almacena una dirección; ahora también se explica el circuito que
calcula la siguiente, quién decide si cargarla y cómo MAR obtiene la
dirección del byte que debe leerse **antes** de que PC avance.

## Resultados incorporados al libro

- **PC de 16 bits:** red candidata de incremento por acarreo, módulo 65536.
  Demostración de 0x6000→0x6001, 0x60FF→0x6100 y 0xFFFF→0x0000.
  El acarreo de dirección no altera FLAGS.C.
- **Saltos:** selector de 16 bits con TAKE = JMP OR (JNZ AND NOT Z).
  La combinación simultánea JMP+JNZ se rechaza en el contrato del piloto.
  No se confunde la salida combinacional con una orden de PC_LOAD.
- **JNZ no tomado:** después de buscar sus tres bytes, PC ya apunta a la
  próxima instrucción. Mantener PC_LOAD=0 evita incrementar una vez más
  y perder el siguiente opcode.
- **MAR:** con FETCH=1, MAR_D toma el PC_Q anterior; con FETCH=0, toma
  DATA_ADDR. MAR_LOAD permite retener o capturar. En un mismo flanco
  ideal de lectura, MAR recibe 6000 y PC pasa de 6000 a 6001.
- **Ilustración:** lámina de acarreo PC+1 integrada al Word/PDF; segunda
  lámina de estados de dos rutas incluida como material de ampliación.
  Tablas nativas de estado en el texto para lectura cómoda en A4.

## Evidencia reproducible

El script `scripts/c28f_incremento_mary_saltos.py` construye **177 puertas
NAND combinacionales candidatas** y las representa en una única netlist:

| Parte | NAND |
| --- | ---: |
| Incrementador PC+1 | 75 |
| Selector de incremento / destino | 53 |
| Selector de entrada de MAR | 49 |
| **Total** | **177** |

El verificador completó **161.537 comparaciones**, incluyendo las
65.536 direcciones PC posibles, 96.000 combinaciones de saltos y fuentes
de dirección, y una selección de dirección de datos. Además comprueba
las dos rutas del programa candidato de trece bytes y que MAR captura
el valor anterior al flanco. Las trazas se conservan en JSON.

Los archivos `pc_mar_c28f.v` y `tb_pc_mar_c28f.v` se generan desde la
netlist para facilitar una prueba HDL posterior. **No se ha ejecutado
Icarus Verilog en esta edición.** En particular, el HDL actual es
combinacional: no sustituye los registros de PC/MAR ni sus tiempos reales.

## Límites y decisiones pendientes

- No está aprobado si PC+1 tendrá un incrementador separado o utilizará ALU.
- Falta integrar reloj, arbitraje real de bus, señales de espera de memoria,
  flancos y RESET por vector ROM con secuenciación de control completa.
- La temporización eléctrica, la selección de integrados, alimentación,
  márgenes de ruido, PCB y montaje permanecen sin validar.
- Tampoco se ha certificado el resto de diagramas heredados ni se ha
  hecho una revisión humana completa de todas las páginas del libro.
- La conversación sobre UX/UI del futuro taller visual permanece
  pendiente y se hará fuera del texto didáctico.

**Entrega editorial:** libro maestro C28-F de 26 secciones capitulares;
mantiene el Word editable, PDF de lectura, índice y todas las ediciones
anteriores. La nueva expansión se concentra en el capítulo 15.

## Próximo paso propuesto: C28-G

Comprobar la red en un simulador HDL real; después, tratar el origen de
MAR durante operandos, datos, CALL/RET y vector de RESET. Antes de
afirmar que los circuitos funcionan como procesador, deberá existir
un contrato temporal verificable para la memoria y la unidad de control.
