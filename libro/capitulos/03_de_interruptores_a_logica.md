# Capítulo 3. De interruptores a lógica

*Parte I · Electricidad y electrónica básica · Aula-Computadora*

En el capítulo anterior conseguimos que una señal eléctrica encendiera y apagara un LED mediante un transistor. Era un gran paso: ya no hacía falta mover manualmente un interruptor en la rama de la carga. Sin embargo, una computadora debe responder a **varias condiciones a la vez**. Por ejemplo: «continúa solamente cuando la máquina esté encendida **y** la puerta esté cerrada». ¿Cómo puede un circuito tomar esa decisión sin que una persona interprete las señales?

En este capítulo aprenderás a representar dos condiciones como 0 y 1, construir tablas de verdad, reconocer un inversor y explicar la función **NAND**. Al final conocerás un circuito integrado real de cuatro NAND, el SN74HCT00, y calcularás una resistencia de LED para observar una de sus salidas. Separaremos cuidadosamente lo que es **lógica ideal** de lo que garantiza un componente físico.

## 1. Dos respuestas y una pregunta nueva

Imagina un sistema que solo debe avisar cuando se cumplen **dos** condiciones: A indica que hay autorización; B indica que la puerta se encuentra cerrada. Cada condición puede describirse con dos estados: no cumplida o cumplida. Por convenio asignamos 0 y 1, respectivamente.

No estamos diciendo que «0» signifique necesariamente **0,000 V** en cualquier sistema ni que «1» signifique siempre **5,000 V**. Los números son una representación de estados. Para construir un circuito real necesitaremos determinar qué intervalos de tensión acepta una familia de componentes como entrada baja y alta.

La distinción importa. En la pizarra podemos escribir A = 1 sin más aclaraciones; sobre la protoboard debemos saber si ese 1 se está entregando dentro del intervalo eléctrico aceptado. Un voltaje intermedio no es un tercer valor de la tabla de verdad: puede significar una **entrada no garantizada**.

## 2. Antes de la compuerta: la tabla de verdad

Una **tabla de verdad** enumera todas las combinaciones posibles de las entradas y el resultado correspondiente. Con una sola entrada binaria existen dos combinaciones. Con dos entradas independientes existen cuatro: 00, 01, 10 y 11.

**Número de combinaciones binarias:**

[[EQ:Combinaciones = 2ⁿ]]

**Para dos entradas:**

[[EQ:Combinaciones = 2² = 4]]

La letra *n* representa la cantidad de entradas; no es el número de transistores ni la cantidad de terminales del circuito. Con tres entradas obtendríamos ocho combinaciones, aunque alguna función devuelva el mismo resultado en varias filas.

| Entrada A | Entrada B | Lectura de las condiciones |
|---|---|---|
| 0 | 0 | Ninguna condición se cumple |
| 0 | 1 | Solo B se cumple |
| 1 | 0 | Solo A se cumple |
| 1 | 1 | Ambas condiciones se cumplen |

La tabla no depende del orden en que un estudiante mueva las conexiones. Es una descripción **exhaustiva del comportamiento esperado** para todas las combinaciones. Esto la convierte en una herramienta para diseñar y también para buscar errores.

## 3. El inversor: responder lo contrario

Comencemos con una sola condición. La operación **NOT**, o negación, devuelve el valor opuesto al de su entrada. Si A vale 0, NOT A vale 1; si A vale 1, NOT A vale 0. Se representa mediante una barra sobre A o escribiendo **¬A**.

**Ecuación de la negación:**

[[EQ:Y = ¬A]]

| A | Y = ¬A |
|---|---|
| 0 | 1 |
| 1 | 0 |

Una interpretación cotidiana sería una alarma que se activa cuando **no** hay permiso de acceso. Pero debemos recordar qué se ha definido como 1: si A = 1 significa permiso presente, entonces Y = 1 significa permiso ausente. Elegir nombres precisos evita equivocaciones al convertir una tabla en cableado.

El transistor del capítulo 2 ya sugiere un mecanismo inversor: cuando activa el paso hacia GND, el colector puede ir a un potencial bajo. Pero nuestro circuito con un LED no era una salida lógica normalizada. Para construir un inversor eléctrico confiable deben elegirse carga, resistencias, márgenes y familia lógica. Por ahora conservamos el significado matemático de NOT sin afirmar que cualquier transistor conectado a una resistencia ya cumpla los niveles eléctricos de una compuerta comercial.

