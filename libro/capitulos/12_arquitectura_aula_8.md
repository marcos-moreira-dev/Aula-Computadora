# Capítulo 12. Arquitectura Aula-8

*Parte IV · Construir Aula-8 · Aula-Computadora*

Ya sabemos construir funciones lógicas, conservar bits en registros, direccionar memorias y calcular con una ALU de ocho bits. Nos falta responder una pregunta: **¿cómo cooperan esas piezas para que una computadora pueda seguir las instrucciones de un programa?** Si conectamos una ALU y una memoria sin un camino organizado para los datos, ninguna sabrá qué hacer después. La **arquitectura** describe qué recursos existen y cómo se coordinan; el **camino de datos** o *datapath* muestra por dónde viaja cada valor.

En este capítulo reuniremos los bloques de **Aula-8**, nuestra computadora educativa propuesta. Veremos qué guarda cada registro, qué hace un bus, cómo se lee un byte de RAM y cómo se prepararía una instrucción para su ejecución. Los valores de ejemplo y la codificación de instrucciones provienen de un **borrador candidato**, no de una CPU fabricada, una ISA aprobada ni un simulador que haya ejecutado esos programas.

## 1. Antes de dibujar la CPU: distinguir funciones

Imaginemos la instrucción «coloca el número 42 en R0». La memoria debe proporcionar los bytes de la orden; un registro debe conservar la instrucción actual; un mecanismo de control debe identificar su destino; y otro registro debe recibir `0x2A`, representación hexadecimal de 42. **La ALU no hace todo eso.** La ALU calcula cuando alguien selecciona una operación; otros bloques transportan, guardan y ordenan.

Una primera división útil es entre el **camino de datos**, que conecta registros, ALU y memoria, y la **unidad de control**, que determina qué se lee, qué se selecciona y cuándo se permite una escritura. Esta diferencia es semejante a la de una carretera y sus señales: la carretera permite el paso, pero no decide por sí misma quién avanza.

[[EQ:42₁₀ = 32 + 8 + 2 = 00101010₂ = 0x2A]]

En Aula-8, los datos habituales se calculan y transportan como bytes. No obstante, **una dirección debe identificar hasta 65536 posiciones distintas**, por eso tiene 16 bits. Esta distinción ya apareció al hablar de buses: ancho de dirección y ancho del dato son propiedades diferentes.

[[EQ:2¹⁶ = 65536 direcciones de byte = 64 KiB de espacio]]

Que una CPU pueda **direccionar** 64 KiB no implica que estén instalados 64 KiB de RAM. Parte del espacio puede corresponder a ROM, entrada/salida o regiones todavía no asignadas. Un mapa de memoria físico definitivo requiere decisiones posteriores.

## 2. Los registros tienen tareas diferentes

Un **registro** conserva bits entre operaciones. No todos almacenan el mismo tipo de información, aunque muchos estén hechos, en principio, a partir de flip-flops. La tabla muestra los recursos propuestos para Aula-8. Los nombres y anchos son un punto de partida de ingeniería, mientras que la conexión concreta sigue pendiente.

| Recurso | Bits | Papel principal |
| --- | --- | --- |
| **R0–R3** | 8 cada uno | Datos generales sobre los que trabaja el programa. |
| **PC** | 16 | Dirección del próximo byte de programa que se leerá. |
| **SP** | 16 | Ubicación de la pila; ayuda a llamadas y datos temporales. |
| **X** | 16 | Base para recorrer tablas y arreglos en memoria. |
| **MAR** | 16 | Mantiene la dirección de la transacción de memoria. |
| **MDR** | 8 | Retiene el byte que entra o sale de memoria. |
| **IR** | 8 | Conserva el código de operación que se está interpretando. |
| **SEL / TMP** | 8 cada uno | Selector de registro y dato temporal de una instrucción. |
| **FLAGS** | 4 | Indicadores Z, N, C y V para resultados de datos. |

