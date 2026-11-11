# Aula-8 — ABI candidata para funciones de MiniC-Aula (R0.10)

**Estado: PROPUESTA NO APROBADA.** Complementa [ISA R0.3](ISA_AULA8_CANDIDATA.md), [CALL/RET R0.6](CONTROL_FLUJO_PILA_AULA8_BORRADOR.md), [pila R0.7](PILA_Y_BANDERAS_AULA8_BORRADOR.md), [indexación R0.8](DIRECCIONAMIENTO_INDEXADO_AULA8_BORRADOR.md) y [marcos R0.9](AJUSTES_X_SP_Y_MARCOS_AULA8_BORRADOR.md). **ABI** significa *interfaz binaria de aplicación*: normas entre código llamador, llamado, ensamblador y compilador. Este texto es una propuesta propia de Aula-8 y no constituye un estándar de C ni arquitectura física aprobada.

## 1. Contrato que debe conocer MiniC

Sin un convenio, dos funciones correctas por separado pueden destruirse mutuamente: una podría mover SP sin devolverlo, sobrescribir un registro que el llamador aún necesita o buscar su parámetro en una dirección equivocada.

| Asunto | Regla propuesta V1 Aula-8 |
| --- | --- |
| Pila | Desciende; `SP=0x8000` inicial es sentinela **fuera de la RAM**, primera escritura en `0x7FFF` |
| Palabras | Direccionadas por bytes, **little-endian** en memoria |
| Parámetros | Una ranura de **2 bytes por parámetro**, incluso `u8` y `char`; para 8 bits, alto = `00` |
| Orden de argumentos | El llamador coloca argumentos de **derecha a izquierda** |
| Orden de los dos PUSH por ranura | **Primero byte alto, después byte bajo**; la pila descendente deja el bajo en dirección menor |
| Limpieza de parámetros | **El llamador** ejecuta `ADJSP +(2×n)` tras `RET` |
| Retorno `void` | No se interpreta el resultado de R0/R1 |
| Retorno `u8`/`char` | `R0`; alto no tiene contrato |
| Retorno `u16` | `R1:R0` (alto:bajo) |
| Volátiles | `R0`, `R1` y los flags Z/N/C/V; una llamada puede modificarlos |
| Conservados por llamado | `R2`, `R3` y `X`; `SP` recupera su valor salvo limpieza de argumentos pendiente del llamador |
| Parámetros V1 | Máximo **4** por función para mantener desplazamientos sencillos y controlar stack |
| Variables locales | `u8` = 1 byte; `u16` = 2 bytes, bajo primero; reservar con `ADJSP`, no inicializa contenido |

La cantidad de argumentos de cada firma es conocida por el compilador. Un procedimiento declarado con otros tamaños o más de cuatro parámetros requiere ampliación **explícita**, no suponer que hay otro formato.

**Advertencia:** `ADJSP` admite desplazamiento firmado de −128 a +127. Para una reserva o limpieza mayor se requieren varias instrucciones u otro mecanismo; no truncar silenciosamente el tamaño.

## 2. Marco fijo, más fácil de enseñar y compilar

En esta ABI candidata todas las funciones que utilicen el convenio ejecutan, sin omitir pasos:

~~~asm
PROLOGO:
    PUSHX                 ; conserva X del llamador (2 bytes)
    PUSH R2               ; conserva R2 (1 byte)
    PUSH R3               ; conserva R3 (1 byte)
    XFROMSP               ; X = SP: puntero estable del marco
    ADJSP -L              ; L bytes de variables locales, si L > 0
~~~

El valor de `X` queda fijo durante la vida del marco. Al finalizar:

~~~asm
EPILOGO:
    ADJSP +L              ; libera locales, si L > 0
    POP R3                ; restaura R3
    POP R2                ; restaura R2
    POPX                  ; restaura X
    RET                   ; restaura PC y libera dos bytes de retorno
~~~

Los cuatro bytes de guardados (X=2, R2=1, R3=1) hacen que **los offsets sean constantes**, aun si una función no usa R2. Es ineficiente, pero simple y predecible para el primer libro y compilador.

Con `X` definido al terminar los tres PUSH del prólogo, la disposición será:

