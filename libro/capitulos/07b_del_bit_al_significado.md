# Capítulo 7B. Del bit al significado

*Parte II · Puente entre registros y direcciones · Aula-Computadora*

Acabamos de construir un registro capaz de conservar ocho bits. Sabemos cargar `01000001` mediante un flanco del reloj y leerlo por un bus. Sin embargo, todavía falta responder una pregunta que aparece en cuanto una computadora empieza a ser útil: **¿qué significa ese byte?** Si una pantalla muestra la letra A, si una calculadora muestra el número 65 y si un circuito enciende dos indicadores, ¿podrían estar usando exactamente los mismos bits?

Sí, siempre que cada dispositivo o programa aplique sus propias reglas para interpretarlos. Este capítulo puente explica dónde empieza el significado lógico en el circuito, cómo surgen las codificaciones de datos y qué añaden los lenguajes de programación. Conecta el registro del capítulo 7 con las direcciones y los buses del capítulo 8.

## 1. Un voltaje no es literalmente un número binario

En un cable real existe una **tensión eléctrica** respecto a una referencia. En nuestros dibujos escribimos `0` y `1` para representar estados lógicos, pero esas cifras **no son mediciones universales** de 0 V y 5 V. Los dispositivos electrónicos reconocen ciertos intervalos como nivel bajo o alto, según su familia lógica, alimentación y hoja de datos. Puede existir una región intermedia que no garantice una interpretación válida como 0 o 1. El ruido y los tiempos de transición también importan.

Una puerta digital recibe niveles eléctricos admitidos y realiza una función lógica. Así surge un primer tipo de significado, propio del **hardware**: una entrada es una condición, una NAND aplica una regla booleana y un flip-flop conserva un estado. Son convenciones de diseño del circuito, no todavía una palabra escrita en español.

Recordemos la puerta NAND de dos entradas. Su salida es 0 **solo cuando ambas entradas valen 1**; en los otros tres casos es 1. El 0 de su salida significa «la condición AND no se cumple» si usamos la polaridad positiva de esa función.

[[EQ:Y = NOT (A ∧ B)]]

| A | B | A AND B | NAND |
|---|---|---|---|
| 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 0 |

La figura 1 separa el fenómeno físico de la interpretación lógica. También muestra por qué el símbolo `0` puede significar **orden activa**: si una señal se denomina `RESET_n`, el sufijo `_n` indica aquí que su acción se solicita llevando la señal a nivel bajo. En ese contrato, `RESET_n = 0` pide restablecer el circuito; `RESET_n = 1` deja de pedirlo. Una señal llamada `RESET` podría diseñarse con la polaridad opuesta. Hay que leer siempre el contrato del componente.

[[FIG:p07b_fig01_del_voltaje_a_la_logica|Figura 1. El circuito transforma niveles eléctricos admitidos en estados lógicos y asigna funciones a las señales.|La tensión de entrada se compara con las regiones admitidas para bajo y alto. La puerta lógica procesa 0 y 1; RESET_n es un ejemplo de señal activa en bajo. La región intermedia no está garantizada.]]

## 2. Ocho bits ofrecen patrones, no etiquetas incorporadas

El registro del capítulo 7 contiene ocho posiciones: `b7 b6 b5 b4 b3 b2 b1 b0`. Cada posición guarda 0 o 1; por ello hay 256 combinaciones. Una combinación almacenada es un **patrón**. No lleva grabada en cada flip-flop una etiqueta que diga «número», «carácter», «color» o «instrucción».

[[EQ:2^8 = 256  combinaciones posibles]]

Tomemos `01000001`. Si interpretamos las ocho posiciones como un **entero sin signo**, aplicamos los pesos 128, 64, 32, 16, 8, 4, 2 y 1, de izquierda a derecha. La suma manual deja a la vista incluso los términos que valen cero:

[[EQ:01000001_2 = 0×128 + 1×64 + 0×32 + 0×16 + 0×8 + 0×4 + 0×2 + 1×1]]