Piensa en `PC=0x6000` y `R0=0x2A`. **PC no contiene el número 42:** contiene una dirección de memoria. **R0 no contiene una dirección:** en ese ejemplo guarda el patrón de ocho bits que interpretamos como 42. En el capítulo 7B «Del bit al significado» aprendimos por qué esa interpretación depende del contexto.

[[EQ:PC = 0x6000 ; R0 = 0x2A]]

También conviene distinguir `SP` de `X`. `SP` sostiene la posición de la pila, una zona usada por llamadas y valores temporales; `X` es un índice más general, útil para caminar por un arreglo. Ambos tienen 16 bits, pero **compartir tamaño no significa compartir función**. Su actualización y sus límites deberán definirse con el diseño de la máquina.

## 3. Un dibujo de bloques no es un montón de cables unidos

La propuesta utiliza un **bus interno de datos de ocho bits**, un bus **externo de direcciones de dieciséis** y otro externo **de datos de ocho**. Así, internamente podemos mover un byte y, cuando hablamos con memoria, indicamos tanto **dónde** actuar como **qué byte** leer o escribir.

[[FIG:c12_fig01_mapa_cpu_aula8|Figura 1. Vista funcional de Aula-8: registros, ALU y buses internos separados de las direcciones y datos que llegan a RAM, ROM y E/S.|Bloques: registros generales de 8 bits, PC SP X de 16 bits, ALU8 y FLAGS, bus interno de ocho bits, MAR de 16 y MDR de 8, unidad de control y buses externos A0-A15 y D0-D7 hacia memoria y E/S. Los flujos son rutas posibles, no controladores simultáneos.]]

Un bus compartido no admite cualquier cantidad de salidas activas. **Solo una fuente debe conducir un segmento de datos a la vez**; varios destinos podrían leer ese valor si la lógica lo permite, pero una escritura debe habilitarse de manera explícita. Si R0 intenta colocar `1` en una línea mientras R1 intenta colocar `0`, no se obtiene mágicamente un nuevo bit: existe un conflicto eléctrico que el circuito real debe impedir.

La unidad de control, todavía no diseñada físicamente, tendría que seleccionar **fuente**, **destino**, **función de ALU** y **lectura o escritura de memoria**. Las líneas dibujadas como flechas dobles indican alternativas a seleccionar; **no** ordenan que todas las piezas conduzcan el bus simultáneamente.

## 4. Un movimiento pequeño: copiar R1 hacia R0

Supongamos que `R1=0x3C` y `R0=0x00`. Queremos conservar una copia en R0. Basta una transferencia controlada: seleccionar R1 como fuente, presentar su byte en el bus interno, y habilitar el almacenamiento de R0. Al terminar, **ambos registros contienen `0x3C`**.

[[EQ:R1 = 00111100₂ = 0x3C ; R0 inicial = 00000000₂]]

[[EQ:R0 nuevo ← R1 = 00111100₂ ; R1 permanece = 0x3C]]

[[FIG:c12_fig02_movimiento_registros|Figura 2. Copiar el byte de R1 a R0 exige seleccionar una fuente para el bus y habilitar la carga de un destino; R1 conserva su contenido.|Diagrama didáctico de R1 con 00111100 conectado a un bus de ocho bits y a R0; se distinguen selección de fuente, permiso de carga de destino y valores antes y después.]]

Lo importante es la **secuencia lógica**: una ruta disponible no equivale a un dato almacenado. En una realización con flip-flops, el valor se captura bajo la condición de carga y el evento temporal apropiado. No podemos prometer que todo este movimiento ocurra en un solo ciclo hasta elegir circuitos, reloj y temporización.

La instrucción candidata `MOV` podría solicitar esa copia, pero un opcode no es una señal eléctrica directa: **la unidad de control tendría que traducir la orden a acciones sobre fuentes y destinos**. El capítulo 13 explicará esa coordinación con más detalle.

## 5. La memoria necesita una dirección estable y un dueño del bus

Un acceso a RAM añade dos recursos: **MAR** y **MDR**. MAR conserva la dirección de 16 bits, mientras MDR retiene un byte de datos. Durante la operación, el programa puede estar avanzando con PC; por eso conviene que MAR mantenga la dirección de memoria de la transacción actual sin depender de que PC cambie después.

