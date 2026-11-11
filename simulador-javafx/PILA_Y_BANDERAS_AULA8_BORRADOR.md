# Aula-8 — pila de datos, INC/DEC y banderas (R0.7)

**Estado: PROPUESTA PARA REVISIÓN, NO APROBADA.** Continúa el [contrato de ISA candidato R0.3](ISA_AULA8_CANDIDATA.md), las [microacciones R0.5](UNIDAD_CONTROL_AULA8_BORRADOR.md) y el [flujo de pila R0.6](CONTROL_FLUJO_PILA_AULA8_BORRADOR.md). La especificación es **lógica**, sin ciclos eléctricos, netlist ni CPU ejecutable.

## 1. ¿Qué añade una pila aparte de CALL/RET?

Una subrutina necesita conservar datos, no solamente recordar dónde regresar. Si el programa está usando `R0` y otra rutina necesita temporalmente ese registro, puede guardarlo en la pila y recuperarlo después.

En Aula-8 `PUSH R0` consume dos bytes (`1A 00`) y `POP R0` otros dos (`1B 00`). Los selectores `0..3` corresponden a `R0..R3`; un selector distinto **no** debe realizar una escritura parcial antes de detectar error. Para leer el selector se usa el fetch de operandos de R0.5.

### PUSH: decremento previo

Con `SP=0x8000` y `R0=0x2A`:

1. Leer y validar el selector del registro.
2. `SP ← SP-1 = 0x7FFF`, sin cambiar `Z/N/C/V`.
3. `MAR ← SP`; `MDR ← R0`.
4. Activar la escritura de RAM en `0x7FFF` con dato `0x2A`; desactivar `WR`.

### POP: incremento posterior

Con `SP=0x7FFF`:

1. Leer y validar selector, preparar `MAR ← SP`.
2. Leer `RAM[0x7FFF]` y capturar el dato en `TMP`; no conducir simultáneamente el bus externo.
3. `R0 ← TMP`; `SP ← SP+1 = 0x8000`.
4. Conservar **todos** los flags. La celda de RAM permanece con su byte anterior hasta ser sobrescrita.

| Momento | SP | R0 | RAM[0x7FFF] | Flags |
| --- | --- | --- | --- | --- |
| Antes del PUSH | `8000` | `2A` | No determinado | Se conservan |
| Después del PUSH | `7FFF` | `2A` | `2A` | Se conservan |
| Si `R0` cambia a `00` | `7FFF` | `00` | `2A` | Según operación usada |
| Después del POP | `8000` | `2A` | `2A` residual | Se conservan en POP |

El espacio de pila previsto es `0x7000–0x7FFF`; un `PUSH` fuera de ese espacio **no tiene protección física demostrada**. El futuro taller podrá advertir un fallo, pero eso no equivale a un circuito hardware que lo detecte.

## 2. PUSHX y POPX: 16 bits con bus de datos de 8

R0.3 ya reservó `PUSHX` (`1C`) y `POPX` (`1D`), sin bytes de operando.

- `PUSHX`: `SP ← SP-2`; escribir byte bajo de `X` en `[SP]` y byte alto en `[SP+1]`.
- `POPX`: leer bajo y alto desde `[SP]` y `[SP+1]`; cargar `X` y después `SP ← SP+2`.
- **La secuencia de almacenamiento tiene el mismo orden little-endian que CALL/RET**, por lo que puede compartir una parte de la lógica, sujeto a multiplexores concretos.
- Las lecturas de `POPX` requieren retener ambos bytes, por ejemplo reutilizando `ADDR_LO/ADDR_HI` **cuando no albergan otro valor vivo**.
- `SP+1` se calcula para dirigir `MAR`; no modifica SP por sí solo, ni toca los flags del programa.

Ejemplo: si `X=0x12AB` y `SP=0x8000`, tras `PUSHX` habrá `AB` en `0x7FFE` y `12` en `0x7FFF`, con `SP=0x7FFE`. `POPX` restituye `X=0x12AB` y `SP=0x8000`; RAM no se borra.

## 3. El registro FLAGS: cuatro conceptos distintos

| Bandera | Significado para operaciones de 8 bits | Cómo leerla |
| --- | --- | --- |
| `Z` | Resultado de 8 bits igual a cero | `JZ` salta si es 1. |
| `N` | Bit más significativo (bit 7) del resultado | Indica signo negativo solo interpretando u8 como complemento a dos. |
| `C` | Acarreo en suma; **préstamo** en resta | No es una bandera de «mayor o menor» universal. |
| `V` | Desbordamiento **con signo** en suma o resta | Distinto de `C`. |

El uso de `C=préstamo` es una **decisión candidata explícita de la ISA R0.3**. Permite encadenar `SUB` del byte bajo y `SBC` del alto con el préstamo como entrada.

### Tabla de cambios candidata

