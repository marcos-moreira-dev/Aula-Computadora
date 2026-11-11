# Capítulo 21. Qué implica ampliar la palabra

*Parte VI · Aula-16 y comparación · Aula-Computadora*

El capítulo 20 mostró que Aula-8 puede **describir sobre el papel** una suma, un bucle y funciones, aunque todavía falte la CPU que ejecute sus bytes. Sus registros generales contienen ocho bits. ¿Qué ocurre cuando queremos sumar `0x01FF + 0x0001` o calcular un término de Fibonacci superior a 255? Podemos usar dos bytes y dos operaciones en Aula-8, pero cada programa debe ocuparse de conservar y transmitir el acarreo.

Una solución consiste en construir otra máquina con **registros generales y ALU de 16 bits**. La llamaremos **Aula-16**. No es Aula-8 con nombres de instrucciones más largos: necesita su propio circuito de datos, codificación de instrucciones, control y convenio de llamadas. Aquí estudiaremos **qué cambia en cada componente** y cuánto cuesta esa comodidad. En el capítulo 22 veremos con detalle el bus de memoria de 16 bits.

Las figuras son **diagramas funcionales con cantidades calculables**. No son pistas de una placa ni una ALU sintetizada. No contamos todavía con ISA binaria de Aula-16, circuitos medidos, micro-ROM o programas ejecutados en ella; por eso no inventaremos opcodes, tiempos de reloj ni una cifra de transistores que dependa de puertas todavía no elegidas.

## 1. El ancho de una palabra no define cuántas direcciones existen

En el lenguaje de arquitectura, **palabra** suele ser una cantidad de bits que la CPU maneja de manera natural. Aula-8 posee cuatro registros generales de ocho bits y ALU de ocho; Aula-16 tendrá cuatro de dieciséis y ALU de dieciséis. Sin embargo, ambas arquitecturas conservan **16 líneas de dirección** y **memoria direccionable por bytes**. Una línea de dirección adicional duplicaría el número de direcciones; un dato más ancho, por sí solo, no lo hace.

[[EQ:Direcciones posibles con 16 bits de dirección = 2^16 = 65536]]

[[EQ:Espacio direccionable = 65536 bytes = 64 KiB, tanto en Aula-8 como en Aula-16]]

La primera máquina transfiere ocho bits de datos por su bus externo. La segunda tendrá un **bus externo de 16 bits**, pero su capacidad de direccionamiento sigue siendo 65536 bytes. Eso no debe interpretarse como «65536 palabras de dieciséis bits»: violaría nuestro acuerdo de **direccionamiento por byte**.

| Propiedad | Aula-8 | Aula-16 |
| --- | --- | --- |
| Registros R0–R3 | 8 bits cada uno | 16 bits cada uno |
| ALU | 8 bits | 16 bits |
| PC, SP y X | 16 bits | 16 bits |
| Bus externo de datos | 8 bits | 16 bits |
| Bus externo de direcciones | 16 bits | 16 bits |
| Direcciones de bytes | 65536 | 65536 |

[[FIG:c21_fig01_palabra_y_direcciones|Figura 1. Dos computadoras con igual espacio de direcciones pueden tener registros y ALU de anchuras diferentes.|Aula-8: R0 de 8, ALU8, bus externo8; Aula-16: R0 de16, ALU16, bus externo16; ambas mantienen direcciones de16 bits y 65536 bytes direccionables.]]

## 2. Un registro de dieciséis bits necesita guardar dieciséis bits

Recuerda el capítulo 6: un flip-flop D ideal conserva un bit y responde a un flanco de reloj. Un registro de ocho bits puede modelarse como ocho flip-flops gobernados conjuntamente. Al ampliar su ancho a dieciséis, necesitamos **dieciséis elementos de almacenamiento**, más la habilitación y las conexiones necesarias. Eso no prueba que un diseño concreto emplee exactamente dieciséis encapsulados: un chip puede contener varios flip-flops.

[[EQ:Bits de R0–R3 en Aula-8 = 4 × 8 = 32]]

[[EQ:Bits de R0–R3 en Aula-16 = 4 × 16 = 64]]

La diferencia de **32 bits de almacenamiento** corresponde **solo a los cuatro registros generales**. PC, SP y X siguen teniendo 16 bits en ambas; hay más registros temporales y latches de control que todavía no se han dimensionado para la versión Aula-16. Por tanto, afirmar «toda la CPU requiere exactamente el doble de flip-flops» sería un error.

El valor hexadecimal `0x1234` contiene dos bytes: alto `12` y bajo `34`. Aula-16 podría mantener ambos dentro de un solo registro general. En Aula-8 habría que repartirlos, por ejemplo, en R1:R0, con R1=`12` y R0=`34`, y coordinar ambos cuando se suman o desplazan.

