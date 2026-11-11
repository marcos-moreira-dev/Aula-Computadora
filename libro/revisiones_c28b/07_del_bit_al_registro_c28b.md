# Capítulo 7. Del bit al registro

*Parte II · Memoria digital elemental · Aula-Computadora*

El capítulo anterior nos dejó una pieza capaz de guardar un bit cuando llega un flanco del reloj. Una computadora, sin embargo, tiene que conservar valores que ocupan **varios bits**: la intensidad de un color, un resultado de suma o una parte de una instrucción. ¿Cómo conseguimos que ocho memorias de un bit funcionen como un solo conjunto?

En este capítulo construiremos el **modelo lógico de un registro de ocho bits**. Veremos cómo se carga un byte, qué significa conservarlo, cómo leer su orden de bits y por qué una señal que permite *actualizar* un registro es diferente de otra que permite *colocar su valor en un bus*. Terminaremos transfiriendo un byte entre dos registros mediante una secuencia de control. Los dibujos representan funciones lógicas, no un circuito físico probado.

## 1. Ocho posiciones para un mismo dato

El nombre **bit** se refiere a una posición binaria que puede valer 0 o 1. Un **byte** es un grupo de ocho bits. Cuando escribimos `10110110`, contamos exactamente ocho posiciones; para leerlas sin confusiones podemos separar el grupo en cuatro y cuatro: `1011 0110`.

Numeraremos las posiciones de derecha a izquierda. El bit **b0** está en el extremo derecho y es el menos significativo (*LSB*) para un entero sin signo. El bit **b7** está a la izquierda y es el más significativo (*MSB*). Cada posición tiene un peso distinto cuando decidimos interpretar todo el byte como un número natural.

| Posición | Dígito | Peso | Aporte |
|---|---|---|---|
| b7 | 1 | 128 | 128 |
| b6 | 0 | 64 | 0 |
| b5 | 1 | 32 | 32 |
| b4 | 1 | 16 | 16 |
| b3 | 0 | 8 | 0 |
| b2 | 1 | 4 | 4 |
| b1 | 1 | 2 | 2 |
| b0 | 0 | 1 | 0 |

La conversión manual consiste en multiplicar cada dígito por su potencia de dos y sumar los resultados. El cero también cuenta como posición, aunque su aporte numérico sea nulo:

[[EQ:10110110_2 = 1×128 + 0×64 + 1×32 + 1×16 + 0×8 + 1×4 + 1×2 + 0×1]]

[[EQ:10110110_2 = 128 + 32 + 16 + 4 + 2 = 182_10]]

Como hay ocho posiciones, existen **256 patrones distintos**, desde `00000000` hasta `11111111`. Si los interpretamos como enteros sin signo, corresponden a los valores **0 a 255**; el registro no «sabe» por sí mismo que deben leerse así.

[[EQ:2^8 = 256  patrones]]

La figura 1 une dos ideas: los ocho bits se guardan en ocho memorias separadas, pero un mismo reloj permite capturarlos como una **palabra de ocho bits** después de los retardos correspondientes.

[[FIG:c07_fig01_ocho_flips_un_registro|Figura 1. Ocho flip-flops D comparten el reloj y forman un registro de ocho bits.|Ocho posiciones b7 a b0, cada una con su entrada D y salida Q, capturan en el mismo flanco ascendente del reloj compartido.]]

## 2. El byte y el registro no son lo mismo

Un byte indica **cuántos bits agrupamos**. Un registro indica **dónde y bajo qué reglas se conservan** esos bits dentro de un circuito. Un registro de ocho bits puede guardar un byte; un registro de dieciséis bits puede guardar dos bytes, si así definimos su organización. No todo grupo de ocho bits es un registro físico.

