# Capítulo 5. La realimentación conserva información

*Parte II · Memoria digital elemental · Aula-Computadora*

En el capítulo anterior aprendimos a diseñar una función: damos dos entradas a unas compuertas, recorremos sus conexiones y obtenemos un resultado. Eso sirve para responder «¿son diferentes A y B?» o «¿se cumple A y también B o C?». Pero una computadora necesita responder otra pregunta: **¿qué ocurrió antes?**. Si desaparece una señal que dio una orden, queremos que cierta información continúe presente hasta que llegue una orden contraria.

Una lámpara indicadora puede ayudarnos a imaginarlo. Un pulsador marca «activar» y otro «desactivar». Si la lámpara dependiese directamente del primer pulsador, se apagaría al soltarlo. En cambio, deseamos que **recuerde** la última orden válida. No estamos diseñando una alarma certificada ni una instalación doméstica; usamos ese comportamiento para estudiar el primer circuito de memoria del libro.

## 1. Una función combinacional no recuerda el pasado

Revisemos la compuerta NAND del capítulo 3. Con A = 1 y B = 1, su salida es 0; si A cambia a 0, la salida pasa a 1 después del retardo de propagación. No conserva por sí sola una decisión anterior.

[[EQ:Y(t) = NAND(A(t), B(t))]]

Aquí la letra *t* solo distingue el instante observado. En una red **combinacional**, la salida estable puede determinarse a partir de sus entradas actuales. La memoria exige algo más: que una señal dentro del circuito dependa también de un **estado anterior**.

Imagina que una señal SET solicita que un indicador pase a 1. Después la solicitud desaparece. Si el circuito sigue en 1, ya no podemos deducir su salida mirando solo la solicitud actual. Ese es el comportamiento que construiremos.

## 2. La idea de realimentación

La **realimentación** ocurre cuando una salida influye de nuevo en una entrada del sistema. No es sinónimo de memoria en todos los circuitos: existen realimentaciones que oscilan o que producen inestabilidad. Pero una conexión adecuada entre compuertas puede mantener uno de dos estados lógicos.

La figura 1 enfrenta una NAND aislada con dos NAND conectadas entre sí. Observa que la segunda recibe una señal de la primera, mientras la primera también recibe la salida de la segunda. Ya no existe un único camino de izquierda a derecha: ambas se influyen mutuamente.

[[FIG:c05_fig01_combinacional_realimentacion|Figura 1. Una función combinacional depende de sus entradas; una pareja realimentada puede conservar un estado.|A la izquierda, una NAND aislada con entradas A y B; a la derecha, dos bloques NAND que reciben realimentación cruzada y conservan Q y Q_n.]]

La memoria elemental que estudiaremos se llama **latch SR**: la letra S viene de *set* (poner en 1), y R de *reset* (poner en 0). *Latch* puede entenderse como un cerrojo lógico: responde a órdenes y mantiene una condición cuando esas órdenes dejan de estar presentes.

## 3. Las dos NAND de un latch SR activo en bajo

Para mantener continuidad con el capítulo 4 usaremos **dos compuertas NAND**. Sus entradas de control se llamarán `S_n` y `R_n`. La letra `n` recuerda que son **activas en bajo**:

- `S_n = 0`: ordenar que Q pase a 1 (*set*).
- `R_n = 0`: ordenar que Q pase a 0 (*reset*).
- `S_n = R_n = 1`: no ordenar cambio; conservar el estado anterior, si el latch ya está en un estado válido.

La salida principal es `Q`. La segunda salida, `Q_n`, debe ser su complemento en un **estado válido**: si Q vale 1, Q_n vale 0; si Q vale 0, Q_n vale 1. La letra `n` en las salidas no significa que debamos crear otro inversor: es el nombre que damos a la otra salida del par.

**Primera relación, para Q:**

[[EQ:Q = NAND(S_n, Q_n)]]

**Segunda relación, para Q_n:**

[[EQ:Q_n = NAND(R_n, Q)]]

Estas dos expresiones deben cumplirse **simultáneamente en el estado estable**. No podemos evaluarlas como si una salida se calculase una sola vez y la otra nunca pudiera reaccionar: la realimentación permite que los cambios se propaguen de una NAND a la otra hasta asentarse.

