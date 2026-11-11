# Capítulo 1. La corriente y sus caminos

*Parte I · Electricidad y electrónica básica · Aula-Computadora*

Una computadora parece una colección de decisiones: suma un número, conserva un dato, enciende una pantalla. Pero, dentro de sus circuitos, cada una de esas decisiones depende de un hecho más elemental: la electricidad tiene que circular por un camino previsto, con valores que los componentes puedan soportar. Antes de hablar de transistores o de bits, construiremos ese camino.

Al terminar este capítulo podrás distinguir tensión, corriente, resistencia y potencia; leer un circuito sencillo; calcular una resistencia para un diodo emisor de luz (LED); reconocer dónde se conecta un multímetro; y explicar por qué un circuito aparentemente simple puede fallar. No necesitas experiencia previa con electrónica.

## 1. Una luz que necesita un recorrido

Imagina una pequeña luz roja sobre la mesa. Tienes una fuente de corriente continua de 5 voltios (5 V), un LED y un puñado de cables. Si unes las piezas sin pensar en sus conexiones, puedes no conseguir luz alguna; también podrías dañar el LED. El propósito de este capítulo es averiguar qué condiciones permiten encenderlo de manera razonable.

Un circuito eléctrico es un conjunto de componentes unidos mediante un recorrido conductor. En nuestro ejemplo, la fuente ofrece una diferencia de potencial entre sus terminales; las conexiones conducen la corriente; una resistencia limita cuánto circula; y el LED transforma parte de la energía eléctrica en luz y calor. El recorrido debe volver hasta la fuente: una conexión de ida sin retorno no cierra el circuito.

La fuente no es un depósito de corriente que vierte siempre una cantidad fija. Una fuente regulada de 5 V intenta mantener una **tensión** de 5 V entre sus terminales dentro de sus límites de funcionamiento. La corriente que circulará depende de la carga conectada. Esta diferencia entre tensión disponible y corriente resultante evitará muchas confusiones más adelante.

## 2. Cuatro magnitudes para hacer preguntas precisas

| Magnitud | Símbolo | Unidad | Pregunta que responde |
|---|---|---|---|
| Tensión o diferencia de potencial | V | voltio (V) | ¿Qué diferencia de potencial hay entre dos puntos? |
| Corriente eléctrica | I | amperio (A) | ¿Cuánta carga cruza una sección por unidad de tiempo? |
| Resistencia eléctrica | R | ohmio (Ω) | ¿Qué relación entre tensión y corriente ofrece un elemento resistivo? |
| Potencia eléctrica | P | vatio (W) | ¿A qué ritmo se transfiere o transforma energía? |

### 2.1. Tensión: siempre entre dos puntos

Decir «hay 5 V en el circuito» es una abreviatura útil, pero incompleta. Una tensión se establece **entre dos puntos**. En la fuente de nuestro ejemplo, el terminal positivo está a un potencial 5 V mayor que el negativo. Elegiremos el negativo como referencia de 0 V, también llamada masa o *GND* en muchos esquemas.

Esa elección de referencia no significa que la masa esté conectada a la tierra física del edificio. En un circuito pequeño alimentado por una fuente aislada, *GND* suele ser simplemente el punto desde el cual describimos las demás tensiones.

### 2.2. Corriente: carga que atraviesa una sección

Una corriente de 1 A equivale al paso de 1 culombio de carga por segundo. Un LED de enseñanza suele funcionar con una corriente mucho menor: hablamos de miliamperios (mA), donde 1 mA = 0,001 A. Así, 9 mA significan 0,009 A.

En los diagramas usamos la **corriente convencional**, que va del potencial mayor hacia el menor a través del circuito externo. En un cable metálico, los electrones se desplazan, en promedio, en el sentido contrario. No son dos corrientes distintas: son dos maneras de describir el mismo fenómeno. Mantendremos la convención habitual de los esquemas para que las flechas no cambien de sentido cada vez que aparezca un componente.

### 2.3. Resistencia: una relación, no una barrera absoluta

Si un resistor se comporta aproximadamente como un elemento óhmico en las condiciones consideradas, la diferencia de potencial en sus terminales es proporcional a la corriente que lo atraviesa. Esto se expresa mediante la ley de Ohm.