Imagina ocho flip-flops D: uno para b0, otro para b1 y así sucesivamente hasta b7. Sus salidas constituyen el valor presente `Q7…Q0`. Sus entradas `D7…D0` reciben el valor candidato. Si todos comparten un reloj de flanco ascendente, capturan sus entradas en ese mismo evento lógico, siempre que estas cumplan las condiciones temporales.

[[EQ:Q[7:0]_{nuevo} = D[7:0]  en el flanco ascendente]]

Esto no significa que los ocho cables cambien exactamente en el mismo nanosegundo: cada salida presenta un retardo. En un diseño sincronizado se considera **estable** el registro después de que transcurre el margen necesario. Si no hay un mecanismo de reset o carga inicial, el valor tras encenderlo **no debe darse por conocido**.

## 3. La orden LOAD permite conservar sin perder el reloj

El capítulo 6 nos enseñó que un flip-flop de flanco ascendente captura D cuando llega el flanco. Si queremos que un registro **a veces se actualice y a veces se conserve**, necesitamos una señal de control adicional, a la que llamaremos **LOAD**. En nuestro modelo didáctico LOAD es **activo en alto**.

Un modo de implementarlo es colocar delante de cada flip-flop un **multiplexor de dos entradas**. El multiplexor elige entre el dato nuevo `IN_i` y la salida almacenada `Q_i`. Si LOAD = 1, propone el dato nuevo; si LOAD = 0, devuelve el valor guardado. Cuando llega el siguiente flanco ascendente, el flip-flop captura la entrada seleccionada.

[[EQ:D_i = (LOAD ∧ IN_i) ∨ (NOT LOAD ∧ Q_i)]]

[[EQ:Q_{nuevo} = IN  si LOAD = 1 en el flanco; de lo contrario, Q_{nuevo} = Q_{anterior}]]

La figura 2 dibuja **una posición** del registro. Se replica ocho veces, con una sola señal LOAD común y un reloj compartido. El lazo de realimentación pasa por la selección de entrada; **no cortamos ni manipulamos el cable del reloj** para lograr la retención.

[[FIG:c07_fig02_multiplexor_y_carga|Figura 2. Un multiplexor elige entre el dato nuevo y el valor guardado antes del flip-flop.|La entrada IN_i y la realimentación Q_i llegan a un multiplexor; LOAD selecciona cuál alimenta D_i y el flip-flop captura en el flanco ascendente de CLK.]]

| LOAD en el flanco | IN | Q antes | Q después |
|---|---|---|---|
| 0 | Cualquier byte | 00111100 | 00111100 |
| 1 | 10100101 | 00111100 | 10100101 |
| 1 | 00000000 | 10100101 | 00000000 |
| 0 | 11111111 | 00000000 | 00000000 |

Cada fila presupone un **flanco ascendente válido**, y las salidas se leen después de asentarse. Entre flancos, cambiar IN o LOAD no transforma inmediatamente Q. LOAD debe respetar los tiempos de preparación y mantenimiento aplicables a la implementación real.

Para entender **por qué** se conservan o cambian los bits, conviene mirar el multiplexor antes del reloj. En la siguiente tabla seguimos **un solo bit**, de modo que podemos enumerar sus ocho combinaciones sin perder ninguna. `D_i` es lo que el multiplexor prepara, no lo que el flip-flop ha guardado todavía.

[[FIG:c28a_registro8_tabla_mux|Lámina complementaria 7A. Tabla de verdad de las ocho combinaciones del multiplexor de entrada de R0.|Ocho filas de LOAD, Q_i anterior e IN_i, con la salida D_i. LOAD cero conserva el valor anterior y LOAD uno selecciona la entrada nueva.]]

Observa el caso `LOAD=1`, `Q_i=1`, `IN_i=0`: la salida preparada es **0**, pero Q seguirá valiendo **1 hasta el próximo flanco ascendente válido**. Esta diferencia entre *preparar* y *guardar* es fundamental para comprender la memoria digital.

## 4. El registro de ocho bits en hexadecimal