Si queremos **leer** el byte guardado en `0x6F00`, el modelo sigue esta secuencia de dependencias: `MAR←0x6F00`, selección de la memoria apropiada, solicitud de lectura `RD`, aparición del byte válido en `D0...D7`, captura en `MDR` y, finalmente, transferencia al registro destino. **La CPU no debe conducir el bus externo de datos durante esa lectura**.

[[EQ:MAR = 0x6F00 ; MDR ← memoria[0x6F00]]]

Para **escribir** `0x2A` en `0x6F00`, primero se prepara `MAR=0x6F00` y `MDR=0x2A`; entonces la CPU presenta el dato, selecciona RAM y solicita escritura `WR`. **En ese momento no debe haber otro dispositivo conduciendo el bus de datos**. ROM y dispositivos de entrada/salida tienen reglas propias: una instrucción de almacenamiento no autoriza automáticamente escribir en cualquier chip.

[[EQ:memoria[0x6F00] ← 0x2A]]

[[FIG:c12_fig03_lectura_escritura|Figura 3. En la lectura conduce el dispositivo de memoria y captura MDR; en la escritura conduce la CPU y captura RAM. Nunca hay dos conductores de datos simultáneos.|Dos paneles con MAR=6F00: lectura RD, RAM entrega byte a MDR y CPU no conduce datos; escritura WR, MDR/CPU presenta 2A y RAM captura; se marca propiedad exclusiva del bus.]]

| Acceso externo | Dirección | Quién conduce datos | Quién recibe |
| --- | --- | --- | --- |
| Lectura | CPU, mediante MAR | RAM/ROM/E/S seleccionada | MDR de CPU |
| Escritura | CPU, mediante MAR | Salida de CPU preparada desde MDR | RAM/E/S seleccionada |

Las señales `RD` y `WR` representan aquí **acciones**, sin definir aún si sus pines concretos serán activos en alto o en bajo. Tampoco se asigna una cifra de nanosegundos. Las hojas de datos de chips reales determinarán qué combinaciones eléctricas y tiempos serán válidos. Como regla funcional, **no se debe leer y escribir simultáneamente en una misma transacción**.

## 6. ¿Cómo comienza a entenderse una instrucción?

PC señala el **próximo byte** que debe leerse, IR conserva el opcode actual y registros temporales reciben los datos que acompañan a ese opcode. Usaremos el ejemplo de la **ISA candidata**, todavía revisable: colocar el número decimal 42 en R0 con la escritura `LDI R0, 42`.

El borrador representa esa instrucción mediante **tres bytes consecutivos**. El primero identifica la operación; el segundo selecciona R0; el tercero es el propio valor de ocho bits. Esta separación permite que cada campo se vea con claridad en el laboratorio.

| Dirección | Byte en RAM | Interpretación de este ejemplo |
| --- | --- | --- |
| `0x6000` | `0x11` | Opcode candidato de `LDI`. |
| `0x6001` | `0x00` | Selector candidato de `R0`. |
| `0x6002` | `0x2A` | Inmediato decimal `42`. |

Una secuencia de dependencias sería: poner `PC=0x6000` en MAR, leer `0x11` e introducirlo en IR, avanzar PC a `0x6001`; leer el selector y avanzar a `0x6002`; leer el inmediato y avanzar a `0x6003`; por último, permitir que R0 capture `0x2A`. Nada de ello exige una operación de suma de datos del programa. El incremento de PC tiene su propio problema de diseño, que abordaremos enseguida.

[[EQ:PC inicial = 0x6000 ; PC tras tres bytes = 0x6003]]

[[EQ:IR = 0x11 ; SEL = 0x00 ; TMP = 0x2A ; R0 ← TMP]]

¿Por qué `PC=0x6003` y no `0x6001`? Porque **esa instrucción de ejemplo ocupa tres posiciones de memoria**, no una. El opcode mide un byte, pero una instrucción puede contener más bytes. De momento esto es un recorrido **explicado en papel**, no un registro de ejecución de CPU ni microcódigo capaz de encender señales.

