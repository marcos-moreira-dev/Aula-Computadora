# Capítulo 8. Direcciones y buses

*Parte III · Memoria, buses y aritmética · Aula-Computadora*

En el capítulo 7 copiamos `0x3C` desde un registro A hasta un registro B. Solo había dos lugares y ambos estaban dibujados. Una computadora necesita algo más exigente: guardar miles de bytes, volver a uno de ellos cuando lo necesite y distinguir el lugar elegido del contenido que se encuentra allí. ¿Cómo pide un procesador «dame el byte de la posición 0x1200» sin tender un cable independiente hasta cada byte?

La respuesta combina **direcciones**, **buses** y **selección**. Partiremos de cuatro posiciones de memoria imaginarias para entender el mecanismo y después ampliaremos el dibujo al espacio de 16 bits previsto para Aula-8. Mantendremos separados los ejemplos lógicos, los chips comerciales y los circuitos de Aula que todavía deben diseñarse y probarse.

## 1. La dirección no es el dato

Imagina cuatro cajones numerados `00`, `01`, `10` y `11`. Cada cajón puede guardar un byte. Si el cajón `10` contiene `00111100`, podemos describir dos cosas diferentes: **la dirección es `10`** y **el dato almacenado es `00111100`**. El primero indica *dónde* buscar; el segundo indica *qué* leer o escribir.

| Dirección de 2 bits | Contenido de 8 bits | Contenido hexadecimal |
|---|---|---|
| `00` | `00010010` | `0x12` |
| `01` | `10100101` | `0xA5` |
| `10` | `00111100` | `0x3C` |
| `11` | `11111111` | `0xFF` |

Con la dirección `10` no estamos enviando el número decimal diez: **`10₂` vale dos en decimal**. La memoria entrega `0x3C` porque así lo establecimos en la tabla. Podríamos poner `0x00` en ese mismo cajón sin cambiar su dirección; también podríamos copiar `0x3C` a otros cajones sin que se conviertan en la misma posición.

[[EQ:10₂ = 1×2¹ + 0×2⁰ = 2₁₀]]

Este es el primer puente con la semántica del capítulo 7B: el circuito interpreta ciertos bits como **selección de una posición**, y otros como **valor transportado**. Esa función viene del cableado y del protocolo de acceso. Si un programa interpretará luego `0x3C` como número, máscara o carácter es otra decisión.

## 2. Dos bits eligen cuatro posiciones

Un **decodificador de direcciones** recibe una combinación binaria y activa la salida que corresponde a ella. Para cuatro posiciones necesitamos dos señales, `A1` y `A0`. En el dibujo cada salida `SEL0`…`SEL3` es activa en alto: exactamente una vale 1 para cada combinación de entrada, siempre que el decodificador esté habilitado. Es una convención didáctica, no el pinout de un chip elegido.

[[EQ:N = 2ⁿ;  si n = 2, entonces N = 2² = 4 posiciones]]

| A1 | A0 | Salida seleccionada |
|---|---|---|
| 0 | 0 | `SEL0` |
| 0 | 1 | `SEL1` |
| 1 | 0 | `SEL2` |
| 1 | 1 | `SEL3` |

[[FIG:c08_fig01_decodificador_dos_bits|Figura 1. Dos bits de dirección seleccionan una de cuatro posiciones; cada posición guarda ocho bits.|A1 y A0 llegan a un decodificador de 2 a 4; las salidas SEL0 a SEL3 seleccionan cuatro celdas de ocho bits. El dato de la dirección 10 es 0x3C.]]

**Leer** significa seleccionar un cajón y obtener su contenido. **Escribir** significa seleccionar un cajón y reemplazar su contenido por el byte entregado. En nuestro ejemplo, escribir `0x7E` en la dirección `01` modifica ese cajón, pero deja `00`, `10` y `11` como estaban. El decodificador no almacena los bytes: produce señales que permiten elegir qué almacenamiento participa.