| Familia | Z | N | C | V |
| --- | --- | --- | --- | --- |
| `INC` | Resultado cero | Bit 7 | **Conserva** | 1 solo si `0x7F→0x80` |
| `DEC` | Resultado cero | Bit 7 | **Conserva** | 1 solo si `0x80→0x7F` |
| `ADD/ADC` | Resultado cero | Bit 7 | Acarreo de salida | Overflow de suma con signo |
| `SUB/SBC/CMP` | Resultado cero | Bit 7 | Préstamo de salida | Overflow de resta con signo |
| `AND/OR/XOR/NOT` | Resultado cero | Bit 7 | **Conserva** | 0 |
| `SHL/SHR` | Resultado cero | Bit 7 del resultado | Bit expulsado | 0 |
| `PUSH/POP/PUSHX/POPX` | **Conserva** | **Conserva** | **Conserva** | **Conserva** |
| `LDI/MOV/LD/ST/CALL/RET/JMP/Jcc/HALT` | **Conserva** | **Conserva** | **Conserva** | **Conserva** |

Los cálculos internos de direcciones de `SP` y `X` conservan las banderas: utilizan `ADDR_CARRY` privado del datapath propuesto, no la bandera `C` visible para instrucciones.

## 4. INC/DEC en números de ocho bits

Una operación aritmética sobre un registro de 8 bits conserva solamente los ocho bits bajos (aritmética módulo 256):

| Operación | Entrada | Resultado | Z | N | V | C |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `INC` | `0x7F` | `0x80` | 0 | 1 | 1 | Conserva valor anterior |
| `INC` | `0xFF` | `0x00` | 1 | 0 | 0 | Conserva valor anterior |
| `DEC` | `0x80` | `0x7F` | 0 | 0 | 1 | Conserva valor anterior |
| `DEC` | `0x00` | `0xFF` | 0 | 1 | 0 | Conserva valor anterior |
| `DEC` | `0x01` | `0x00` | 1 | 0 | 0 | Conserva valor anterior |

**¿Por qué `INC 0xFF→0x00` no activa necesariamente C?** Porque la ISA *candidata* establece que `INC` **preserva C**. En cambio, `ADD` sí escribiría C según su acarreo. Para un programa, operaciones que parecen sumar uno pueden tener contratos de banderas diferentes.

### Bucle completo del ejemplo R0.3

~~~asm
LDI R0, 3
CONTAR:
    DEC R0
    JNZ CONTAR
HALT
~~~

`LDI` no modifica flags. Cada `DEC` actualiza `Z` y `N/V`, pero mantiene `C`. La secuencia visible sería:

| Iteración | R0 antes | R0 después | Z | ¿JNZ salta? |
| --- | ---: | ---: | ---: | --- |
| 1 | 3 | 2 | 0 | Sí |
| 2 | 2 | 1 | 0 | Sí |
| 3 | 1 | 0 | 1 | No |

El salto [R0.6](CONTROL_FLUJO_PILA_AULA8_BORRADOR.md) lee siempre sus dos bytes de destino. Esto es una **predicción verificable** de la futura CPU, no una ejecución que haya ocurrido hoy.

## 5. Un programa que prueba PUSH, POP y DEC

En el área de programa propuesta `0x6000`:

~~~text
6000: 11 00 2A   LDI R0, 42
6003: 1A 00      PUSH R0
6005: 11 00 00   LDI R0, 0
6008: 1B 00      POP R0
600A: 2A 00      DEC R0
600C: 01         HALT
~~~

Se espera `R0=41` (`0x29`) y `SP=0x8000` tras `HALT`. Como el último paso aritmético es `DEC 42`, el estado final de `Z/N/V` será `0/0/0`; el `C` inicial debe permanecer inalterado durante todo el ejemplo. `RAM[0x7FFF]=0x2A` queda como residuo. El bus efectúa **13 lecturas de bytes de programa, 1 escritura y 1 lectura de pila**: 14 lecturas + 1 escritura = **15 transacciones lógicas**, sin fijar su número de ciclos eléctricos.

El [JSON R0.7](MICRODATOS_PILA_FLAGS_AULA8_R0_7_BORRADOR.json) conserva las rutas lógicas y los bytes, y el verificador coteja la traza declarada con el formato de ISA. No es un intérprete de CPU ni prueba de microcódigo.

## 6. Reglas para los circuitos que todavía faltan

- Para `POP` hay que capturar el dato **antes** de cambiar `MAR` o volver a usar `MDR`.
- Para `PUSH`, preparar `MAR` y `MDR` **antes** de activar `WR`; no pueden conducir datos CPU y memoria a la vez.
- Las operaciones de `SP` de 16 bits no deben alterar `Z/N/C/V`; el carry privado necesita ruta de almacenamiento real.
- En `DEC` e `INC`, el registro destino y `FLAGS` deben capturar un mismo resultado definido; la implementación determinará si ocurre en un paso eléctrico o varios.
- La unidad de control deberá habilitar escritura de flags solo en instrucciones que correspondan; los saltos los **leen**.
- Las sumas/restas de 8 bits deberán verificarse con datos exhaustivos y comprobar signed overflow por separado; el contraste de fórmulas matemáticas no reemplaza un sumador construido.
- El presupuesto de RAM/ROM y la protección de pila no están medidos ni certificados.

**Resultado R0.7:** se puede explicar la pila de datos y el ciclo `DEC→JNZ` de modo compatible con la ISA y las tandas anteriores. **Pendiente:** circuitos, tiempos eléctricos, microcódigo binario, CPU independiente, aprobación de semántica, prueba física y después redacción del libro.