## 4. La condición que exige dos permisos: AND

La operación **AND** devuelve 1 únicamente cuando **ambas entradas** valen 1. Si falta una de las dos condiciones, el resultado es 0. Se expresa A ∧ B y también A · B.

**Ecuación de AND:**

[[EQ:Z = A ∧ B]]

| A | B | Z = A ∧ B |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

Piensa en dos interruptores ideales colocados en serie. Para que exista una ruta conductora, **los dos** deben estar cerrados. Esa imagen mental reproduce la tabla de AND y sirve para comprender por qué dos condiciones pueden combinarse mediante circuitos.

No obstante, un interruptor ideal en una figura de explicación no representa directamente el interior completo de un circuito integrado. Los transistores de verdad necesitan polarización, conexión adecuada a la alimentación y márgenes eléctricos. La figura 1 es un modelo de **conexión de condiciones**, no un esquema para montar dos NPN del capítulo anterior sin cálculos adicionales.

[[FIG:c03_fig01_serie_ideal|Figura 1. Dos interruptores ideales en serie: la ruta se cierra solo cuando A y B están cerrados.|Representación conceptual de dos interruptores ideales A y B conectados en serie entre un inicio y una carga: cuando cualquiera queda abierto, la ruta se interrumpe. Advertencia explícita de que no es un esquema de dos transistores montables.]]

## 5. NAND: negar el resultado de AND

Ahora cambiemos la pregunta. Queremos que la salida sea 1 cuando **no** se cumplan las dos condiciones simultáneamente. La operación se llama **NAND**, contracción de *NOT AND*. Primero hacemos AND y luego negamos ese resultado.

**Ecuación de NAND:**

[[EQ:Y = ¬(A ∧ B)]]

| A | B | AND: A ∧ B | NAND: Y |
|---|---|---|---|
| 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 0 |

La última columna es exactamente la opuesta de AND. No confundas **NAND** con **OR**: OR también vale 1 para 01, 10 y 11, mientras NAND vale **0** precisamente para 11. Es una diferencia pequeña en la tabla, pero decisiva en el circuito.

En los símbolos lógicos habituales, la NAND se reconoce por la forma de una AND y un **pequeño círculo en la salida**. Ese círculo indica negación. La figura 2 muestra el símbolo y la tabla correspondiente. Las señales se denominan A y B en la entrada y Y en la salida; no se representa ninguna fuente de energía dentro del símbolo lógico.

[[FIG:c03_fig02_nand_simbolo|Figura 2. Símbolo lógico de NAND y las cuatro filas de su tabla de verdad.|Símbolo de una compuerta NAND con entradas A y B a la izquierda y salida Y con burbuja de inversión a la derecha; junto a él, las combinaciones 00, 01, 10 y 11 y resultados 1, 1, 1, 0.]]

### 5.1. Cómo razonar cada fila sin memorizarla

En la fila 00 ninguna condición está activa, por tanto AND = 0; al negar, NAND = 1. En 01 o 10 solamente una condición está activa: AND continúa en 0, de modo que NAND continúa en 1. Solo en 11 las dos condiciones son verdaderas: AND = 1 y su negación produce NAND = 0.

Esta forma de razonar es más sólida que aprender de memoria cuatro filas. Cuando lleguemos a compuertas con tres o más entradas, podrás construir sus tablas aplicando exactamente el mismo criterio.

## 6. Por qué NAND resulta tan útil

Con compuertas NAND se pueden realizar otras operaciones lógicas. No significa que cada circuito físico deba estar hecho solo con NAND; significa que NAND es **funcionalmente completa** en el álgebra booleana: combinando sus salidas y entradas podemos implementar NOT, AND y OR, entre otras funciones.

Para obtener una negación basta **conectar la misma señal A a las dos entradas** de una NAND. Si A = 0, la tabla de NAND para 00 devuelve 1. Si A = 1, la tabla para 11 devuelve 0. Por tanto:

**Inversor construido con NAND:**

[[EQ:¬A = NAND(A, A)]]

Para obtener AND, negamos la salida de una primera NAND usando una segunda NAND con sus dos entradas unidas:

**AND a partir de dos NAND:**

[[EQ:A ∧ B = NAND(NAND(A, B), NAND(A, B))]]

