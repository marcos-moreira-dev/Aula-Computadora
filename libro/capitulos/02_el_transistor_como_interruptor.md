# Capítulo 2. El transistor como interruptor

*Parte I · Electricidad y electrónica básica · Aula-Computadora*

El LED del capítulo anterior podía encenderse mientras su circuito estuviera conectado. Para apagarlo, había que interrumpir un cable o utilizar un interruptor manual. Una computadora necesita algo diferente: **que una señal eléctrica controle el estado de otra ruta eléctrica**. Ese es el problema que vamos a resolver.

Al terminar, podrás explicar la función de base, colector y emisor de un transistor bipolar NPN; distinguir corte y saturación; conectar un LED controlado por una señal de 0 V o 5 V; calcular las dos resistencias necesarias; e identificar por qué un transistor puede conducir mal incluso cuando parece estar encendido. Partimos de tensión, corriente, potencia y resistencia del capítulo 1.

## 1. El interruptor que no necesita una mano

Un interruptor mecánico abre o cierra una conexión cuando lo movemos. El transistor permite controlar el paso de corriente mediante una entrada eléctrica. La señal que llega a la entrada puede provenir de otro circuito y, más adelante, de una compuerta lógica o de un registro.

No todos los transistores funcionan igual. En esta práctica utilizaremos uno **bipolar de unión, tipo NPN**; después compararemos su idea básica con un transistor de efecto de campo MOSFET. La distinción importa: los métodos de control y las especificaciones de ambas familias no son intercambiables.

El montaje seguirá trabajando con corriente continua de 5 V, un LED rojo y resistencias. Elegiremos una conexión llamada **interruptor del lado bajo**: la carga queda entre el positivo y el transistor, mientras que el transistor conecta la carga al retorno. Es un circuito introductorio muy común porque permite ver claramente dos caminos de corriente.

## 2. Tres terminales y dos caminos

Un transistor NPN tiene tres terminales que llamaremos **B** (base), **C** (colector) y **E** (emisor). Conviene distinguir sus responsabilidades antes de mirar ningún dibujo: el colector recibe la corriente que atraviesa la carga; el emisor proporciona la ruta de retorno; la base recibe una corriente de control limitada por su propia resistencia.

El primer camino atraviesa la carga y después el transistor, aproximadamente desde el colector hacia el emisor. El segundo atraviesa una resistencia de base y la unión base-emisor. La corriente de base ayuda a controlar la conducción del camino del colector. En el tipo de conexión que estudiaremos, **los dos caminos comparten el retorno GND**.

Un NPN no es simplemente «un cable que se abre al recibir 0 V y se cierra al recibir 5 V». Su estado depende de la diferencia de potencial **entre base y emisor**, de la corriente de base, de la carga y de los límites eléctricos del transistor. Precisamente por eso añadimos resistencias y hacemos cálculos.

### 2.1. Corte: la ruta principal queda interrumpida

Cuando la base se mantiene al mismo potencial que el emisor, aproximadamente 0 V en nuestro montaje, la unión base-emisor no recibe la polarización directa necesaria para establecer una corriente apreciable. El transistor queda en **corte**. En condiciones normales, la corriente de la carga es despreciable para esta práctica y el LED permanece apagado.

La expresión «no pasa corriente» es una idealización útil. Un componente real puede presentar corrientes de fuga pequeñas y capacitancias internas; no prometemos un aislamiento perfecto ni un interruptor que cambie de estado en tiempo cero.

### 2.2. Saturación: una ruta de baja caída de tensión

Cuando aplicamos una señal positiva a la base **a través de un resistor**, aparece corriente en la unión base-emisor. Si es suficiente para la corriente que exige la carga, el transistor puede entrar en **saturación**. Entonces la tensión entre colector y emisor se vuelve pequeña y el transistor se comporta aproximadamente como un interruptor cerrado, sin ser un cortocircuito ideal.

