# Capítulo 4. Construir funciones con compuertas

*Parte II · Memoria digital elemental · Aula-Computadora*

En el capítulo anterior aprendimos a reconocer dos condiciones como 0 y 1. Una compuerta NAND recibía A y B y devolvía 0 únicamente cuando ambas eran 1. Ahora daremos el siguiente paso: diseñar la función que necesitamos, comprobarla con una tabla y elegir compuertas para realizarla. En una computadora no existe una compuerta distinta para cada pregunta de la vida cotidiana. Existen unas pocas operaciones que podemos combinar.

Imagina dos interruptores que informan si dos compartimentos están abiertos. Quizás queremos encender un testigo cuando **al menos uno** esté abierto. En otra aplicación puede interesarnos saber si **exactamente uno** lo está. Las entradas son las mismas; cambia la respuesta deseada. Este capítulo explica cómo convertir frases precisas en tablas, ecuaciones y conexiones lógicas sin confundir ese diseño abstracto con un circuito eléctrico ya validado.

## 1. Las mismas entradas pueden expresar preguntas diferentes

Tomaremos A y B como entradas de dos estados. A = 1 significa que se cumple la primera condición; B = 1 significa que se cumple la segunda. La salida Y también se representa por un bit. La palabra **significa** es importante: el 1 es el símbolo que asignamos a un estado lógico. Para conectarlo a una compuerta comercial habrá que respetar los niveles de tensión, alimentación y límites explicados en el capítulo 3.

Con dos entradas existen cuatro combinaciones, que ordenaremos siempre de forma 00, 01, 10 y 11. El resultado no se deduce mirando los números como si fueran cantidades decimales: depende de la función que estamos definiendo.

| A | B | Interpretación de la combinación |
|---|---|---|
| 0 | 0 | Ninguna condición se cumple |
| 0 | 1 | Solo la condición B se cumple |
| 1 | 0 | Solo la condición A se cumple |
| 1 | 1 | Ambas condiciones se cumplen |

Establecer el significado de las entradas antes de dibujar el circuito evita errores. Una señal A puede significar «puerta abierta» en un ejemplo y «puerta cerrada» en otro. Las compuertas no conocen esas palabras; solo aplican relaciones lógicas a sus entradas.

## 2. OR: basta con que ocurra una condición

La función **OR**, o disyunción inclusiva, devuelve 1 si A vale 1, si B vale 1 o si **ambas** valen 1. Solo devuelve 0 cuando no se cumple ninguna. En castellano la palabra «o» a veces significa «una cosa u otra, pero no ambas»; en álgebra booleana **OR incluye el caso 11**. Por eso conviene enseñar la tabla antes de confiar en una frase informal.

**Ecuación de OR:**

[[EQ:Y = A ∨ B]]

| A | B | Y = A ∨ B |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

Por ejemplo, si A es el aviso del primer sensor y B el del segundo, la función OR enciende un testigo cuando **cualquiera de los dos** se activa. Esto define una condición lógica, no garantiza que el testigo real pueda conectarse directamente a una salida: aún hacen falta resistencia, polaridad y capacidad de corriente adecuadas.

## 3. NOR: negar el resultado de OR

Podemos combinar una operación con la negación aprendida anteriormente. **NOR** significa NOT OR: devuelve el resultado contrario de OR. Solo produce 1 si A y B están en 0. Su símbolo es el de una OR con un pequeño círculo de negación en la salida.

**Ecuación de NOR:**

[[EQ:Y = ¬(A ∨ B)]]

| A | B | Y = ¬(A ∨ B) |
|---|---|---|
| 0 | 0 | 1 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 0 |

Observa en la figura 1 que OR y NOR reciben las mismas entradas, pero sus salidas se oponen en las cuatro filas. El círculo sobre la salida de una compuerta **representa una negación lógica**, no un componente que debamos añadir en serie a un cable.

[[FIG:c04_fig01_or_nor|Figura 1. OR y NOR: símbolos y comparación completa de sus cuatro resultados.|Dos compuertas OR y NOR con entradas A/B, círculo de negación en NOR y tabla de verdad contrastada.]]