[[EQ:01000001_2 = 64 + 1 = 65_10 = 0x41]]

Ahora observemos las mismas ocho posiciones como una **máscara de indicadores**. Si b7 es el indicador 7 y b0 el indicador 0, están activos únicamente **b6 y b0**. Este resultado no contradice al número 65: son dos lecturas del mismo estado. En el uso real tendríamos que acordar qué controla cada indicador.

Como **carácter de texto**, el código ASCII asigna al valor 65 el símbolo `A`. El patrón puede representar esa letra cuando el sistema decide decodificarlo como texto ASCII. Una CPU que guarda `0x41` en un registro no dibuja por sí sola la letra: intervienen un programa y un dispositivo capaz de mostrarla.

La figura 2 ofrece tres lecturas verificables. Una cuarta salida, «instrucción», aparece deliberadamente como **no determinada**: sin conocer el repertorio y el formato de instrucciones de una CPU concreta (su **ISA**), sería inventar decir qué operación ejecuta `0x41`.

[[FIG:p07b_fig02_un_byte_varios_significados|Figura 2. El mismo patrón 01000001 se interpreta como 65, A o una máscara con b6 y b0 activos.|Un byte central 01000001 se conecta con tres lecturas acordadas: entero sin signo 65, carácter ASCII A y bits b6 y b0 activos. Una lectura como instrucción requiere una ISA definida.]]

| Regla de interpretación | Lectura de `01000001` | Información necesaria |
|---|---|---|
| Entero sin signo de 8 bits | 65 | Pesos binarios y longitud de 8 bits |
| Texto ASCII | `A` | Tabla de caracteres y decisión de mostrar texto |
| Máscara de 8 indicadores | b6 y b0 activos | Correspondencia entre bits y funciones |
| Instrucción de máquina | Indeterminada | ISA y formato de instrucciones |

**Importante:** la memoria no necesita modificar un solo transistor para que cambie la lectura humana. Lo que cambia es la operación, el programa o el dispositivo que **interpreta** los bits.

## 3. El signo cambia la lectura de 11111111

Un error habitual consiste en pensar que el bit más a la izquierda «siempre es el signo». No lo es. En la lectura **sin signo**, `11111111` suma todos los pesos positivos y vale 255. En la representación de enteros **con signo en complemento a dos** de ocho bits, el bit más a la izquierda tiene peso −128, y los demás conservan pesos positivos.

[[EQ:11111111_2  sin signo = 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255]]

[[EQ:11111111_2  con signo = -128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = -1]]

De forma equivalente, para un patrón de ocho bits cuyo b7 es 1, podemos tomar su valor sin signo y restarle 256. Por eso `255 − 256 = −1`. Para b7 igual a 0, el resultado firmado coincide con el sin signo. Este procedimiento describe **complemento a dos de exactamente ocho bits**, no cualquier forma posible de almacenar enteros negativos.

[[EQ:valor_firmado = valor_sin_signo - 256  cuando b7 = 1]]

La figura 3 contrasta dos interpretaciones del mismo registro. El patrón no ha cambiado, pero el resultado de una comparación firmada y una comparación sin signo sí podría ser diferente. El rango sin signo de ocho bits es de 0 a 255; el de complemento a dos firmado es de −128 a 127.

[[FIG:p07b_fig03_pesos_con_y_sin_signo|Figura 3. Un byte de unos vale 255 sin signo y menos uno en complemento a dos.|Los ocho bits 11111111 se muestran con pesos positivos 128 a 1 para el entero sin signo y pesos -128, 64 a 1 para el entero firmado en complemento a dos de ocho bits.]]

| Patrón de ocho bits | Sin signo | Con signo en complemento a dos |
|---|---|---|
| `00000000` | 0 | 0 |
| `01111111` | 127 | 127 |
| `10000000` | 128 | −128 |
| `11111111` | 255 | −1 |