Llamaremos a esa pequeña caída **VCE(sat)**. En nuestro ejemplo emplearemos 0,2 V como hipótesis de cálculo. Ese número depende del componente, de las corrientes, de la temperatura y de las condiciones de prueba de la hoja de datos; no es una propiedad universal de todos los transistores.

### 2.3. La región intermedia también existe

Si la base recibe algo de corriente, pero no la suficiente para llevar al transistor a saturación con la carga conectada, el dispositivo puede operar en una **región activa**. El colector conduce, pero la caída entre colector y emisor puede ser apreciable. En un interruptor que pretende estar «encendido», esto representa una pérdida de tensión y potencia que debemos tener en cuenta.

La región activa es valiosa en circuitos amplificadores; aquí queremos dos estados de funcionamiento bien diferenciados. No basta constatar que el LED emite algo de luz para concluir que el transistor está correctamente saturado.

## 3. Un transistor real: 2N3904

Para dejar de hablar de un transistor imaginario, elegimos como **referencia de estudio** el **2N3904 de onsemi**, un NPN de señal pequeña. Su hoja de datos permite justificar las corrientes y la tensión de saturación utilizadas; el diseño no depende de que debas comprar exactamente esta marca.

| Dato de la hoja de datos onsemi | Condición indicada | Lectura correcta |
|---|---|---|
| VCE máxima 40 V | Tensión colector-emisor | Límite absoluto, no valor habitual de trabajo |
| IC continua máxima 200 mA | Colector | Límite absoluto, no corriente recomendada |
| VCE(sat) máxima 0,2 V | IC = 10 mA; IB = 1 mA | Dato válido bajo esa condición de prueba |
| VBE(sat) de 0,65 a 0,85 V | IC = 10 mA; IB = 1 mA | Rango de esa prueba; 0,7 V será una aproximación |

El componente puede encontrarse en encapsulado plástico **TO-92**, con tres patas. La figura 1 representa la identificación **1 = emisor, 2 = base, 3 = colector** indicada en la hoja de datos del 2N3904 de onsemi. Esta vista sirve para estudiar ese encapsulado; **no debes memorizarla como regla para todos los NPN**. Otros fabricantes o encapsulados pueden ordenar sus patas de manera distinta. La orientación de lectura del dibujo también importa, por lo que conviene comparar físicamente la pieza con su documentación antes de conectarla.

[[FIG:c02_fig01_bce_pinout|Figura 1. Terminales del 2N3904 de onsemi y función de cada conexión.|Vista explicativa del encapsulado TO-92 onsemi 2N3904, con tres terminales numerados: 1 emisor, 2 base, 3 colector. A la derecha se resume su función, y se advierte que no debe generalizarse el patillaje.]]

La figura separa dos preguntas que suelen confundirse: «¿qué función tiene un terminal?» y «¿en qué pata física se encuentra?». La primera se responde con B, C y E; la segunda exige el modelo comercial y la vista correcta del encapsulado.

Un dato de catálogo tampoco es una medición del montaje. Que el fabricante indique VCE(sat) de hasta 0,2 V bajo una condición concreta **no demuestra automáticamente** que nuestro circuito tenga exactamente esa caída. Utilizaremos ese valor como una referencia razonable para desarrollar el ejemplo; después explicaremos cómo comprobar el circuito físicamente.

## 4. El LED controlado por una señal

Conservamos la fuente de 5 V, la resistencia de **330 Ω** y el LED rojo del capítulo 1. Agregamos el transistor Q1 y una segunda resistencia de **4,7 kΩ**, que limita la corriente hacia la base. El extremo libre de esta última resistencia constituye la entrada de control **IN**.

El circuito se organiza en dos ramas funcionales. En la rama de la carga, la corriente sale del positivo, atraviesa los 330 Ω, pasa por el LED, entra al colector de Q1, sale por su emisor y vuelve a GND. En la rama de control, una señal de 5 V llega a IN, atraviesa los 4,7 kΩ, entra a la base y regresa por el emisor. La fuente y la señal **deben compartir referencia GND**.

