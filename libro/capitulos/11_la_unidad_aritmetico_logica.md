# Capítulo 11. La unidad aritmético-lógica

*Parte III · Memoria, buses y aritmética · Aula-Computadora*

En el capítulo anterior construimos, sobre el papel, un circuito que suma dos bytes propagando el acarreo de derecha a izquierda. Pero una computadora necesita más que sumar: debe **restar**, averiguar qué número es mayor, comprobar si un bit está encendido y decidir qué resultado entregar. ¿Tenemos que fabricar un circuito aritmético diferente para cada operación? No necesariamente. Un mismo sumador puede servir para sumar y restar; otras compuertas trabajan bit a bit; y un **multiplexor** elige cuál de los resultados pasa a la salida. Esa combinación funcional es una **unidad aritmético-lógica**, o **ALU**.

Construiremos la idea para operandos de ocho bits, con el diseño **candidato** de Aula-8 como contexto. Aprenderemos a distinguir el noveno bit interno del sumador de la bandera de préstamo, y a comparar los mismos ocho bits como números con signo o sin él. Estos diagramas son modelos didácticos, no esquemas eléctricos aprobados ni instrucciones ejecutadas por una CPU construida.

## 1. Restar también puede ser sumar

Pensemos primero en una resta conocida: `13 − 9 = 4`. Un circuito digital reconoce bits y operaciones lógicas, no el símbolo escolar de «quitar». La clave es representar el negativo de `9` en **complemento a dos**: invertir los ocho bits de `9` y sumar una unidad. El procedimiento da un patrón que, sumado a 13 y conservando ocho bits, equivale a restar 9.

[[EQ:A − B ≡ A + (¬B) + 1  (módulo 256)]]

La negación `¬B` invierte **cada uno de los ocho bits**: donde había `0` escribe `1` y viceversa. No significa negar una proposición única ni cambiar solamente el bit más alto. Como `9 = 00001001₂`, su inversión en ocho bits es `11110110₂`; al sumar `1` aparece `11110111₂`, que representa `−9` si lo leemos con signo. Es el mismo patrón que **247 sin signo**: los bits solos no imponen una interpretación.

[[EQ:9 = 00001001₂  →  ¬9 = 11110110₂]]

[[EQ:11110110₂ + 1₂ = 11110111₂ = 0xF7]]

Un diseño habitual introduce una señal de control `SUB`: con `SUB=0` deja pasar B y pone el acarreo inicial a cero; con `SUB=1` invierte B mediante XOR y pone el acarreo inicial a uno. De este modo reutiliza un **sumador de ocho bits**. Es una arquitectura posible, no una asignación física de pines de Aula-8.

Llamemos `m` a esa señal en la fórmula siguiente: es un bit que vale cero en ADD y uno en SUB. Así evitamos confundir el nombre de una instrucción con una entrada eléctrica.