## 4. Una letra necesita una codificación acordada

Los caracteres no son una propiedad eléctrica de los cables. ASCII estableció códigos para representar caracteres básicos, entre ellos la `A` mayúscula con valor hexadecimal `0x41`. **UTF-8** es una codificación de Unicode que representa caracteres mediante uno o varios bytes. Para los caracteres del rango ASCII, la codificación UTF-8 conserva el mismo byte; `A` se codifica como `0x41`.

Pero no todas las letras caben en un byte UTF-8. El carácter `é` (Unicode `U+00E9`) se representa en UTF-8 mediante **dos bytes consecutivos**, `0xC3 0xA9`. Si alguien muestra cada uno como si fuera un carácter ASCII independiente, no obtiene la letra correcta. Un archivo de texto necesita reglas de codificación además de bits bien almacenados.

[[EQ:0x41 = 4×16 + 1 = 65]]

Una imagen también necesita un acuerdo: un byte podría representar una intensidad de gris de 0 a 255 si se usa un formato que la defina así. En un formato diferente podrían existir canales de color, compresión o encabezados. **El valor 65 no es intrínsecamente «gris» ni «A».** Lo vuelve interpretable un formato conocido.

Para comprobar esta diferencia, piensa en un receptor que recibe dos bytes `C3 A9`. Ambos pueden estar perfectamente conservados. Si el receptor desconoce UTF-8, el fallo aparece **en la interpretación**: el problema no exige que un cable haya cambiado de 0 a 1.

## 5. El contenido de memoria y su dirección son cosas distintas

En el capítulo 8 aprenderemos a seleccionar posiciones de memoria con un bus de direcciones. Por ahora adelantemos el concepto con una situación sencilla: imaginemos que la posición de RAM identificada por la **dirección hexadecimal `0x1200`** contiene el byte `0x41`.

[[EQ:RAM[0x1200] = 0x41]]

La expresión distingue tres piezas. `RAM` nombra el espacio de memoria; `0x1200` identifica **dónde** se consulta; `0x41` es el **contenido** que se lee allí. Como la dirección `0x1200` necesita más de ocho bits para escribirse en binario, en este ejemplo se representa con dieciséis bits. El contenido `0x41` sí cabe en un byte.

No deduzcas que la dirección es una letra porque dentro hay `A`. Tampoco que el contenido `0x41` señala necesariamente otra posición. Un programa podría tratarlo como dato o, dentro de un contrato de arquitectura, como parte de una dirección. **Dirección y valor son papeles distintos** en una operación de memoria.

| Pregunta | Respuesta en el ejemplo | Papel |
|---|---|---|
| ¿Dónde leer? | `0x1200` | Dirección |
| ¿Qué ocho bits hay allí? | `01000001` | Contenido |
| ¿Cuánto valen sin signo? | 65 | Interpretación numérica |
| ¿Qué letra pueden mostrar? | `A` | Interpretación textual |

Una memoria habitual guarda **patrones**. La regla que identifica su tipo suele residir en el programa, el formato del archivo, el conjunto de instrucciones o algún mecanismo adicional del sistema. En este modelo de enseñanza, una celda de RAM no almacena junto al byte una etiqueta universal de «carácter» o «entero».

## 6. De los bytes a las instrucciones

Un programa almacenado también está formado por bits. Una CPU recibe patrones y, al ejecutar instrucciones, consulta su **ISA**, que define qué combinaciones significan operaciones, modos de direccionamiento o argumentos. Una parte de esos bits puede leerse como **código de operación** (*opcode*), y otras partes como operandos. La interpretación depende del diseño y de la posición que ocupa cada campo.

Para no inventar una instrucción real, imaginemos una **CPU de juguete** cuya tabla, creada solo para este ejemplo, declara que `0x41` significa «sumar uno al acumulador». Si esa máquina lee `0x41` como opcode en la fase adecuada, ejecutaría la operación definida. Otra máquina podría reservar `0x41` para algo distinto, y una tercera no reconocerlo. Nada en la forma `01000001` obliga al silicio a llamarlo suma.