**No confundas NOR con NAND.** NAND solo es 0 cuando A y B son 1; NOR solo es 1 cuando ambas son 0. Difieren, por ejemplo, en la fila 01: NAND = 1, mientras NOR = 0.

## 4. XOR: exactamente una condición, no dos

La función **XOR**, abreviatura de exclusive OR, es la «o exclusiva». Produce 1 cuando las entradas **son diferentes** y 0 cuando son iguales. Su símbolo habitual se parece al de OR, pero lleva una segunda línea curva junto a las entradas.

**Definición de XOR por desigualdad:**

[[EQ:Y = A ⊕ B]]

[[EQ:Y = 1  si y solo si  A ≠ B]]

| A | B | Y = A ⊕ B |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Piensa en dos interruptores que indican el estado de dos señales que deberían coincidir. Un testigo de **discrepancia** puede utilizar XOR: apagado si ambos informan 00 o 11; encendido si informan 01 o 10. Esto es un ejemplo lógico, **no** una propuesta certificada de seguridad de máquinas o detección de fallos de sensores.

La figura 2 destaca las dos filas que activan XOR. Compárala con la tabla OR: en la fila 11, OR devuelve 1 y XOR devuelve 0. Esa única diferencia basta para que dos circuitos respondan de manera distinta en una aplicación.

[[FIG:c04_fig02_xor_discrepancia|Figura 2. XOR detecta entradas distintas: 01 y 10 generan un testigo lógico de discrepancia.|Símbolo XOR con entradas A y B, salida D y tabla de verdad que destaca las filas 01 y 10.]]

## 5. De una tabla de verdad a una expresión

Hasta aquí conocemos tablas de funciones ya definidas. Pero ¿cómo se diseña una función nueva? Un método es señalar las filas en las que la salida deseada debe valer 1 y describir cada una con una condición AND. Después reunimos esas condiciones con OR.

Para XOR hay exactamente dos filas activas. En la fila 01 debemos exigir **NOT A y B**. En la fila 10 debemos exigir **A y NOT B**. Al unir ambas obtenemos:

**XOR escrito con AND, OR y NOT:**

[[EQ:A ⊕ B = (¬A ∧ B) ∨ (A ∧ ¬B)]]

Compruébalo con la fila 01: ¬A = 1 y B = 1, por tanto el primer término vale 1; el segundo vale 0. OR devuelve 1. En la fila 11 los dos términos valen 0, porque cada uno exige que una de las entradas esté negada. Así recuperamos la tabla de XOR sin usar aún una compuerta XOR comercial.

La expresión anterior recibe el nombre de **suma de productos**: los «productos» son conjunciones AND y la «suma» es una disyunción OR. Los nombres vienen del álgebra booleana; no indican que estemos sumando voltajes o multiplicando corrientes.

## 6. Una compuerta NAND puede construir XOR

El capítulo 3 mostró que NAND es funcionalmente completa: podemos construir NOT, AND y OR con ella. Como XOR acaba de escribirse usando esas operaciones, debe ser posible construir también XOR. Existe una realización especialmente útil con **cuatro NAND de dos entradas**. En vez de adivinar cables, daremos nombre a cada resultado intermedio.

**Primera NAND:**

[[EQ:N1 = NAND(A, B)]]

**Segunda NAND:**

[[EQ:N2 = NAND(A, N1)]]

**Tercera NAND:**

[[EQ:N3 = NAND(B, N1)]]

**Cuarta NAND, salida final:**

[[EQ:D = NAND(N2, N3) = A ⊕ B]]

Sigamos el caso **A = 1, B = 0**. Primero N1 = NAND(1,0) = 1. Luego N2 = NAND(1,1) = 0 y N3 = NAND(0,1) = 1. Finalmente D = NAND(0,1) = 1. El testigo de discrepancia se activa, como pedía la tabla XOR.