En la figura 2 las líneas que vuelven de cada salida hacia la NAND contraria son la clave. El dibujo representa relaciones lógicas; no pretende describir la física interna ni el recorrido temporal exacto de cada transición.

[[FIG:c05_fig02_latch_nand_cruzado|Figura 2. Latch SR con dos NAND y controles activos en bajo: S_n, R_n, Q y Q_n.|Dos bloques NAND; S_n entra en la NAND superior, R_n en la inferior, Q y Q_n realimentan la compuerta opuesta.]]

## 4. Orden SET: hacer que Q valga 1

Supón que inicialmente Q = 0 y Q_n = 1. Queremos **guardar un 1**. Aplicamos S_n = 0 y dejamos R_n = 1.

En la primera NAND hay una entrada 0, por lo que Q pasa a 1 con independencia del valor previo de Q_n:

[[EQ:Q = NAND(0, Q_n) = 1]]

Ese nuevo Q = 1 llega a la NAND inferior. Como R_n = 1, esta produce Q_n = NAND(1,1) = 0. Queda el estado válido **Q = 1, Q_n = 0**.

Ahora retiramos la orden: S_n vuelve a 1. Con las dos entradas de control en 1, las ecuaciones se satisfacen así:

[[EQ:Q = NAND(1,0) = 1]]

[[EQ:Q_n = NAND(1,1) = 0]]

¡Ahí está la memoria! El 1 de Q ya no necesita que S_n permanezca en 0. La red lo conserva por sus propias conexiones, mientras tenga alimentación y se mantengan las condiciones eléctricas válidas.

## 5. Orden RESET: hacer que Q valga 0

Hagamos el proceso contrario. Partimos de Q = 1 y Q_n = 0. Aplicamos **R_n = 0** y mantenemos S_n = 1. La NAND inferior fuerza Q_n = 1. Este valor entra en la NAND superior, que ahora devuelve Q = NAND(1,1) = 0.

[[EQ:Q_n = NAND(0, Q) = 1]]

[[EQ:Q = NAND(1,1) = 0]]

Cuando R_n vuelve a 1, la pareja conserva **Q = 0, Q_n = 1**. SET y RESET no requieren un reloj en este latch elemental: el dispositivo es **asíncrono**, porque responde a cambios de sus controles cuando ocurren, sujetos a los retardos reales.

Llamamos **un bit de memoria** a esa capacidad de mantener dos estados válidos distinguibles: Q = 0 o Q = 1. Que un circuito tenga dos salidas no implica que guarde dos bits independientes; Q_n está determinada por Q durante el funcionamiento válido.

## 6. La tabla de estados necesita el valor anterior

En una tabla combinacional bastaba poner las entradas actuales. Aquí hay una novedad: con S_n = R_n = 1, Q puede quedarse en 0 **o** quedarse en 1. Ambos resultados son correctos, según el estado que el circuito ya tenía. Por eso una tabla de un latch debe expresar la **retención del estado anterior**.

| S_n R_n | Q después de asentarse | Q_n después de asentarse | Interpretación |
|---|---|---|---|
| 0 1 | 1 | 0 | SET: guarda 1 |
| 1 0 | 0 | 1 | RESET: guarda 0 |
| 1 1 | Q anterior | Q_n anterior | HOLD: conserva un estado válido previo |
| 0 0 | 1 | 1 | Entrada prohibida: salidas no complementarias |

La figura 3 destaca que el caso 11 tiene dos posibilidades válidas distintas, no una salida arbitraria. En la última fila, ambas NAND reciben una entrada en 0 y fuerzan sus salidas a 1. **El estado 11 de las salidas no representa un bit válido**, porque Q y Q_n deberían ser complementarias.

[[FIG:c05_fig03_tabla_estados|Figura 3. SET, RESET y HOLD del latch NAND; la entrada 00 rompe la complementariedad de las salidas.|Tabla de cuatro combinaciones de S_n y R_n y los resultados Q, Q_n, resaltando HOLD y la entrada prohibida.]]

En una descripción abreviada podemos escribir:

