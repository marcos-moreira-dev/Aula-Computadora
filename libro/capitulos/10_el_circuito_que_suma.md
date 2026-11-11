# Capítulo 10. El circuito que suma

*Parte III · Memoria, buses y aritmética · Aula-Computadora*

En el capítulo anterior aprendimos a localizar un byte dentro de una memoria. Pero una computadora no se limita a guardar números: también debe **operar con ellos**. Si colocamos trece objetos en una caja y luego añadimos nueve, sabemos que hay veintidós. Aquí responderemos una pregunta distinta: **¿cómo puede un circuito obtener 22 sin reconocer ni la palabra «trece» ni el símbolo decimal «13»?**

La respuesta comienza con una operación sobre dos bits. Construiremos primero un **medio sumador**, después un **sumador completo** que recibe un acarreo, y finalmente una cadena capaz de sumar ocho bits. Todos los resultados se comprobarán con tablas y con una suma escrita columna por columna. Los esquemas son funcionales y didácticos: aún no representan el circuito eléctrico definitivo de Aula-8 ni una placa ensayada.

## 1. Sumar en base dos conserva la misma idea de la escuela

Cuando sumamos `8 + 7` en decimal, obtenemos `15`: anotamos `5` en esa columna y llevamos `1` a la columna de las decenas. La razón es que una posición decimal admite los dígitos de 0 a 9. En **binario** cada posición admite únicamente `0` y `1`, así que al sumar `1 + 1` ya alcanzamos el valor que corresponde a **dos unidades**: escribimos `0` en la columna actual y llevamos `1` a la siguiente, de peso doble.

[[EQ:1₂ + 1₂ = 10₂  ⇒  suma = 0, acarreo = 1]]

Aquí la escritura `10₂` representa el número decimal **2**, no diez decimal. La cifra de la derecha tiene peso `2⁰ = 1`, la siguiente `2¹ = 2`, luego vienen `2² = 4`, `2³ = 8` y así sucesivamente. A partir de esto podemos diseñar un circuito que atienda una columna sin saber cuánto vale el número completo.

## 2. Medio sumador: dos entradas y dos salidas

Un **medio sumador** (*half-adder*) recibe dos bits `A` y `B`. Produce dos salidas distintas: el bit de **suma** `S` que se escribe en esa columna, y el **acarreo** `C` que se envía a la columna de mayor peso. Cuando ambos bits son `1`, la suma de esa columna vale cero porque el dos se transporta íntegramente a la siguiente.

| A | B | S | C |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

La columna de `S` coincide con la función **XOR** estudiada en el capítulo 4: vale `1` cuando las entradas son distintas. La columna de `C` coincide con **AND**: vale `1` únicamente cuando ambas son `1`. Un mismo par de entradas puede alimentarse simultáneamente a esas dos compuertas.

[[EQ:S = A ⊕ B]]

[[EQ:C = A ∧ B]]

[[FIG:c10_fig01_medio_sumador|Figura 1. Un medio sumador conecta A y B a una XOR para obtener S y a una AND para obtener el acarreo C.|Diagrama funcional de dos entradas A y B que se bifurcan a una XOR y una AND; las dos salidas son S y C, sin entrada de acarreo.]]

Por ejemplo, `A=1`, `B=0` da `S=1`, `C=0`; pero `A=1`, `B=1` da `S=0`, `C=1`. **El medio sumador tiene una limitación:** no recibe el acarreo que podría llegar desde una columna anterior. Por eso no basta con encadenar medios sumadores independientes para sumar números de varios bits.

## 3. Sumador completo: ahora entran tres bits

En una columna intermedia pueden coincidir **tres** unos: `A=1`, `B=1` y el acarreo entrante `Cin=1`. Su suma decimal es `3`, escrita `11₂`. Por tanto, `S=1` y `Cout=1`. A esto responde el **sumador completo** (*full-adder*), con tres entradas (`A`, `B`, `Cin`) y dos salidas (`S`, `Cout`).

| A | B | Cin | S | Cout |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

Podemos construirlo a partir de **dos medios sumadores**. El primero obtiene `P = A XOR B` y un acarreo parcial `G = A AND B`. El segundo suma `P` y `Cin`, y obtiene `S = P XOR Cin` junto con otro acarreo `H = P AND Cin`. Una compuerta OR combina ambos acarreos posibles. No es una regla memorizada: cada señal sale de una tabla de verdad que podemos comprobar.

[[EQ:P = A ⊕ B ; G = A ∧ B]]