Con **A = 1, B = 1** ocurre lo contrario: N1 = NAND(1,1) = 0; N2 y N3 valen 1; D = NAND(1,1) = 0. La discrepancia desaparece porque las entradas son iguales.

La figura 3 conecta los cuatro bloques lógicos y nombra N1, N2, N3 y D. La línea N1 se **ramifica** hacia dos entradas de otras NAND; eso no significa que una compuerta tenga dos salidas independientes. Estamos repartiendo una misma señal lógica a dos destinos, siempre que la capacidad de carga del componente físico lo permita.

[[FIG:c04_fig03_xor_cuatro_nand|Figura 3. Un XOR construido con cuatro NAND: sigue N1, N2 y N3 hasta la salida D.|Red de cuatro compuertas NAND con entradas A/B, ramificación de N1 y salida D igual a XOR.]]

El SN74HCT00 del capítulo anterior contiene cuatro NAND de dos entradas. Eso significa que, **en el plano de la función lógica**, un solo integrado de ese tipo tiene suficientes compuertas para este XOR. La figura no es un plano de protoboard: para montarlo hay que identificar los pines exactos de las cuatro compuertas, alimentar el integrado, fijar entradas, añadir desacoplo y revisar cargas y condiciones eléctricas del fabricante.

## 7. Cómo comprobar la red completa sin memorizar su dibujo

Una red combinacional puede evaluarse siempre que sepamos sus conexiones y la operación de cada bloque. Empezamos por las señales que solo dependen de las entradas principales y seguimos en orden hasta la salida. En nuestra red, **N1 va antes de N2 y N3**; ambas van antes que D.

| Entradas AB | N1 | N2, N3 | D |
|---|---|---|---|
| 00 | 1 | 1, 1 | 0 |
| 01 | 1 | 1, 0 | 1 |
| 10 | 1 | 0, 1 | 1 |
| 11 | 0 | 1, 1 | 0 |

Esta tabla incluye señales internas que no aparecían en la definición abstracta de XOR. Es una forma sencilla de **diagnosticar**: si D es incorrecta, podemos comprobar si el error aparece ya en N1 o en una de las ramas posteriores. No hace falta describir el interior de los transistores de cada NAND para realizar este razonamiento lógico.

En la práctica, las compuertas no responden instantáneamente. Cada una tiene un **retardo de propagación**. Una red de varias etapas puede presentar cambios transitorios, especialmente si dos caminos tienen retardos diferentes. Las tablas de verdad describen estados estables ideales, no todos los detalles temporales. Antes de usar una salida como reloj, reset o señal de seguridad hacen falta análisis adicionales.

## 8. Simplificar significa conservar la tabla y reducir trabajo

Es posible describir una misma función con expresiones distintas. Considera una salida F que se activa si A y B son 1, **o** si A es 1 y B es 0. En lenguaje natural ya hay una pista: si A es 1, el resultado no depende de B.

**Expresión inicial:**

[[EQ:F = (A ∧ B) ∨ (A ∧ ¬B)]]

Aplicamos la **propiedad distributiva**: A aparece en los dos términos. Podemos sacarla como factor común.

[[EQ:F = A ∧ (B ∨ ¬B)]]

Como B y ¬B cubren todos los valores posibles, B ∨ ¬B = 1. Por tanto:

[[EQ:F = A ∧ 1 = A]]

No es magia algebraica. Comprueba las cuatro filas:

| Entradas AB | F inicial | F simplificada = A |
|---|---|---|
| 00 | 0 | 0 |
| 01 | 0 | 0 |
| 10 | 1 | 1 |
| 11 | 1 | 1 |

La figura 4 contrasta una expresión que requiere varios operadores con otra que solo necesita la señal A. **Ambas dan la misma respuesta lógica estable**, pero no necesariamente tienen idéntico retardo, consumo, comportamiento de arranque o características eléctricas en cualquier montaje. Por ello la simplificación booleana es el primer paso del diseño, no su certificación final.