[[EQ:Q_siguiente = Q_anterior   si   S_n = R_n = 1]]

Esta ecuación habla del **estado almacenado**, no de la tensión exacta en un instante de transición. Las salidas físicas necesitan tiempo para propagarse y asentarse.

## 7. Recorremos cinco momentos de un solo bit

La forma más clara de comprobar una memoria es seguir una **secuencia**. Supondremos un estado inicial **conocido Q = 0**, obtenido mediante RESET. Luego aplicaremos órdenes válidas, nunca S_n = R_n = 0 al mismo tiempo.

| Momento | S_n R_n | Orden | Q estable |
|---|---|---|---|
| t0 | 1 1 | Ninguna, Q inicial conocido | 0 |
| t1 | 0 1 | SET | 1 |
| t2 | 1 1 | Soltar SET, mantener | 1 |
| t3 | 1 0 | RESET | 0 |
| t4 | 1 1 | Soltar RESET, mantener | 0 |

En t2 y t4 las **entradas son iguales: 11**. Sin embargo, las salidas son distintas: en t2 Q = 1 y en t4 Q = 0. Esto demuestra que las entradas actuales ya no explican todo el circuito. Necesitamos conocer su historia.

La figura 4 presenta la secuencia sin inventar tiempos en nanosegundos. Las transiciones se dibujan como pasos lógicos ideales; un montaje real tendrá retardos y puede necesitar un tiempo de establecimiento antes de observar cada salida.

[[FIG:c05_fig04_secuencia_memoria|Figura 4. Una misma entrada 11 conserva Q = 1 después de SET y Q = 0 después de RESET.|Cinco momentos discretos muestran SET, HOLD, RESET y HOLD; dos entradas 11 idénticas conservan estados diferentes.]]

## 8. Qué pasa si activamos SET y RESET simultáneamente

En nuestro latch NAND, las órdenes se activan con 0. Si **S_n = 0 y R_n = 0**, ambas NAND fuerzan sus respectivas salidas a 1:

[[EQ:Q = NAND(0, Q_n) = 1]]

[[EQ:Q_n = NAND(0, Q) = 1]]

Durante esa condición estable, las salidas son **Q = 1 y Q_n = 1**. No es correcto presentar ese par como los complementos de un bit guardado. Por ello llamamos a 00 **entrada prohibida** para esta realización simple.

El problema más delicado aparece al **liberar ambas entradas a 1 casi al mismo tiempo**. Las dos NAND compiten por establecer la nueva pareja de salidas. Dependiendo de retardos y pequeñas diferencias físicas, el latch puede terminar guardando 0 o 1, y transitoriamente puede tardar en resolver su estado. No hay un resultado final que podamos garantizar con una tabla de lógica ideal. No intentamos calcular ese comportamiento analógico con las ecuaciones de 0 y 1.

Esta advertencia no quiere decir que el estado 00 produzca siempre «una salida aleatoria mientras está aplicado»: bajo el modelo NAND ideal, **fuerza 11 en las salidas**. La incertidumbre se vuelve crítica al retirarlo conjuntamente. Evitar esta condición es una regla del diseño, no un experimento de seguridad que recomendemos reproducir sin control.

## 9. ¿Con qué integrado podríamos identificar las conexiones?

El **SN74HCT00N PDIP-14** estudiado en el capítulo 3 contiene cuatro NAND de dos entradas. Dos de ellas bastan **lógicamente** para formar el latch. Esta tabla muestra una asignación de pines para quien quiera **leer el esquema**, no una garantía de funcionamiento de una protoboard determinada:

| Señal del latch | Pin SN74HCT00N | Función |
|---|---|---|
| S_n | 1 (1A) | Control SET a primera NAND |
| Q_n | 2 (1B) | Realimentación a primera NAND desde pin 6 |
| Q | 3 (1Y) | Salida primera NAND y realimentación al pin 5 |
| R_n | 4 (2A) | Control RESET a segunda NAND |
| Q | 5 (2B) | Realimentación desde pin 3 |
| Q_n | 6 (2Y) | Salida segunda NAND y realimentación al pin 2 |
| GND | 7 | Referencia de alimentación |
| VCC | 14 | Alimentación de 4,5 a 5,5 V según hoja de datos |