[[EQ:S = P ⊕ Cin = A ⊕ B ⊕ Cin]]

[[EQ:Cout = G ∨ (P ∧ Cin) = (A ∧ B) ∨ (Cin ∧ (A ⊕ B))]]

[[FIG:c10_fig02_sumador_completo|Figura 2. Dos medios sumadores y una OR forman un sumador completo: el acarreo recibido participa en la suma y en el acarreo que sale.|Diagrama de bloques: A y B al medio sumador 1; su suma parcial P y Cin al medio sumador 2; los acarreos G y H se reúnen en OR para producir Cout.]]

**Comprobación concreta.** Para `A=1`, `B=1`, `Cin=1`, el primer medio sumador calcula `P=0` y `G=1`; el segundo calcula `S=1` y `H=0`; la OR da `Cout=1`. Se cumple `1 + 1 + 1 = 3 = 11₂`. Si `Cin` fuese cero, tendríamos `S=0`, `Cout=1`.

El acarreo saliente también puede entenderse como una **mayoría de tres bits**: es `1` si por lo menos dos de las entradas `A`, `B`, `Cin` son `1`. Esta descripción y la fórmula con compuertas representan **la misma función**; la tabla completa permite demostrarlo, no solo suponerlo.

## 4. Ocho sumadores completos en cadena

Para sumar dos bytes no necesitamos inventar otra clase de aritmética. Conectamos ocho etapas, una por posición `i=0...7`. La posición cero es la de menor peso. Allí fijamos `C0=0` cuando hacemos una suma ordinaria sin acarreo previo. Cada etapa calcula `Si` y entrega `C(i+1)` a la siguiente. Esa conexión recibe el nombre de **sumador de acarreo propagado** (*ripple-carry adder*).

La dirección de trabajo puede confundir: **escribimos normalmente los bits de mayor a menor peso, de izquierda a derecha**, pero para sumar empezamos **por la derecha** (`i=0`) porque de allí nace el acarreo que necesita la columna siguiente.

[[EQ:Ai + Bi + Ci = Si + 2×C(i+1)]]

En esta igualdad, cada símbolo representa un bit, salvo la suma numérica de la derecha; el factor dos expresa exactamente el valor transportado a la columna siguiente. Si una etapa recibe `1+0+1=2`, entrega `S=0` y `Cout=1`, de modo que `0+2×1=2`.

No debe imaginarse que las ocho etapas producen necesariamente su salida final en el mismo instante. En un circuito físico el acarreo debe atravesar compuertas y cada una tiene retardo. La cifra máxima de frecuencia o de nanosegundos **no puede deducirse únicamente de la tabla de verdad**.

## 5. Ejercicio completo: 13 + 9, columna por columna

Primero traducimos cada número a binario usando las potencias de dos. `13` contiene `8 + 4 + 1`; `9` contiene `8 + 1`. Los dos caben en ocho bits con ceros a la izquierda.

[[EQ:13 = 1×8 + 1×4 + 0×2 + 1×1 = 00001101₂]]

[[EQ:9 = 1×8 + 0×4 + 0×2 + 1×1 = 00001001₂]]

La tabla sigue el movimiento real del acarreo **desde el bit 0 hasta el bit 7**. La columna `Cin` dice qué llega desde la etapa anterior; `Cout` indica qué se llevará a la siguiente. El lector puede comprobar cada fila con la tabla del sumador completo.

| Posición i | Peso | Ai | Bi | Cin | Si | Cout |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 0 | 0 | 1 |
| 1 | 2 | 0 | 0 | 1 | 1 | 0 |
| 2 | 4 | 1 | 0 | 0 | 1 | 0 |
| 3 | 8 | 1 | 1 | 0 | 0 | 1 |
| 4 | 16 | 0 | 0 | 1 | 1 | 0 |
| 5 | 32 | 0 | 0 | 0 | 0 | 0 |
| 6 | 64 | 0 | 0 | 0 | 0 | 0 |
| 7 | 128 | 0 | 0 | 0 | 0 | 0 |

[[FIG:c10_fig03_suma_trece_mas_nueve|Figura 3. Suma de 13 y 9 en ocho bits. Las columnas de la derecha producen acarreos hacia las de la izquierda y el resultado es 00010110.|Lámina de suma binaria 00001101 más 00001001 igual a 00010110, con acarreos C1 y C4 destacados y lectura de pesos 16 más 4 más 2.]]

