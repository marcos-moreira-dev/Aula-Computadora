# Aula-8 — ajustes de X y SP, palabras y marcos de pila (R0.9)

**Estado: PROPUESTA NO APROBADA.** Este documento extiende la [ISA R0.3](ISA_AULA8_CANDIDATA.md), el [CALL/RET de R0.6](CONTROL_FLUJO_PILA_AULA8_BORRADOR.md), la [pila de R0.7](PILA_Y_BANDERAS_AULA8_BORRADOR.md) y los [accesos indexados R0.8](DIRECCIONAMIENTO_INDEXADO_AULA8_BORRADOR.md). Describe transferencias lógicas, no microcódigo binario, ciclos o una CPU construida.

## 1. Cinco instrucciones, sin añadir opcodes

| Opcode hexadecimal | Instrucción | Bytes | Efecto candidato | Flags |
| --- | --- | ---: | --- | --- |
| `15` | `LEAX d` | 2 | `X ← (X + sign8(d)) mod 65536` | Intactos |
| `16` | `ADDXW` | 1 | `X ← (X + (R1:R0)) mod 65536` | Intactos |
| `17` | `SETSP imm16` | 3 | `SP ← imm16` little-endian | Intactos |
| `18` | `ADJSP d` | 2 | `SP ← (SP + sign8(d)) mod 65536` | Intactos |
| `19` | `XFROMSP` | 1 | `X ← SP` | Intactos |

`R1:R0` significa byte alto de la palabra en `R1` y byte bajo en `R0`. Todas las instrucciones utilizan opcodes y formatos **ya reservados en R0.3**; aquí se refina su secuenciación sin congelar la ISA.

¿Por qué son útiles? `LEAX` recorre arreglos de elementos consecutivos; `ADDXW` añade un índice variable de 16 bits; `ADJSP` reserva/libera espacio sin escribirlo; `XFROMSP` permite que `X` apunte a un marco mientras `SP` cambia.

## 2. Una ALU8 calcula sumas de dieciséis bits

Para sumar `A16 + B16` sin ocultar una ALU de 16 bits:

1. Capturar las fuentes **antes** de sobrescribir X o SP, cuando se reutilicen buses y latches.
2. `s0 ← A_low + B_low`, guardar `RESULT_LO = s0 & 0xFF` y `ADDR_CARRY = s0 >> 8`.
3. `s1 ← A_high + B_high + ADDR_CARRY`, guardar `RESULT_HI = s1 & 0xFF`.
4. En un instante de compromiso lógico, escribir ambos bytes de la base destino; descartar acarreo más allá del bit 15.
5. Preservar `Z/N/C/V` visibles. El acarreo `ADDR_CARRY` es **interno** y no es la bandera C.

`LEAX` y `ADJSP` extienden el signo del `disp8` antes de sumar. Ejemplo: `0x1200 + 0xFF` no significa sumar 255, sino sumar `−1`, representado como `0xFFFF`; el resultado es `0x11FF`.

`ADDXW` suma una **palabra sin signo de 16 bits** procedente de `R1:R0`. Con `X=0x12FF`, `R1=0x01`, `R0=0x02`, el cálculo produce `0x1401`. Con `X=0xFFFF` y `R1:R0=0x0001` produce `0x0000` por desbordamiento modular.

| Caso | Antes | Operación | Después | Observación |
| --- | --- | --- | --- | --- |
| Cruce de byte | X=`12FF` | `LEAX +2` | X=`1301` | Acarreo privado |
| Retroceso | X=`1200` | `LEAX −1` | X=`11FF` | Extensión de signo |
| Rollover | X=`FFFF` | `LEAX +1` | X=`0000` | Módulo 65536 |
| Pila | SP=`8000` | `ADJSP −1` | SP=`7FFF` | Solo cambia puntero |
| Marco | SP=`7FFC` | `XFROMSP` | X=`7FFC` | No toca la RAM |

La aritmética modular por sí misma **no asegura acceso válido**. `ADJSP +1` con SP=`0x8000` daría `0x8001` matemáticamente, pero no es una reserva de pila segura en el mapa inicial. El monitor/taller podría detectar desbordamientos; **no existe protección hardware probada**.

## 3. Propuesta de microacciones

El fetch común [R0.5](UNIDAD_CONTROL_AULA8_BORRADOR.md) ya consumió un byte de opcode. Para `LEAX` y `ADJSP` se lee **un byte adicional** de desplazamiento; `SETSP` lee **dos bytes** en orden bajo, alto. `ADDXW` y `XFROMSP` no consumen operandos.

| Instrucción | Microacciones posteriores al fetch (granularidad lógica) |
| --- | --- |
| `LEAX` | Leer d8; signar; conservar X y d; sumar bajo + acarreo; sumar alto; comprometer nuevo X; fetch |
| `ADJSP` | Leer d8; signar; conservar SP y d; sumar bajo + acarreo; sumar alto; comprometer nuevo SP; fetch |
| `ADDXW` | Conservar X y R1:R0; sumar bajos; sumar altos con acarreo; comprometer X; fetch |
| `SETSP` | Leer inmediato bajo; leer inmediato alto; cargar SP; fetch |
| `XFROMSP` | Capturar SP16; cargar X16; fetch |