Para OR aplicamos una identidad del álgebra de Boole llamada **ley de De Morgan**: A OR B es igual a negar (NOT A AND NOT B). Si producimos ¬A y ¬B con dos NAND, una tercera NAND recibe esos resultados:

**OR a partir de tres NAND:**

[[EQ:A ∨ B = NAND(NAND(A, A), NAND(B, B))]]

Estas expresiones son recetas lógicas, no instrucciones para enlazar libremente cualquier terminal eléctrico. El siguiente capítulo estudiará AND, OR, NOR y XOR con más detalle y comprobará sus relaciones mediante tablas.

## 7. Las señales lógicas deben tener límites eléctricos

Una puerta lógica ideal solo conoce 0 y 1. Una puerta comercial recibe tensiones físicas y garantiza determinados resultados **dentro de condiciones de operación especificadas**. Para fijar los términos, llamaremos VIL al máximo nivel de tensión que la entrada reconoce como bajo y VIH al mínimo nivel que reconoce como alto.

Si una tensión está **por debajo o igual a VIL**, el componente la reconoce como 0 lógico. Si está **por encima o igual a VIH**, la reconoce como 1 lógico. Entre ambos valores se encuentra una zona que **no tiene un nivel lógico garantizado**. No debemos inventar una tercera fila «medio» ni afirmar que siempre se interpretará como 0.

El intervalo y los niveles dependen de la familia elegida. No puedes trasladar sin revisión la tolerancia de una entrada TTL a otra CMOS de familia diferente. Además, las tensiones de salida que una puerta puede entregar como 0 y 1 son características distintas de los umbrales que **acepta como entrada**.

## 8. Una NAND comercial: SN74HCT00 de Texas Instruments

Para un ejemplo de montaje concreto tomamos como referencia el **SN74HCT00** de Texas Instruments, un circuito integrado que contiene **cuatro compuertas NAND de dos entradas**. En la variante **SN74HCT00N**, el encapsulado PDIP tiene 14 terminales. Se alimenta con 5 V nominales y la hoja de datos especifica un rango recomendado de **4,5 a 5,5 V**. No lo alimentaremos con la tensión máxima absoluta de la tabla de daños.

Según la hoja de datos del fabricante, para el intervalo de alimentación recomendado, una entrada se considera baja si **VIL ≤ 0,8 V** y alta si **VIH ≥ 2,0 V**. Estas desigualdades expresan las regiones válidas de entrada, no una supuesta condición de salida que pueda medirse en todos los montajes sin carga.

| Tensión aplicada a una entrada | Interpretación garantizada |
|---|---|
| 0 V a 0,8 V | Nivel bajo: 0 lógico |
| Mayor que 0,8 V y menor que 2,0 V | Región sin interpretación garantizada |
| 2,0 V a VCC | Nivel alto: 1 lógico |

La figura 3 representa **la vista superior** del PDIP-14 con muesca arriba, siguiendo la numeración indicada por el fabricante. Los terminales 1 y 2 son las entradas 1A y 1B de la primera compuerta; el terminal 3 es su salida 1Y; el terminal **7** es GND; y el **14** es VCC. La numeración de la figura es para el encapsulado indicado y debe revisarse si cambia el modelo.

[[FIG:c03_fig03_pines_74hct00|Figura 3. Vista superior del SN74HCT00N PDIP-14 y terminales de su primera NAND.|Encapsulado de 14 patas SN74HCT00N visto desde arriba con muesca: patas 1 y 2 son 1A y 1B, pata 3 es 1Y, pata 7 GND y pata 14 VCC. Se marcan las restantes patas de las otras tres NAND.]]

En el integrado, «cuatro compuertas» no significa cuatro entradas para **una sola** función. Son cuatro funciones NAND independientes, y cada una tiene **dos** entradas y **una** salida. Todas comparten alimentación y retorno. Esta diferencia también importa para conectar correctamente una protoboard.

## 9. Un LED que indica cuándo la salida NAND es cero

Queremos observar la primera NAND sin exigirle que entregue una corriente excesiva. Conectamos **VCC → resistor de 1 kΩ → ánodo de LED rojo → cátodo de LED → salida 1Y (pin 3)**. Es una indicación **activa en bajo**: cuando Y está cerca de GND, el integrado absorbe corriente a través del LED y este se ilumina. Cuando Y está alto, el LED queda prácticamente apagado.