El componente real SN74HC138 de Texas Instruments hace una tarea emparentada: decodifica **tres entradas de selección en ocho salidas activas en bajo** y dispone de entradas de habilitación. Por eso no podemos conectar la figura como si sus señales `SEL` coincidieran sin más con las del integrado. Al trabajar con un chip hay que leer su tabla de funciones y su hoja de datos.

## 3. Un bus agrupa cables con una función definida

Un **bus** es un conjunto de líneas que transportan señales relacionadas. No significa necesariamente un solo cable ni implica que todos los participantes puedan conducirlo al mismo tiempo. En nuestro modelo sencillo aparecen tres grupos:

1. **Bus de direcciones** `A15…A0`: dieciséis líneas que indican la posición solicitada.
2. **Bus de datos** `D7…D0`: ocho líneas que transportan el byte entre la CPU Aula-8 y la memoria seleccionada.
3. **Señales de control**: indican si se está leyendo, escribiendo y habilitando el dispositivo elegido.

[[FIG:c08_fig02_buses_separados|Figura 2. La CPU Aula-8 propone una dirección de 16 bits, intercambia un dato de 8 bits y controla el sentido de la operación.|Diagrama funcional entre CPU Aula-8, decodificación y memoria: 16 líneas de dirección CPU a memoria; 8 líneas de datos bidireccionales; controles de lectura, escritura y selección, sin temporización eléctrica comprometida.]]

En la figura 2 las flechas del bus de direcciones apuntan desde quien inicia la operación hacia la selección de memoria. El bus de datos tiene dos sentidos posibles, **pero no a la vez**: durante una lectura responde la memoria y durante una escritura la CPU proporciona el byte. Es una explicación funcional que habrá que convertir en control eléctrico y temporal concreto antes de construir Aula-8.

Una dirección de **16 bits** no exige que el dato tenga 16 bits. Son magnitudes independientes. Aula-8 tendrá dirección externa de 16 y dato externo de 8; Aula-16 conservará **16 bits de dirección**, pero transportará **16 bits de datos** en su bus externo. La amplitud de un bus de datos expresa cuántos bits puede transferir por operación de ese tipo, no cuántas posiciones puede nombrar el procesador.

## 4. Calcular una dirección de 16 bits sin saltos

Con dieciséis bits se forman patrones desde `0000 0000 0000 0000` hasta `1111 1111 1111 1111`. Si los empleamos como direcciones sin signo, representan **65 536 valores**. Como el modelo de ambas máquinas es direccionable por **bytes**, hay 65 536 direcciones de byte posibles: **64 KiB de espacio direccionable**. Esto *no* demuestra que se hayan instalado 64 KiB de chips RAM; parte del espacio puede destinarse a ROM, periféricos o posiciones sin respuesta.

[[EQ:2¹⁶ = 65 536 direcciones de byte]]

[[EQ:65 536 bytes ÷ 1 024 = 64 KiB]]

El ejemplo del capítulo 7B era `RAM[0x1200] = 0x41`. Aquí nos interesa abrir la dirección. Cada cifra hexadecimal corresponde a cuatro bits:

| Cifra hexadecimal | Valor decimal | Grupo binario |
|---|---|---|
| `1` | 1 | `0001` |
| `2` | 2 | `0010` |
| `0` | 0 | `0000` |
| `0` | 0 | `0000` |

De este modo, `0x1200` se escribe `0001 0010 0000 0000₂`. Para convertir a decimal multiplicamos por las potencias de dieciséis correspondientes. Los dos ceros no desaparecen: ocupan posiciones con aporte nulo.

[[EQ:1×16³ + 2×16² + 0×16¹ + 0×16⁰ = 4 608₁₀]]

En particular, `16³ = 4096` y `2×16² = 512`; las dos últimas posiciones aportan cero. Por tanto, la dirección hexadecimal `0x1200` es **4608 en decimal**. Su contenido en RAM podría ser otro número completamente distinto.

También podemos comprobarlo bit a bit. Los únicos unos están en las posiciones **b12** y **b9**, medidas desde la derecha; por tanto aportan `4096` y `512`. Los restantes catorce bits aportan cero. No hay que sumar `1 + 2` ni interpretar `12` como decimal doce: hay que respetar el peso de **cada posición**.