La misma ruta permite después explicar una orden candidata de almacenamiento `ST [0x6F00], R0`: además del opcode y selector, debe leer la dirección baja `00` y la alta `6F`. Esos valores se retienen mientras el circuito organiza una transacción hacia RAM. **No basta conservarlos solo en MDR**, porque cada lectura posterior puede sobrescribirlo.

## 7. Dieciséis bits de dirección con una ALU de ocho

Un problema arquitectónico aparece enseguida: si ALU tiene ocho bits, ¿cómo aumentamos PC, SP o X, que contienen **dieciséis**? En principio es posible procesar por separado los bytes **bajo** y **alto**, transportando un acarreo temporal entre las operaciones. Para X, tomemos `0x12FF` y sumemos `2`.

[[EQ:X inicial = 0x12FF ; desplazamiento = 0x0002]]

Primero se calcula `0xFF+0x02=0x101`: se conserva el byte bajo `0x01` y se transporta un acarreo de `1`. Después se calcula `0x12+0x00+1=0x13` para el byte alto. Al unir las mitades, obtenemos `X=0x1301`.

[[EQ:0xFF + 0x02 = 0x101 ⇒ bajo = 0x01, acarreo = 1]]

[[EQ:0x12 + 0x00 + 1 = 0x13 ⇒ X nuevo = 0x1301]]

[[FIG:c12_fig04_direccion_dos_pasadas|Figura 4. El registro X de 16 bits puede incrementarse con una ALU de ocho mediante una pasada por cada byte y un acarreo interno separado de la bandera C visible.|Esquema paso a paso: X inicial 12 FF; suma baja FF+02 entrega 01 y acarreo interno 1; suma alta 12+00+1 entrega 13; X final 13 01. La señal ADDR_CARRY se separa de FLAGS.C.]]

Hay una condición esencial: este acarreo para **calcular direcciones** no debería sobrescribir la bandera `C` que una instrucción aritmética dejó para el programa. La microarquitectura candidata reserva una señal temporal llamada `ADDR_CARRY` para evitar esa confusión. Si `FLAGS.C` valía `1` antes de actualizar X, seguirá valiendo `1` después de esa actualización en la propuesta actual.

Para incrementar PC existe otra alternativa candidata: un **incrementador dedicado de 16 bits**. Facilitaría el avance secuencial del programa, aunque añadiría componentes. Todavía no hemos escogido físicamente entre esa opción y reutilizar la ALU de ocho bits. **El libro no debe dibujar una ALU de dieciséis bits escondida** y llamarla Aula-8 sin explicar el cambio de diseño.

## 8. La unidad de control organiza movimientos, no inventa datos

El componente que falta en el mapa es la **unidad de control**. Conceptualmente, recibe información como el opcode en IR y el estado actual, y decide acciones lógicas: cuál fuente del bus habilitar, qué destino cargar, qué operación pedir a la ALU, qué dirección presentar y si procede acceder a memoria. Un diseño candidato contempla una pequeña ROM **interna de microcontrol**, distinta de la ROM de **firmware** que ocupa direcciones visibles para el programa.

| Situación | Fuente o acción necesaria | Destino o efecto |
| --- | --- | --- |
| Copiar `R1 → R0` | Seleccionar R1 en el bus interno | Cargar R0, conservar R1. |
| Leer RAM | MAR presenta dirección; RAM entrega dato | MDR captura byte válido. |
| Escribir RAM | MAR presenta dirección; MDR entrega dato | RAM captura byte bajo WR. |
| Leer opcode | PC proporciona dirección para MAR | IR captura byte y PC avanza. |
| Sumar en ALU | Seleccionar operandos y función ADD | Destino recibe S si está habilitado. |

El dibujo funcional no responde todavía **cuántos ciclos** demora cada acción, qué estados forman el microsecuenciador o cómo se implementan sus selectores con chips. Por eso **ninguna de estas filas debe leerse como un circuito eléctrico ya probado**.