Esta conexión invierte la interpretación visual intuitiva: **LED encendido no significa Y = 1**. En este montaje significa justamente que la salida Y está en su estado bajo. La tabla combina la función NAND y la observación del indicador:

| A (pin 1) | B (pin 2) | Y (pin 3) | LED activo en bajo |
|---|---|---|---|
| 0 | 0 | 1 | Apagado |
| 0 | 1 | 1 | Apagado |
| 1 | 0 | 1 | Apagado |
| 1 | 1 | 0 | Encendido |

La figura 4 hace explícita la polaridad del LED, su resistencia en serie y la alimentación del integrado. Las entradas A y B son **bornes que se conectan físicamente a 0 V o 5 V**; no quedan flotando. Un condensador cerámico de **100 nF** entre VCC y GND, lo más cerca posible del integrado, ayuda a desacoplar las variaciones rápidas de corriente durante la conmutación.

[[FIG:c03_fig04_nand_led|Figura 4. Primera NAND del SN74HCT00 con LED indicador activo en bajo.|Conexiones de la compuerta 1 del SN74HCT00: VCC pin 14 a 5 V, GND pin 7 a 0 V, entradas A pin 1 y B pin 2, salida Y pin 3 a cátodo del LED; ánodo de LED hacia resistencia de 1 kiloohmio y 5 V. Incluye condensador de 100 nF entre alimentación y GND.]]

### 9.1. Ecuación mágica de la resistencia del LED

La corriente del LED depende de su caída directa y de cuánto baja la salida del integrado cuando absorbe corriente. Para una **estimación inicial**, supongamos VCC = 5,0 V, LED rojo con caída de 2,0 V y salida baja VOL ≈ 0,3 V. El valor real de VOL depende de la corriente absorbida, tensión y temperatura; no afirmamos haberlo medido.

**Tensión estimada sobre la resistencia:**

[[EQ:VR ≈ VCC − VLED − VOL]]

[[EQ:VR ≈ 5,0 V − 2,0 V − 0,3 V = 2,7 V]]

**Corriente estimada del indicador:**

[[EQ:ILED ≈ (VCC − VLED − VOL) / R]]

[[EQ:ILED ≈ 2,7 V / 1 000 Ω = 0,0027 A = 2,7 mA]]

El SN74HCT00 especifica capacidad de salida de **±4 mA** dentro de las condiciones correspondientes de su ficha técnica. Nuestra estimación de 2,7 mA es menor que 4 mA, pero el resultado final debe revisarse con el voltaje de salida y los componentes físicos. No sustituyas 1 kΩ por 330 Ω sin volver a calcular: aumentarías la corriente requerida del integrado.

**Potencia estimada del resistor de 1 kΩ:**

[[EQ:PR ≈ ILED² × R]]

[[EQ:PR ≈ (0,0027 A)² × 1 000 Ω ≈ 0,00729 W]]

Son unos **7,29 mW**, muy por debajo de 0,25 W en la hipótesis adoptada. Ni el brillo exacto del LED ni su comportamiento a corrientes pequeñas pueden prometerse sin elegir un componente con hoja de datos. La lectura lógica de la salida debe comprobarse con un multímetro o instrumento apropiado, no solo por el brillo aparente.

## 10. Ensayar las cuatro combinaciones sin dejar entradas al aire

La práctica es **opcional**. Emplea una fuente de laboratorio regulada de 5 V con limitación de corriente, un SN74HCT00N PDIP-14 de procedencia conocida, protoboard, 1 kΩ de 1/4 W, LED rojo, condensador cerámico de 100 nF y cables. Para cada entrada se puede utilizar un selector que la conecte alternativamente a GND o a +5 V; esos selectores no deben unir ambos raíles entre sí. No usaremos red de 110/220 V ni baterías de litio improvisadas.