[[EQ:0001 0010 0000 0000₂ = 1×2¹² + 1×2⁹ = 4 608₁₀]]

La dirección posterior a `0x1200` es **`0x1201`**, no el siguiente número del byte almacenado. La dirección máxima de dieciséis bits es `0xFFFF` (decimal 65 535), y `0x10000` exige **17 bits**, por lo que queda fuera de ese espacio de direcciones.

[[EQ:0xFFFF = 15×16³ + 15×16² + 15×16¹ + 15×16⁰ = 65 535]]

## 5. Lectura y escritura son operaciones diferentes

Nuestro modelo usa señales de control con sufijo `_n` para indicar que se **activan con cero**. `CS_n` (*chip select*) habilita el dispositivo; `RD_n` solicita lectura; `WR_n` solicita escritura. La tabla es una simplificación didáctica de las condiciones estables durante una transacción, **no una secuencia de nanosegundos ni una especificación eléctrica**.

| Operación | CS_n | RD_n | WR_n |
|---|---|---|---|
| Dispositivo no seleccionado | 1 | 1 | 1 |
| Leer | 0 | 0 | 1 |
| Escribir | 0 | 1 | 0 |
| Combinación prohibida en este modelo | 0 | 0 | 0 |

Para **leer** `0x1200`, el controlador pone la dirección sobre `A15…A0`, habilita la memoria y solicita lectura. Una vez satisfechos los tiempos de acceso del dispositivo, la memoria seleccionada puede conducir el bus `D7…D0`. Si esa posición contiene `0x41`, el bus ofrece `01000001`. La CPU debe capturarlo cuando sea válido; no basta con suponer que aparece inmediatamente al mover un cable.

Para **escribir** `0x53` en `0x1201`, la CPU coloca `0x1201` en el bus de direcciones y `01010011` sobre el bus de datos, selecciona el dispositivo y presenta la señal de escritura conforme al protocolo. La memoria registra el dato cuando se satisfacen sus condiciones de escritura. En la representación didáctica, `RAM[0x1200]` sigue valiendo `0x41` y `RAM[0x1201]` pasa a `0x53`.

[[FIG:c08_fig03_lectura_escritura|Figura 3. La dirección elige la misma memoria en ambos casos, pero cambia quién conduce el bus de datos.|Comparación de una lectura en 0x1200 que devuelve 0x41 con una escritura de 0x53 en 0x1201. En lectura conduce la memoria; en escritura conduce la CPU; ambas operaciones son conceptuales.]]

| Paso | Dirección | Bus de datos y resultado |
|---|---|---|
| Leer | `0x1200` | Memoria → CPU: `0x41` |
| Escribir | `0x1201` | CPU → memoria: `0x53` |
| Volver a leer | `0x1201` | Memoria → CPU: `0x53` |
| Comprobar vecino | `0x1200` | Memoria → CPU: `0x41` |

Este ejemplo **supone** que las posiciones pertenecen a RAM escribible, que la memoria estaba inicializada con el primer valor y que la escritura terminó correctamente. Las direcciones no constituyen un mapa definitivo de Aula-8. El capítulo 9 distinguirá lo que ofrece una SRAM comercial, una ROM y los dispositivos que comparten un mapa de direcciones.

## 6. Triestado, multiplexación y conflicto de bus

El capítulo 7 presentó la **alta impedancia**, que escribimos `Z`. Si un dispositivo pone su salida en Z, deja de conducir esa línea: **Z no es el bit cero**. Este comportamiento es necesario cuando varios dispositivos comparten `D7…D0`. Si dos memorias diferentes intentan imponer simultáneamente niveles opuestos, aparece una **contención eléctrica** potencialmente dañina. El decodificador y las señales de habilitación deben evitarla.

