# Matriz de trazabilidad conocimiento -> hardware -> software -> prueba

Las referencias de capítulo son **provisionales**; se fijarán al escribir el currículo definitivo. Esta matriz busca que ninguna explicación quede desconectada del comportamiento real.

| Tema | Libro | Circuito o modelo | Resultado observable / prueba |
| --- | --- | --- | --- |
| Electricidad CC | Parte I | fuente, resistencias, LED | corriente calculada y medida sin exceder límites |
| Transistor | Parte I | NPN/MOSFET como interruptor | conmutación de salida bajo entradas conocidas |
| Boole y NAND | Parte I–II | puerta discreta y 74HCT00 | 4 combinaciones de dos entradas |
| Realimentación | Parte II | latch SR, latch D | conservación y transición de 1 bit |
| SRAM | Parte II–III | celda 6T conceptual y chip | escribir/leer bit, límite físico explícito |
| Registro | Parte II–III | flip-flops y enable | cargar/retener byte; aislar salida triestado |
| Sumador | Parte III | medio/completo y cadena | todos los casos de bit; carry correcto |
| ALU y flags | Parte III | ALU 8/16 | Z/C/N/V y operaciones de borde |
| ROM y RAM | Parte III | decodificador, bancos | no colisión; dirección correcta |
| Datapath | Parte IV | buses y multiplexores | transferencia entre registros rastreable |
| Control CPU | Parte IV | microsecuenciador | señales correctas por paso de instrucción |
| Aula-8 | Parte IV | CPU 8 bit | programas ensamblados idénticos al intérprete de referencia |
| ISA candidata Aula-8 | Parte IV | opcodes y registros, **aún sin CPU** | borrador JSON decodificable; tres ejemplos legibles, sin afirmar ejecución |
| Microarquitectura candidata Aula-8 | Parte IV | MAR/MDR/IR, buses, datapath, microsecuenciador y ALU8 | traza teórica LDI/ST/HALT de nueve transacciones; sin reloj fijado |
| Control candidato Aula-8 R0.5 | Parte IV | ROM de control, µPC, fetch común, latches candidatos de dirección | JSON de transiciones de LDI/ST/HALT, 8 lecturas + 1 escritura; **no** ejecución ni ciclos reales |
| Flujo y pila candidatos Aula-8 R0.6 | Parte IV–V | SP16, latches retorno, RAM y rutas microprogramadas | CALL→LDI→RET→HALT, 10 lecturas+2 escrituras esperadas; saltos Z/C, sin CPU ejecutada |
| Pila y banderas candidatas Aula-8 R0.7 | Parte III–V | registros, SP, ALU8, RAM y FLAGS | PUSH/POP/INC/DEC, vectores de carry/borrow y 459776 contrastes aritméticos, sin ALU física |
| Direccionamiento indexado candidato Aula-8 R0.8 | Parte IV–V | X/SP16, ALU8, MAR16, RAM y selectores | LD/ST X/SP + disp8, 526592 sumas modulares y traza 14 lecturas+1 escritura; sin CPU o memoria implementadas |
| Ajustes y marcos candidatos Aula-8 R0.9 | Parte IV–V | X/SP16, R1:R0, ALU8, SP descendente, CALL/RET y RAM | LEAX/ADJSP/ADDXW y función con local: 1572864 contrastes de direcciones y 29 lecturas+5 escrituras teóricas; sin CPU ni ABI final |
| ABI MiniC-Aula8 candidata R0.10 | Parte IV–VI | pila, PUSH/POP, X, R0–R3, CALL/RET, memoria u8/u16 y compilador | 640 marcos con 0..4 argumentos, función u16 en 63 B, traza 73 lecturas+10 escrituras esperadas; sin CPU/compilador |
| Firmware y monitor Aula-8 candidatos R0.11 | Parte IV–V | ROM firmware 8 KiB, tabla FF00–FF7F, RESET FFFC/FFFD, terminal MMIO y pila CALL/RET | cuatro ranuras JMP/NOP y vector little-endian contrastados, 40 casos de parser/límites, doble retorno RET y HALT diferenciado; sin ROM ni CPU ejecutadas |
| Controlador de bloques candidato R0.12 | Parte V | periférico MMIO C010–C01F de ocho registros de 8 bits, imagen cruda de sectores 256 B y RAM de carga | 20 pruebas de modelo anfitrión con READ/WRITE/abortos, reapertura y LOAD futuro restringido; sin CPU, firmware, sistema de archivos o controlador construido |
| Formato de ejecutable Aula-8 AEX1 candidato R0.13 | Parte V | controlador de bloques R0.12, paquetes 256 B, cabecera 32 B y ventanas RAM 1000–2FFF / 6000–6FFF | 42 pruebas de CRC16, header, payload, límites, staging en anfitrión y CLI, sin CPU/ROM ni cargador nativo; staging real superior a 3584 B pendiente |
| LOADX Aula-8 en dos pasadas R0.14 | Parte V | bloques de 256 B, CRC16 incremental, RAM de práctica/overlay y búfer provisional 0200–0FFF | 30 pruebas anfitrionas de prevalidación sin RAM alterada, segunda lectura, error tardío y RAM parcial que **no habilita entrada**; CPU/ROM ausentes, atomicidad no probada |
| Terminal | Parte V | DATA/STATUS mapeados | leer/escribir caracteres |
| Firmware | Parte V | vector y tabla ROM | arranque reproducible, ABI estable |
| Programación de panel | Parte IV–V | CPU detenida, control exclusivo de RAM/bus | introducir y examinar bytes; ROM protegida |
| Monitor hexadecimal | Parte V | firmware real en ROM | MEM/POKE/RUN, entradas inválidas y reinicio con RAM arbitraria |
| Editor de líneas | Parte V | utilidad Aula cargada a RAM | líneas persistentes en memoria, edición y errores sin pérdida |
| Ensamblador nativo | Parte V | dos pasadas ejecutadas por CPU Aula | etiquetas resueltas, binario idéntico al cruzado |
| Subrutinas | Parte V | pila y CALL/RET | parámetros, retorno y registros |
| Ensamblador | Parte V | reglas de encoding | listado/imagen binaria contrastable |
| Persistencia | Parte V | bloques de 256 B | leer, escribir, reiniciar y recuperar |
| Bootstrap de utilidades | Parte V | ROM, cargador de bloques y RAM | herramientas externas se cargan y luego ejecutan en CPU Aula |
| Presupuesto de memoria de software | Parte V | RAM, ROM y carga alternada de utilidades | tamaños de binario medidos; sin traslapes y con errores de capacidad |
| Mini C | Parte V–VI | compilación cruzada | u8/u16, bucles, funciones, arreglos |
| Aula-16 | Parte VI | dos bancos de 8 | palabra par, byte impar y error desalineado |
| Construcción guiada | App posterior | netlist de módulos | detectar pieza/cable incorrecto y validar completado |
| Vista 3D | App posterior | modelo geométrico por pieza | representa el estado del mismo circuito que se simula |

## Reglas

- Una figura debe provenir de una especificación concreta.
- Una operación de ensamblador debe disponer de semántica y vector de prueba.
- Una certificación requiere identificar la evidencia, fecha, entorno y limitaciones.
- En cada hito completar las columnas de pruebas reales y ejemplos ejecutables.