En la figura 2, **IN se conecta al positivo de 5 V** mediante un puente externo. No dibujamos ese puente sobre el trayecto principal para que los caminos se distingan: los bornes de IN y GND representan conexiones reales que deben hacerse según el procedimiento, no conexiones inalámbricas. El LED aparece iluminado porque estamos representando el estado de saturación previsto.

[[FIG:c02_fig02_npn_encendido|Figura 2. Interruptor NPN con IN a 5 V y LED encendido.|Circuito de 5 V con resistor de 330 ohmios, LED rojo y transistor NPN Q1 en serie por colector y emisor. La base recibe IN a cinco voltios mediante resistor de 4,7 kiloohmios; se indica saturación como estado calculado.]]

Si ahora llevamos IN a GND, **con la fuente apagada durante el cambio de cable**, la diferencia base-emisor cae aproximadamente a 0 V. En la figura 3 se muestra esa condición y el LED apagado. No quitamos ni invertimos el resistor de 330 Ω; la carga permanece conectada tal como antes. Lo que cambió fue la polarización del transistor.

[[FIG:c02_fig03_npn_apagado|Figura 3. Interruptor NPN con IN a 0 V y LED apagado.|El mismo circuito del LED y transistor NPN, pero con la entrada IN conectada a cero voltios mediante la resistencia de base; el estado de Q1 es corte y la corriente de colector se aproxima a cero.]]

Conviene comparar las figuras antes de avanzar: **las posiciones del LED, del resistor de carga, del colector y del emisor no cambiaron**. Únicamente cambiamos la tensión aplicada a la base a través de su resistencia. Esa capacidad de cambiar el estado de otra rama es la idea que necesitaremos para construir funciones lógicas.

## 5. Calcular la corriente de la carga

Empecemos con la rama que enciende el LED. Para el estado encendido usaremos tres supuestos explícitos: fuente regulada de 5,0 V; caída directa del LED rojo de aproximadamente 2,0 V; y tensión colector-emisor en saturación de aproximadamente 0,2 V.

La tensión que queda en la resistencia de 330 Ω es la tensión de fuente **menos las otras dos caídas**. Esta es la ecuación general antes de sustituir valores:

**Tensión sobre la resistencia de carga:**

[[EQ:Vᵣ = Vfuente − VLED − VCE(sat)]]

[[EQ:Vᵣ ≈ 5,0 V − 2,0 V − 0,2 V = 2,8 V]]

Aplicamos la ley de Ohm **a esa resistencia**, no al transistor completo:

**Corriente estimada del colector y del LED:**

[[EQ:IC ≈ (Vfuente − VLED − VCE(sat)) / RLED]]

[[EQ:IC ≈ 2,8 V / 330 Ω ≈ 0,00848 A ≈ 8,48 mA]]

Los aproximadamente 8,48 mA atraviesan el LED y el colector porque están en la misma rama. En el capítulo 1 habíamos calculado 9,09 mA sin transistor. La diferencia tiene sentido: ahora parte de los 5 V cae entre colector y emisor, de modo que queda algo menos de tensión para los 330 Ω.

El resultado depende de nuestras hipótesis. Si el LED real cae 1,8 V o 2,2 V, su corriente cambiará. Cuando se mida, esos valores deberán anotarse como **mediciones**, no como una supuesta confirmación automática de los números del libro.

## 6. Calcular la corriente de la base

La base y el emisor de un BJT de silicio conducen de manera semejante a una unión semiconductora polarizada directamente. Para estimar la corriente de base suponemos que **VBE es aproximadamente 0,7 V**. Utilizaremos una resistencia de 4 700 Ω, equivalente a 4,7 kΩ.

**Tensión aproximada sobre la resistencia de base:**

[[EQ:VRB = VIN − VBE]]

[[EQ:VRB ≈ 5,0 V − 0,7 V = 4,3 V]]