Las fuentes pueden necesitar temporales `ADDR_LO/HI` o equivalentes, pero **no** están asignados a componentes físicos exclusivos ni se han calculado conflictos de latches. El [JSON R0.9](MICROAJUSTES_AULA8_R0_9_BORRADOR.json) registra las acciones propuestas sin afirmar que una acción equivalga a un ciclo.

## 4. Una llamada real necesita un marco legible

En RAM inicial `0x0000–0x7FFF` el SP candidato comienza en `0x8000` como **sentinela de primera posición libre**, no como dirección RAM escribible. Para la siguiente función suponemos `X=0x6F00` y flags sin modificar.

~~~asm
.ORG 0x6000
    SETSP 0x8000
    CALL FUN
    HALT
FUN:
    PUSHX              ; salvar X del llamador, SP=0x7FFC
    XFROMSP            ; X=0x7FFC: referencia estable del marco
    ADJSP -1           ; reservar un byte local, SP=0x7FFB
    LDI R0, 42
    ST [SP+0], R0      ; guardar byte local en 0x7FFB
    LD R1, [SP+0]      ; recuperar 42
    ADJSP +1           ; liberar local: SP=0x7FFC
    POPX               ; restituye X anterior, SP=0x7FFE
    RET                ; restituye PC=0x6006, SP=0x8000
~~~

| Dirección | Bytes | Función |
| --- | --- | --- |
| `6000` | `17 00 80` | SETSP |
| `6003` | `35 07 60` | CALL 0x6007 |
| `6006` | `01` | HALT |
| `6007` | `1C` | PUSHX |
| `6008` | `19` | XFROMSP |
| `6009` | `18 FF` | ADJSP −1 |
| `600B` | `11 00 2A` | LDI R0, 42 |
| `600E` | `13 08 00` | ST [SP+0], R0 |
| `6011` | `12 09 00` | LD R1, [SP+0] |
| `6014` | `18 01` | ADJSP +1 |
| `6016` | `1D` | POPX |
| `6017` | `02` | RET |

### Mapa de pila en el punto más profundo

Después de `ADJSP −1`, con X=`7FFC` y SP=`7FFB`:

| Dirección | Valor tras ST | Dueño semántico |
| --- | --- | --- |
| `7FFB` | `2A` | Variable local de 1 byte |
| `7FFC` | `00` | X anterior, byte bajo |
| `7FFD` | `6F` | X anterior, byte alto |
| `7FFE` | `06` | Retorno, byte bajo |
| `7FFF` | `60` | Retorno, byte alto |

Este ejemplo usa una **disposición de marco ilustrativa**, no una ABI universal. Una función que reserve dos bytes o pase parámetros necesitará reglas adicionales; no fijar desplazamientos de parámetros por analogía.

Si la instrucción `HALT` consume su opcode, al terminar se esperan `PC=0x6007`, `SP=0x8000`, `X=0x6F00`, `R0=R1=42` y banderas intactas. El contenido de las cinco celdas de pila permanece como **residuo**. El recuento de bus externo esperado es **29 lecturas** (24 bytes de instrucciones + 2 retornos + 2 X salvado + 1 local) y **5 escrituras** (2 retorno + 2 X + 1 local).

No se presupone reloj ni protección del bus; el recuento es una **traza de escritorio**. La función no ha sido ejecutada por un procesador implementado.

## 5. Límites y preguntas para R1

- Determinar una ABI definitiva: registros salvados, bytes de locales, parámetros, retorno, marco fijo, alineación y recursividad.
- Decidir si `ADJSP` debe quedar restringida a región de pila mediante comprobación de software, hardware opcional o ambos; por ahora es aritmética modular.
- Diseñar latches y señales concretas para conservar las fuentes durante dos pasadas, retener el acarreo, bloquear escritura parcial ante fallo y cargar los dos bytes de X/SP.
- Verificar si `SETSP` se permite sin privilegios: hoy es propuesta pedagógica, no un mecanismo seguro para usuarios.
- Comprobar qué sucede al interrumpir una microsecuencia antes de comprometer el destino; por ahora no hay interrupciones V1.
- Medir tamaño de control ROM, rendimiento y electrónica antes de afirmar viabilidad física.

**Resultado documental:** ya podemos razonar sobre una función con variable local y retorno correcto manteniendo un datapath8. **No** se ha aprobado la ISA ni implementado CPU, compilador, firmware, JavaFX o montaje físico.

**Continuación documental R0.10:** el [borrador de ABI MiniC-Aula8](ABI_MINIC_AULA8_R0_10_BORRADOR.md) propone un prólogo fijo que además conserva R2/R3 y define offsets de parámetros y retornos. No asumir que el ejemplo didáctico R0.9, sin esos guardados, sea la convención definitiva del compilador.