Escribir ocho ceros y unos cada vez resulta incómodo. El hexadecimal permite representar cada grupo de **cuatro bits** con un solo símbolo: `0000` es `0`, `1001` es `9`, `1010` es `A`, `1011` es `B` y `1111` es `F`.

El byte `10110110` se divide en `1011` y `0110`. El primer grupo equivale a **B** hexadecimal y el segundo a **6**. Por eso escribimos `0xB6`, donde `0x` nos indica que los símbolos siguientes están en base dieciséis.

[[EQ:1011_2 = B_16;  0110_2 = 6_16;  10110110_2 = 0xB6]]

Podemos verificarlo en decimal sin ninguna calculadora:

[[EQ:0xB6 = 11×16 + 6×1 = 176 + 6 = 182]]

El patrón es el mismo, aunque lo escribamos en binario, hexadecimal o decimal. El sistema de numeración cambia la **representación para quien lee**. Que ese byte represente además una letra, una bandera o una parte de una instrucción requiere reglas que estudiaremos en el puente semántico.

## 5. Un registro puede conservar datos sin mostrarlos en un bus

Un **bus de datos** es un conjunto de líneas que permite llevar un grupo de bits entre bloques. Por ejemplo, un bus de ocho bits tiene ocho líneas, que podemos llamar BUS7 a BUS0. Si dos circuitos intentan imponer simultáneamente niveles opuestos sobre la misma línea de salida, aparece un **conflicto eléctrico** que no debemos permitir.

Para compartir líneas existen salidas de **tres estados**: nivel lógico 0, nivel lógico 1 y **alta impedancia (Z)**. Z significa que el controlador de esa salida deja de conducir activamente la línea; **no es un tercer valor almacenado** en el flip-flop. Además, una línea sin controlador activo puede quedar flotante si no hay otra polarización o conexión definida.

El control `OE_n` (*output enable*, activo en bajo) es distinto de LOAD. En el modelo que dibujaremos, **LOAD decide si se escribe el registro**; `OE_n` decide si un búfer conectado al registro **conduce su valor al bus**. Deshabilitar `OE_n` no borra el registro.

| LOAD en flanco | OE_n | Registro Q | Salida al bus |
|---|---|---|---|
| 0 | 0 | Conserva Q | Conduce Q |
| 0 | 1 | Conserva Q | Z |
| 1 | 0 | Captura IN | Conduce Q nuevo tras retardo |
| 1 | 1 | Captura IN | Z |

La tabla junta **dos controles conceptualmente independientes**. LOAD se evalúa en el flanco del modelo de registro; OE_n controla el búfer de salida y puede cambiar entre flancos. No se debe interpretar como la tabla de un único integrado comercial.

[[FIG:c07_fig03_almacenamiento_y_triestado|Figura 3. La carga modifica el almacenamiento; OE_n gobierna una salida triestado separada.|Un registro de ocho bits conserva Q mientras un búfer de salida ofrece Q al bus con OE_n igual a cero, o estado Z cuando OE_n vale uno.]]

Ahora volvamos al registro completo. Supongamos que R0 guarda inicialmente `0x3C` y que la entrada propone `0xA5`. La lámina 7B combina **presencia o ausencia de flanco**, LOAD y `OE_n`: muestra a la vez qué queda almacenado y qué podemos observar en el bus.

[[FIG:c28a_registro8_tabla_estado_bus|Lámina complementaria 7B. Estado del registro y salida al bus para ocho combinaciones de control.|Ocho casos en los que R0 comienza con 0x3C e IN vale 0xA5; el flanco ascendente con LOAD uno cambia R0 y OE_n controla separadamente si el bus presenta el valor o alta impedancia.]]

Por ejemplo, en la última fila **sí se guarda `0xA5`**, aunque el bus indique **Z** porque su búfer está deshabilitado. La información no desaparece: simplemente no está siendo conducida hacia ese cable. En ausencia de una carga inicial válida, la salida almacenada sería desconocida (`X`), no necesariamente cero.