**Ley de Ohm (para un resistor):**

[[EQ:V = I × R]]

También podemos despejar la corriente o la resistencia:

[[EQ:I = V / R]]

[[EQ:R = V / I]]

Ojo con un detalle decisivo: en estas ecuaciones, **V es la tensión que cae en ese resistor**, no cualquier tensión cercana del circuito. Además, un LED no se comporta como una resistencia fija: es un componente semiconductor y su tensión directa varía con la corriente, la temperatura y el modelo. Por eso no aplicaremos sin más la ley de Ohm al LED.

### 2.4. Potencia: cuánto trabajo eléctrico ocurre por segundo

Una resistencia disipa energía en forma de calor. Un LED emite luz, pero también produce calor. Para estimar la potencia eléctrica absorbida por un componente usamos la tensión **sobre ese componente** y la corriente **a través de él**.

**Potencia eléctrica:**

[[EQ:P = V × I]]

Como en un resistor V = I × R, podemos escribir asimismo:

[[EQ:Pᵣ = I² × R]]

No basta escoger el valor de resistencia en ohmios: también necesitamos comprobar la potencia que podrá disipar sin exceder su especificación. Ese cálculo aparece en nuestro ejemplo.

## 3. Un camino, dos componentes y una fuente

Observa primero el recorrido que empieza en el terminal positivo de la fuente, cruza una resistencia de 330 Ω, pasa por el LED y regresa al negativo. En la figura 1 no hay bifurcaciones: todos los elementos forman un único lazo. El rectángulo identificado como LED representa **sus terminales A (ánodo) y K (cátodo)**, no pretende sustituir el símbolo normalizado de un diodo.

[[FIG:c01_fig01_lazo_serie|Figura 1. Camino de corriente convencional en un circuito de LED y resistencia en serie.|Circuito cerrado con fuente regulada de cinco voltios, resistor de 330 ohmios y LED rojo. Una flecha indica la corriente convencional desde el terminal positivo hacia el negativo.]]

La corriente llega a la resistencia, continúa hacia el ánodo del LED, sale por el cátodo y vuelve al terminal negativo. Por estar **en serie**, resistor y LED comparten la misma corriente. En cambio, cada uno presenta una caída de tensión distinta. Cuando sigamos la rama desde el positivo al negativo, la suma de esas caídas será aproximadamente igual a la tensión proporcionada por la fuente.

En el LED común de dos terminales, el ánodo se conecta hacia el lado positivo y el cátodo hacia el retorno. La pata más larga suele indicar el ánodo en un LED nuevo de terminales tradicionales; la cara plana del encapsulado suele señalar el cátodo. Sin embargo, los encapsulados pueden cambiar o estar recortados: si existe duda, consulta la hoja de datos del componente o utiliza la función de prueba de diodos del multímetro.

## 4. Elegir una resistencia mediante un cálculo completo

Usaremos un ejemplo **calculado, no medido**. Supongamos una fuente de 5,0 V, un LED rojo cuya caída directa estimamos en 2,0 V bajo las condiciones previstas y una resistencia comercial de 330 Ω. Los 2,0 V no son una constante universal: para un montaje físico hay que revisar el LED concreto y sus límites de corriente.

Primero calculamos qué tensión queda para el resistor. En una única rama, la tensión de la fuente se reparte entre los componentes en serie.

**Tensión aproximada en el resistor:**

[[EQ:Vᵣ = Vfuente − VLED]]

[[EQ:Vᵣ = 5,0 V − 2,0 V = 3,0 V]]

Ahora aplicamos la ley de Ohm **solo** al resistor. Se deja la ecuación general visible antes de sustituir los datos.

**Corriente prevista en la rama:**

[[EQ:I = (Vfuente − VLED) / R]]

[[EQ:I = 3,0 V / 330 Ω ≈ 0,00909 A ≈ 9,09 mA]]

El resultado no es «9,09 voltios» ni «9,09 amperios». Es una corriente aproximada de **nueve miliamperios**. Si el LED real presenta una caída diferente o si la fuente varía ligeramente, la corriente también variará. Aun así, este cálculo permite elegir y discutir un resistor de manera razonada.