1. Con la alimentación **desconectada**, verifica la muesca y la numeración de la versión PDIP-14. Conecta el pin 14 a +5 V y el pin 7 a GND; coloca los 100 nF entre esos dos raíles cerca del chip.
2. Conecta las entradas del primer NAND: A al pin 1 y B al pin 2. Prepara dos puentes o selectores que permitan fijar cada entrada a **GND (0)** o a **+5 V (1)**. Comprueba que ninguna quede flotando antes de encender.
3. Conecta la resistencia de 1 kΩ desde +5 V al ánodo del LED, y el cátodo al pin 3. Comprueba la polaridad y recuerda que la luz será **activa en bajo**.
4. Fija las **seis entradas no usadas** de las otras tres compuertas (pines 4, 5, 9, 10, 12 y 13) a GND o VCC; deja sus salidas 6, 8 y 11 sin conectar. La hoja de datos advierte que las entradas no utilizadas deben estar en un nivel conocido.
5. Con A = 0 y B = 0, enciende la fuente y espera Y = 1 con LED apagado. **Apaga antes de mover cables**, fija 01, enciende y observa; repite con 10 y luego 11. Para 11 se espera Y = 0 y LED encendido.
6. Registra cada combinación observada y, si hay multímetro, mide la tensión de Y respecto de GND. No confundas lectura de tensión con medición de corriente: para medir voltaje se usan dos puntos en paralelo.

Con cualquier resultado inesperado, apaga primero la alimentación. Revisa conexiones del pin 7, pin 14, polaridad del LED, estado de entradas, sentido de la muesca y posibles cortos. **No conectes una salida directamente a +5 V o GND** como forma de comprobarla: el pin de salida es una ruta conducida por el chip, no una entrada para forzar niveles. Tampoco unas dos salidas entre sí sin una función expresamente diseñada.

## 11. Distinguir un error de tabla de un error eléctrico

Si tu tabla de verdad está equivocada, el problema es **lógico** y puede detectarse sin montar nada: basta recorrer las cuatro filas. Si la tabla es correcta, pero el LED no sigue lo esperado, el problema puede ser **eléctrico**: alimentación, límites, polaridad, entradas flotantes, salida sobrecargada o pieza distinta de la especificada.

| Observación | Comprobación inicial con la fuente apagada |
|---|---|
| LED siempre encendido | Revisar que A y B no estén ambos permanentemente en alto; confirmar Y conectado al cátodo |
| LED siempre apagado | Verificar polaridad del LED, resistor y ruta completa hacia la salida 1Y |
| Resultado distinto de NAND | Confirmar pin 1, pin 2, pin 3 y referencia común GND |
| Comportamiento errático | Revisar entradas flotantes, alimentación de 5 V y condensador de desacoplo |

Para diagnosticar con método, escribe primero la combinación A y B, predice Y con la ecuación NAND y solo después compara el LED y la tensión medida. Esto impide cambiar cables al azar hasta que una prueba parezca funcionar.

## 12. De una tabla a una computadora

Una puerta NAND puede decidir según **dos señales presentes**. Todavía no conserva información cuando esas señales cambian; no sabe qué ocurrió hace un segundo. El paso siguiente será combinar compuertas para expresar funciones más ricas. Después aprenderemos por qué la **realimentación** permite que una red de compuertas retenga un estado, incluso cuando cambia una de sus entradas.

La cadena de aprendizaje queda así: primero controlamos corriente con un transistor; después convertimos condiciones de entrada en resultados lógicos; más adelante podremos almacenar bits, reunirlos en registros y operar con ellos. La computadora deja de parecer una caja misteriosa cuando cada etapa responde a una necesidad concreta.

## Construimos Aula-8: la primera señal útil

Todavía no hay una CPU. Sin embargo, ya podemos reservar una tarea concreta para las compuertas que acabamos de estudiar: **permitir o impedir una acción**. Supón que un registro solo debe recibir un dato si una señal `LOAD` vale 1. Una compuerta puede participar en la lógica que genera esa autorización. No confundamos el resultado booleano `LOAD = 1` con el pulso eléctrico que hará que un flip-flop capture información; ese segundo mecanismo llegará con el reloj y la memoria de los capítulos 5 a 7.

La aportación de este capítulo es modesta pero real: sabemos deducir una señal desde entradas lógicas y verificar sus cuatro combinaciones. Cuando veamos la primera memoria Aula-8 volveremos a esta idea. El **SN74HCT00** es un ejemplo de integrado comercial que contiene NAND, pero aquí no hemos decidido aún qué NAND de un circuito completo desempeñará cada función ni hemos construido una placa de procesador.

## 13. Ejercicios para comprobar el mecanismo

**Ejercicio 1 — Combinaciones.** ¿Cuántas filas completas necesita la tabla de una función de dos entradas? ¿Y una función de tres entradas? Escribe primero la ecuación general.

