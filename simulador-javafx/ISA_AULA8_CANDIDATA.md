# Aula-8: primera propuesta de lenguaje máquina

**Estado R0.3: PROPUESTA PARA REVISIÓN, NO ISA APROBADA.** Este documento da una codificación concreta y programas byte por byte para discutirla antes de construir microcódigo, circuitos, ensambladores o texto definitivo del libro.

La fuente de verdad para valores de opcode es [ISA_AULA8_CANDIDATA.json](ISA_AULA8_CANDIDATA.json). El verificador documental de la ISA comprueba estructura y decodificación de ejemplos; **no** simula el comportamiento de una CPU real.

## 1. Restricciones que no se cambian

- Registros generales `R0`, `R1`, `R2`, `R3` de **8 bits**.
- `PC`, `SP` y `X` de **16 bits**, direcciones de 16 bits y bus externo de datos **de 8 bits**.
- Memoria direccionable por bytes, operando de 16 bits en **little-endian**.
- Indicadores `Z`, `N`, `C` y `V`; llamadas y retornos mediante pila descendente.
- ROM de firmware de 8 KiB separada de la ROM interna de microcontrol; terminal por E/S mapeada en memoria.
- **Aula-16 conserva su bus de datos externo de 16 bits**. Su encoding se diseñará por separado; no reutilizar bytes de Aula-8 automáticamente.

## 2. Una elección pedagógica: opcode y operandos en bytes separados

Una instrucción comienza por un **opcode de 8 bits** y puede contener los siguientes campos:

| Forma | Bytes de la instrucción | Interpretación |
| --- | --- | --- |
| `none` | `OP` | Operación sin operandos |
| `reg` | `OP r` | Registro `0..3`; los seis bits superiores del segundo byte deben valer cero |
| `regpair` | `OP rr` | `rr=(destino<<2)\|fuente`, valores `0..15` |
| `reg_imm8` | `OP r valor8` | Cargar constante en un registro |
| `imm16` | `OP bajo alto` | Dirección o constante de 16 bits, little-endian |
| `disp8` | `OP d` | Desplazamiento `-128..127`, complemento a dos |
| `memory` absoluto | `OP selector bajo alto` | `selector=(0<<2)\|r`, dirección de 16 bits |
| `memory` por X | `OP selector d` | `selector=(1<<2)\|r`, dirección `X+sign(d)` |
| `memory` por SP | `OP selector d` | `selector=(2<<2)\|r`, dirección `SP+sign(d)` |

En el selector de memoria, el modo `3` queda **reservado**. Los cuatro bits superiores de los selectores de memoria y de pares de registro deben ser cero, para que haya una sola representación válida por combinación. No confundir registro `R1` con el byte `0x01` de una instrucción: cada campo tiene interpretación distinta según su posición.

**Costo de esta elección:** programas algo más grandes porque no comprimimos agresivamente registros en el primer byte. **Ventaja:** decodificador y material didáctico más explícitos. La propuesta tiene **36 opcodes**, en vez del intervalo preliminar de 25–30 mencionado al planificar; hay operaciones adicionales de pila/índice para permitir el futuro MiniC. Se revisará el costo antes de adoptar la ISA.

## 3. Tabla candidata de opcodes

Los valores siguientes están en **hexadecimal**, no decimal.