Leemos ahora `S7...S0` **de izquierda a derecha**: `00010110₂`. Los unos ocupan las posiciones 4, 2 y 1, cuyos pesos son 16, 4 y 2. Su suma decimal es 22, exactamente `13 + 9`.

[[EQ:00001101₂ + 00001001₂ = 00010110₂ = 22₁₀]]

[[EQ:22 = 1×16 + 0×8 + 1×4 + 1×2 + 0×1]]

Esta demostración resuelve una confusión frecuente: los **ocho bits de salida no son ocho sumas decimales independientes**. Cada bit necesita saber si la etapa anterior transportó una unidad de peso doble. Para comprobarlo, basta mirar el bit 1: en los operandos hay `0` y `0`, pero el resultado es `1` porque recibió el acarreo de `1+1` en el bit 0.

## 6. Cuando el resultado no cabe en ocho bits

Ocho bits sin signo representan valores de `0` a `255`. El circuito de ocho etapas siempre produce ocho bits `S7...S0` y un acarreo final `C8`. Si la suma total supera 255, el byte de salida conserva solo el **resto al dividir para 256** y `C8` avisa que hubo una unidad adicional de peso 256.

[[EQ:S8 = (A + B + C0) mod 256]]

[[EQ:C8 = ⌊(A + B + C0) / 256⌋]]

Por ejemplo, `250 + 10 = 260`. Como `260 = 256 + 4`, en ocho bits aparece `00000100₂` (`4`) y `C8=1`. Es un **desbordamiento del rango sin signo**: descartar el noveno bit cambia el valor numérico.

[[EQ:250 + 10 = 260 = 1×256 + 4  ⇒  S8 = 4, C8 = 1]]

En cambio, si representamos enteros **con signo en complemento a dos**, el rango de ocho bits es `−128...127`. Entonces el acarreo final **no equivale** a desbordamiento con signo (*signed overflow*). Un ejemplo opuesto es `127 + 1`: la salida `10000000₂` se interpreta como `−128`, aunque `C8=0`. Este fallo de rango con signo se señala con `V=1`, porque se sumaron dos positivos y apareció un resultado con bit de signo negativo.

[[EQ:0x7F + 0x01 = 0x80  ⇒  C8 = 0, V = 1]]

Para la suma de dos operandos de ocho bits, una forma de reconocer desbordamiento con signo es comparar sus bits de signo con el bit de signo de la salida. También equivale a comparar el acarreo que **entra** al bit 7 con el que **sale** de él.

[[EQ:V = C7 ⊕ C8]]

## 7. Las banderas cuentan hechos diferentes

Cuando una futura ALU entregue un resultado, varias señales resumen propiedades distintas. **Z** indica que el byte calculado es cero; **N** copia su bit más alto (`S7`); **C** puede representar el acarreo final de una **suma sin signo**; **V** indica que una **suma con signo** quedó fuera de rango. Estas definiciones de suma son coherentes con el diseño candidato de Aula-8, pero todavía no aprueban su circuito ni el comportamiento final de todas sus instrucciones.

| Operación de 8 bits | Resultado | C | V | Z | N |
| --- | --- | --- | --- | --- | --- |
| `13 + 9` | `0x16` (22) | 0 | 0 | 0 | 0 |
| `250 + 10` | `0x04` (4) | 1 | 0 | 0 | 0 |
| `127 + 1` | `0x80` (−128 con signo) | 0 | 1 | 0 | 1 |
| `0xFF + 0x01` | `0x00` (0) | 1 | 0 | 1 | 0 |

Un detalle importante: en la tercera fila, el patrón `0x80` también representa **128 sin signo**. Los bits no contienen por sí solos la palabra «negativo»; se necesita el criterio de interpretación explicado en el capítulo 7B «Del bit al significado». En una resta, la convención de `C` puede ser distinta y depende de la arquitectura: la propuesta de Aula-8 usa `C` como **préstamo** para resta, asunto que abordaremos con cuidado en el capítulo 11.

## 8. Un byte es una etapa hacia dieciséis bits

Para hacer una suma de dieciséis bits con un sumador de ocho bits, se puede trabajar primero con los bytes bajos y luego con los altos, **transportando el acarreo** entre ambas operaciones. Así, `0x01FF + 0x0001`: los bytes bajos hacen `0xFF + 0x01 = 0x00`, con acarreo `1`. Los bytes altos hacen `0x01 + 0x00 + 1 = 0x02`. La palabra resultante será `0x0200`.

[[EQ:0x01FF + 0x0001 = 0x0200]]