**Ejercicio 2 — Inversor.** Completa los resultados de NOT A cuando A vale 0 y 1. ¿Por qué NOT no necesita dos entradas diferentes?

**Ejercicio 3 — Dos permisos.** Completa AND para 00, 01, 10 y 11. Explica verbalmente qué significa el último resultado.

**Ejercicio 4 — NAND.** A partir de AND, construye NAND negando cada resultado. Comprueba en qué fila AND y NAND se diferencian: ¿una o todas?

**Ejercicio 5 — Comparación.** ¿Por qué NAND no significa lo mismo que OR? Da al menos una combinación que las distinga.

**Ejercicio 6 — NAND como NOT.** Si conectas A a ambas entradas de NAND, calcula Y para A = 0 y para A = 1.

**Ejercicio 7 — NAND como AND.** Evalúa la expresión NAND(NAND(A, B), NAND(A, B)) para A = 1 y B = 1; repite con A = 0 y B = 1.

**Ejercicio 8 — Niveles físicos.** Con el SN74HCT00 alimentado en su rango especificado, clasifica 0,5 V, 1,2 V y 3,0 V como bajo garantizado, alto garantizado o región sin nivel garantizado.

**Ejercicio 9 — Patillaje.** En la variante SN74HCT00N PDIP-14, identifica VCC, GND, las entradas 1A/1B y la salida 1Y. Explica por qué se debe observar la muesca.

**Ejercicio 10 — LED activo en bajo.** ¿En cuál combinación A, B se enciende el LED de la figura 4? ¿Qué nivel toma entonces la salida Y?

**Ejercicio 11 — Resistencia del indicador.** Calcula ILED suponiendo VCC = 5,0 V, VLED = 2,0 V, VOL = 0,3 V y R = 1 000 Ω. Da amperios y miliamperios; calcula también la potencia de la resistencia.

**Ejercicio 12 — Seguridad de entradas.** ¿Qué ocurre con la garantía lógica si una entrada queda sin conexión? ¿Qué pines del chip no utilizados debemos fijar a GND o VCC?

## Solucionario del capítulo 3

Resuelve los ejercicios antes de consultar estas respuestas. Los números provienen de fórmulas y condiciones declaradas; **no son mediciones de un circuito armado**.

**1.** Número de combinaciones = 2ⁿ. Dos entradas: 2² = **4**; tres entradas: 2³ = **8**.

**2.** A = 0 → Y = 1; A = 1 → Y = 0. NOT opera sobre una condición, aunque pueda implementarse con dos terminales de NAND unidos al mismo valor.

**3.** AND en el orden 00, 01, 10, 11: **0, 0, 0, 1**. La última fila significa que los dos permisos están presentes.

**4.** NAND: **1, 1, 1, 0**. AND y NAND son opuestos en **las cuatro filas**; siempre difieren.

**5.** Para A = 1 y B = 1, OR produce 1, pero NAND produce **0**.

**6.** NAND(0,0) = 1 y NAND(1,1) = 0, por lo tanto NAND(A,A) = ¬A.

**7.** Si A = B = 1, la NAND interior devuelve 0 y NAND(0,0) devuelve **1**. Si A = 0 y B = 1, la interior devuelve 1 y NAND(1,1) devuelve **0**. Se reproduce AND.

**8.** 0,5 V: **bajo garantizado** (≤ 0,8 V). 1,2 V: **región no garantizada**. 3,0 V: **alto garantizado** (≥ 2,0 V), suponiendo alimentación dentro del rango indicado.

**9.** VCC = pin **14**, GND = pin **7**, 1A = pin **1**, 1B = pin **2**, 1Y = pin **3**. La muesca orienta la vista superior para no invertir la numeración física.

**10.** Se enciende con A = 1 y B = 1; entonces la NAND entrega **Y = 0**. El LED está conectado para conducir cuando la salida es baja.

**11.** ILED ≈ (5 − 2 − 0,3) / 1 000 = **0,0027 A = 2,7 mA**. PR ≈ (0,0027)² × 1 000 = **0,00729 W = 7,29 mW**.

**12.** Una entrada flotante no tiene nivel lógico garantizado y puede responder a perturbaciones. Deben fijarse las entradas no usadas **4, 5, 9, 10, 12 y 13** a GND o VCC; las salidas 6, 8 y 11 se pueden dejar sin conexión.