## 6. Dos registros necesitan reglas para compartir el bus

Llamaremos **A** y **B** a dos registros de ocho bits. Cada uno tiene su propia orden de carga. Para leerlos mediante un bus compartido, cada registro dispone de un búfer triestado con una habilitación independiente. Definiremos `A_OUT = 1` cuando A puede conducir el bus y `B_OUT = 1` cuando B puede hacerlo; estas son **señales abstractas activas en alto** del controlador, no nombres de patillas de un chip.

| A_OUT | B_OUT | Estado del bus | Diagnóstico |
|---|---|---|---|
| 0 | 0 | Ninguno conduce (Z) | Debe recibir otra fuente para leerse |
| 1 | 0 | Valor de A | Selección válida |
| 0 | 1 | Valor de B | Selección válida |
| 1 | 1 | Conflicto potencial | Estado prohibido por diseño |

La regla de control es sencilla: **como máximo uno de estos dos registros conduce el bus a la vez**. Si no conduce ninguno, no podemos inventar que BUS vale cero. Un bus real puede usar búferes, lógica de selección o distintas topologías; la restricción concreta depende del circuito elegido.

[[EQ:A_OUT + B_OUT ≤ 1  (suma de enteros 0 o 1)]]

## 7. Transferir 0x3C de A hacia B

Construyamos una secuencia verificable en papel. Usaremos el modelo de los apartados anteriores: ambos registros cargan en el **flanco ascendente** cuando su señal LOAD vale 1. Sus búferes ponen un dato en el bus cuando OUT vale 1. Empezaremos con estados **conocidos porque antes los cargamos de manera controlada**: A = `0x3C` (`00111100`) y B = `0xA5` (`10100101`).

**Primer paso.** Con `A_LOAD = 0` y `B_LOAD = 0`, habilitamos `A_OUT = 1` y `B_OUT = 0`. Después de asentarse la selección y la salida, el bus contiene `0x3C`. A y B no han cambiado.

**Segundo paso.** Con A todavía conduciendo el bus, establecemos `B_LOAD = 1` y mantenemos `A_LOAD = 0`. Esperamos a que la entrada de B sea estable antes del siguiente flanco ascendente. En ese flanco B captura **todo el byte `0x3C`**. A sigue almacenando `0x3C`.

**Tercer paso.** Bajamos `B_LOAD` a 0 de modo que cumpla el tiempo de mantenimiento. Después deshabilitamos la salida de A; esperamos que deje de conducir y habilitamos la de B. Tras la transición de los búferes, el bus muestra `0x3C` procedente de B.

| Etapa estable | Control principal | A guardado | B guardado |
|---|---|---|---|
| Inicio | Estados precargados | 0x3C | 0xA5 |
| Presentación | A_OUT = 1 | 0x3C | 0xA5 |
| Captura | B_LOAD = 1 y CLK ↑ | 0x3C | 0x3C |
| Lectura final | B_OUT = 1 | 0x3C | 0x3C |

La figura 4 representa la dirección de este traslado. No estamos «moviendo» el dato fuera de A: en una transferencia ordinaria el origen **conserva su copia** y B captura otra. Tampoco aparece aquí una dirección de memoria RAM, que estudiaremos después.

[[FIG:c07_fig04_transferencia_a_b|Figura 4. Transferencia de un byte mediante bus y una carga por flanco.|El registro A presenta 0x3C al bus, B lo captura con B_LOAD durante el siguiente flanco, y luego B puede presentarlo tras deshabilitar la salida de A.]]

## 8. Distinguir circuito didáctico de componentes reales