### 4.1. ¿Qué potencia soportará la resistencia?

Usamos ahora la potencia en el resistor, no la potencia de toda la fuente.

**Potencia disipada por la resistencia:**

[[EQ:Pᵣ = I² × R]]

[[EQ:Pᵣ ≈ (0,00909 A)² × 330 Ω ≈ 0,0273 W]]

Eso equivale a unos 27,3 mW. Un resistor común especificado para 0,25 W (1/4 W) supera holgadamente esa potencia calculada; aun así, hay que respetar sus condiciones de trabajo y evitar montajes que lo sobrecalienten. Incluso si por error los 5 V completos quedaran aplicados a los 330 Ω, la disipación ideal sería 5²/330 ≈ 0,0758 W, aún inferior a 0,25 W. Este último cálculo no convierte en segura cualquier conexión incorrecta: **un cortocircuito que omite la resistencia ya es otra situación**.

### 4.2. ¿Dónde se utiliza el resto de la potencia?

La potencia aproximada en el LED se obtiene multiplicando su caída de tensión por la corriente de la rama.

**Potencia eléctrica aproximada en el LED:**

[[EQ:PLED ≈ 2,0 V × 0,00909 A ≈ 0,0182 W]]

La fuente entregaría aproximadamente 5,0 V × 0,00909 A = 0,0455 W. El total coincide, dentro del redondeo, con los 0,0273 W del resistor más los 0,0182 W del LED. No estamos afirmando que toda la potencia del LED se convierta en luz: una parte termina como calor.

### 4.3. ¿Y si la fuente fuera de 4,5 V?

Tres pilas alcalinas AA en serie proporcionan nominalmente 4,5 V cuando cada una se considera de 1,5 V; su tensión real cambia con el estado de carga y la corriente. Si conservamos como **suposición** 2,0 V sobre el LED y los 330 Ω:

[[EQ:I ≈ (4,5 V − 2,0 V) / 330 Ω ≈ 7,58 mA]]

Una tensión menor deja menos tensión sobre la resistencia y, en esta aproximación, reduce la corriente. No hay que alterar la resistencia «a ojo» para conseguir que brille más. Tampoco debemos conectar nunca el LED directamente a las pilas para buscar más luz.

## 5. Montaje propuesto: una práctica de baja tensión

El objetivo de esta práctica **opcional** es observar el comportamiento del circuito; el cálculo anterior ya es un ejercicio completo incluso si no dispones de materiales. La práctica aún **no está certificada mediante mediciones físicas** para este libro. Usa exclusivamente alimentación de baja tensión y piezas comerciales en buen estado.

**Materiales:** fuente regulada de 5 V CC con limitación de corriente ajustable; LED rojo de dos terminales con especificación conocida; resistor de 330 Ω y potencia nominal de 0,25 W o mayor; protoboard y cables adecuados. Un multímetro digital es opcional para la verificación. Ajusta la limitación de la fuente por debajo de la corriente continua máxima autorizada **por el LED concreto**; para uno cuyo fabricante permita al menos 12 mA, un límite inicial de 12 mA es una referencia conservadora para nuestro cálculo. Si no hay fuente regulada de laboratorio, la actividad se puede estudiar sobre el papel; no improvises cables pelados desde enchufes o cargadores.

1. Con la fuente **apagada**, identifica el terminal positivo (+5 V), el retorno (GND), el valor del resistor y los terminales del LED. Si dudas de la polaridad, detente y consulta el componente.
2. Conecta el positivo de la fuente a un extremo del resistor. Une el otro extremo con el ánodo del LED. Une el cátodo del LED al retorno de la fuente. Comprueba que no existan puentes directos entre los bornes de la fuente.
3. Si utilizas una fuente de laboratorio, configura 5 V CC y un límite de corriente adecuado **antes** de energizar. Enciende y observa. Un brillo moderado sería compatible con el cálculo, pero ni el brillo ni el número del display sustituyen una medida exacta.
4. Apaga la fuente **antes de mover cables**. Si decides tomar medidas, empieza por la tensión, siguiendo el apartado siguiente. No cambies conexiones con el circuito energizado.