[[FIG:c04_fig04_simplificacion|Figura 4. La función (A AND B) OR (A AND NOT B) se reduce lógicamente a A.|Comparación visual de la expresión original con dos ramas y su función simplificada igual a A.]]

## 9. Tres entradas y una función que sí podemos explicar

Diseñemos ahora una lámpara **indicadora lógica** para una actividad de laboratorio. A significa «sistema habilitado». B y C representan dos solicitudes independientes. Queremos Y = 1 únicamente cuando el sistema está habilitado **y** al menos una solicitud se ha activado. La expresión es:

[[EQ:Y = A ∧ (B ∨ C)]]

Esta vez tenemos tres entradas y, por tanto, **2³ = 8 combinaciones**. Para no perder filas, podemos contar de 000 a 111 como si los tres bits fueran un número binario; ese orden es solo una técnica para enumerar estados.

| ABC | B ∨ C | Y = A ∧ (B ∨ C) |
|---|---|---|
| 000 | 0 | 0 |
| 001 | 1 | 0 |
| 010 | 1 | 0 |
| 011 | 1 | 0 |
| 100 | 0 | 0 |
| 101 | 1 | 1 |
| 110 | 1 | 1 |
| 111 | 1 | 1 |

Es importante leer la fila 011: aunque B y C sean 1, A vale 0, de modo que Y debe permanecer en 0. Es un error común quedarse solo con la parte OR y olvidarse de la condición de habilitación. También es útil verificar la fila 111: OR es inclusiva, por lo que B ∨ C continúa valiendo 1 cuando ambas solicitudes están presentes.

Una realización directa puede utilizar primero una OR para B y C y luego una AND para combinar ese resultado con A. Más adelante podremos comparar una red equivalente de NAND o NOR. No hay que conectar físicamente la salida de una compuerta a una carga grande sin estudiar sus límites: **la expresión no informa la corriente disponible**.

## 10. Los errores que delatan una función mal entendida

Un error de **tabla** sucede antes de montar nada: escribir XOR = 1 para 11, por ejemplo. Un error de **implementación** ocurre cuando la tabla deseada es correcta pero una señal va al pin equivocado o una rama tiene la inversión equivocada. Y un error **eléctrico** aparece cuando la función lógica está bien pero el hardware no recibe tensiones válidas, presenta entradas flotantes, exceso de carga o alimentación incorrecta.

Las correcciones siguen ese orden: **primero especificación, después equivalencia, finalmente electrónica**. Podemos aislar las tres preguntas: ¿qué queremos?, ¿qué red calcula esa tabla?, ¿la pieza concreta respeta las condiciones de su ficha técnica?

Debes distinguir además la señal física de la interpretación que asignamos. Si llamamos D a la salida XOR, un 1 puede significar «entradas distintas». En otro programa el mismo bit podría significar «se solicita una acción». El circuito no conoce las palabras. Precisamente por eso hemos reservado un **capítulo puente futuro sobre el significado de los bits**, después de aprender registros y antes de entrar de lleno en memoria y programación.

## 11. Del cálculo de hoy a la memoria de mañana

Todas las redes estudiadas aquí son **combinacionales**: su salida estable depende de las entradas que reciben en ese momento. No recuerdan si ayer se activó un interruptor. Sin embargo, una computadora necesita recordar datos. El siguiente capítulo introducirá la **realimentación**: conectar la salida de un circuito de manera controlada para que su estado influya en lo que ocurrirá después. Allí aparecerá el primer dispositivo de memoria lógica del curso.

Antes de avanzar debes poder explicar en voz alta por qué OR y XOR no son iguales, cómo obtiene su resultado una red de cuatro NAND y cómo demostrar que una expresión simplificada mantiene la tabla original. Si puedes hacerlo sin depender del dibujo, ya estás razonando sobre **funciones digitales**.

## 12. Ejercicios para comprobar el mecanismo

**Ejercicio 1 — OR.** Escribe los resultados de OR para 00, 01, 10 y 11. Explica qué ocurre cuando ambas entradas son 1.