| Opcode | Instrucción | Forma | Acción |
| --- | --- | --- | --- |
| `00` | NOP | none | No altera estado visible salvo PC y tiempo |
| `01` | HALT | none | Detiene ejecución; **no** regresa al monitor automáticamente |
| `02` | RET | none | Recupera PC de pila |
| `10` | MOV | regpair | `Rd ← Rs` |
| `11` | LDI | reg_imm8 | `Rd ← inmediato8` |
| `12` | LD | memory | `Rd ← memoria[dirección efectiva]` |
| `13` | ST | memory | `memoria[dirección efectiva] ← Rs` |
| `14` | SETX | imm16 | `X ← inmediato16` |
| `15` | LEAX | disp8 | `X ← X + desplazamiento firmado` |
| `16` | ADDXW | none | `X ← X + (R1:R0)`; R0 es byte bajo |
| `17` | SETSP | imm16 | `SP ← inmediato16` |
| `18` | ADJSP | disp8 | `SP ← SP + desplazamiento firmado` |
| `19` | XFROMSP | none | `X ← SP` |
| `1A` | PUSH | reg | Inserta un byte en la pila |
| `1B` | POP | reg | Extrae un byte de la pila |
| `1C` | PUSHX | none | Inserta X como palabra de dos bytes |
| `1D` | POPX | none | Extrae X como palabra de dos bytes |
| `20` | ADD | regpair | `Rd ← Rd + Rs` |
| `21` | ADC | regpair | `Rd ← Rd + Rs + C_entrada` |
| `22` | SUB | regpair | `Rd ← Rd - Rs` |
| `23` | SBC | regpair | `Rd ← Rd - Rs - C_entrada` |
| `24` | CMP | regpair | Resta virtual para actualizar flags; no almacena resultado |
| `25` | AND | regpair | AND bit a bit |
| `26` | OR | regpair | OR bit a bit |
| `27` | XOR | regpair | XOR bit a bit |
| `28` | NOT | reg | Complemento bit a bit |
| `29` | INC | reg | Incrementa registro en 1 |
| `2A` | DEC | reg | Decrementa registro en 1 |
| `2B` | SHL | reg | Desplaza a izquierda, entra 0, bit alto sale por C |
| `2C` | SHR | reg | Desplaza lógicamente a derecha, entra 0, bit bajo sale por C |
| `30` | JMP | imm16 | Salto incondicional absoluto |
| `31` | JZ | imm16 | Salta si Z=1 |
| `32` | JNZ | imm16 | Salta si Z=0 |
| `33` | JC | imm16 | Salta si C=1 |
| `34` | JNC | imm16 | Salta si C=0 |
| `35` | CALL | imm16 | Inserta retorno de 16 bits y salta |

Los nombres heredados `LDX Rn,[X+d]` y `STX [X+d],Rn` podrán conservarse como **alias de ensamblador**, traducidos a `LD`/`ST` modo X; no necesitan opcodes nuevos. De igual manera pueden existir alias didácticos para el modo relativo a SP. El contrato definitivo de sintaxis queda pendiente.

## 4. Las banderas no pueden quedar ambiguas

La tabla es una propuesta completa para definir pruebas antes de implementar circuitos:

| Instrucciones | Z | N | C | V |
| --- | --- | --- | --- | --- |
| ADD / ADC | Resultado=0 | Bit 7 del resultado | Acarreo de salida | Overflow de suma con signo |
| SUB / SBC / CMP | Resultado=0 | Bit 7 del resultado | **Préstamo**: 1 si hubo borrow | Overflow de resta con signo |
| INC | Resultado=0 | Bit 7 | Conserva | 1 si `7F→80` |
| DEC | Resultado=0 | Bit 7 | Conserva | 1 si `80→7F` |
| AND / OR / XOR / NOT | Resultado=0 | Bit 7 | Conserva | 0 |
| SHL | Resultado=0 | Bit 7 | Bit 7 anterior | 0 |
| SHR | Resultado=0 | Siempre 0 | Bit 0 anterior | 0 |
| MOV / LDI / LD / ST | Conserva | Conserva | Conserva | Conserva |
| Índice X / SP, pila, saltos, RET, CALL, NOP, HALT | Conserva | Conserva | Conserva | Conserva |

`SBC` toma **C como préstamo entrante**, no como «sin préstamo» al estilo de otras arquitecturas; así se encadena naturalmente `SUB` del byte bajo con `SBC` del byte alto. Tras `CMP` sin préstamo, `JNC` significa «mayor o igual» en comparación **sin signo**. El orden para comparaciones con signo necesitará decisiones adicionales o una secuencia de software, sin inventar una instrucción mágica.

Todas las sumas y restas sobre `R0..R3` almacenan el resultado módulo 256. Los desplazamientos de X y SP usan aritmética módulo 65536 y **conservan flags** para no interferir con comparaciones de datos.

## 5. El primer programa introducido byte por byte

Para que no entre en conflicto con el presupuesto provisional de RAM de R0.2, utilizamos la región reservada para **binario/programa**: el código comienza en `0x6000` y deja su resultado en `0x6F00`. No se necesita editor ni ensamblador para cargarlo.

Objetivo: escribir el número decimal 42 (`0x2A`) en la RAM.

~~~asm
; Sintaxis candidata; NO es código de un ensamblador existente.
.ORG 0x6000
    LDI R0, 0x2A
    ST [0x6F00], R0
    HALT
~~~