La hoja de datos de **Texas Instruments SN74HC377** describe **ocho flip-flops D de flanco ascendente con habilitación de reloj**. Su entrada de habilitación `CLKEN` es activa en bajo: al estar habilitada en el momento válido de captura, se carga D; de lo contrario, se conserva Q. El dispositivo ofrece salidas normales; **no tiene salidas triestado ni reset común como características equivalentes al modelo completo de nuestros apartados 5 y 6**.

La hoja de datos del **Texas Instruments SN74HC245** describe un **transceptor de bus de ocho bits** con salidas de tres estados. Con `OE_n = 1` aísla ambos lados; con `OE_n = 0`, la entrada `DIR` decide si las señales van desde A hacia B o desde B hacia A. **No es un registro de almacenamiento**: si se pretende construir una ruta física, hay que integrar por separado almacenamiento, control de salida, dirección y temporización.

Los diagramas educativos no especifican patillas, alimentación, desacoplo, retardos máximos ni corrientes de una placa real. Además, el SN74HC377 no dispone de borrado asíncrono común: antes de su primera carga no debemos presuponer un valor de Q. La prueba de un montaje concreto exigiría consultar el encapsulado, la hoja de datos y medir o simular el circuito con un modelo adecuado.

## 9. Por qué un registro prepara el camino hacia la memoria

Ya podemos construir conceptualmente un bloque que conserva ocho bits, puede cargar otros ocho en un flanco y puede conectar su salida al bus mediante control independiente. Para disponer de **muchos** bytes, en vez de repetir cientos de selectores manuales necesitamos un mecanismo para **elegir qué posición leer o escribir**. En el capítulo 8 aparecerán las direcciones y los buses de manera formal; el capítulo 9 mostrará qué cambia al emplear memorias RAM y ROM.

El registro tiene una semántica lógica concreta: **LOAD solicita capturar**, `OE_n` permite conducir y el reloj determina *cuándo* se captura. El patrón `10110110`, por su parte, todavía no posee una etiqueta de «número», «letra» u «objeto» en sus flip-flops. Esa diferencia entre **estado físico-lógico** e **interpretación convencional** será el centro del puente editorial «Del bit al significado», previsto después de este capítulo sin renumerar por ahora los 24 capítulos.

## Construimos Aula-8: nuestro primer registro R0

Ya podemos reconocer una pieza concreta de la computadora. Reunimos ocho elementos de memoria de tipo D, uno para cada bit de `R0`. Sus entradas son `D7…D0` y las salidas conservadas son `Q7…Q0`. El reloj coordina la captura; una habilitación de carga permite que el banco **ignore un dato mientras no se le ordene almacenarlo**. La figura siguiente no pretende elegir pines de un chip ni afirmar que los ocho flip-flops ya están soldados.

[[FIG:c07_fig05_registro_aula8|Figura 5. Primer banco didáctico R0 de Aula-8: ocho flip-flops D comparten el reloj y una política de carga.|Ocho celdas DFF, una por bit, desde D7 hasta D0 y desde Q7 hasta Q0; el registro conserva un byte de ocho bits.]]

Probemos la idea con un dato conocido. Si ponemos `0011 1100₂` en las entradas y habilitamos la carga durante el flanco correcto, `R0` pasa a contener `0x3C`. Si luego las entradas cambian a `0xA5` pero la carga no se autoriza, **R0 conserva 0x3C**. El bus de salida puede mostrar ese byte cuando el circuito de selección se lo permita. Esto todavía no es RAM: poseemos **un lugar de ocho bits**, no miles de lugares seleccionables mediante direcciones. Los capítulos 8 y 9 introducirán justamente esa diferencia.

## 10. Ejercicios del registro y del bus

**Ejercicio 1 — Posiciones.** Escribe los ocho nombres de bit de un registro, desde el más significativo hasta el menos significativo, e indica sus pesos si se interpreta como número sin signo.

**Ejercicio 2 — Conversión manual.** Convierte `10110110` a decimal mostrando cada multiplicación por potencias de dos, incluidos los ceros.