**Corriente aproximada de base:**

[[EQ:IB ≈ (VIN − VBE) / RB]]

[[EQ:IB ≈ 4,3 V / 4 700 Ω ≈ 0,000915 A ≈ 0,915 mA]]

La base no debería conectarse directamente al positivo sin esa resistencia. Su unión no tiene una resistencia fija que pueda utilizarse para limitar con seguridad la corriente. El resistor establece una condición de control calculable.

En un interruptor saturado interesa que la base reciba **corriente suficiente**, sin obligar al transistor a disipar más energía de la necesaria. Una comprobación sencilla consiste en comparar la corriente de colector prevista con la corriente de base prevista.

**Relación de corrientes para el diseño de conmutación:**

[[EQ:βforzada = IC / IB]]

[[EQ:βforzada ≈ 8,48 mA / 0,915 mA ≈ 9,27]]

Obtenemos una relación cercana a 10. La hoja de datos onsemi especifica una caída de saturación máxima de 0,2 V cuando IC = 10 mA e IB = 1 mA: ese ensayo también emplea una relación de 10. **La coincidencia es un criterio de diseño**, no una garantía de que las condiciones de nuestro LED sean idénticas al ensayo del fabricante.

No confundas esta relación forzada de conmutación con la ganancia de corriente hFE medida en la región activa. Un valor hFE = 100 no significa que debamos usar siempre IC/100 para saturar un interruptor. Para conmutación conviene dar margen a la corriente de base y contrastarlo con los datos de saturación del componente.

## 7. Potencia y límites: los transistores también se calientan

La resistencia de carga conduce aproximadamente 8,48 mA. Podemos calcular su disipación sin inventar una medición:

**Potencia de la resistencia de 330 Ω:**

[[EQ:PLEDresistencia ≈ IC² × RLED]]

[[EQ:PLEDresistencia ≈ (0,00848 A)² × 330 Ω ≈ 0,0238 W]]

El resultado, unos 23,8 mW, está por debajo de los 250 mW de un resistor nominal de 1/4 W, considerando las condiciones adecuadas de empleo. La resistencia de base también disipa energía:

**Potencia de la resistencia de 4,7 kΩ:**

[[EQ:PBresistencia ≈ IB² × RB ≈ 0,00394 W]]

Para el transistor, una primera aproximación de la potencia en el camino colector-emisor es VCE × IC, que con 0,2 V y 8,48 mA da aproximadamente 1,7 mW. También existe una contribución pequeña de base-emisor, VBE × IB, del orden de 0,64 mW. La potencia total estimada del transistor sería entonces cercana a 2,3 mW. Estos cálculos sirven para comparar órdenes de magnitud, **no sustituyen una revisión térmica para cualquier otra carga**.

Observa una consecuencia: si el transistor no satura y VCE sube, por ejemplo, hasta 1 V, no podemos conservar sin cambios el cálculo de corriente de 8,48 mA. Habría que volver a repartir los 5 V entre LED, resistor y transistor. Esa es una de las razones para medir VCE cuando intentamos determinar si un interruptor está correctamente encendido.

## 8. La tabla de estados del interruptor

Un transistor real tiene un comportamiento continuo, pero para operar como interruptor lo conducimos hacia dos condiciones diferenciadas. La tabla siguiente describe **el circuito concreto** que acabamos de calcular, suponiendo una alimentación correcta y componentes dentro de sus especificaciones.

| Entrada IN | Condición esperada de Q1 | LED | Corriente de carga |
|---|---|---|---|
| 0 V respecto de GND | Corte | Apagado | Aproximadamente 0 mA |
| 5 V respecto de GND | Saturación prevista | Encendido | Aproximadamente 8,5 mA |

Esta tabla es útil porque vincula una **entrada** con una **consecuencia observable**. Sin embargo, el LED no se enciende mágicamente por detectar el número «1». Se enciende porque una polarización adecuada de la base permite que circule la corriente de la rama de la carga.