La protoboard no es una colección de agujeros independientes: ciertos orificios comparten contactos metálicos ocultos. En la figura 2, los cinco orificios de la fila 3 representan **un nodo eléctrico**, y los cinco de la fila 8 otro. Por eso el resistor puede terminar en un orificio y el ánodo del LED comenzar en otro de la misma fila, sin necesidad de un cable visible entre ambos. Los rieles de alimentación son grupos distintos; algunas placas incluso interrumpen sus rieles a mitad de camino. Hay que comprobar la continuidad antes de conectar la fuente.

[[FIG:c01_fig04_protoboard_conexiones|Figura 2. Vista de conexiones internas en protoboard: un resistor une el positivo con la fila 3, el LED enlaza las filas 3 y 8 y un puente devuelve la corriente al negativo.|Placa de pruebas con dos rieles de alimentación y dos filas de cinco orificios conectados internamente. Resistencia desde riel positivo hasta primera fila, LED entre filas y retorno al riel negativo.]]

**Seguridad que sí importa:** una alimentación nominal de 5 V reduce ciertos riesgos de descarga, pero una fuente capaz de suministrar mucha corriente puede calentar cables, contactos o pilas ante un corto. No uses la red eléctrica doméstica, no desmontes cargadores, no conectes baterías de litio sin protección y no cortocircuites pilas. Si aparece olor, calor anormal o decoloración, desconecta y revisa. Los menores deben trabajar supervisados.

## 6. Leer una medida sin alterar el circuito

El multímetro puede servir para verificar lo que hemos calculado, pero cada magnitud exige una conexión distinta. Los siguientes esquemas son **conceptuales**; la posición exacta de los bornes (COM, V, mA o A) depende del instrumento. Antes de medir, lee sus instrucciones.

### 6.1. Tensión: dos puntas, dos puntos del circuito

Para medir la tensión aproximada del LED, coloca el multímetro en **V de corriente continua** y conecta las puntas **en paralelo** con sus terminales. La figura 3 conserva el mismo lazo de alimentación de la figura 1; lo nuevo es una rama que llega al instrumento. Una punta toca el nodo próximo al ánodo y la otra, el nodo próximo al cátodo.

[[FIG:c01_fig02_medir_tension|Figura 3. La tensión se observa entre dos nodos; el voltímetro se conecta en paralelo con el LED.|Fuente de cinco voltios, resistencia y LED en serie; multímetro en modo voltios de corriente continua conectado a ambos extremos del LED mediante dos ramales.]]

Con la hipótesis del ejemplo, esperaríamos una lectura próxima a 2 V, **no necesariamente idéntica**, porque depende del LED real. Si las puntas se intercambian en un multímetro digital, suele aparecer el signo negativo delante de la lectura. Medir voltaje requiere que las puntas estén en los bornes del instrumento destinados a **COM y V**, nunca dejar el cable en el borne de corriente cuando se vaya a medir tensión.

### 6.2. Corriente: el instrumento debe formar parte de la ruta

Un amperímetro no observa simplemente dos puntos; la corriente que queremos medir debe **atravesar el instrumento**. Por eso se abre el circuito, con la alimentación apagada, y se coloca el multímetro **en serie**. En la figura 4 está ubicado entre el resistor y el LED: la rama conserva un solo camino.

[[FIG:c01_fig03_medir_corriente|Figura 4. Para medir corriente, el amperímetro se intercala en serie con la carga.|Circuito con multímetro representado como amperímetro en serie entre el resistor y el LED. Advertencia de no unirlo directamente entre positivo y negativo.]]

**Nunca conectes un multímetro configurado como amperímetro directamente entre +5 V y GND.** Su resistencia interna suele ser baja y esa conexión puede producir un cortocircuito, quemar un fusible o dañar la fuente o el instrumento. Verifica borne y rango; si no sabes hacerlo con seguridad, no realices esta medición. Puedes estimar la corriente sin abrir el circuito a partir de la caída de tensión medida en un resistor conocido: I ≈ Vᵣ/R, recordando las tolerancias.