También podemos seleccionar datos mediante un **multiplexor**. Un multiplexor 4 a 1 elige una de cuatro *fuentes de datos* y conduce una salida; un decodificador 2 a 4 convierte dos *bits de selección* en cuatro habilitaciones. Ambos usan bits de control, pero **cumplen funciones diferentes**. En una memoria real pueden combinarse decodificadores, multiplexores y control de salida; la topología depende de la tecnología elegida.

[[EQ:Decodificador 2→4: 00→SEL0; 01→SEL1; 10→SEL2; 11→SEL3]]

El circuito SN74HC138 es una referencia de decodificación, no una memoria. La SRAM AS6C62256 de Alliance Memory es un ejemplo distinto: organiza **32 K × 8 bits** y emplea señales de selección, habilitación de salida y escritura. Su hoja de datos especifica cuándo sus pines de datos pueden quedar en alta impedancia y los tiempos que se deben respetar. No se deduce de esos dos nombres que nuestro diseño de buses ya esté cableado o probado.

## 7. Aula-8 y Aula-16 comparten direcciones, no el ancho de dato

Las dos máquinas del proyecto mantienen direcciones de 16 bits. Aula-8 tiene un bus externo de **8 bits** y puede transportar directamente un byte. Aula-16 tiene un bus externo de **16 bits**, pero sus direcciones siguen nombrando **bytes**. Para que un acceso de palabra de 16 bits sea coherente, el diseño base propone **dos bancos de ocho bits** y el convenio *little-endian*: el byte menos significativo se coloca en la dirección menor.

| Propiedad | Aula-8 | Aula-16 |
|---|---|---|
| Dirección externa | 16 bits | 16 bits |
| Bus de datos externo | 8 bits | 16 bits |
| Posición direccionada | Byte | Byte |
| Espacio de direcciones | 64 KiB | 64 KiB |
| Palabra de 16 bits | Necesita varias transferencias de byte | Una transferencia de palabra alineada en el diseño base |

Por ejemplo, si la palabra de 16 bits es `0x1234`, en el orden little-endian sus dos bytes se almacenan así:

| Dirección de byte | Banco / posición | Contenido |
|---|---|---|
| `0x2000` (par) | Bajo | `0x34` |
| `0x2001` (impar) | Alto | `0x12` |

[[EQ:0x1234 = 0x12×256 + 0x34 = 4 660₁₀]]

[[FIG:c08_fig04_aula8_aula16|Figura 4. Igual dirección de 16 bits, diferente ancho de datos; Aula-16 combina dos bancos de ocho bits.|Comparación de Aula-8 con D7…D0 y Aula-16 con D15…D0; para la palabra 0x1234 en Aula-16 el byte bajo 0x34 ocupa 0x2000 y el alto 0x12 ocupa 0x2001.]]

Para la primera versión de Aula-16 acordamos **accesos de palabra alineados**, es decir, la palabra del ejemplo comienza en dirección par. El detalle eléctrico de selección de bancos y líneas por byte, y qué hacer en todas las variantes de acceso, corresponde al diseño específico del capítulo 22. No confundir el formato little-endian con el sentido del bus: describe **orden de los bytes en memoria**, no la dirección de las flechas.

## 8. Cómo leer un esquema de bus sin inventar lo que falta

Frente a un diagrama de memoria, conviene hacer cinco preguntas en este orden. Primero, ¿cuántos bits forman la dirección y quién los suministra? Segundo, ¿cuántos bits forman los datos, quién los conduce en lectura y quién en escritura? Tercero, ¿qué combinaciones de dirección activan cada chip? Cuarto, ¿qué señales son activas en bajo y cuándo se permite conectar una salida al bus? Quinto, ¿qué tiempos necesita el fabricante antes de capturar o cambiar los datos?

El dibujo funcional suele omitir detalles que son decisivos al construir: **desacoplo, alimentación, carga capacitiva, tiempos de establecimiento, retardo de propagación, secuencia de deshabilitación y posibles estados indeterminados al encender**. Que una tabla sea correcta no demuestra que un cableado sea seguro. Para convertir este capítulo en práctica de laboratorio habrá que elegir dispositivos concretos, calcular su decodificación y revisar el ciclo de lectura/escritura de sus hojas de datos.