También conviene distinguir dos posibles salidas: la **luz del LED** y la **tensión en el colector**. Cuando Q1 está encendido y saturado, el colector se aproxima a un potencial bajo respecto del emisor. Cuando está apagado, la tensión exacta del colector en este montaje con LED no debe confundirse automáticamente con un «1 lógico de 5 V»: hay una unión no lineal en serie y pueden existir fugas. En el próximo capítulo definiremos salidas lógicas con niveles y condiciones explícitas.

## 9. Una práctica opcional que puede hacerse por etapas

**Materiales:** fuente de laboratorio regulada a 5 V de corriente continua y con limitación ajustable; LED rojo de especificación conocida; resistor de 330 Ω y resistor de 4,7 kΩ, ambos de al menos 1/4 W; transistor 2N3904 **con hoja de datos correspondiente a su fabricante**; protoboard, cables y, opcionalmente, multímetro. Para este circuito de referencia el consumo nominal calculado en estado encendido ronda 9,4 mA entre carga y base; un límite de fuente de alrededor de 15 mA ofrece una protección preliminar, pero debes comprobar el límite admisible de **todas** las piezas.

1. Con la fuente **apagada**, identifica B, C y E comparando el transistor real con la hoja de datos de su fabricante. Si no puedes determinar la orientación física de las patas, no lo energices.
2. Conecta +5 V a los 330 Ω; el otro extremo al ánodo del LED; el cátodo al colector C; y el emisor E al retorno GND. Mantén las conexiones cortas y comprueba que no existan puentes directos entre +5 V y GND.
3. Conecta una resistencia de 4,7 kΩ a la base B. El extremo restante será IN. **Antes de encender**, lleva IN al GND de la misma fuente. No dejes IN flotando: un terminal sin referencia puede producir un comportamiento inestable.
4. Configura 5 V y limitación de corriente sin exceder las especificaciones, energiza y observa el LED apagado. Apaga la fuente antes de cambiar el puente de IN.
5. Con la alimentación apagada, cambia IN desde GND hacia el positivo +5 V. Enciende y espera que el LED se ilumine. Apaga de nuevo para dejar IN a GND. Repite solo si el montaje no presenta calentamiento ni fallos.

Si no tienes fuente de laboratorio o piezas con documentación confiable, estudia los dos estados sobre las figuras y haz los ejercicios. No necesitas reproducir físicamente el circuito para entender su mecanismo. **No conectes este montaje a la red doméstica**, no improvises conexiones desde baterías de litio, y no utilices motores o relés como sustitutos del LED: una carga inductiva exige protecciones adicionales que aún no hemos estudiado.

### 9.1. ¿Qué mediríamos con un multímetro?

Primero recuerda la regla del capítulo anterior: **tensión en paralelo, corriente en serie**. Para verificar el estado encendido resulta útil medir la tensión entre C y E con el multímetro en V CC, sin interrumpir la carga. Un valor pequeño sería compatible con saturación; el criterio final depende de la hoja de datos y de las condiciones reales. También puedes medir VBE y la tensión sobre el resistor de 330 Ω.

Si mides una caída aproximada de 2,8 V en los 330 Ω, la ley de Ohm da una estimación de 2,8/330 ≈ 8,48 mA. Así podemos **inferir** la corriente sin introducir un amperímetro en la rama. Las resistencias y los instrumentos tienen tolerancias; registra siempre valores reales, unidades y modo de conexión.

Una lectura inesperada no autoriza a retirar la resistencia de base ni a cortocircuitar el LED para «ver si responde». Apaga, inspecciona el orden de terminales, revisa las referencias de GND y vuelve a calcular el circuito que realmente hayas montado.

## 10. Averías: diagnosticar antes de mover cables