| Dirección | Byte | Propósito |
| --- | --- | --- |
| `6000` | `11` | Opcode LDI |
| `6001` | `00` | Registro R0 |
| `6002` | `2A` | Inmediato 42 decimal |
| `6003` | `13` | Opcode ST |
| `6004` | `00` | Modo absoluto, registro R0 |
| `6005` | `00` | Dirección baja del destino |
| `6006` | `6F` | Dirección alta del destino |
| `6007` | `01` | HALT |

**Secuencia binaria candidata:**

~~~text
11 00 2A 13 00 00 6F 01
~~~

Al terminar, el panel debe poder **examinar `0x6F00`** y leer `2A`, **si** se confirma el encoding y la lógica funciona. La prueba actual verifica solo la **coherencia de bytes y longitudes**; no hay CPU que lo haya ejecutado todavía.

### Qué observaríamos en el bus externo

| Orden lógico | Operación | Dirección | Dato | Significado |
| --- | --- | --- | --- | --- |
| 1 | Leer | `6000` | `11` | Fetch del opcode LDI |
| 2 | Leer | `6001` | `00` | Selector de registro |
| 3 | Leer | `6002` | `2A` | Constante que llega a R0 |
| 4 | Leer | `6003` | `13` | Fetch del opcode ST |
| 5 | Leer | `6004` | `00` | Selector de modo/registro |
| 6 | Leer | `6005` | `00` | Dirección baja |
| 7 | Leer | `6006` | `6F` | Dirección alta |
| 8 | **Escribir** | `6F00` | **`2A`** | RAM captura el dato desde R0 |
| 9 | Leer | `6007` | `01` | Fetch de HALT y detención |

Este es un **recorrido lógico esperado**: no asigna ciclos de reloj, tiempos de establecimiento ni microinstrucciones concretas. Durante la ejecución el propietario del bus es **la CPU**, no el panel manual. Los indicadores del panel pueden observar estados, pero no conducir el bus hasta detener/aislar el procesador. Después de fetch de HALT, el PC candidato sería `0x6008`; las banderas permanecerían como estaban antes del programa, porque LDI/ST/HALT se proponen sin modificación de flags.

## 6. Segundo programa: sumar 13 + 9

~~~asm
.ORG 0x6000
    LDI R0, 13
    LDI R1, 9
    ADD R0, R1
    ST [0x6F00], R0
    HALT
~~~

Propuesta de bytes:

~~~text
11 00 0D   ; LDI R0, 13
11 01 09   ; LDI R1, 9
20 01      ; ADD R0, R1  (selector = 0*4+1)
13 00 00 6F; ST [0x6F00], R0
01         ; HALT
~~~

Resultado semántico esperado **cuando exista la CPU**: `R0=0x16`, `RAM[0x6F00]=0x16`, `Z=0`, `N=0`, `C=0`, `V=0`.

## 7. Tercer programa: un bucle

~~~asm
.ORG 0x6000
    LDI R0, 3
CONTAR:
    DEC R0
    JNZ CONTAR
    HALT
~~~

~~~text
6000: 11 00 03  ; LDI R0, 3
6003: 2A 00     ; DEC R0
6005: 32 03 60  ; JNZ 0x6003 (little-endian)
6008: 01        ; HALT
~~~

El contador baja `3→2→1→0`. El salto se toma dos veces y no se toma la tercera, al aparecer `Z=1`.

## 8. Índice, memoria y dirección efectiva

- Modo absoluto: `LD R0,[0x6F00]` consume `12 00 00 6F`.
- Modo relativo a X: `LD R1,[X-1]` consume `12 05 FF`: `modo=1`, `reg=1`, desplazamiento `-1`.
- Modo relativo a SP: `LD R2,[SP+6]` consume `12 0A 06`: `modo=2`, `reg=2`, desplazamiento `+6`.
- `SETX 0x6000` consume `14 00 60`.
- `ADDXW` suma `R1:R0` (dos bytes) a X, ideal para índices variables y arreglos; internamente puede usar dos pasadas de la ALU de 8 bits.

Estas operaciones exigen un registro de dirección de memoria (MAR) de 16 bits y un camino real para calcular sumas de direcciones. La CPU de 8 bits **no** gana una ALU de 16 bits por tener PC, SP y X de 16: las sumas de dirección pueden descomponerse en dos operaciones de 8 bits con acarreo.

## 9. Contrato de pila propuesto para Aula-8

Todavía pendiente de aprobación y de validar compatibilidad con MiniC:

1. Tras el arranque de firmware, `SP=0x8000`, un puntero a la **primera dirección libre por encima** de RAM. La primera escritura de pila ocurre después de decrementar SP, en dirección RAM válida.
2. `PUSH Rn`: `SP ← SP-1`, después `RAM[SP] ← Rn`.
3. `POP Rn`: `Rn ← RAM[SP]`, después `SP ← SP+1`.
4. `CALL destino`: calcula primero `PC_siguiente`; `SP ← SP-2`; guarda byte bajo del retorno en `RAM[SP]`, alto en `RAM[SP+1]`; después salta a `destino`.
5. `RET`: lee byte bajo/alto en `SP` y `SP+1`, suma 2 a SP y restaura PC.
6. `PUSHX` y `POPX` trabajan sobre dos bytes contiguos little-endian, con decremento/incremento de SP de 2.
7. `ADJSP d` reserva o libera espacio, pero **no** inicializa contenido. La pila descendente debe tener límite, comprobado por software/herramienta de enseñanza hasta definir protección física real.
8. Parámetros MiniC inicialmente en ranuras de 2 bytes. Quien llama limpia sus argumentos; R0 y R1 son volátiles; R2, R3 y X se preservan por convenio de función cuando se utilicen.

Una llamada desde el monitor que efectivamente use `CALL` puede volver mediante `RET`; ejecutar `HALT` detiene la CPU y **no** devuelve el control por sí mismo. La relación con el monitor de ROM necesita su contrato y sus vectores de prueba.

### Ejemplo de operación de 16 bits en registros de 8

Si el primer número está en `R1:R0` (alto:bajo) y el segundo en `R3:R2`, una suma de 16 bits utiliza:

~~~asm
ADD R0, R2   ; suma bytes bajos, actualiza C
ADC R1, R3   ; suma bytes altos con C entrante
~~~

Así se conecta el ALU de 8 bits con el compilador MiniC-Aula: no hace falta una segunda ALU de 16 bits oculta.

## 10. Consecuencias sobre los circuitos y microcódigo

Por lo menos habrá que representar:

- Registro de instrucción `IR` de 8 bits; capturador de selector de registro y modo.
- Registros temporales de inmediato de 8/16 y desplazamiento firmado.
- `MAR` de 16 bits y `MDR` de 8 bits para lectura/escritura por bus externo.
- Incremento del PC durante la lectura de uno, dos, tres o cuatro bytes de instrucción.
- Suma de 16 bits para dirección efectiva, PC, SP y X, en microoperaciones de 8 bits o circuito auxiliar documentado.
- Multiplexores para seleccionar fuentes de datos, memoria, registros y banderas.
- ROM de microcontrol **interna**, distinta de ROM de firmware de 8 KiB.
- Estado explícito `HALT`; la respuesta a opcode inválido queda como **propuesta** de parada con diagnóstico, aún sin circuito validado.

No se puede asegurar número de transistores, frecuencia ni que el microcódigo cabe hasta establecer señales, temporización y codificación de microinstrucción.

## 11. Pruebas pendientes para aceptar o descartar la propuesta

1. Unicidad de opcode y validez de formatos/seletores; **automatizada documentalmente**.
2. Decodificación exacta de los tres ejemplos anteriores; **automatizada documentalmente**, sin afirmar ejecución.
3. Tablas de verdad y flags para ADD, ADC, SUB, SBC, CMP, INC, DEC, SHL, SHR, con casos de carry/borrow/overflow.
4. Secuencias de `CALL/RET`, `PUSH/POP`, `PUSHX/POPX`, parámetros y recursividad.
5. Direcciones efectivas por X y SP con desplazamientos `-128`, `-1`, `0`, `127`.
6. Compatibilidad con el presupuesto ROM/RAM, con **código máquina real**.
7. Capacidad de expresar MiniC-Aula: arreglos, bucles, variables locales, funciones y u16, sin instrucciones auxiliares inventadas por el compilador.
8. Circuito y microcódigo realista sin explosión de compuertas para una máquina didáctica.
9. Decidir si 36 opcodes son el punto óptimo frente a 25–30 con más modos o menos servicios especiales.
10. **Solo entonces** convertir esta propuesta en ISA y ABI de referencia definitiva para Aula-8 y el libro.

## 12. Qué NO es este hito

No es un ensamblador, un emulador, una CPU simulada ni una placa construida. Su verificador no pretende ejecutar ninguna instrucción: solamente rechaza duplicaciones, bytes inválidos, campos mal formados y longitudes que no coincidan con el contrato propuesto.