## 9. Problema completo: elegir, leer, escribir y conservar

Partimos de un modelo de RAM de bytes con `RAM[0x1200] = 0x41` y `RAM[0x1201] = 0x00`. Queremos leer el primero, escribir `0x53` en el segundo y comprobar que el primero no cambió. **Paso 1:** expresamos `0x1200` como 16 bits: `0001 0010 0000 0000`. **Paso 2:** activamos conceptualmente lectura; la RAM seleccionada entrega `0x41 = 0100 0001₂`. **Paso 3:** cambiamos la dirección a `0x1201 = 0001 0010 0000 0001₂` y escribimos `0x53 = 0101 0011₂`. **Paso 4:** desactivamos escritura y realizamos una nueva lectura válida de `0x1201`: debe devolver `0x53`. **Paso 5:** volvemos a leer `0x1200`: debe seguir en `0x41`.

[[EQ:0x41 = 0×128 + 1×64 + 0×32 + 0×16 + 0×8 + 0×4 + 0×2 + 1×1 = 65]]

[[EQ:0x53 = 0×128 + 1×64 + 0×32 + 1×16 + 0×8 + 0×4 + 1×2 + 1×1 = 83]]

La prueba distingue tres niveles: los **bits de dirección** solicitan una posición, los **bits de datos** representan un contenido y el **protocolo** determina si leemos o modificamos ese contenido. Nada en esta secuencia exige que el valor `0x41` sea una letra, aunque un software que aplique ASCII podría mostrar `A`. Así se conserva la diferencia entre el significado lógico de hardware y la interpretación de software.

## Construimos Aula-8: conectar el registro con un lugar de memoria

Antes teníamos un registro que conservaba el byte `0x3C`. Ahora queremos que ese dato llegue a un lugar elegido de RAM, por ejemplo `0x1200`, y que la CPU pueda leerlo después. La máquina debe poder expresar **dos cosas simultáneamente**: la dirección con dieciséis líneas y el contenido con ocho. Si solo dibujáramos una flecha entre dos cuadros, ocultaríamos esa diferencia esencial.

[[FIG:c08_fig05_buses_aula8|Figura 5. La CPU Aula-8 usa un bus de direcciones de 16 bits y un bus bidireccional de datos de 8 bits para comunicarse con la memoria.|El MAR aporta A15 hasta A0; el MDR intercambia D7 hasta D0; lectura o escritura controlan el sentido de los datos.]]

En una escritura, la CPU mantiene estable la dirección en MAR, prepara el byte en MDR y autoriza a la memoria seleccionada a capturarlo. En una lectura, el dispositivo seleccionado conduce los ocho datos hacia MDR y la CPU deja de conducir esas líneas. **Solo un productor puede conducir el bus compartido en un momento dado.** La figura describe las conexiones funcionales necesarias, no las patillas concretas de una RAM. Tampoco las líneas de dirección y datos tienen por qué cambiar exactamente al mismo tiempo: el componente físico impondrá tiempos de preparación, retención y liberación.

## Ejercicios del capítulo 8

Resuelve primero sin mirar las respuestas. En cada conversión anota el valor posicional; si aparecen ceros, escribe también su aporte. Todos los ejercicios usan el modelo lógico del capítulo, no timings reales.

**Ejercicio 1 — Dirección y contenido.** En la tabla de cuatro posiciones, ¿qué dirección produce `0x3C` y cuál es el dato en binario?

**Ejercicio 2 — Número de posiciones.** ¿Cuántas direcciones diferentes se pueden representar con tres bits? Enuméralas.

**Ejercicio 3 — Decimal de la dirección.** Convierte `0x1200` a decimal explicando los cuatro pesos hexadecimales.

**Ejercicio 4 — Binario de la dirección.** Convierte `0x1201` a 16 bits y señala qué bit difiere respecto a `0x1200`.