[[FIG:c10_fig04_cadena_y_dos_bytes|Figura 4. Ocho etapas transportan el acarreo entre bits; la misma idea permite sumar dos bytes en dos pasadas o encadenar dos sumadores de cuatro bits.|Dos esquemas comparativos: cadena de ocho sumadores completos con C0 a C8 y suma de dos bytes, primero FF más 01 produce 00 y carry 1, luego 01 más 00 más carry produce 02.]]

Esto no obliga a que toda CPU real use ocho sumadores completos discretos. Un componente comercial como el **CD74HC283** de Texas Instruments ya implementa un sumador completo de **cuatro bits** con acarreo de entrada y salida; dos bloques de esa anchura pueden combinarse para estudiar una suma de ocho bits. Por su parte, el **SN74HC86** contiene cuatro XOR de dos entradas. Estos ejemplos muestran que la función lógica puede construirse con compuertas o integrarse en chips; **no** permiten asumir que ambas soluciones tengan la misma temporización o las mismas conexiones eléctricas.

Antes de conectar chips físicos hay que consultar el **encapsulado exacto**, su alimentación permitida, entradas no utilizadas, requisitos de desacoplo, niveles de interfaz y retardos de propagación en la hoja de datos. Una tabla matemática correcta no demuestra por sí sola que un montaje funcione a una frecuencia específica. Tampoco identifica las conexiones de la CPU ni una unidad de control que aún no diseñamos.

## Construimos Aula-8: una operación que cambia el estado

El registro R0 del capítulo 7 conserva un byte y la RAM del capítulo 9 permite guardarlo fuera de la CPU. Pero ninguna de esas dos piezas **calcula** una suma. Ahora podemos intercalar un sumador de ocho bits entre las fuentes de datos y un registro de destino. Si R0 contiene `13` y R1 contiene `9`, las entradas de los ocho sumadores forman `0000 1101₂` y `0000 1001₂`; el resultado es `0001 0110₂`, es decir `0x16`.

Para que R0 cambie realmente, no basta conectar la salida del sumador a su entrada D: hace falta que la unidad de control autorice **cuándo** capturar `0x16`. Sin esa orden el resultado puede existir momentáneamente en los cables, mientras R0 mantiene `0x0D`. Este es el siguiente escalón de Aula-8: **una función combinacional unida a una memoria temporal**. Todavía no se ha fijado la frecuencia ni calculado el retardo máximo de una cadena física de acarreo.

## Ejercicios del capítulo 10

Resuelve cada problema escribiendo primero los bits y, cuando haya varias columnas, **marca todos los acarreos de derecha a izquierda**. Después comprueba el resultado convirtiéndolo a decimal. Las banderas se refieren únicamente a las **sumas de ocho bits** de este capítulo.

**Ejercicio 1 — Medio sumador.** Con `A=1` y `B=1`, determina la suma y el acarreo usando XOR y AND.

**Ejercicio 2 — Medio sumador alternativo.** Con `A=1` y `B=0`, calcula ambas salidas y explica por qué no se necesita acarreo.

**Ejercicio 3 — Tres unos.** Para `A=1`, `B=1`, `Cin=1`, halla `P`, `G`, `S`, `H` y `Cout` a partir de dos medios sumadores.

**Ejercicio 4 — Mayoría.** Explica por qué el acarreo de salida de un sumador completo vale uno exactamente cuando al menos dos entradas valen uno.

**Ejercicio 5 — Primeros acarreos de 13 + 9.** Escribe las posiciones `i=0` e `i=1` con sus entradas, bit de suma y acarreo de salida.

**Ejercicio 6 — Suma de 13 y 9.** Realiza las ocho columnas, escribe `S7...S0` y comprueba el decimal mediante potencias de dos.

**Ejercicio 7 — Otra suma manual.** Suma `00101101₂` (45) más `00010111₂` (23) e identifica en qué columnas aparece un acarreo de salida.

**Ejercicio 8 — Rango sin signo.** Suma `250 + 10` en un circuito de ocho bits. Da los ocho bits de salida, `C8` y la suma decimal real.

**Ejercicio 9 — Rango con signo.** Para `0x7F + 0x01`, determina resultado y banderas `C`, `V`, `Z`, `N`, explicando por qué `C` y `V` difieren.

**Ejercicio 10 — Cero y acarreo.** Para `0xFF + 0x01`, determina resultado, `C`, `V`, `Z` y `N`.

**Ejercicio 11 — Dos bytes.** Calcula `0x01FF + 0x0001` en dos pasos de ocho bits. Indica el acarreo que pasa del byte bajo al alto.

