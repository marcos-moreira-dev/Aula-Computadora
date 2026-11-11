# Plan de pruebas para el futuro simulador

**Estado R0.12:** criterios de futura aplicación; se han ejecutado verificadores documentales y un **modelo Python de almacenamiento en anfitrión**, pero ninguna suite de la aplicación porque todavía no existe.

## Banco de pruebas digital

| ID | Entrada | Resultado esperado |
| --- | --- | --- |
| G-01 | NAND 00, 01, 10, 11 | 1, 1, 1, 0 |
| G-02 | Full adder, 8 combinaciones | suma y carry correctos |
| S-01 | Latch, escribir y mantener | Q persiste según señal de control |
| R-01 | Registro, clock y enable | captura o retiene sin corrupción |
| A8-01 | Suma de dos u8 | registro y Z/C/N/V correctos |
| A8-02 | u16 por dos bytes | ADD/ADC correlacionados con referencia |
| M-01 | RAM 0x0000, 0x7FFF | direcciones aisladas y bits correctos |
| M-02 | ROM seleccionada | no escritura de programa en memoria de solo lectura |
| A16-01 | Byte en dirección par/impar | carril y registro correctos |
| A16-02 | Palabra en dirección par | un único valor little-endian correcto |
| A16-03 | Palabra en dirección impar | error definido |
| C-01 | Secuencia de microoperaciones | coincide con intérprete ISA independiente |
| C-02 | CALL/RET y pila | restaura PC/SP y registros acordados |
| FW-01 | Reset + ROM | muestra terminal listo |
| FW-02 | PUTC/GETC/PUTS | caracteres correctos |
| FS-01 | Escribir/leer bloque | persiste tras cerrar y abrir |
| BLOCK-REF-01 | Modelo anfitrión de ocho registros C010–C01E | READ/WRITE de 256 B exactos, COUNT=0100 y STATUS coherentes, sin atribuir ejecución de CPU |
| BLOCK-REF-02 | Abortos a 255 B, block out of range y fallos inyectados de imagen | contenido anterior se conserva; ERROR y RESET deterministas; solo archivo temporal de referencia |
| BLOCK-REF-03 | Futuro LOAD crudo con bloque/destino/cantidad hexadecimales | rechazar destino sin alineación, pila, ROM, RAM reservada y bloque inexistente; no habilitar comando en firmware inexistente |
| BLOCK-CPU-01 | Futuro controlador MMIO implementado y firmware | comparar 256 accesos DATA reales, señales y COUNT/STATUS/ERROR contra modelo de referencia |
| LOAD-CPU-01 | Futuro cargador de bloques en CPU Aula | copiar primero a buffer, ejecutar solo tras carga completa y demostrar manejo de error a mitad de varios bloques |
| ASM-01 | Etiquetas y directivas | binario y mapa reproducibles |
| ISA-DOC-01 | Leer JSON de ISA candidata | 36 opcodes únicos, formatos y selectores reconocidos |
| ISA-DOC-02 | Decodificar tres programas de bytes candidatos | longitudes y PC coherentes; sin prometer ejecución real |
| ISA-CPU-01 | CPU de referencia implementada en R1/R7 | programas depositados se ejecutan y producen RAM/flags declarados |
| MICRO-DOC-01 | Nueve transacciones del ejemplo R0.3 | coinciden con bytes de ISA y dirección de ST, sin RD/WR a la vez |
| CTRL-DOC-01 | JSON de microsecuencias R0.5 | fetch común y despacho LDI/ST/HALT coherentes con opcodes candidatos |
| CTRL-DOC-02 | ST absoluto con dos operandos de dirección | preservar byte bajo/alto y cargar MDR antes de escribir; ocho lecturas y una escritura en el programa |
| CTRL-DOC-03 | Transiciones y banderas de control | estados referenciados existentes, HALT terminal, sin flags modificadas, sin atribuir ciclos |
| CTRL-CPU-01 | Micro-ROM y CPU realmente implementadas | comparar pasos ejecutados con semántica ISA y bus observado |
| FLOW-DOC-01 | CALL destino y RET tras subrutina | retorno little-endian guardado bajo/alto, PC/restauración de SP coherentes; sin ejecutar CPU |
| FLOW-DOC-02 | JMP/JZ/JNZ/JC/JNC candidatos | siempre consumir dos operandos; conservar flags, no cargar PC cuando no se toma |
| FLOW-DOC-03 | CALL→LDI→RET→HALT desde RAM | traza de 10 lecturas y 2 escrituras, R0=42; comprobación de escritorio |
| FLOW-CPU-01 | CPU y micro-ROM construidas | comprobar CALL/RET anidados, overflow de SP y saltos tomados/no tomados contra intérprete |
| STACK-DOC-01 | PUSH/POP con R0=42 y SP=0x8000 | escritura a 0x7FFF y posterior lectura, SP restaurado, RAM residual y flags intactas |
| STACK-DOC-02 | PUSHX/POPX de 0x12AB | bajo AB en SP, alto 12 en SP+1, restituye X y SP |
| FLAGS-DOC-01 | INC/DEC sobre u8 | Z/N/V y C conservada; vectores exhaustivos de 256 entradas y carry inicial 0/1 |
| FLAGS-DOC-02 | ADD/ADC/SUB/SBC/CMP en 8 bits | carry/borrow y overflow con signo contrastados con enteros matemáticos; no ALU ejecutada |
| STACK-DOC-03 | Programa LDI/PUSH/LDI/POP/DEC/HALT | 14 lecturas y 1 escritura esperadas; R0=41; SP restaurado |
| IDX-DOC-01 | `LD/ST` candidato X/SP+disp8 | selectores `04–0B`, registros R0–R3, desplazamiento con signo y longitud de 3 bytes coherentes |
| IDX-DOC-02 | Suma de dirección por dos pasos ALU8 | comparar extensión de signo, acarreo privado y módulo 65536; 526592 casos matemáticos, flags y bases conservadas |
| IDX-DOC-03 | Programa `SETX/LDI/ST [X+1]/LD [X+1]/HALT` | 14 lecturas y 1 escritura esperadas, dirección 0x6F01 y PC 0x600D; sin ejecutar CPU |
| IDX-CPU-01 | Futuro motor CPU con X/SP y decodificador RAM/ROM/E/S | resultados y transacciones coinciden con intérprete independiente; rechazar accesos no autorizados según mapa |
| ADJ-DOC-01 | LEAX/ADJSP disp8 y ADDXW R1:R0 | 1572864 sumas ALU8 en dos pasos equivalentes a referencia módulo 65536; flags intactas |
| ADJ-DOC-02 | SETSP imm16 y XFROMSP | preservar endian, copiar registro completo y regresar al fetch sin accesos extra a RAM |
| FRAME-DOC-01 | CALL/PUSHX/XFROMSP/ADJSP/local/POPX/RET | SP/X restaurados, local 0x7FFB, retorno 0x6006 y flags intactas; traza 29 lecturas+5 escrituras |
| FRAME-CPU-01 | Futuro motor ISA+microcontrol independiente | prólogo, epílogo, interrupción de secuencia y desbordes de pila verificados en código real, no solo documental |
| ABI-DOC-01 | Parámetros de 0 a 4 argumentos u8/u16 | derecha a izquierda; PUSH de alto antes que bajo; 640 marcos reproducibles y desplazamientos estables desde X |
| ABI-DOC-02 | Prólogo fijo PUSHX/PUSH R2/PUSH R3/XFROMSP | R2/R3/X preservados, retorno en X+4/5, argumento0 en X+6/7 |
| ABI-DOC-03 | SUMAR_UNO(0x01FF) por ADD/ADC y retorno u16 | R1:R0=0x0200, PC=0x6013, SP=0x8000, 73 lecturas+10 escrituras esperadas |
| ABI-DOC-04 | Profundidad recursiva con stack 0x7000–0x7FFF | 409 marcos de 10 B como máximo teórico idealizado, no garantía física |
| ABI-CPU-01 | ABI en CPU + compilador MiniC realmente implementados | comprobar llamadas anidadas, retorno de u8/u16, preservación R2/R3/X, FLAGS volátiles y desbordamiento sin corrupción |
| MICRO-CPU-01 | CPU realmente implementada | recorrido de bus y estado observado coincide con traza documental |
| MICRO-CPU-02 | Operación de direccionamiento por X/SP | acarreo de dirección interno no modifica flags visibles |
| MICRO-ELEC-01 | Esquemas físicos y temporización | mediciones reales y ausencia de conflictos, no cubierta por traza JSON |
| BP-01 | Panel con CPU detenida | depósito y lectura de bytes sin dos controladores activos en bus |
| BP-02 | Panel escribe en ROM | rechazo, sin daño a contenido |
| BP-03 | Aula-16 byte impar desde panel | carril correcto y bus externo aún de 16 bits |
| MON-01 | RAM aleatoria al RESET | monitor arranca sin suponer ceros |
| MON-02 | POKE ROM y comando inválido | error sin efectos laterales |
| MON-03 | RUN / HALT / retorno | cumple contrato explícito una vez especificado |
| ED-01 | Introducir, reemplazar, listar, borrar línea | contenido y orden correcto |
| ED-02 | Editor sin memoria / salida sin guardar | manejo de errores y aviso |
| ASM-N-01 | Nativo: etiquetas hacia delante | salida igual a ensamblador cruzado |
| ASM-N-02 | Nativo: etiquetas duplicadas o indefinidas | error con línea, no programa ejecutado |
| ST-02 | Persistencia de archivo de fuente y programa | imagen mantiene bytes tras reinicio |
| BOOT-01 | Carga de herramientas desde bloques | ejecución de instrucciones real de CPU Aula, sin ensamblado oculto en anfitrión |
| MEM-SW-01 | Mapa de enlace real monitor | ROM de firmware no excede 8192 B y no pisa tabla/vectores |
| MEM-SW-02 | Ejecutar editor y ensamblador alternados | regiones overlay, fuente, símbolos, binario y pila no se solapan incorrectamente |
| MEM-SW-03 | Fuente o binario sobre su límite | error sin corrupción de monitor, pila ni ROM |
| MC-01 | MiniC funciones y arreglos | salida idéntica a especificación |
| UI-01 | Error de cable deliberado | ayuda identifica el problema |
| UI-02 | Paso completado | se bloquea/autoriza avance correctamente |