En Aula-8 y Aula-16 estudiaremos esos contratos más adelante. **Sus codificaciones siguen en diseño y no se consideran definitivas aquí**. El recorrido de buscar, decodificar y ejecutar instrucciones aparecerá en sus capítulos; este capítulo establece la diferencia entre patrón y regla de interpretación.

## 7. El software organiza significados y operaciones

Un lenguaje de programación ayuda a nombrar valores y a establecer qué operaciones tienen sentido con ellos. Una **variable** asocia un nombre con un valor dentro de un programa; un **tipo** describe cómo se interpreta y utiliza ese valor. Una **estructura de datos** reúne elementos relacionados según reglas conocidas. Una función añade una operación o comportamiento, no una nueva categoría física de bit.

Pensemos en una aplicación de biblioteca que conserva la edad de una persona, la inicial de su nombre y si puede acceder a una sala. Podrían aparecer patrones de bits semejantes en los tres campos, pero el programa sabe cuál usar para comparar edades, cuál mostrar como letra y cuál tratar como condición. Sus nombres y reglas hacen que el conjunto tenga **significado para una tarea humana**.

La **programación orientada a objetos** lleva más adelante esta organización: un objeto suele combinar estado y operaciones de acuerdo con una clase u otro contrato del lenguaje. Es una forma de diseñar software; **no hay un «transistor de objeto» ni hace falta usar POO para construir nuestra CPU**. Los ejemplos posteriores de MiniC-Aula emplearán variables, arreglos, estructuras sencillas y funciones sin exigir clases.

La figura 4 representa una escalera **conceptual**, no capas físicas obligatorias. El significado lógico de una señal ocurre en el circuito; los programas y los formatos agregan reglas de interpretación cada vez más ligadas a necesidades humanas. También pueden omitir etapas o combinar varias.

[[FIG:p07b_fig04_escalera_de_significado|Figura 4. Desde un estado lógico en hardware hasta un significado definido por el programa.|Escalera conceptual: nivel eléctrico reconocido, señal lógica de control, patrón de bits, valor codificado, tipo y estructura de datos, comportamiento de programa; la POO es contexto posterior y no un componente físico.]]

La programación, por supuesto, hace más que asignar nombres: controla **operaciones, decisiones, cambios de estado y efectos observables**. Podemos describir una parte importante de su trabajo como administración de representaciones y significados, siempre que no olvidemos esas acciones.

## 8. Una comprobación completa de interpretación

Un registro ha conservado `01000001` sin errores. Tres lectores reciben ese patrón. El primero calcula 65 mediante los pesos binarios; el segundo usa ASCII y muestra A; el tercero activa los indicadores b6 y b0. Los tres pueden estar **correctos simultáneamente**. Si un cuarto lector afirma que el byte representa necesariamente «sumar uno», necesitamos preguntarle qué ISA ha definido antes de aceptar su respuesta.

Ahora cambia el registro a `11111111`. Un lector sin signo ve 255; otro que aplica complemento a dos de ocho bits ve −1. Ambos tienen razón dentro de sus reglas. Pero si se pretendía imprimir texto ASCII, `0xFF` **no es un carácter ASCII de siete bits**, y tampoco constituye por sí solo una secuencia UTF-8 válida. La interpretación adecuada no siempre existe para cualquier patrón y cualquier formato.

Este es el puente hacia los capítulos siguientes: el hardware puede **guardar y transferir bits fielmente**, y aun así un sistema puede producir un resultado equivocado por elegir el formato, el tipo, la dirección o la instrucción incorrectos. Aprender arquitectura de computadoras exige comprender tanto el recorrido de las señales como **las reglas que les dan una función**.

## 9. Ejercicios del bit y su significado

**Ejercicio 1 — Voltaje.** ¿Por qué no es correcto afirmar que todo 0 lógico equivale a 0 V y todo 1 lógico a 5 V? ¿Dónde se consulta el comportamiento de un componente real?