En las próximas lecciones distinguiremos entre ejecutar una orden, entrar en estado de detención `HALT` y arrancar con `RESET`. **Reiniciar no equivale necesariamente a ejecutar los bytes recién depositados en RAM**: un arranque normal podría obtener un vector desde ROM y comenzar en el firmware. Esa diferencia será decisiva cuando lleguemos al panel manual.

## Construimos Aula-8: lo acumulado ya tiene una arquitectura

Conviene detenernos a reconocer lo que hemos ensamblado sobre el papel. El capítulo 7 añadió un registro que conserva un byte; los capítulos 8 y 9 introdujeron los buses y las posiciones de RAM; los capítulos 10 y 11 aportaron el cálculo. La unidad de control seleccionará rutas y cargas, mientras PC, SP y X conservarán direcciones de **dieciséis bits**, aunque la ALU general sea de ocho. MAR y MDR hacen explícita la separación entre **dirección** y **dato**.

[[FIG:c12_fig05_ruta_acumulada_aula8|Figura 5. Vista acumulativa de Aula-8: registros generales, ALU8, direccionamiento, control y memoria son subsistemas diferentes.|Diagrama funcional de R0 a R3, ALU8, RAM/ROM, PC/SP/X, CONTROL y MAR/MDR, todavía sin una netlist física definitiva.]]

Este dibujo no pide memorizar seis rectángulos: sirve para **seguir una operación**. Al ejecutar conceptualmente una suma, R0 y R1 proporcionan operandos, la ALU calcula y la orden de carga conserva el resultado. Al almacenar el valor, los datos pasan por la ruta de MDR y la dirección por MAR hacia la memoria seleccionada. El capítulo siguiente comenzará a decidir en qué orden se producen esos movimientos. Una figura de esta escala muestra la relación entre unidades; para comprobar un pin o un flanco deberemos acercarnos al nivel lógico o a un componente seleccionado.

## Ejercicios del capítulo 12

Indica siempre si escribes una **dirección de 16 bits** o un **dato de ocho**. Cuando uses bytes candidatos de instrucción, aclara qué campo representan: ninguno se interpreta por intuición.

**Ejercicio 1 — Datos y direcciones.** Si `R0=0x2A` y `PC=0x6000`, explica qué representa cada valor y cuántos bits tiene su registro.

**Ejercicio 2 — Espacio direccionable.** Calcula cuántas direcciones de byte hay con 16 líneas A0–A15. ¿Implica eso instalar esa cantidad de RAM?

**Ejercicio 3 — Tabla de registros.** Identifica qué recurso se usa para cada tarea: datos ordinarios, dirección de instrucción, pila, índice, dirección estable de memoria y byte transferido.

**Ejercicio 4 — Copia de registro.** Dado `R1=0x3C` y `R0=0x00`, describe fuente, destino y condición de carga para que `R0` termine valiendo `0x3C` sin borrar R1.

**Ejercicio 5 — Conflicto del bus.** Explica por qué es incorrecto habilitar simultáneamente R0 con bit `0` y R1 con bit `1` como fuentes sobre la misma línea.

**Ejercicio 6 — Leer memoria.** Ordena MAR, RD, bus de datos y MDR para leer un byte en `0x6F00`. ¿Quién conduce el bus externo de datos?

**Ejercicio 7 — Escribir memoria.** Si `R0=0x2A`, describe el valor que recibirían MAR y MDR para guardar el byte en `0x6F00`; indica qué se solicita a RAM.

**Ejercicio 8 — Una instrucción de tres bytes.** Para el ejemplo candidato `11 00 2A` iniciado en `0x6000`, di los contenidos de IR, SEL y TMP y el valor de PC después de leer sus tres bytes.

**Ejercicio 9 — Byte bajo y alto.** Al preparar el destino `0x6F00` para una orden candidata ST, ¿qué byte de dirección se lee primero y por qué hay que conservar ambos fuera de MDR?

**Ejercicio 10 — Índice de dieciséis bits.** Calcula `X=0x12FF+2` con dos operaciones de ocho bits. Muestra el acarreo entre ellas.