[[EQ:B' = B ⊕ (m repetido en 8 bits) ; Cin = m]]

[[FIG:c11_fig01_resta_complemento_dos|Figura 1. Un banco de XOR condicionales y el acarreo inicial permiten usar un sumador para ADD o SUB. El acarreo final interno se invierte para producir préstamo en SUB.|Entradas A y B de ocho bits; B pasa por ocho XOR controladas por SUB; el sumador recibe Cin igual a SUB; salida S de ocho bits y Cout interno; un bloque lógico invierte Cout para la bandera préstamo durante resta.]]

## 2. Hacer 13 − 9 con todas sus columnas visibles

Escribimos ambos operandos con ocho posiciones, alineando unidades con unidades y centenas binarias con centenas binarias. Seguimos los acarreos internos exactamente como en el capítulo 10: empezamos en el **bit 0, a la derecha**. La suma usa `A=00001101₂`, `¬B=11110110₂` y `Cin=1`.

| Posición i | Ai | (¬B)i | Cin | Si | Cout |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | 1 |
| 1 | 0 | 1 | 1 | 0 | 1 |
| 2 | 1 | 1 | 1 | 1 | 1 |
| 3 | 1 | 0 | 1 | 0 | 1 |
| 4 | 0 | 1 | 1 | 0 | 1 |
| 5 | 0 | 1 | 1 | 0 | 1 |
| 6 | 0 | 1 | 1 | 0 | 1 |
| 7 | 0 | 1 | 1 | 0 | 1 |

El byte `S7...S0`, leído ahora de **izquierda a derecha**, es `00000100₂`, equivalente a `4`. El acarreo de salida más allá del bit 7 vale uno. Mostrando también ese noveno bit, la cuenta queda así:

[[EQ:00001101₂ + 11110111₂ = 1 00000100₂]]

[[EQ:13 − 9 = 4 ; S = 0x04 ; Cout interno = 1]]

¡Atención!: en una resta implementada como suma con complemento a dos, **`Cout interno = 1` significa que no hubo préstamo sin signo**. La propuesta actual de Aula-8 llama `C` al **préstamo** en la resta; por eso, para `SUB` se obtiene `C=0` a partir de `1 − Cout interno`. Este `C` de la ISA candidata **no es el mismo sentido de C que en ADD**.

[[EQ:C en SUB = préstamo = 1 − Cout interno]]

Para `13−9`: `Z=0` porque la salida no es cero; `N=0` porque su bit 7 vale cero; `V=0` porque `4` cabe en el rango firmado. El par de números también puede tratarse sin signo: no se pidió un valor que no exista en ese rango.

## 3. Cuando el minuendo es menor: 9 − 13

Ahora el resultado matemático es `−4`. El complemento de `13=00001101₂` es `11110010₂`; sumar la unidad inicial genera `11110011₂`. Al sumar `9` obtenemos **solo ocho bits de resultado** `11111100₂`, o `0xFC`.

[[EQ:00001001₂ + 11110010₂ + 1₂ = 0 11111100₂]]

[[EQ:0xFC = 252 sin signo = −4 en complemento a dos]]

El bit que sale del sumador es `0`: hubo **préstamo sin signo**, de modo que `C=1` según la convención candidata. El bit más alto del resultado es `1`, por tanto `N=1`; `Z=0`. En números firmados `9−13=−4` **sí cabe** en `−128...127`, de modo que `V=0`.

No hay que escribir que `9−13=252` como si fuera una igualdad entre números enteros habituales. La igualdad verdadera es **entre sus patrones de ocho bits**: `−4` y `252` tienen el mismo patrón si cambiamos la regla de interpretación. El resultado no dice por sí solo cuál pretendía el programa.

## 4. Las cuatro banderas no contestan la misma pregunta

En el modelo de Aula-8 que estamos estudiando, el resultado de ocho bits se resume mediante **Z**, **N**, **C** y **V**. Conviene mirar cada una como una pregunta distinta, no como cuatro palabras para decir «resultado incorrecto».

| Bandera | Pregunta que contesta | En ADD | En SUB / comparación |
| --- | --- | --- | --- |
| **Z** | ¿Los ocho bits de salida son cero? | `1` si S=0 | `1` si S=0 |
| **N** | ¿El bit 7 de la salida vale uno? | `N=S7` | `N=S7` |
| **C** | ¿Se produjo una condición sin signo? | Acarreo final | **Préstamo** (`1−Cout`) |
| **V** | ¿La cuenta con signo excedió el rango? | Overflow firmado de suma | Overflow firmado de resta |

[[EQ:Z = 1 si S = 00000000₂ ; N = S7]]

El desbordamiento **con signo** al restar se detecta cuando A y B tienen signos distintos y el resultado tiene signo distinto de A. Una expresión booleana de ocho bits usa las XOR en el bit más alto:

[[EQ:V_SUB = bit7((A ⊕ B) ∧ (A ⊕ S))]]

Por ejemplo, `0x80` significa `−128` con signo. Si restamos `0x01` (uno positivo), la respuesta matemática `−129` **no cabe** en ocho bits con signo. La operación devuelve `0x7F`, que se leería erróneamente como `+127` si olvidáramos `V=1`. En esta cuenta `C=0` (sin préstamo sin signo), `Z=0`, `N=0` y `V=1`.

[[EQ:0x80 − 0x01 = 0x7F  (8 bits) ; V = 1]]

| Resta de 8 bits | S | C préstamo | V | Z | N |
| --- | --- | --- | --- | --- | --- |
| `13 − 9` | `0x04` | 0 | 0 | 0 | 0 |
| `9 − 13` | `0xFC` | 1 | 0 | 0 | 1 |
| `0x80 − 0x01` | `0x7F` | 0 | 1 | 0 | 0 |
| `0x2A − 0x2A` | `0x00` | 0 | 0 | 1 | 0 |

Estas banderas describen operaciones aritméticas de nuestro modelo. **Todavía no hemos especificado qué banderas modificarán las operaciones AND, OR, XOR y NOT**; elegir esa política corresponde a una decisión posterior de arquitectura y no debe inventarse silenciosamente.

## 5. Las operaciones lógicas atienden a cada posición por separado

La aritmética necesita transportar acarreos entre columnas; la lógica bit a bit, en cambio, aplica una misma tabla de verdad a cada posición **sin comunicarla con la vecina**. Usemos dos bytes visualmente distinguibles: `A=0x5A=01011010₂` y `B=0x3C=00111100₂`.

**AND** produce `1` si ambos bits de esa columna son `1`; sirve para consultar máscaras. **OR** produce `1` si al menos uno vale `1` y sirve para activar bits determinados.

**XOR** produce `1` si los bits son distintos y permite alternar los seleccionados. **NOT** invierte todos los bits de un operando; no necesita B.

[[EQ:A AND B = 00011000₂ = 0x18]]

[[EQ:A OR B = 01111110₂ = 0x7E]]

[[EQ:A XOR B = 01100110₂ = 0x66]]

[[EQ:NOT A = 10100101₂ = 0xA5]]

[[FIG:c11_fig03_logica_por_bits|Figura 2. Los ocho bits de A y B se alinean para realizar AND, OR, XOR y NOT sin acarreo entre columnas.|Tabla visual de A igual 01011010 y B igual 00111100, con resultados AND 00011000, OR 01111110, XOR 01100110 y NOT A 10100101. Cada columna se calcula independientemente.]]

Una máscara da contexto. Si `registro=10110110₂` y deseamos comprobar si está activo el bit de peso `2²=4`, usamos `00000100₂`. El resultado de `registro AND 00000100₂` es `00000100₂`, distinto de cero: **ese bit estaba activo**. Si deseáramos apagarlo, usaríamos `registro AND NOT 00000100₂`.

[[EQ:10110110₂ AND 00000100₂ = 00000100₂]]

Las palabras AND y OR también se usan para decisiones booleanas de programas, pero aquí trabajan sobre **ocho pares de bits**. Confundir una condición verdadera/falsa con una máscara de ocho posiciones equivale a perder información: ambas ideas se relacionan, pero no son la misma operación.

## 6. Comparar es restar sin necesitar guardar la diferencia

Supongamos que un programa pregunta si `A` es menor que `B`. Una solución práctica es hacer internamente `A−B` y mirar ciertas banderas. La operación de **comparación** podría usar el mismo circuito de resta pero **sin escribir el byte calculado en el registro destino**. Esto describe un comportamiento lógico candidato, no congela un opcode `CMP` en Aula-8.

Para números **sin signo**, `A < B` exactamente cuando la resta necesita préstamo (`C=1`). Si la resta da cero (`Z=1`), ambos operandos son iguales. Si no hay préstamo ni igualdad, A es mayor.

[[EQ:A < B sin signo ⇔ C_préstamo = 1]]

[[EQ:A = B ⇔ Z = 1 ; A > B sin signo ⇔ C = 0 y Z = 0]]

Para números **con signo**, la bandera N por sí sola no basta: una resta puede desbordarse y cambiar de signo aparente. La corrección utiliza `N XOR V`. La igualdad se sigue indicando con Z.

[[EQ:A < B con signo ⇔ N ⊕ V = 1]]

[[EQ:A > B con signo ⇔ Z = 0 y (N ⊕ V) = 0]]

Comprobémoslo con `A=0xFF` y `B=0x01`. Los **mismos ocho bits** de A significan **255 sin signo** o **−1 con signo**. La resta interna `FF−01=FE` da `C=0`, `Z=0`, `N=1`, `V=0`: sin signo, 255 es mayor que 1; con signo, −1 es menor que +1. La circuitería no cambia, **cambia la condición que interpreta sus banderas**.

[[FIG:c11_fig04_comparaciones_banderas|Figura 3. Una misma resta 0xFF − 0x01 produce banderas que permiten comparar de manera diferente valores con signo y sin signo.|Dos paneles: comparación sin signo 255 mayor que 1 porque C préstamo vale 0 y Z vale 0; comparación con signo menos 1 menor que más 1 porque N XOR V vale 1. Patrón de resta interna FE en ambos casos.]]

## 7. Reunir los resultados en una ALU

Hasta ahora hemos mostrado circuitos o funciones que podrían existir a la vez: la ruta del sumador para ADD/SUB, las compuertas AND/OR/XOR/NOT, y la lógica que calcula banderas. Pero si seis resultados aparecieran simultáneamente en cables separados, ¿cuál recibiría el registro de destino? Necesitamos **seleccionar exactamente uno**.

Un **multiplexor**, estudiado en la selección de registros del capítulo 7, se comporta como un selector digital: recibe varias fuentes y unas señales de control; conecta una fuente a una salida lógica. Con ocho bits hay ocho elecciones coordinadas, una para cada posición del byte. No significa unir físicamente las salidas de distintas compuertas en el mismo conductor.

[[FIG:c11_fig02_alu_selector|Figura 4. Una ALU ilustrativa calcula en paralelo aritmética y lógica y elige una ruta mediante selección de operación; las banderas siguen un tratamiento separado.|Entradas A y B de ocho bits alimentan bloque ADD SUB y bloque AND OR XOR NOT; un multiplexor comandado por operación selecciona un byte S; se muestra por separado la lógica Z N C V y la advertencia de que las reglas de flags lógicas están pendientes.]]

| Operación conceptual | Qué calcula | ¿Usa acarreo entre bits? |
| --- | --- | --- |
| ADD | `A+B` módulo 256 | Sí |
| SUB | `A−B` módulo 256 | Sí, por el sumador |
| CMP | Banderas de `A−B`, sin guardar S | Sí, por el sumador |
| AND | `Ai AND Bi` para cada i | No |
| OR | `Ai OR Bi` para cada i | No |
| XOR | `Ai XOR Bi` para cada i | No |
| NOT | `NOT Ai` para cada i | No |

En chips reales hay piezas que materializan porciones de este razonamiento: un **CD74HC283** (Texas Instruments) es un sumador binario completo de cuatro bits; un **SN74HC86** ofrece cuatro XOR de dos entradas; un **SN74HC157** selecciona, por cada uno de cuatro canales, entre dos fuentes de datos. Estos componentes ilustran funciones reutilizables, pero **no forman por sí solos una ALU de ocho bits lista para conectar**. Harían falta selección, tratamiento de flags, control de escritura y decisiones de temporización, junto con una revisión eléctrica completa.

## 8. Qué resuelve la ALU y qué deja pendiente

La ALU **calcula**, pero por sí sola no decide qué instrucción se ejecuta, de qué registro proviene un operando ni en qué memoria se guarda el resultado. Esas responsabilidades corresponden a rutas de datos, registros y unidad de control que conoceremos más adelante. Tampoco fija un lenguaje de programación: un programa puede interpretar el patrón `11111100` como byte 252, entero firmado −4, máscara o dato codificado según su contrato.

**Límite del ejemplo.** Hemos concretado matemáticamente el significado de Z, N, C y V para ADD/SUB y las comparaciones derivadas. La política de actualización de flags al ejecutar funciones lógicas, las instrucciones definitivas, sus códigos binarios, la velocidad del circuito y su montaje real permanecen por decidir o validar. Una prueba exhaustiva de fórmulas no sustituye las mediciones sobre un circuito.

## Construimos Aula-8: elegir la operación antes de escribir

El sumador anterior solo sabe sumar. La ALU permite seleccionar, por señales de control, entre varias funciones que reciben los mismos operandos. Una señal de selección apropiada puede elegir suma, resta o lógica por bits; un multiplexor entrega **un resultado seleccionado**, no todos los resultados mezclados en la misma línea. Después, el registro de destino solo debe capturarlo cuando llegue su orden de carga.

Sigamos una operación concreta: R0=`0x0D`, R1=`0x09`, selección `ADD`. La ruta combinacional produce `0x16`; si la captura se autoriza en el momento correcto, R0 cambia a `0x16`. Los flags describen hechos sobre ese resultado según el contrato candidato; no debemos suponer que una mera modificación de R0 actualiza automáticamente todos los flags. El capítulo 12 colocará esta ruta dentro de la CPU. Lo que tenemos aquí es una **especificación lógica de ALU**, no un listado definitivo de integrados y cables.

## Ejercicios del capítulo 11

Resuelve primero sobre papel, indicando **ocho bits** y, cuando corresponda, la columna de acarreo inicial/final. En resta, recuerda que **C es préstamo** para la propuesta candidata de Aula-8. Cada respuesta está desarrollada en el solucionario.

**Ejercicio 1 — Complemento.** Escribe `9` en ocho bits; invierte todos sus bits y suma una unidad. Indica la escritura hexadecimal final.

**Ejercicio 2 — Resta positiva.** Resuelve `13−9` con `A+¬B+1`. Explica qué ocurre con el noveno bit y calcula C, Z, N, V.

**Ejercicio 3 — Resta negativa.** Resuelve `9−13`, escribe S en hexadecimal e interprétalo con signo y sin signo.

**Ejercicio 4 — Préstamo frente a acarreo.** Si el sumador interno de SUB termina con `Cout=1`, ¿qué valor recibe la bandera C de préstamo? Explica por qué.

**Ejercicio 5 — Desbordamiento firmado.** Resuelve `0x80−0x01` en ocho bits y calcula las cuatro banderas.

**Ejercicio 6 — Diferencia nula.** Determina `0x2A−0x2A`, todas las banderas y el resultado de una comparación de igualdad.

**Ejercicio 7 — Máscara AND.** Calcula `0x5A AND 0x3C` alineando ocho columnas y traduce el resultado a hexadecimal.

**Ejercicio 8 — OR y XOR.** Calcula `0x5A OR 0x3C` y `0x5A XOR 0x3C`; explica por qué no llevan acarreos.

**Ejercicio 9 — NOT de un byte.** Invierte `0x5A` en **ocho** bits. ¿Por qué es importante indicar la anchura?

**Ejercicio 10 — Comparación sin signo.** Con `A=0xFF`, `B=0x01`, calcula la resta interna y decide `A<B`, `A=B` o `A>B` **sin signo**.

**Ejercicio 11 — Comparación firmada.** Usa exactamente los mismos patrones del ejercicio 10, pero con signo. Muestra `N XOR V` y explica el cambio de conclusión.

**Ejercicio 12 — Diseño de ALU.** Describe qué bloque selecciona el resultado de ADD, AND o XOR hacia un único bus; distingue ese selector del control de escritura de registro e indica una decisión de flags que sigue pendiente.

## Solucionario del capítulo 11

**1.** `9=00001001₂`, inversión `11110110₂`, más uno `11110111₂ = 0xF7`. Este patrón representa 247 sin signo o −9 con signo.

**2.** `A=00001101`, `¬B=11110110`, `Cin=1`; suma completa `1 00000100₂`. Sale S=`00000100₂`, `Cout=1`, de modo que **C préstamo=0**. `Z=0`, `N=0`, `V=0`. Resultado decimal `4`.

**3.** `9=00001001`, `¬13=11110010`; con `Cin=1`, suma `0 11111100₂`. S=`0xFC`, C préstamo=`1`, Z=`0`, N=`1`, V=`0`; el patrón es 252 sin signo o −4 con signo.

**4.** C préstamo=`1−Cout=1−1=0`. El acarreo final de la suma complementada indica **ausencia** de préstamo; no se copia directamente a la bandera de préstamo.

**5.** `0x80−0x01=0x7F` módulo 256. `C=0`, `V=1`, `Z=0`, `N=0`. La cuenta firmada −128−1=−129 no cabe y se convierte en patrón `0x7F`.

**6.** `0x2A−0x2A=0x00`, `Cout=1`, por tanto `C=0`, `V=0`, `Z=1`, `N=0`. Como Z vale uno, son iguales.

**7.** `01011010 AND 00111100 = 00011000₂ = 0x18`. Solo permanecen las posiciones donde ambos operandos tenían uno.

**8.** OR=`01111110₂=0x7E`; XOR=`01100110₂=0x66`. No hay acarreo: cada columna aplica una función booleana independiente.

**9.** `NOT 01011010₂ = 10100101₂ = 0xA5`. Debemos indicar ocho bits porque invertir un patrón de 16 bits produciría `11111111 10100101₂`, un número diferente.

**10.** `FF−01=FE` en ocho bits; `C=0`, `Z=0`, `N=1`, `V=0`. Sin signo, A=255 y B=1, por tanto **A>B** porque no hay préstamo ni igualdad.

**11.** Con signo, `FF=−1` y `01=+1`; `N XOR V=1 XOR 0=1`, así que **A<B**. No se cambiaron los bits: se aplicó una condición de comparación distinta.

**12.** Un **multiplexor de ocho bits** elige una de las salidas de ADD/AND/XOR. Otra señal de control autoriza o impide que el registro destino capture el byte; no son la misma responsabilidad. Queda pendiente decidir si las operaciones lógicas conservan, borran o recalculan cada bandera.

## Para continuar

Ya sabemos **qué calcula** una ALU y cómo puede compartir un sumador entre suma y resta. Aprendimos a leer sus banderas sin confundir acarreo, préstamo y desbordamiento firmado, y vimos por qué una comparación cambia según el signo atribuido a los mismos bytes. En el capítulo 12 reuniremos ALU, registros, PC, SP y buses dentro de una **arquitectura Aula-8** coherente, todavía candidata hasta recibir especificación y pruebas.

Fuentes primarias: Texas Instruments, *CD74HC283 High-Speed CMOS Logic 4-Bit Binary Full Adder with Fast Carry*, https://www.ti.com/lit/ds/symlink/cd74hc283.pdf; Texas Instruments, *SNx4HC86 Quadruple 2-Input XOR Gates*, https://www.ti.com/lit/ds/symlink/sn74hc86.pdf; Texas Instruments, *SNx4HC157 Quadruple 2-Line to 1-Line Data Selectors/Multiplexers*, https://www.ti.com/lit/ds/symlink/sn74hc157.pdf. Las tablas, los ejemplos y las cuatro figuras son originales de este libro.