[[EQ:0x1234 = (0x12 × 256) + 0x34 = 4660 decimal]]

## 3. Qué hace el sumador cuando se duplica el ancho

El sumador completo del capítulo 10 calcula para cada columna el bit de suma y el acarreo a la columna siguiente. Para la posición `i`, llamaremos `Ai` y `Bi` a los bits de los operandos y `Ci` al acarreo entrante. Primero obtenemos la propagación `Pi` y la generación `Gi`; después calculamos el resultado `Si` y el nuevo acarreo.

[[EQ:Pi = Ai XOR Bi; Gi = Ai AND Bi]]

[[EQ:Si = Pi XOR Ci; C(i+1) = Gi OR (Pi AND Ci)]]

Esas ecuaciones sirven tanto para un sumador de ocho como para uno de dieciséis bits. La diferencia consiste en **cuántas posiciones deben participar** y cómo se conecta la transmisión del acarreo. Con propagación en cascada (*ripple carry*), cada etapa puede esperar la salida de la anterior. Hay **16 etapas de suma** en lugar de ocho; la ruta crítica de acarreo puede ser más larga, pero su duración real depende de compuertas y tecnología que aún no elegimos.

[[FIG:c21_fig02_acarreo_16_bits|Figura 2. Dos grupos de ocho bits transmiten un acarreo intermedio en un sumador de dieciséis bits.|Las posiciones 0–7 producen carry C8, que alimenta las posiciones 8–15; la salida final C16 es el acarreo de palabra. Es un agrupamiento funcional, no un netlist físico.]]

[[EQ:Resultado u16 = (A + B) mod 65536; C = 1 si A+B ≥ 65536]]

Esta explicación **no** obliga a construir la ALU de dieciséis bits como dos chips de ocho. Podríamos usar una cadena de sumadores completos, partes comerciales o una arquitectura de acarreo distinta. El circuito concreto necesita validar alimentación, retardos, selección de operaciones, sincronización y carga eléctrica.

## 4. Comparación paso a paso: 01FF más 0001

Tomemos `A=0x01FF` y `B=0x0001`. Son dos valores sin signo de dieciséis bits. **Aula-8**, con ALU de ocho, operaría primero los bytes bajos: `FF + 01 = 100` hexadecimal. Guarda `00` como byte bajo y `C=1`. Después suma los altos con ADC: `01 + 00 + 1 = 02`.

[[EQ:Byte bajo de Aula-8: 0xFF + 0x01 = 0x100 → 00, acarreo 1]]

[[EQ:Byte alto de Aula-8: 0x01 + 0x00 + 1 = 0x02]]

En **Aula-16**, una sola operación **aritmética de palabra** puede tomar ambos valores de 16 bits y producir `0x0200`, con un sumador de 16 posiciones. Eso **no afirma que la instrucción completa consuma un solo ciclo**: buscar y decodificar la instrucción, leer registros y escribir el resultado requiere una unidad de control cuyo diseño está pendiente.

| Paso | Aula-8 con par R1:R0 | Aula-16 con R0 de 16 bits |
| --- | --- | --- |
| Inicial | R1:R0=`01:FF` | R0=`01FF` |
| Bajo | ADD `FF+01→00`, C=1 | Parte baja `FF+01→00` |
| Alto | ADC `01+00+1→02` | Acarreo cruza internamente a bit 8 |
| Final | R1:R0=`02:00` | R0=`0200` |

[[EQ:0x01FF + 0x0001 = 0x0200 = 512 decimal]]

[[FIG:c21_fig03_suma_dos_anchos|Figura 3. La misma suma se expresa en dos operaciones aritméticas de byte o una de palabra según la ALU.|Aula-8: FF+01 genera C8=1 y 01+00+C8 produce 02; Aula-16: sumador de16 bits recibe 01FF+0001 y produce 0200, sin presupuestar ciclos reales.]]

La comodidad del dato ancho puede reducir la cantidad de instrucciones y transferencias intermedias en muchos algoritmos. No es una garantía universal de que el programa final **sea exactamente el doble de rápido**, pues influyen acceso a RAM, microarquitectura, frecuencia, paralelismo de circuitos y codificación de la ISA.

## 5. El resultado tiene dieciséis bits, pero las banderas siguen importando

Un entero de dieciséis bits sin signo representa valores desde cero hasta 65535. Con complemento a dos, los mismos patrones representan valores desde −32768 hasta +32767. Los bits son los mismos; cambia la interpretación del programa. También cambia qué señal debe observarse como **N**: ahora es el **bit 15**, no el bit 7.

[[EQ:Rango u16 = 0..(2^16−1) = 0..65535]]

[[EQ:Rango i16 = −2^15..(2^15−1) = −32768..32767]]