**Ejercicio 11 — Flags preservadas.** Si antes de actualizar X la bandera visible `C` vale `1`, ¿cuál debe quedar después y en qué señal se conserva el acarreo interno?

**Ejercicio 12 — Arquitectura frente a implementación.** Distingue ALU, datapath, control y memoria. Indica dos cosas que todavía deben validarse antes de afirmar que Aula-8 es una computadora física funcional.

## Solucionario del capítulo 12

**1.** `R0` almacena un dato de ocho bits: `0x2A=00101010₂=42`. `PC` tiene dieciséis bits y señala la dirección `0x6000` del próximo byte de programa; no representa el dato 42.

**2.** `2¹⁶=65536` direcciones posibles; si cada una identifica un byte, el espacio es `65536 B=64 KiB`. No implica RAM instalada: puede haber ROM, E/S y huecos sin asignar.

**3.** Datos ordinarios: `R0–R3`. Próximo byte de instrucción: `PC`. Pila: `SP`. Índice: `X`. Dirección estable durante una transacción: `MAR`. Byte transferido hacia/desde memoria: `MDR`.

**4.** Se selecciona R1 como **única fuente** del bus interno y se habilita **carga de R0**. Cuando se capture el valor, `R0=00111100₂=0x3C`; R1 mantiene su contenido porque no se ordenó escribirlo.

**5.** Dos salidas no pueden imponer simultáneamente niveles lógicos diferentes sobre el mismo conductor; existiría contención eléctrica. Hay que habilitar una sola fuente por segmento de bus.

**6.** `MAR←0x6F00`; seleccionar memoria; solicitar `RD`; el dispositivo presenta el byte válido en D0–D7; `MDR` lo captura. **La memoria seleccionada conduce los datos**, y la CPU solo los recibe.

**7.** `MAR=0x6F00`; `MDR=0x2A` preparado desde R0. La CPU conduce el byte de datos, selecciona RAM y solicita `WR`; RAM captura ese dato. Ninguna otra salida debe conducir simultáneamente.

**8.** `IR=0x11` (opcode LDI candidato), `SEL=0x00` (R0), `TMP=0x2A` (42). Al consumir tres bytes, `PC=0x6003`; después R0 puede cargar `0x2A` al recibir su señal de escritura.

**9.** En el formato little-endian candidato se lee primero `0x00` (bajo) y luego `0x6F` (alto), formando `0x6F00`. Hay que retenerlos en latches candidatos porque cada nueva lectura puede sobrescribir MDR.

**10.** Bajo: `FF+02=101` hexadecimal → bajo `01`, acarreo `1`. Alto: `12+00+1=13`. Dirección final: `0x1301`.

**11.** La bandera visible debe seguir `C=1`. El cálculo auxiliar de la dirección usa `ADDR_CARRY=1` en el paso bajo y lo consume al calcular el alto. No modifica `FLAGS.C`.

**12.** La **ALU** calcula; el **datapath** transporta y guarda valores; el **control** elige movimientos y condiciones; la **memoria** conserva bytes de instrucciones/datos. Faltan, entre otras cosas, conexiones eléctricas verificadas, temporización, microestados codificados y pruebas de ejecución real.

## Para continuar

Ya podemos seguir un dato desde un registro hasta otro, separar una dirección de un byte y entender por qué el PC, los registros temporales y las señales de lectura/escritura son necesarios. En el **capítulo 13, «La unidad de control»**, veremos cómo se ordenan esas acciones en estados lógicos, cómo se selecciona la siguiente acción y por qué una microoperación escrita en papel no es todavía un ciclo de reloj construido.

Fuentes de arquitectura del proyecto: *MICROARQUITECTURA_AULA8_BORRADOR.md*, *UNIDAD_CONTROL_AULA8_BORRADOR.md* e *ISA_AULA8_CANDIDATA.md* (propuestas internas R0.3–R0.5, no aprobadas). Diagramas y ejemplos de este capítulo elaborados originalmente para Aula-Computadora.