| Síntoma | Sospecha razonable | Revisión con alimentación apagada |
|---|---|---|
| LED siempre apagado | C y E invertidos; LED al revés; IN sin 5 V | Patillaje, polaridad y continuidad |
| LED siempre encendido | IN no alcanza 0 V; cableado accidental | Verificar el puente IN-GND |
| Luz débil al activar IN | Corriente de base insuficiente; fuente limitada | Comprobar valores, fuente y modelo de transistor |
| Calentamiento o caída anormal | Corto, valor equivocado o mala conexión | Desconectar y seguir cada rama del circuito |

No uses únicamente el brillo para decidir si un transistor está en saturación. En un caso intermedio el LED puede emitir luz y, sin embargo, la tensión C-E ser mayor de lo deseado. Tampoco confundas el pin 1 con «el terminal que está siempre a la izquierda» sin aclarar desde qué vista se observa el encapsulado.

## 11. ¿Y el MOSFET?

Un **MOSFET** es otro tipo de transistor, cuyo nombre completo proviene de *metal-oxide-semiconductor field-effect transistor*. Para un MOSFET de canal N, sus terminales principales se llaman **G** (gate o puerta), **D** (drain o drenador) y **S** (source o fuente). Puede utilizarse también como interruptor del lado bajo, pero su control se basa principalmente en la **tensión entre puerta y fuente**, no en suministrar una corriente de base como en el BJT.

No significa que «a cualquier MOSFET se le aplican 5 V en la puerta y funciona». La especificación **VGS(th)** solo indica una condición de comienzo de conducción medida con una corriente determinada; por sí sola no garantiza que el MOSFET conduzca nuestra carga con una resistencia drenador-fuente baja. Para escogerlo se revisa **RDS(on)** a una VGS concreta, junto con límites de corriente, disipación, tensión y encapsulado.

Por eso el ejercicio principal usa un NPN documentado y no una mezcla de transistores indistintos. Más adelante veremos por qué los circuitos digitales integrados modernos suelen utilizar MOSFET, y qué condiciones deben cumplirse para que una señal pueda considerarse un cero o un uno confiable.

## 12. Por qué esto ya se parece a una decisión digital

Hemos conseguido que una entrada de control cambie el estado de una carga sin mover manualmente el cable de esa carga. La relación puede expresarse como una condición: si la base recibe polarización adecuada, la rama del LED conduce; si no, la rama se interrumpe prácticamente. El principio es simple, pero no ignora los límites físicos del componente.

Un transistor aislado aún no es una computadora ni una compuerta lógica completa. Para transformar estos estados en funciones repetibles necesitaremos conectar varios transistores, escoger resistencias y niveles adecuados, y comprobar qué tensiones representan realmente un cero y un uno. Ese será el tema del capítulo 3: **de interruptores a lógica**.

## 13. Ejercicios para comprobar el mecanismo

**Ejercicio 1 — Terminales.** Explica la diferencia entre base, colector y emisor en nuestro interruptor NPN. ¿Cuál de ellos va al retorno GND?

**Ejercicio 2 — Dos estados.** IN pasa de 0 V a 5 V. Indica qué ocurre con la unión base-emisor, con la corriente de colector y con el LED, suponiendo que el transistor está correctamente dimensionado.

**Ejercicio 3 — Corriente del LED.** Calcula IC con 5 V de fuente, 2 V supuestos en el LED, 0,2 V supuestos de VCE(sat) y 330 Ω. Da el resultado en A y mA.

**Ejercicio 4 — Corriente de base.** Calcula IB si IN = 5 V, VBE ≈ 0,7 V y RB = 4,7 kΩ. Explica por qué no se debe unir IN directamente a la base.

**Ejercicio 5 — Relación de control.** Con IC = 8,48 mA e IB = 0,915 mA, calcula βforzada. ¿Se parece a la relación de la prueba de saturación de onsemi a 10 mA y 1 mA?

**Ejercicio 6 — Resistencia de carga.** Con IC ≈ 8,48 mA, calcula la potencia P = I²R de los 330 Ω. ¿Basta un resistor de 0,25 W en el caso ideal calculado?