## Trazas y diferencias

Por instrucción, registrar PC, bytes de opcode, R0–R3, SP/X, flags, escrituras de memoria y salida del terminal. La simulación de microcontrol y la referencia ISA deben coincidir. Ante una divergencia, reportar primera instrucción y estado afectado.

## Rendimiento

- Navegación interactiva por módulos sin materializar cada celda RAM como objeto 3D.
- La vista 3D solo actualiza componentes visibles/seleccionados y nivel de detalle adecuado.
- Medir tiempo, memoria y FPS en la máquina real del usuario antes de declarar «funciona fluidamente».

## Entrega profesional

Cuando exista implementación:

- Maven clean verify.
- CI con Java 21.
- Prueba de arranque y comandos del monitor.
- Ejemplos de ensamblador y MiniC que produzcan binarios válidos.
- Manual BUILD y README de cada release.
- Script PowerShell para Windows que compile, pruebe y genere paquete de retroalimentación.

No fabricar certificados ni estadísticas de pruebas antes de que existan resultados.

# EXE-AEX1-R0.13 — solo contrato de host

- 42 pruebas automatizadas para firma/version, cabecera little-endian,
  CRC-16/CCITT-FALSE de cabecera y programa, reserva/relleno cero,
  tamaño y tipo de ventana, entradas y CPU destino.
- Rechazo de paquete truncado, sectores insuficientes o error de payload
  **antes** de generar copia de RAM anfitriona; no afirmar atomicidad de
  carga nativa ni de almacenamiento físico.
- Empaquetador e inspector Python con salida no sobrescribible.
- Pendiente: comprobar una carga de verdad mediante firmware y CPU Aula,
  la validez de instrucciones, el espacio real de staging, mapa de enlace y
  ejecución de herramienta en overlay.

## LOADX-R0.14 — dos pasadas sin ejecución Aula

- Primer pase sin modificar RAM: firmas/campos AEX1, sectores completos,
  CRC incremental y ceros de relleno.
- Segundo pase de bloques 256 B: comparar cabecera, copiar solo payload
  a RAM de anfitrión, recalcular CRC, y deshabilitar entrada en
  error tardío aunque haya RAM parcialmente escrita.
- **30 casos** Python para límites 1/16/32 bloques, CRC en fragmentos,
  fallo de lectura, cambio de fuente entre pasadas y preservación
  de otras regiones de RAM.
- En firmware real quedan pendientes protección de RUN, carga del overlay,
  atomicidad, recuperación de cortes y mapas de ROM; no certificarlos.