**Ejercicio 2 — NOR.** Construye la tabla de NOR negando, fila por fila, los resultados anteriores.

**Ejercicio 3 — XOR.** Escribe la tabla de la función «exactamente una entrada vale 1». ¿Qué filas producen 1?

**Ejercicio 4 — Distinguir OR de XOR.** Da una combinación que produzca resultados distintos y explica por qué.

**Ejercicio 5 — Comparación.** Para A = 1 y B = 0, calcula AND, NAND, OR, NOR y XOR.

**Ejercicio 6 — Expresión de discrepancia.** Escribe XOR usando solamente AND, OR y NOT, señalando qué término corresponde a 01 y cuál a 10.

**Ejercicio 7 — Cuatro NAND, primer recorrido.** Evalúa N1, N2, N3 y D para A = 1, B = 0 siguiendo las ecuaciones de la sección 6.

**Ejercicio 8 — Cuatro NAND, segundo recorrido.** Repite el cálculo con A = 1 y B = 1 y explica por qué D debe valer 0.

**Ejercicio 9 — Simplificación.** Simplifica F = (A ∧ B) ∨ (A ∧ ¬B). Demuestra con las cuatro filas que la expresión simplificada y la original son equivalentes.

**Ejercicio 10 — Tres entradas.** Para Y = A ∧ (B ∨ C), enumera 000, 001, 010, 011, 100, 101, 110 y 111. Escribe los ocho resultados en ese orden.

**Ejercicio 11 — Red física frente a tabla.** ¿Por qué dos redes con la misma tabla de verdad no garantizan la misma respuesta durante una transición rápida de entradas?

**Ejercicio 12 — Significado.** Si D = A ⊕ B y D vale 1, ¿qué sabes matemáticamente sobre A y B? ¿Puedes deducir solo por ese 1 si un dispositivo físico está averiado?

## Solucionario del capítulo 4

Resuelve los enunciados antes de consultar estas respuestas. Las tablas y ecuaciones describen **lógica ideal**; ninguna representa mediciones de un circuito comercial montado.

**1.** OR para 00, 01, 10 y 11: **0, 1, 1, 1**. La disyunción es inclusiva: con ambas entradas en 1, sigue produciendo 1.

**2.** NOR: **1, 0, 0, 0**. Cada salida es exactamente la negación del valor OR correspondiente.

**3.** XOR: **0, 1, 1, 0**. Las filas activas son 01 y 10, porque allí las entradas son diferentes.

**4.** En 11, OR = 1 y XOR = 0. OR permite ambas condiciones simultáneas; XOR exige que sean diferentes.

**5.** Para A = 1, B = 0: AND = 0, NAND = 1, OR = 1, NOR = 0 y XOR = 1.

**6.** A ⊕ B = (¬A ∧ B) ∨ (A ∧ ¬B). El primer término se activa en 01; el segundo, en 10.

**7.** N1 = NAND(1,0) = 1; N2 = NAND(1,1) = 0; N3 = NAND(0,1) = 1; **D = NAND(0,1) = 1**.

**8.** N1 = NAND(1,1) = 0; N2 = NAND(1,0) = 1; N3 = NAND(1,0) = 1; **D = NAND(1,1) = 0**. No hay diferencia entre las entradas.

**9.** F = A ∧ (B ∨ ¬B) = A. Las salidas para 00, 01, 10 y 11 son **0, 0, 1, 1** en ambas expresiones.

**10.** Para ABC desde 000 hasta 111: **0, 0, 0, 0, 0, 1, 1, 1**. Solo se activa si A = 1 y B o C también vale 1.

**11.** Las puertas reales tienen retardos de propagación y sus caminos pueden tardar tiempos distintos. La equivalencia de tablas se refiere a estados lógicos estables, no necesariamente a cada instante de transición.

**12.** D = 1 garantiza, en lógica ideal, que **A ≠ B**. No demuestra por sí sola una avería: también podría representar dos estados legítimamente diferentes o un error de interpretación de la aplicación.