**Ejercicio 12 — Diagnóstico del circuito.** Alguien sostiene que ocho compuertas XOR independientes bastan para sumar dos bytes. Refútalo con el bit `i=1` del ejemplo `13+9` y di por qué los retardos tampoco se deducen de una tabla de verdad.

## Solucionario del capítulo 10

**1.** `S=1 XOR 1=0`; `C=1 AND 1=1`. Dos unidades binarias se escriben `10₂`: cero en la columna actual y uno transportado.

**2.** `S=1 XOR 0=1`, `C=1 AND 0=0`. Una unidad cabe en la columna actual y no hay nada que transportar.

**3.** Primer medio sumador: `P=1 XOR 1=0`, `G=1 AND 1=1`. Segundo: `S=0 XOR 1=1`, `H=0 AND 1=0`. OR final: `Cout=1 OR 0=1`; por tanto, `1+1+1=11₂`.

**4.** Con cero o un solo bit a uno, la suma vale 0 o 1 y no necesita una columna superior. Con exactamente dos bits a uno, la suma vale 2=`10₂`; con tres, vale 3=`11₂`. En ambos casos `Cout=1`.

**5.** En `i=0`: `A0=1`, `B0=1`, `C0=0` → `S0=0`, `C1=1`. En `i=1`: `A1=0`, `B1=0`, `C1=1` → `S1=1`, `C2=0`. El bit 1 vale uno por el acarreo, aunque ambos operandos allí sean cero.

**6.** `00001101 + 00001001 = 00010110₂`. Los acarreos no nulos son `C1=1` y `C4=1`; los otros `C2...C8` son cero. Resultado: `1×16 + 1×4 + 1×2 = 22`.

**7.** `00101101₂ + 00010111₂ = 01000100₂`. Columna 0: `1+1=0`, `C1=1`; columna 1: `0+1+1=0`, `C2=1`; columna 2: `1+1+1=1`, `C3=1`; columna 3: `1+0+1=0`, `C4=1`; columna 4: `0+1+1=0`, `C5=1`; columna 5: `1+0+1=0`, `C6=1`; columna 6: `0+0+1=1`, `C7=0`; columna 7: `0+0+0=0`, `C8=0`. Comprobación decimal: `64+4=68=45+23`.

**8.** `250+10=260=256+4`. Los ocho bits son `00000100₂`; `C8=1`. El resultado completo necesita nueve bits: `1 00000100₂`.

**9.** `0x7F+0x01=0x80`. Banderas: `C=0`, `V=1`, `Z=0`, `N=1`. No hay noveno bit; sí hay desbordamiento firmado porque `127+1=128` excede el máximo `127`.

**10.** `0xFF+0x01=0x100`: salida `0x00`, `C=1`, `V=0`, `Z=1`, `N=0`. En interpretación con signo, `−1+1=0` cabe en rango aunque se haya producido acarreo sin signo.

**11.** Byte bajo: `FF+01+0=100` hexadecimal; guardamos `00` y llevamos `1`. Byte alto: `01+00+1=02`; el resultado final es `0x0200`, sin acarreo final de la palabra de dieciséis bits.

**12.** En el bit 1 del ejemplo `13+9`, `A1=0` y `B1=0`; una XOR independiente daría `0`. La suma correcta es `S1=0 XOR 0 XOR C1=1` porque el bit 0 produjo `C1=1`. Se requiere un sumador que acepte ese acarreo. Las tablas solo especifican resultados estables, no tiempos de propagación, tensiones ni cargas eléctricas.

## Para continuar

Ya tenemos el mecanismo para sumar: un medio sumador muestra las dos salidas de una columna; un sumador completo recibe el acarreo; ocho etapas producen un byte de resultado y las señales necesarias para distinguir distintas condiciones de rango. En el capítulo 11 reutilizaremos esta base para **restar**, comparar, realizar funciones lógicas y reunirlo en la **unidad aritmético-lógica**. Más adelante conectaremos la ALU con registros, buses y control, sin confundir un esquema didáctico con una computadora construida.

Fuentes primarias: Texas Instruments, *CD74HC283 High-Speed CMOS Logic 4-Bit Binary Full Adder with Fast Carry*, https://www.ti.com/lit/ds/symlink/cd74hc283.pdf; Texas Instruments, *SNx4HC86 Quadruple 2-Input XOR Gates*, https://www.ti.com/lit/ds/symlink/sn74hc86.pdf. Las tablas aritméticas y las cuatro figuras del capítulo se han elaborado para este libro.