| Operación u16 | Resultado de 16 bits | C (acarreo) | V (overflow firmado) | Z | N |
| --- | --- | --- | --- | --- | --- |
| `FFFF + 0001` | `0000` | 1 | 0 | 1 | 0 |
| `7FFF + 0001` | `8000` | 0 | 1 | 0 | 1 |
| `00FF + 0001` | `0100` | 0 | 0 | 0 | 0 |

[[EQ:0xFFFF + 1 = 0x0000 con C=1, V=0 y Z=1]]

[[EQ:0x7FFF + 1 = 0x8000 con C=0 y V=1]]

Un acarreo **no es lo mismo** que overflow firmado. El primero pregunta si la suma sin signo rebasa 65535. El segundo pregunta si el resultado firmado salió del intervalo −32768..32767. Al comparar con `CMP`, el proyecto ha elegido en Aula-8 **C=préstamo** para la resta, lo cual hace útil `JNC` en comparaciones sin signo; Aula-16 deberá especificar una convención coherente antes de emitir opcodes oficiales.

## 6. Extender la comparación sin engañar a las banderas

Considera los patrones `0x8000` y `0x7FFF`. Como números **sin signo**, son 32768 y 32767: el primero es mayor. Como números **con signo de dieciséis bits**, son −32768 y +32767: el primero es menor. Ninguna puerta cambia por interpretar el mismo par de bits de otra forma; cambia **la prueba que hace el software sobre las banderas**.

[[EQ:0x8000 sin signo = 32768; con signo = −32768]]

En la semántica candidata de Aula-8, la comparación sin signo usa el préstamo C y la igualdad Z, mientras que la comparación con signo se relaciona con `N XOR V`. La adaptación a dieciséis bits debe aplicar **N al bit 15** y **V a los signos de dieciséis bits completos**. No sería correcto observar simplemente N/V del byte bajo de una resta repartida.

## 7. Una palabra en registro y dos bytes en RAM

La memoria de Aula-16 seguirá direccionándose por bytes. Si escribimos la palabra `0x1234` en la dirección **par** `0x2000`, la convención little-endian deja `34` en `2000` y `12` en `2001`. El **bus externo de dieciséis bits** podrá transferir ambos carriles en una lectura o escritura **alineada**, siempre que el controlador y los bancos físicos se diseñen para ello. El capítulo 22 explicará los dos bancos de ocho bits y el movimiento de bytes impares.

[[EQ:RAM[0x2000]=0x34 y RAM[0x2001]=0x12 → palabra little-endian 0x1234]]

[[FIG:c21_fig04_registro_a_ram|Figura 4. Un registro de dieciséis bits se almacena en dos direcciones consecutivas de bytes.|Registro 1234 se separa en byte bajo 34→2000 y alto 12→2001; el bus externo16 y los carriles de memoria no convierten el espacio de 64 KiB en 128 KiB.]]

La primera versión de Aula-16 aceptará **accesos de palabra alineados en direcciones pares**. Un acceso de palabra que comience en una dirección impar debe señalar **error en V1**; es distinto de una lectura de **un solo byte impar**, que deberá encaminarse al carril correcto. No atribuyamos al circuito que aún no existe la capacidad de fusionar automáticamente dos transacciones desalineadas.

## 8. ¿Cuánto hardware adicional cuesta?

Ampliar la palabra significa agregar caminos de datos, almacenar más bits por registro y extender la lógica de la ALU. Si el banco de cuatro registros generales se implementara con flip-flops de un bit, pasaríamos de 32 a 64 flip-flops **en ese banco**, aparte de selectores, escritura habilitada y cableado. Si usamos un sumador completo por bit, pasaríamos de ocho a dieciséis etapas aritméticas. Ese cálculo es **de funciones mínimas**, no de chips, transistores, watts ni precio final.

[[EQ:Aumento de almacenamiento de R0–R3 = 64 − 32 = 32 bits]]

| Coste conceptual | Beneficio conceptual | Riesgo por verificar |
| --- | --- | --- |
| Más bits de registro | Un valor u16 en un solo registro | Más latches y líneas de selección |
| ALU de 16 posiciones | Aritmética u16 natural | Ruta de acarreo y tiempo crítico |
| Bus de datos externo16 | Palabras alineadas en menos transferencias | Selección de carriles y arbitraje |
| ISA y ABI propias | Programación acorde al ancho | Decodificación, pila y compatibilidad |

No es válido estimar potencia, precio o máxima frecuencia multiplicando por dos una ficha de Aula-8: ni siquiera hemos congelado el circuito de esa primera máquina. La decisión final entre un sumador de acarreo en cascada u otra topología se tomará cuando existan temporización objetivo y componentes concretos.

## 9. Qué debería comprobar una implementación Aula-16