**Ejercicio 2 — Polaridad.** ¿Cuándo está activa una señal `RESET_n` que el diseñador definió activa en bajo? Compárala con una señal activa en alto.

**Ejercicio 3 — NAND.** Calcula la salida NAND para A = 1 y B = 1, y para A = 1 y B = 0.

**Ejercicio 4 — Conversión.** Convierte `01000001` a decimal con **las ocho multiplicaciones** por potencias de dos; escribe también su hexadecimal.

**Ejercicio 5 — Máscara.** Indica qué bits están a 1 en `01000001` utilizando índices b7…b0.

**Ejercicio 6 — Carácter.** Si el byte `0x41` debe mostrarse como texto ASCII, ¿qué carácter aparece? ¿Por qué un registro sin programa de salida no lo muestra por sí solo?

**Ejercicio 7 — Dos signos.** Convierte `11111111` como entero sin signo y como entero firmado de complemento a dos de ocho bits; enseña cada suma de pesos.

**Ejercicio 8 — Límite.** Interpreta `10000000` como entero sin signo y firmado. Señala el rango completo de cada convención para ocho bits.

**Ejercicio 9 — UTF-8.** ¿Cuántos bytes ocupan `A` y `é` en UTF-8? Escribe sus códigos hexadecimales e indica por qué dos bytes no equivalen necesariamente a dos letras.

**Ejercicio 10 — Dirección y valor.** En `RAM[0x1200] = 0x41`, identifica dirección, contenido y lectura decimal sin signo del contenido.

**Ejercicio 11 — Opcode.** ¿Basta ver `01000001` para afirmar qué instrucción ejecutará una CPU? Explica qué información falta.

**Ejercicio 12 — Semántica de software.** Explica con un ejemplo la diferencia entre el byte físico almacenado, el tipo de una variable, una estructura de datos y la idea posterior de objeto.

## Solucionario del capítulo 7B

**1.** Los estados lógicos se reconocen mediante umbrales eléctricos de la familia lógica y del componente, no mediante dos voltajes universales. Hay que consultar su hoja de datos, tensión de alimentación y márgenes de entrada.

**2.** Una `RESET_n` activa en bajo solicita reset cuando vale 0 y lo desactiva cuando vale 1. Una señal RESET activa en alto haría lo contrario según su propio contrato.

**3.** NAND(1,1) = NOT(1) = 0; NAND(1,0) = NOT(0) = 1.

**4.** `0×128 + 1×64 + 0×32 + 0×16 + 0×8 + 0×4 + 0×2 + 1×1 = 65`. Separando en nibbles `0100 0001` obtenemos `0x41`.

**5.** Los unos están en **b6 y b0**; b7, b5, b4, b3, b2 y b1 valen 0.

**6.** Aparece `A` si el sistema interpreta el byte según ASCII y lo envía a un dispositivo de texto. El registro solo conserva el patrón.

**7.** Sin signo: `128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255`. En complemento a dos de ocho bits: `−128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = −1`.

**8.** `10000000` vale 128 sin signo y −128 firmado. Los rangos son 0…255 y −128…127, respectivamente.

**9.** `A` usa un byte UTF-8 (`41`); `é` usa dos (`C3 A9`). UTF-8 puede emplear varios bytes para un solo carácter Unicode.

**10.** La dirección es `0x1200`; el contenido es el byte `0x41` = `01000001`; leído como entero sin signo vale 65.

**11.** No. Se necesita conocer la ISA, el formato de instrucción y el lugar de ese byte dentro de la instrucción o del programa.

**12.** El circuito guarda, por ejemplo, `0x41`; una variable tipada puede interpretarlo como `65` o `A`; una estructura agrupa esa variable con otros campos; un objeto podría además asociar operaciones a ese estado. El objeto pertenece al modelo del programa, no a una clase especial de bit.