**Ejercicio 3 — Capacidad.** ¿Cuántos patrones distintos tiene un registro de ocho bits? ¿Cuál es el máximo valor decimal si interpretamos todos sus bits como entero sin signo?

**Ejercicio 4 — Registro.** ¿Cuántos flip-flops D de un bit hacen falta para un registro de ocho bits? ¿Qué entrada temporal comparten en nuestro modelo?

**Ejercicio 5 — Retención.** Un registro contiene `00111100`. Si LOAD = 0 y llega un flanco ascendente mientras IN = `11111111`, ¿qué conserva Q?

**Ejercicio 6 — Carga.** El mismo registro ahora tiene LOAD = 1 e IN = `10100101`. ¿Qué queda almacenado después de un flanco válido y el tiempo de propagación?

**Ejercicio 7 — Hexadecimal.** Convierte `10110110` a hexadecimal mediante dos grupos de cuatro bits, y comprueba su valor decimal con la expansión hexadecimal.

**Ejercicio 8 — Alta impedancia.** ¿Qué significa Z en la salida de un búfer? ¿Por qué no es un tercer bit que se guarde?

**Ejercicio 9 — Señales diferentes.** Compara LOAD con `OE_n` cuando el registro conserva `0xA5`. Explica qué sucede al deshabilitar la salida.

**Ejercicio 10 — Arbitraje.** Para los controles abstractos A_OUT y B_OUT, enumera los cuatro pares posibles y señala cuál prohíbe nuestro diseño.

**Ejercicio 11 — Transferencia.** A comienza con `0x3C`, B con `0xA5`. Se habilita la salida de A y B captura el bus en un flanco. ¿Qué byte queda en cada registro y cuál fue la fuente del bus?

**Ejercicio 12 — Diagnóstico.** Dos registros conducen simultáneamente el mismo bus, uno intenta producir 0 y el otro 1. ¿Por qué es peligroso y qué cambio de control permitiría una lectura válida?

## Solucionario del capítulo 7

**1.** Desde el MSB hasta el LSB: b7, b6, b5, b4, b3, b2, b1, b0. Sus pesos son 128, 64, 32, 16, 8, 4, 2, 1.

**2.** `1×128 + 0×64 + 1×32 + 1×16 + 0×8 + 1×4 + 1×2 + 0×1 = 128 + 32 + 16 + 4 + 2 = 182`.

**3.** Hay `2^8 = 256` patrones. El máximo entero sin signo vale `128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255`.

**4.** Hacen falta ocho flip-flops D. Todos usan el mismo CLK; cada bit tiene su propia entrada D y su salida Q.

**5.** Q sigue valiendo `00111100` porque LOAD = 0 selecciona el valor anterior, aunque IN sea distinto.

**6.** Q queda en `10100101` después del flanco ascendente válido, suponiendo que se respetan los tiempos del componente.

**7.** `1011 0110` equivale a `B6`, por tanto `0xB6`. Su valor decimal es `11×16 + 6 = 182`.

**8.** Z indica que el búfer deja de imponer un nivel lógico activo sobre el cable. El flip-flop sigue guardando un 0 o un 1; Z pertenece al **modo de la salida**, no al bit almacenado.

**9.** LOAD permite reemplazar Q en un flanco; `OE_n = 1` desconecta la salida del bus y **no cambia** el `0xA5` almacenado.

**10.** `00`: ninguno conduce; `10`: conduce A; `01`: conduce B; `11`: dos conductores activos y posible contención. Se prohíbe `11`.

**11.** A conserva `0x3C` y B pasa a guardar `0x3C`. Durante la captura el bus recibió su valor del búfer de A.

**12.** Las salidas pueden enfrentarse eléctricamente y circular corrientes excesivas; no basta con afirmar que el bus tendrá «un promedio». Se debe deshabilitar **uno de los controladores** antes de habilitar el otro, respetando los tiempos de conmutación.