| Desplazamiento desde X | Contenido |
| --- | --- |
| `X+0` | R3 original |
| `X+1` | R2 original |
| `X+2` | X original, byte bajo |
| `X+3` | X original, byte alto |
| `X+4` | Dirección de retorno, byte bajo |
| `X+5` | Dirección de retorno, byte alto |
| `X+6` | Primer argumento, byte bajo |
| `X+7` | Primer argumento, byte alto |
| `X+8` / `X+9` | Segundo argumento, bajo/alto |
| `X+10` / `X+11` | Tercer argumento |
| `X+12` / `X+13` | Cuarto argumento |
| `X−L .. X−1` | Zona de locales reservada por la función |

Esto **no** describe todos los compiladores C ni el protocolo de servicios de ROM. Se propone para MiniC-Aula, y deberá medirse en R1 contra casos anidados, errores, stack real y llamadas al monitor.

## 3. ¿Por qué se empuja primero el byte alto?

Supongamos que el llamador quiere pasar `0x01FF` en un parámetro de `u16`:

~~~asm
LDI R2, 0x01      ; parte alta
PUSH R2           ; SP: 8000 -> 7FFF, [7FFF] = 01
LDI R3, 0xFF      ; parte baja
PUSH R3           ; SP: 7FFF -> 7FFE, [7FFE] = FF
CALL SUMAR_UNO    ; apila retorno, después entra a la función
ADJSP +2         ; el llamador libera el argumento tras RET
~~~

En memoria el argumento queda correctamente como `FF 01`, porque la CPU es **little-endian**. Si se empujara bajo antes que alto, las direcciones quedarían invertidas.

Con dos argumentos, primero se colocaría el **segundo** completo (alto y bajo) y luego el **primero** completo. Así el primer argumento empieza siempre en `X+6` dentro del llamado.

Para `u8 = 42`, el llamador debe colocar `00` (alto) y `2A` (bajo), en ese orden de PUSH, resultando en memoria `2A 00`. Esto ocupa más RAM pero simplifica las reglas.

## 4. Caso integrado: SUMAR_UNO(u16) devuelve u16

El siguiente programa **no está ejecutado por una CPU**: sus bytes son una especificación contrastable de escritorio. Usa el formato de instrucciones candidato R0.3.

~~~asm
.ORG 0x6000
    SETSP 0x8000
    LDI R2, 0x01        ; argumento 0x01FF, byte alto
    PUSH R2
    LDI R3, 0xFF        ; byte bajo
    PUSH R3
    CALL SUMAR_UNO
    ADJSP +2           ; limpia argumento
    HALT

SUMAR_UNO:
    PUSHX
    PUSH R2
    PUSH R3
    XFROMSP
    ADJSP -2           ; local u16 en X-2 y X-1
    LD R0, [X+6]       ; argumento bajo FF
    LD R1, [X+7]       ; argumento alto 01
    LDI R2, 1
    ADD R0, R2         ; FF+01 = 00, C=1
    LDI R2, 0          ; NO modifica C
    ADC R1, R2         ; 01+00+1 = 02
    ST [X-2], R0
    ST [X-1], R1
    LD R0, [X-2]
    LD R1, [X-1]
    ADJSP +2
    POP R3
    POP R2
    POPX
    RET
~~~

| Dirección | Bytes | Significado |
| --- | --- | --- |
| `6000` | `17 00 80` | SETSP |
| `6003` | `11 02 01` | LDI R2,1 |
| `6006` | `1A 02` | PUSH R2 |
| `6008` | `11 03 FF` | LDI R3,FF |
| `600B` | `1A 03` | PUSH R3 |
| `600D` | `35 13 60` | CALL 0x6013 |
| `6010` | `18 02` | ADJSP +2 |
| `6012` | `01` | HALT |
| `6013` | `1C` | PUSHX |
| `6014` | `1A 02` | PUSH R2 |
| `6016` | `1A 03` | PUSH R3 |
| `6018` | `19` | XFROMSP |
| `6019` | `18 FE` | ADJSP −2 |
| `601B` | `12 04 06` | LD R0,[X+6] |
| `601E` | `12 05 07` | LD R1,[X+7] |
| `6021` | `11 02 01` | LDI R2,1 |
| `6024` | `20 02` | ADD R0,R2 |
| `6026` | `11 02 00` | LDI R2,0 |
| `6029` | `21 06` | ADC R1,R2 |
| `602B` | `13 04 FE` | ST [X−2],R0 |
| `602E` | `13 05 FF` | ST [X−1],R1 |
| `6031` | `12 04 FE` | LD R0,[X−2] |
| `6034` | `12 05 FF` | LD R1,[X−1] |
| `6037` | `18 02` | ADJSP +2 |
| `6039` | `1B 03` | POP R3 |
| `603B` | `1B 02` | POP R2 |
| `603D` | `1D` | POPX |
| `603E` | `02` | RET |