**Las rutas cruzadas importantes son pin 3 → pin 5 y pin 6 → pin 2.** El fabricante prescribe mantener las entradas no utilizadas a un nivel definido y recomienda un capacitor de desacoplo de 0,1 µF cerca de VCC. También debemos asegurar un nivel inicial conocido y señales de control que no floten; pulsadores mecánicos pueden rebotar y requieren una interfaz eléctrica apropiada. Las salidas no deben sobrecargarse.

Para pasar de la tabla a un componente real, conviene **mirarlo desde arriba** y localizar la muesca que fija el extremo del pin 1. La numeración desciende por el costado izquierdo de 1 a 7 y asciende por el derecho de 8 a 14; una inversión de esta vista altera todas las conexiones. La figura 5 muestra las catorce posiciones del encapsulado PDIP y resalta las señales usadas por las dos primeras NAND del latch.

[[FIG:c05_fig05_sn74hct00_patillaje|Figura 5. Patillaje del SN74HCT00N PDIP-14 visto desde arriba, con las patas de alimentación y las dos NAND del latch identificadas.|Vista superior del integrado con muesca, pins 1 a 14, funciones NAND, alimentación en 14 y 7, y recordatorio de puentes externos 3 a 5 y 6 a 2. Es un pinout contrastado con el fabricante, no una protoboard montada.]]

La figura ayuda a **leer conexiones reales** y a evitar colocar un cable en la pata equivocada; no muestra una protoboard completa porque los pulsadores, el desacoplo y los estados iniciales todavía requieren un esquema eléctrico escogido y comprobaciones propias.

Estas condiciones distinguen la función booleana de un circuito construible. **No se ha realizado montaje, medición, simulación de transistores ni comprobación de arranque eléctrico.** Los valores de alimentación y el patillaje se toman de Texas Instruments y no deben extrapolarse a cualquier NAND.

## 10. Guardar un bit no es todavía guardar un byte

El latch es una pieza fundamental, pero no una memoria de computadora lista para utilizar. Todavía faltan mecanismos para escoger **cuándo** puede cambiar el estado, para cargar varios bits coordinadamente y para dirigir datos por un bus. El capítulo 6 presentará un latch D y un flip-flop: allí distinguiremos señales de habilitación, reloj y flancos. El capítulo 7 reunirá varios bits en registros.

Hay también un asunto de **significado lógico**. Dentro del latch, Q = 1 expresa que fue retenida una condición de SET; Q = 0, que quedó retenida una condición de RESET. Ese significado existe en el hardware porque hemos definido las conexiones y reglas del circuito. Sin embargo, no dice todavía si la condición equivale a «una puerta abierta», una letra ASCII o un número. El capítulo puente propuesto tras el capítulo 7 abordará el salto desde significado lógico de hardware a representación de datos y semántica de software, y mencionará los objetos de programación como una abstracción posterior.

Antes de continuar debes explicar por qué las dos filas con entradas 11 pueden conservar resultados diferentes, y qué pierde el circuito cuando S_n y R_n se activan juntos. Son las dos ideas que separan una tabla combinacional de la primera memoria de nuestro curso.

## Construimos Aula-8: un bit que ya podemos conservar

Hasta aquí hemos estudiado el latch SR como un circuito independiente. Su relación con Aula-8 aparece cuando imaginamos una máquina detenida entre dos acciones: **necesitará conservar su estado**. Esta pareja de NAND nos demuestra que tal conservación es posible con realimentación, pero **no elegiremos un latch SR asíncrono como si ya fuera automáticamente el registro R0**. Un registro programable necesita una entrada de datos, una orden de carga y una relación clara con el reloj.

Por ahora conservemos una distinción que evitará un error posterior: la señal `Q` es *un bit guardado*; el conjunto de ocho bits que formará `R0` todavía requiere ocho elementos de memoria apropiados. El capítulo siguiente incorporará esa captura controlada en el tiempo. En el esquema acumulativo de la computadora podemos marcar **memoria de un bit: mecanismo entendido; registro de ocho bits: aún por construir**.

## 11. Ejercicios para comprobar la memoria