**Ejercicio 7 — Falta un terminal.** El LED y la resistencia de carga están bien colocados, pero el emisor no está unido a GND. Explica por qué el LED no debería encenderse de manera normal.

**Ejercicio 8 — Señal flotante.** IN queda desconectada y alguien supone que eso equivale siempre a 0 V. ¿Por qué es una mala suposición? ¿Cómo se fija un estado bajo en esta práctica?

**Ejercicio 9 — Resistencia equivocada.** Por error se utiliza RB = 47 kΩ en lugar de 4,7 kΩ. Estima IB con VBE ≈ 0,7 V y explica qué efecto podría tener en la saturación.

**Ejercicio 10 — Región activa.** En una medición real el transistor encendido presenta VCE = 1 V. Con 5 V, LED de 2 V y resistor de 330 Ω, recalcula aproximadamente IC. ¿Puedes conservar 8,48 mA sin cambios?

**Ejercicio 11 — Fuente total.** Si ambas ramas del interruptor encendido utilizan el mismo suministro de 5 V, estima la corriente total aportada por la fuente, sumando la rama del LED y la base.

**Ejercicio 12 — MOSFET.** Explica por qué conocer VGS(th) de un MOSFET no demuestra por sí solo que sea adecuado para controlar una carga a 5 V.

## Solucionario del capítulo 2

*Consulta esta sección después de intentar los ejercicios. Son soluciones analíticas de la práctica propuesta, no resultados de medidas físicas.*

**1.** La base recibe corriente de control a través de RB; el colector forma parte de la rama de la carga; el emisor llega al retorno GND.

**2.** A 0 V respecto de GND, Q1 se encuentra aproximadamente en corte y el LED apagado. Con IN a 5 V por RB, aparece corriente de base; si alcanza la saturación prevista, circula corriente por el colector y el LED se enciende.

**3.** IC ≈ (5 − 2 − 0,2) V / 330 Ω = **0,00848 A ≈ 8,48 mA**. No es una medida de un LED real.

**4.** IB ≈ (5 − 0,7) V / 4 700 Ω = **0,000915 A ≈ 0,915 mA**. RB limita la corriente de la unión base-emisor; sin ella, la fuente puede imponer una corriente destructiva.

**5.** βforzada ≈ 8,48 / 0,915 = **9,27**, cercana a 10. El fabricante documenta VCE(sat) bajo la condición de 10 mA y 1 mA; la comparación orienta el diseño, pero no garantiza una caída idéntica.

**6.** P ≈ (0,00848 A)² × 330 Ω ≈ **0,0238 W = 23,8 mW**. Está por debajo de 0,25 W para las condiciones ideales consideradas.

**7.** Falta el retorno de la rama colector-emisor. En el circuito ideal abierto no se establece la trayectoria necesaria de corriente para encender el LED.

**8.** Flotante significa que la entrada carece de potencial definido y puede responder a perturbaciones o fugas. Para el estado bajo conectamos IN a GND **mediante la resistencia de base**, con el circuito desenergizado durante el cambio.

**9.** IB ≈ 4,3 V / 47 000 Ω ≈ **0,0915 mA**. Diez veces menos corriente de base puede impedir alcanzar la saturación prevista y aumentar la caída C-E.

**10.** IC ≈ (5 − 2 − 1) V / 330 Ω ≈ **0,00606 A = 6,06 mA**. La tensión sobre la resistencia cambió; no se puede conservar el resultado anterior de 8,48 mA.

**11.** IFuente ≈ IC + IB ≈ 8,48 + 0,915 = **9,40 mA**. Se supone que la corriente de control proviene del mismo suministro y que no existen otras cargas.

**12.** VGS(th) caracteriza el comienzo de conducción bajo un ensayo concreto, no la baja resistencia requerida en estado encendido. Es necesario consultar RDS(on) a la VGS realmente disponible, así como el resto de límites del componente.