### 6.3. Resistencia: circuito sin alimentación

Para medir el valor de un resistor, **apaga y desconecta la alimentación**. Utiliza la función de ohmios del multímetro sobre el componente aislado o sobre un extremo levantado del resto del circuito; en paralelo con otras piezas, la lectura puede describir rutas adicionales y no el valor individual del resistor. Nunca midas resistencia sobre un circuito energizado.

## 7. Las cuatro averías más instructivas

| Síntoma | Posible causa | Comprobación segura |
|---|---|---|
| El LED no enciende | Circuito abierto o mala conexión | Apagar y seguir la ruta, pieza por pieza |
| El LED no enciende | LED invertido | Apagar y verificar ánodo y cátodo |
| El LED brilla débilmente | Tensión menor o corriente limitada | Revisar fuente y caída en resistor, sin retirar la resistencia |
| El circuito se calienta | Cortocircuito, resistor erróneo o límite de corriente insuficiente | Desconectar inmediatamente; revisar cableado, valor y potencia |

Un **circuito abierto** interrumpe la trayectoria: idealmente deja de pasar corriente. Un **cortocircuito** crea una ruta de resistencia muy pequeña que evita una parte prevista del circuito; puede producir una corriente excesiva. Son fallos opuestos, pero ambos pueden hacer que el montaje deje de funcionar como esperamos.

Hay un tercer tipo de confusión frecuente: creer que la fuente «inyecta toda su corriente nominal» al LED. Una fuente rotulada con una capacidad de 2 A no obliga al LED a consumir 2 A; indica una capacidad máxima de suministro bajo condiciones definidas. Nuestro resistor gobierna aproximadamente la corriente de la rama mientras la fuente mantiene los 5 V y los componentes trabajan dentro de sus especificaciones. Esto no elimina el riesgo de un error de cableado.

## 8. De un LED a una computadora

Por ahora hemos construido una ruta que funciona mientras está cerrada y correctamente polarizada. Todavía no podemos **elegir mediante una señal** cuándo se enciende el LED. Podríamos insertar un interruptor manual, pero una computadora necesita miles o millones de decisiones gobernadas eléctricamente. El siguiente paso será conocer un dispositivo que usa una señal pequeña para controlar el paso de corriente por otra ruta: el **transistor**.

No hace falta memorizar veinte fórmulas. Conserva cuatro ideas: la tensión se compara entre dos puntos; la corriente atraviesa un camino; una resistencia permite calcular y limitar corriente; y la potencia indica el ritmo de energía que cada componente debe manejar. Con ellas leeremos circuitos mucho más interesantes.

## 9. Ejercicios para comprobar que entendiste

**Ejercicio 1 — Unidades.** Convierte 0,012 A a mA y 35 mA a A. Escribe la operación que justifica cada resultado.

**Ejercicio 2 — Resistor aislado.** Un resistor de 1 000 Ω tiene una caída de 5 V. ¿Qué corriente pasa por él? Expresa el resultado en A y mA.

**Ejercicio 3 — Nuestro LED.** Con 5 V, una caída supuesta de LED de 2 V y una resistencia de 1 000 Ω, estima la corriente. ¿Sería mayor o menor que con 330 Ω? ¿Por qué?

**Ejercicio 4 — Potencia.** Una resistencia de 330 Ω conduce 0,010 A. Calcula su potencia disipada con I²R. ¿Supera 0,25 W?

**Ejercicio 5 — Instrumentos.** Explica en dos frases dónde se conecta un voltímetro y dónde se conecta un amperímetro. ¿Cuál de las dos conexiones sería peligrosa si se hiciera directamente entre los bornes de la fuente?

**Ejercicio 6 — Diagnóstico.** Un LED no enciende. Indica una secuencia de tres verificaciones que puedas hacer **con la alimentación apagada**, sin sustituir el resistor por un cable.

**Ejercicio 7 — Elegir un valor comercial.** Si quieres que la corriente ideal calculada no supere 10 mA con 5 V y un LED que cae aproximadamente 2 V, ¿qué valor mínimo de resistencia te da la ecuación? ¿Sirve 330 Ω?