**Ejercicio 5 — Capacidad de direcciones.** ¿Cuántas posiciones de byte hay con 16 bits? ¿Cuántos KiB representan en un espacio direccionable por bytes?

**Ejercicio 6 — Límite.** Indica el último valor de dirección de 16 bits y explica por qué `0x10000` no cabe.

**Ejercicio 7 — Decodificador.** Para A1 = 1 y A0 = 0, ¿qué salida se activa en el decodificador del ejercicio? ¿Cuáles quedan inactivas?

**Ejercicio 8 — Señales de lectura.** En la tabla didáctica, ¿qué valores deben tener CS_n, RD_n y WR_n para leer?

**Ejercicio 9 — Señales de escritura.** En el mismo modelo, ¿cuáles son los valores para escribir y quién conduce D7…D0?

**Ejercicio 10 — Alta impedancia.** ¿Por qué Z no se puede sustituir por 0? ¿Qué problema produce habilitar dos salidas opuestas?

**Ejercicio 11 — Palabra little-endian.** Se guarda `0x1234` en Aula-16 a partir de `0x2000`. ¿Qué byte aparece en `0x2000` y cuál en `0x2001`?

**Ejercicio 12 — Caso integrado.** Si `RAM[0x1200]` vale `0x41` y escribimos `0x53` en `0x1201`, ¿cuál será el resultado de leer ambas direcciones? Expande `0x53` a binario y decimal.

## Solucionario del capítulo 8

**1.** Dirección `10₂` (dos decimal). Contenido `00111100₂`, equivalente a `0x3C`.

**2.** `2³ = 8`: `000`, `001`, `010`, `011`, `100`, `101`, `110`, `111`.

**3.** `1×4096 + 2×256 + 0×16 + 0×1 = 4096 + 512 = 4608`.

**4.** `0x1201 = 0001 0010 0000 0001₂`; cambia solamente b0, que pasa de 0 a 1.

**5.** `2¹⁶ = 65 536` direcciones de byte; `65 536/1024 = 64 KiB` de espacio, no necesariamente de RAM instalada.

**6.** `0xFFFF` (65 535 decimal). `0x10000` vale 65 536 y requiere 17 bits.

**7.** `SEL2 = 1` y `SEL0 = SEL1 = SEL3 = 0`, según el decodificador activo en alto de la figura 1.

**8.** `CS_n = 0`, `RD_n = 0`, `WR_n = 1`; se permite a la memoria seleccionada conducir los datos después del retardo de acceso.

**9.** `CS_n = 0`, `RD_n = 1`, `WR_n = 0`; conduce la CPU y la memoria recibe el byte según la temporización válida.

**10.** Z significa salida desconectada eléctricamente del bus; cero es un nivel lógico conducido. Dos salidas enfrentadas pueden causar contención y exceso de corriente.

**11.** `0x2000 → 0x34` (byte bajo); `0x2001 → 0x12` (byte alto). La dirección sigue siendo de byte, aunque el bus de datos sea de 16 bits.

**12.** La lectura de `0x1200` devuelve `0x41`; la de `0x1201` devuelve `0x53`. El byte escrito es `01010011₂ = 0×128 + 1×64 + 0×32 + 1×16 + 0×8 + 0×4 + 1×2 + 1×1 = 83₁₀`.

## Para continuar

Ya sabemos **cómo pedir una posición** y **cómo mover su contenido** sin confundir dirección, dato y control. Todavía debemos explicar **cómo está construida la memoria** capaz de responder: en qué se diferencian SRAM y ROM, qué terminales aparecen en los chips reales y cómo se amplía capacidad sin activar dos dispositivos a la vez. Ese será el capítulo 9, «RAM y ROM reales».

Fuentes para contrastar el paso a componentes reales: Texas Instruments, *SNx4HC138 3-Line To 8-Line Decoders/Demultiplexers*, https://www.ti.com/lit/ds/symlink/sn74hc138.pdf; Alliance Memory, *AS6C62256 Low Power Asynchronous SRAM*, https://www.alliancememory.com/as6c62256/. Los diagramas de este capítulo son originales y conceptuales.