### En el punto más profundo de la pila

Inicialmente X era `0x6F00`. Tras los parámetros, CALL y el prólogo, el puntero de marco es `X=0x7FF8` y el de pila `SP=0x7FF6`.

| Dirección | Valor después de guardar el local | Función |
| --- | --- | --- |
| `7FF6` | `00` | Local u16, bajo |
| `7FF7` | `02` | Local u16, alto |
| `7FF8` | `FF` | R3 preservado |
| `7FF9` | `01` | R2 preservado |
| `7FFA` | `00` | X anterior, bajo |
| `7FFB` | `6F` | X anterior, alto |
| `7FFC` | `10` | Retorno a `6010`, bajo |
| `7FFD` | `60` | Retorno, alto |
| `7FFE` | `FF` | Argumento u16, bajo |
| `7FFF` | `01` | Argumento u16, alto |

Después de RET, el llamador continúa en `0x6010`, limpia dos bytes y llega a HALT. El estado esperado es:

- `R1:R0=0x0200` (512), porque `0x01FF + 1 = 0x0200`.
- `R2=0x01`, `R3=0xFF` y `X=0x6F00` restaurados; `SP=0x8000`.
- `PC=0x6013` después de consumir el byte HALT.
- Banderas finales `Z=0, N=0, C=0, V=0`, resultado de `ADC` (las operaciones de movimiento/pila no tocan FLAGS). Las llamadas **no** garantizan conservar flags del llamador.
- La RAM retiene los diez bytes residuales de las posiciones indicadas. Liberar pila **no borra** RAM.

El programa ocupa **63 bytes de instrucciones**. La traza prevista tiene **73 lecturas** (63 bytes de código + 10 lecturas de datos) y **10 escrituras** (dos argumentos, dos bytes de retorno, cuatro bytes de registros preservados y dos de local): **83 transacciones externas**.

## 5. Recursividad y presupuesto de pila

La recursión no requiere un «registro mágico»: cada `CALL` apila su propio retorno, cada prólogo sus cuatro bytes conservados, y las variables locales y parámetros se reservan en su propia región.

Para una función de **un argumento u16** y **dos bytes locales**, cada nivel simultáneo puede demandar al menos:

`2 (argumento) + 2 (retorno) + 4 (registros conservados) + 2 (locales) = 10 bytes`.

En los 4096 bytes propuestos de `0x7000–0x7FFF`, el límite **matemático idealizado** es `floor(4096/10)=409` niveles, sin contar otros usos de pila, monitor, interrupciones, temporales, llamadas auxiliares ni reservas existentes. **No** debe anunciarse como profundidad segura; el runtime deberá imponer márgenes y detectar desbordamientos.

Un compilador puede necesitar reutilizar `X` temporalmente para arreglos. Antes de cambiarlo debe **guardar X y recuperarlo** sin perder el marco y evitando accesos a parámetros durante el periodo en que X esté prestado. Esta interacción deberá probarse antes de compilar expresiones complejas.

## 6. Lo que sigue pendiente

1. Confirmar o corregir este ABI candidata según las restricciones reales de circuitos, MiniC y ROM.
2. Diseñar un intérprete de referencia ISA independiente y comparar sus instrucciones con un microcontrol digital real cuando existan.
3. Especificar funciones con varios parámetros, llamadas anidadas y recursivas con pruebas que no corrompan memoria.
4. Diseñar entradas de ROM compatibles: **no** asumir que los servicios públicos de firmware usen automáticamente esta misma ABI.
5. Definir manejo de fallos al exceder pila, código reentrante y depuración del monitor; no existe hardware de protección.
6. Establecer posteriormente reglas propias de Aula-16; **su bus externo continúa siendo de 16 bits**.

**Verificación R0.10:** el [contrato JSON](ABI_MINIC_AULA8_R0_10_BORRADOR.json) y un verificador compararán offsets de pila, fórmulas de retorno y codificación del ejemplo. Esto **no** genera firmware, CPU, compilador MiniC ni simulador JavaFX.