**Ejercicio 8 — Cambiar la alimentación.** Un LED y un resistor de 330 Ω funcionan con la hipótesis de 2 V en el LED. Calcula la corriente si se utiliza una fuente de 4,5 V. Indica la razón física de la diferencia respecto al caso de 5 V.

**Ejercicio 9 — Potencia de la fuente.** Una fuente mantiene 5 V sobre una rama por la que circulan 10 mA. ¿Qué potencia eléctrica entrega a esa rama? Expresa el resultado en W y mW.

**Ejercicio 10 — Lecturas verosímiles.** Una persona espera 9,09 mA, pero obtiene 8,5 mA. ¿Esto demuestra necesariamente que la ley de Ohm es incorrecta? Explica dos causas por las que el cálculo aproximado podría diferir de la medida.

**Ejercicio 11 — Errores de unidades.** Un estudiante calcula «3 V / 330 Ω = 0,00909 A» y escribe «9,09 A». Explica exactamente dónde está el error y cuál es el factor de conversión correcto.

**Ejercicio 12 — El retorno olvidado.** La fuente está conectada al resistor y al ánodo del LED, pero el cátodo no está unido al retorno. ¿Se forma un circuito cerrado? ¿Qué corriente ideal esperarías en estado estacionario?

## Solucionario del capítulo 1

*Consulta esta sección después de intentar los ejercicios. Las respuestas son cálculos o criterios de comprobación, no mediciones físicas obtenidas por el libro.*

**1.** 0,012 A × 1 000 mA/A = **12 mA**; 35 mA ÷ 1 000 = **0,035 A**.

**2.** I = V/R = 5 V/1 000 Ω = **0,005 A = 5 mA**. Se aplicó la tensión del resistor, no una tensión ajena a él.

**3.** I ≈ (5 V − 2 V)/1 000 Ω = **0,003 A = 3 mA**. Es menor que los aproximadamente 9,09 mA del caso de 330 Ω porque, para la misma tensión disponible en el resistor, una resistencia mayor conduce menos corriente.

**4.** P = (0,010 A)² × 330 Ω = **0,033 W = 33 mW**. Es inferior a 0,25 W, suponiendo un resistor con esa potencia nominal y condiciones adecuadas.

**5.** El voltímetro se conecta **en paralelo** entre los dos puntos cuya tensión se quiere comparar. El amperímetro se intercala **en serie** con la rama cuya corriente se desea medir. Conectar el amperímetro entre positivo y negativo de la fuente es peligroso: puede provocar un corto.

**6.** Por ejemplo: (1) comprobar la continuidad de la ruta y contactos; (2) verificar polaridad A/K del LED; (3) leer el valor real del resistor y compararlo con el esquema. Después de corregir, se puede energizar con limitación de corriente. También sería correcto empezar verificando la polaridad de la fuente desconectada.

**7.** R ≥ (5 V − 2 V) / 0,010 A = **300 Ω**. Sí: **330 Ω** supera ese mínimo. Se trata de una aproximación que requiere comprobar tolerancias y datos del LED antes del montaje.

**8.** I ≈ (4,5 V − 2,0 V) / 330 Ω = **0,00758 A ≈ 7,58 mA**. Hay menos tensión disponible sobre la resistencia, por eso disminuye la corriente estimada.

**9.** Primero 10 mA = 0,010 A. Después P = 5 V × 0,010 A = **0,050 W = 50 mW**. Esta es la potencia entregada a toda la rama.

**10.** No. La caída del LED varía con el modelo y la corriente; además, la fuente y el resistor poseen tolerancias, y el multímetro introduce incertidumbre de medida. La ecuación se aplicó a un resistor y se acompañó de una hipótesis aproximada para el LED.

**11.** 0,00909 A es **9,09 mA**, no 9,09 A. La equivalencia correcta es **1 A = 1 000 mA**; se multiplica el número expresado en amperios por 1 000 para pasarlo a miliamperios.

**12.** No hay un lazo cerrado. En el modelo ideal del circuito interrumpido, la corriente de régimen estacionario es **0 A**. Una corriente transitoria mínima por fenómenos parásitos no cambia la conclusión pedagógica.