Primero verificaremos aritmética exhaustiva de casos representativos y límites `0000`, `7FFF`, `8000` y `FFFF`. Luego una referencia independiente comprobará banderas C/V/Z/N, sumas y restas por byte, y el recorrido de dos carriles de memoria. Finalmente, cuando existan microcontrol y circuito, se observarán señales de selección de RAM y transacciones de bus **sin conflicto de conductores**.

El programa de suma de Aula-8 del capítulo 20 no puede introducirse sin cambios en Aula-16: **la codificación binaria de Aula-16 aún no está definida**. Podremos conservar los casos de prueba y resultados, pero habrá que generar el programa correspondiente mediante una ISA de dieciséis bits aprobada. Esta separación evita confundir compatibilidad de **problema** con compatibilidad de **código máquina**.

[[PAGEBREAK]]
## Construimos Aula-16: ensanchar el cálculo no ensancha las direcciones

Aula-8 ya nos enseñó a seguir un byte por el bus y una instrucción por su dirección. Aula-16 conserva esa disciplina, pero sus registros generales, ALU y bus externo de datos trabajan con **16 bits**. Una dirección de dieciséis bits sigue seleccionando entre **65 536 posiciones de byte**, no el doble de direcciones ni una palabra en cada dirección. Esta distinción obliga a estudiar qué sucede cuando una lectura necesita uno o dos bytes.

Al sumar `0x00FF + 0x0001`, la propagación del acarreo ocurre dentro de una operación de palabra de 16 bits. Al almacenar el resultado de dieciséis bits en RAM, en cambio, debemos decidir cómo se distribuyen los bytes en los bancos bajo y alto. El capítulo 22 introduce esa **ruta externa concreta**, que no debe tomarse prestada de un dibujo de Aula-8 con un simple cambio de etiqueta.

## Ejercicios del capítulo 21

**Ejercicio 1 — Direcciones.** ¿Cuántos bytes direccionan ambas máquinas si conservan 16 bits de dirección?

**Ejercicio 2 — Anchura.** ¿Cuántos bits suman R0–R3 en Aula-8 y en Aula-16?

**Ejercicio 3 — Interpretación.** Convierte `0x1234` a decimal sin signo.

**Ejercicio 4 — Acarreo.** ¿Qué byte bajo resulta de `0xFF+0x01` y qué acarreo recibe la mitad alta?

**Ejercicio 5 — Palabra.** ¿Cuál es el resultado `u16` de `0x01FF+0x0001`?

**Ejercicio 6 — Frecuencia.** ¿Por qué una operación de palabra no demuestra que una instrucción termine en un único ciclo?

**Ejercicio 7 — Rango.** Indica los intervalos de `u16` e `i16`.

**Ejercicio 8 — Banderas.** Calcula C, V, Z y N para `0xFFFF+1` en 16 bits.

**Ejercicio 9 — Overflow.** ¿Por qué `0x7FFF+1` activa V pero no C?

**Ejercicio 10 — Signo.** ¿Cómo se interpretan `0x8000` y `0x7FFF` con y sin signo?

**Ejercicio 11 — Memoria.** ¿Qué bytes quedan en `2000` y `2001` al guardar `0x1234` little-endian?

**Ejercicio 12 — Compatibilidad.** ¿Puede ejecutarse sin cambios en Aula-16 el binario de Euclides de Aula-8? ¿Por qué?

[[PAGEBREAK]]
## Solucionario del capítulo 21

**1.** `2^16=65536` direcciones de **bytes**, equivalentes a 64 KiB de espacio direccionable.

**2.** Aula-8: 32 bits. Aula-16: 64 bits en esos cuatro registros generales.

**3.** `18×256+52=4660` decimal.

**4.** Byte bajo `00` y acarreo C=1 hacia los bits altos.

**5.** `0x0200`, igual a 512 decimal.

**6.** Porque fetch, decodificación, transporte y almacenamiento dependen de control, memoria y frecuencia aún no diseñados.

**7.** `u16: 0..65535`. `i16: −32768..32767`.

**8.** Resultado `0000`; C=1, V=0, Z=1, N=0.

**9.** El valor firmado máximo +32767 pasa a un patrón negativo `8000`; no hay acarreo fuera del bit 15.

**10.** Sin signo: 32768 > 32767. Con signo: −32768 < +32767.

**11.** En `2000` va `34` y en `2001`, `12`.

**12.** No se ha definido ninguna compatibilidad binaria; Aula-16 tendrá encoding y ABI propios. Se pueden reutilizar las entradas y salidas esperadas, no sus opcodes.

## Para continuar

Ahora conocemos **por qué** Aula-16 necesita datos más anchos y qué problemas resuelve. En el capítulo 22 construiremos la explicación detallada del **bus externo de dieciséis bits**: dos carriles de ocho, direcciones pares e impares, orden de bytes y una palabra alineada sobre RAM direccionada por bytes.