**Ejercicio 1 — Comparación.** Explica por qué la salida de una NAND aislada depende de las entradas actuales, pero Q de un latch puede depender del pasado.

**Ejercicio 2 — Polaridad.** ¿Qué significan S_n = 0 y R_n = 0 por separado? ¿Por qué no basta decir «1 significa activar»?

**Ejercicio 3 — SET.** Si inicialmente Q = 0, Q_n = 1 y se aplica S_n = 0, R_n = 1, calcula Q y Q_n en estado estable mediante las dos NAND.

**Ejercicio 4 — Retención tras SET.** Después del ejercicio anterior se aplican S_n = R_n = 1. ¿Qué valores conservan Q y Q_n? Sustitúyelos en ambas ecuaciones.

**Ejercicio 5 — RESET.** Partiendo de Q = 1, Q_n = 0, se aplica S_n = 1, R_n = 0. Calcula el nuevo estado.

**Ejercicio 6 — Retención tras RESET.** Tras soltar R_n a 1, ¿por qué Q permanece en 0?

**Ejercicio 7 — Secuencia.** Con Q inicial conocido igual a 0, enumera Q estable para las entradas S_n R_n: 11, 01, 11, 10, 11.

**Ejercicio 8 — Entrada prohibida.** Con S_n = R_n = 0, calcula las salidas ideales. ¿Por qué no son las salidas normales de un bit guardado?

**Ejercicio 9 — Liberación simultánea.** ¿Podemos garantizar si Q será 0 o 1 después de liberar conjuntamente S_n y R_n desde 00 a 11? Justifica.

**Ejercicio 10 — Pines.** En la asignación del SN74HCT00N, ¿qué pines llevan Q y Q_n? ¿Qué dos conexiones permiten la realimentación cruzada?

**Ejercicio 11 — Dos latches.** Si construimos dos latches SR independientes y ambos están en estados válidos conocidos, ¿cuántas combinaciones de sus salidas principales Q1 y Q2 pueden representar?

**Ejercicio 12 — Semántica lógica.** ¿Qué significa Q = 1 dentro del circuito, y por qué no demuestra por sí solo que «una puerta física está abierta»?

## Solucionario del capítulo 5

Las respuestas se refieren a **estados estables ideales**; nunca prueban un dispositivo comercial cableado.

**1.** Una NAND aplica una función fija a sus entradas actuales. El latch realimenta Q y Q_n entre sí: para S_n R_n = 11 conserva uno de dos pares de valores según su historia.

**2.** S_n = 0 solicita SET y R_n = 0 solicita RESET. Son señales **activas en bajo**: aquí 0 significa «orden activa», según el contrato del circuito.

**3.** Q = NAND(0,1) = 1; luego Q_n = NAND(1,1) = 0. Resultado estable **(Q,Q_n) = (1,0)**.

**4.** Q = NAND(1,0) = 1 y Q_n = NAND(1,1) = 0. Permanece (1,0) aunque SET esté inactivo.

**5.** Q_n = NAND(0,1) = 1; luego Q = NAND(1,1) = 0. Estado (0,1).

**6.** Q_n = NAND(1,0) = 1 y Q = NAND(1,1) = 0: las dos salidas se sostienen mutuamente.

**7.** Para 11, 01, 11, 10, 11 con Q inicial 0: **0, 1, 1, 0, 0**.

**8.** Q = 1 y Q_n = 1. No son complementarias y, por tanto, no representan un estado válido para el bit retenido.

**9.** **No.** Liberar simultáneamente puede producir una carrera entre caminos y el estado final depende de detalles físicos; pueden existir transitorios de resolución.

**10.** Q sale por el **pin 3** y Q_n por el **pin 6**. Las realimentaciones son **3 → 5** y **6 → 2**.

**11.** Dos bits independientes admiten **2² = 4** combinaciones: 00, 01, 10 y 11. No confundir cada Q_n, que es complementaria de su Q, con un bit adicional.

**12.** Q = 1 significa que el latch quedó en el estado de SET según su lógica. Una aplicación puede asociarlo a un sensor, pero la correspondencia, polaridad, funcionamiento del sensor y validez de su lectura requieren información adicional.

