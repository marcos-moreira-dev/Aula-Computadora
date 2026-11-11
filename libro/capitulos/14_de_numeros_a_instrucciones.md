# Capítulo 14. De números a instrucciones

*Parte IV · Construir Aula-8 · Aula-Computadora*

En el capítulo 13 seguimos las órdenes internas que permitirían leer, interpretar y ejecutar una instrucción. Falta responder una pregunta más cercana a nuestras manos: **¿cómo entra una orden en la memoria si todavía no tenemos teclado, editor ni ensamblador?** Una pequeña computadora puede comenzar con interruptores, un panel de direcciones y datos y un mecanismo que deposite bytes en RAM, siempre que su circuito de control se haya construido correctamente. Podemos preparar el programa **antes** de que exista el software capaz de escribir programas.

Vamos a traducir un ejemplo completo de lenguaje ensamblador a bytes, colocarlos uno a uno en posiciones de memoria y examinar el resultado esperado. Trabajamos con la **ISA candidata de Aula-8**, no con una máquina terminada: los opcodes, el panel, la ROM de arranque y los mecanismos de parada son propuestas documentales. Aquí sí podemos demostrar conversiones y comprobar que los bytes son coherentes. **Todavía no podemos afirmar que Aula-8 los ejecutó.**

## 1. La memoria no guarda palabras como «cargar»

Una celda de ocho bits almacena un patrón de ceros y unos. Si depositamos `00101010`, un observador puede leer ese patrón como el número decimal **42** o como `0x2A` hexadecimal. Ninguna de esas interpretaciones viaja dentro del byte: las aporta quien lo lee. Si el procesador usa esa posición como parte de una instrucción, la interpretación depende de **la posición en la secuencia** y de las reglas de su ISA.

El hexadecimal nos permite escribir ocho bits con dos símbolos. Cada grupo de cuatro bits se llama **nibble**: `0010` vale `2` y `1010` vale `A` (diez). Así, `0010 1010` se escribe `2A`, y `0x2A` indica explícitamente que no estamos usando decimal. También puede comprobarse por divisiones: `42 ÷ 16 = 2`, resto `10`; el resto diez se representa como `A`.

[[EQ:42 en decimal = 00101010 en binario = 0x2A]]

[[EQ:42 = (2 × 16) + 10]]

[[FIG:c14_fig01_un_byte_tres_lecturas|Figura 1. El mismo patrón de ocho bits se puede leer en binario, hexadecimal o decimal; su significado de instrucción depende del contexto.|Un byte 00101010 dividido en dos grupos de cuatro bits: 0010 y 1010. Debajo aparecen los dígitos 2 y A, el hexadecimal 0x2A y su valor decimal 42. Una nota distingue valor almacenado de significado del programa.]]

**No es lo mismo el número 42 que el texto «42».** Si tecleamos los caracteres `4` y `2` en una terminal, esos caracteres necesitan una codificación textual y, normalmente, ocupan dos bytes. Un valor numérico de ocho bits como `0x2A` ocupa un byte. En nuestro programa elegimos **el segundo caso**: cargar el número, no escribir dos caracteres.

## 2. Una ISA es un acuerdo para interpretar bytes

La **arquitectura de conjunto de instrucciones**, abreviada ISA, establece qué patrones representan operaciones, cuántos bytes ocupa cada una y qué deben significar sus operandos. En la propuesta de Aula-8, **el primer byte es el opcode**. Después pueden venir un selector de registro, un valor inmediato, una dirección o un desplazamiento.

| Forma candidata | Bytes consecutivos | Para qué sirve |
| --- | --- | --- |
| Sin operandos | `OP` | `HALT` termina la búsqueda de nuevas instrucciones. |
| Registro | `OP r` | Indica uno de R0–R3. |
| Par de registros | `OP rr` | Compacta destino y fuente en un byte. |
| Registro e inmediato | `OP r valor` | Deja un número de ocho bits en el registro. |
| Dirección absoluta | `OP bajo alto` | Referencia una dirección de dieciséis bits. |
| Memoria | `OP sel dir16` o `OP sel d` | Identifica modo, registro y dirección. |

En la tabla, `OP` no significa el carácter literal O seguido de P: es **un lugar reservado para el byte de operación**. Tampoco es código de procesadores comerciales; nuestra propuesta tiene **36 opcodes distintos**, que todavía necesitan implementación y revisión. En el capítulo anterior solo describimos **tres rutas de microcontrol**, así que no debemos confundir «tiene un número asignado» con «está construido».

Una buena regla de lectura es preguntar: *¿estoy mirando el primer byte de una instrucción o uno de sus operandos?* El valor `0x01` puede aparecer como opcode `HALT`, o como selector de `R1`, o como un dato numérico. La CPU no debería interpretar cada byte de RAM como un opcode independiente.

## 3. Traducir `LDI R0,42` de izquierda a derecha

Empecemos con la instrucción **LDI R0,42**. `LDI` significa en esta propuesta «cargar un valor inmediato»; el registro es R0 y el valor es el decimal 42. La especificación candidata asigna `0x11` al opcode `LDI`; el selector de R0 es `0x00`; el valor 42 es `0x2A`.

| Posición | Byte hexadecimal | Función |
| --- | --- | --- |
| Primero | `11` | Opcode de `LDI`. |
| Segundo | `00` | Selector de R0; `01`, `02` y `03` seleccionarían R1, R2 y R3. |
| Tercero | `2A` | Dato inmediato, el número 42. |

Juntos, de izquierda a derecha, los tres bytes quedan **11 00 2A**. El espacio los separa solo para facilitar nuestra lectura: en RAM ocuparían celdas consecutivas.

[[EQ:LDI: 1 opcode + 1 selector + 1 inmediato = 3 bytes]]

Si el primer byte se deposita en la dirección `0x6000`, los siguientes van en `0x6001` y `0x6002`. Después de consumir los tres, el próximo inicio de instrucción estará en `0x6003`. No necesitamos que `0x6000` tenga un significado especial universal: es una **dirección elegida** dentro de la ventana de práctica propuesta.

[[EQ:PC siguiente = 0x6000 + 3 = 0x6003]]

El registro PC es de dieciséis bits, aunque cada celda del programa almacene solo ocho. Por eso una instrucción puede ocupar tres posiciones **de memoria consecutivas** mientras PC almacena una única **dirección**. Si el selector fuese `07`, sería inválido para R0–R3 en esta forma: el control debe detectar el error antes de escribir un registro.

## 4. Traducir una dirección de dieciséis bits

Nuestra segunda instrucción, `ST [0x6F00],R0`, dice: **guardar el contenido de R0 en la celda de RAM cuya dirección es 0x6F00**. La ISA candidata asigna el opcode `0x13` a `ST`. Para el modo absoluto y R0, el selector es `00`. El destino ocupa **dos bytes de dirección**, porque existen 65536 posiciones direccionables con dieciséis bits.

La dirección `0x6F00` se separa en byte alto `6F` y byte bajo `00`. La propuesta utiliza orden **little-endian en los operandos de dieciséis bits**: deposita **primero 00, después 6F**. Al leerlos, el procesador debe reconstruir la dirección original, no la dirección `0x006F`.

[[EQ:0x6F00 = (0x6F × 256) + 0x00]]

[[EQ:ST: 1 opcode + 1 selector + 2 dirección = 4 bytes]]

Por tanto, `ST [0x6F00],R0` se convierte en **13 00 00 6F**. El primer `00` indica registro y modo; el segundo `00` es el byte bajo de dirección. Son iguales como valores, pero **cumplen papeles distintos**. El opcode y el contexto son los que permiten descodificarlos.

[[FIG:c14_fig02_mapa_programa|Figura 2. Ocho posiciones consecutivas almacenan tres instrucciones de longitudes diferentes; 0x6F00 es el destino de datos, no parte del bloque de código.|Mapa de programa 6000 a 6007 con colores para opcode, selector, inmediato y dirección baja/alta. Las agrupaciones identifican LDI de tres bytes, ST de cuatro y HALT de uno, con flecha separada hacia RAM 6F00 que recibirá 2A.]]

## 5. Tres maneras de señalar una celda

El programa anterior usa **direccionamiento absoluto**: escribimos en los propios bytes de instrucción la dirección final. Pero una CPU también puede necesitar recorrer arreglos o variables próximas a un registro. La propuesta de Aula-8 distingue tres modos para `LD` y `ST`: **absoluto**, **relativo a X** y **relativo a SP**. Los dos últimos agregan un desplazamiento de ocho bits con signo a un registro de dieciséis bits.

| Forma de ejemplo | Bytes candidatos | Dirección efectiva |
| --- | --- | --- |
| `LD R0,[0x6F00]` | `12 00 00 6F` | Exactamente `0x6F00`. |
| `LD R1,[X-1]` | `12 05 FF` | `X−1`, con aritmética módulo 65536. |
| `LD R2,[SP+6]` | `12 0A 06` | `SP+6`, también módulo 65536. |

El byte selector combina **modo** y **registro**: los bits inferiores identifican R0–R3 y el siguiente par identifica el modo (0 absoluto, 1 por X, 2 por SP). El modo 3 está **reservado**. En `05` tenemos `1×4+1`: modo X, registro R1; en `0A` tenemos `2×4+2`: modo SP, registro R2.

[[EQ:selector = (modo × 4) + registro]]

[[EQ:0x05 = (1 × 4) + 1]]

[[FIG:c14_fig03_modos_direccion|Figura 3. El direccionamiento absoluto aporta dos bytes de dirección; los modos X y SP calculan la dirección usando un desplazamiento firmado de ocho bits.|Tres paneles comparan LD R0,[6F00] con selector 00 y operandos 00 6F; LD R1,[X-1] con selector 05 y FF, donde FF es -1; LD R2,[SP+6] con selector 0A y 06. Ningún modo implica una CPU implementada.]]

Hay un detalle que conviene practicar: `0xFF` interpretado como **entero sin signo** vale 255, pero como **desplazamiento firmado de ocho bits** vale −1. La ISA señala el papel de ese byte. Si X fuera `0x6004`, `X−1` produciría `0x6003`, y no `0x6103`. La ALU de ocho bits puede calcular la dirección en dos pasadas, como ya estudiamos: **la regla de programación no implica una ALU física de dieciséis bits**.

[[EQ:X = 0x6004 ; d = −1 ; dirección = 0x6003]]

## 6. Escribir el programa completo en papel

Unamos nuestras tres órdenes. La última es `HALT`, opcode candidato `0x01`, que no trae operandos. Las direcciones siguientes muestran el programa **completo**, no solo los números que lo forman. El contenido inicial de RAM es desconocido; solo las ocho posiciones que depositamos quedan determinadas por esta actividad.

| Dirección de RAM | Byte a depositar | Interpretación |
| --- | --- | --- |
| `6000` | **11** | Comienza `LDI R0,42`. |
| `6001` | `00` | Selector de R0. |
| `6002` | `2A` | Inmediato 42. |
| `6003` | **13** | Comienza `ST [6F00],R0`. |
| `6004` | `00` | Selector absoluto/R0. |
| `6005` | `00` | Dirección baja. |
| `6006` | `6F` | Dirección alta. |
| `6007` | **01** | `HALT`. |

[[EQ:3 + 4 + 1 = 8 bytes]]

Si un ensamblador existiera, podría aceptar esta escritura simbólica y emitir los bytes, pero **todavía no existe un ensamblador Aula ejecutable**. Aquí hicimos esa traducción a mano. Al decir «opcode `13`», nos referimos al byte hexadecimal **0x13**, no al número decimal trece. Quien prepara los interruptores debe decidir antes qué base numérica está usando.

## 7. ¿Cómo entra un byte si no tenemos software?

Imaginemos un **panel manual didáctico**. Para introducir un byte, el operador detiene o aísla la CPU, selecciona una dirección de dieciséis bits, dispone ocho interruptores de datos y activa un pulso **DEPOSIT**. En un diseño real, esa acción debe pedir el bus, excluir a otros conductores, presentar dirección y dato con tiempos válidos y habilitar correctamente la escritura de RAM. No basta con conectar interruptores directamente a un bus ocupado. Para inspeccionar, **EXAMINE** solicitaría una lectura segura y mostraría el byte mediante indicadores.

[[FIG:c14_fig04_panel_seguro|Figura 4. El panel manual puede depositar y examinar bytes solo después de detener y aislar la CPU; después devuelve el control antes de iniciar el programa.|Secuencia conceptual: CPU detenida y bus concedido al panel; dirección de 16 bits y datos de 8 bits con interruptores; DEPOSIT/EXAMINE sobre RAM; liberación del bus; arranque explícito desde la dirección del programa. Advertencia de que no es un esquema eléctrico ni una rutina programada.]]

El orden de operación propuesto sería: **detener**, establecer `6000` y `11`, solicitar DEPOSIT, inspeccionar si la celda se grabó, avanzar a `6001`, poner `00` y repetir. Un panel puede disponer de **DEPOSIT NEXT**, que incrementaría la dirección automáticamente; pero tampoco podemos asumir que ya existe un contador, pulso o circuito con esa función. Primero hay que diseñarlos y comprobarlos.

**Cargar no equivale a ejecutar.** Después del último depósito, el panel debe ceder el bus. Además hace falta un mecanismo explícito para establecer el PC de arranque en `0x6000` o invocar el programa desde un monitor. Pulsar RESET no implica comenzar en RAM: el diseño candidato consulta el vector de firmware en `0xFFFC–0xFFFD`, que podría llevar a un monitor de ROM.

## 8. Panel detenido y monitor de firmware no son lo mismo

Existen dos caminos conceptuales para escribir RAM. El **panel detenido** usa controles físicos propuestos sobre los buses y necesita arbitraje. Un **monitor hexadecimal** sería un programa ejecutado por la CPU desde una ROM **ya grabada**: recibiría comandos como `POKE 6000 11` y `MEM 6000 08`, convertiría los caracteres a valores y haría las escrituras o lecturas mediante instrucciones reales. El segundo camino presupone **un firmware funcional**, que no aparece mágicamente por instalar RAM.

| Panel físico propuesto | Monitor propuesto en firmware |
| --- | --- |
| Opera con CPU detenida y bus concedido. | Opera como código nativo de la CPU. |
| Usa interruptores, pulsos y visualización. | Usa comandos y rutinas de E/S. |
| Requiere arbitraje y señales físicas. | Requiere ROM grabada, CPU, terminal y parser. |
| No necesita un intérprete de texto. | Debe interpretar texto hexadecimal como bytes. |

En el monitor candidato, `POKE` solo admite la ventana de práctica `6000–6FFF`; `MEM` puede examinar rangos legibles de RAM o ROM bajo reglas de validación. **Ningún comando de ese monitor está ejecutándose hoy sobre Aula-8**. Tampoco sería correcto presentar un `POKE` en ROM como válido: no es una operación ordinaria de escritura de RAM.

Una diferencia de finalización merece atención: el ejemplo usa `HALT`, que **detendría la CPU**, no devolvería automáticamente el prompt. En la propuesta de monitor, `RUN` inicia una rutina mediante `CALL`; un programa que termina con `RET` y mantiene equilibrada la pila podría regresar al monitor. **HALT y RET no son intercambiables**, y el panel de parada/reanudación todavía necesita diseño.

## 9. Leer la tabla de depósitos y detectar errores

Antes de cualquier intento de arranque hay que hacer una **comprobación por lectura**: examinar `6000–6007` y comparar los ocho valores con la tabla. Si `6002` contiene `42` hexadecimal en lugar de `2A`, el programa no cargaría el decimal 42: cargaría **66 decimal**. Si intercambiamos `00` y `6F` en los dos bytes de dirección, reconstruiríamos `0x006F` en lugar de `0x6F00`.

[[EQ:0x42 = (4 × 16) + 2 = 66 decimal]]

Otros errores de principiante también importan: depositar el byte correcto en la **dirección equivocada**; tratar un operando como nueva instrucción; intentar usar el modo reservado 3; dar DEPOSIT con el bus de CPU activo; o creer que RAM conserva el programa indefinidamente después de apagar. La RAM de trabajo es **volátil**; para permanencia haría falta almacenamiento no volátil y un mecanismo de carga probado.

El **resultado funcional esperado**, si finalmente se construyen la CPU, el control y el sistema de memoria acordados, sería `R0=0x2A` y `RAM[0x6F00]=0x2A`. Al leer el opcode final `HALT`, PC apuntaría a `0x6008`. En papel esperamos **ocho lecturas de bytes de programa y una escritura de dato**, no nueve ciclos de reloj.

[[EQ:RAM[0x6F00] = 0x2A ; PC final = 0x6008]]

## 10. Cuando un byte es una dirección de salto

El programa anterior sigue la memoria en orden. Un futuro bucle necesitará cambiar el PC: por ejemplo, el borrador propone `JNZ 0x6003` con los bytes **32 03 60**. El opcode `32` significa «saltar si Z es cero»; `03` y `60` forman el destino `0x6003` en orden little-endian. Si Z fuera uno, se continuaría después de los tres bytes. El salto sigue siendo candidato: **aún no hemos presentado una microsecuencia ejecutada ni un circuito real de selección de PC**.

Esta pequeña muestra prepara el capítulo siguiente: un programa no consiste solo en valores y direcciones bien escritos; necesitamos observar el **recorrido de buscar, decodificar y ejecutar**, incluido el momento en que PC avanza o cambia de destino.

## Construimos Aula-8: leer la RAM como si estuviéramos frente al panel

En los esquemas anteriores la memoria era un bloque con una dirección de entrada. Ahora abrimos ese bloque: cada fila representa **una dirección consecutiva** y su byte. La instrucción `LDI R0,42` no ocupa una única posición misteriosa: el opcode `11`, el selector `00` y el dato `2A` residen en `0x6000`, `0x6001` y `0x6002`. Los cuatro bytes de ST siguen inmediatamente, y HALT está en `0x6007`. La interpretación depende de la posición en la instrucción y de la ISA candidata.

[[FIG:c14_fig05_ram_contigua_deposito|Figura 5. Los ocho bytes candidatos de LDI, ST y HALT ocupan las direcciones consecutivas 0x6000 a 0x6007.|Mapa vertical de ocho posiciones RAM contiguas y una segunda celda RAM 0x6F00; ST almacena 0x2A en esa celda sin alterar los bytes del programa.]]

La flecha de escritura apunta a `0x6F00`, **fuera del tramo donde guardamos el programa**. Así podemos explicar a la vez por qué un opcode es un dato binario y por qué los programas suelen distinguir espacio de instrucciones, variables y pila aunque compartan la misma RAM. La figura ilustra la operación esperada; no prueba que una CPU ya la haya ejecutado.

Un salto muestra otra propiedad del mismo arreglo de bytes. En este ejemplo complementario, `30 06 60` significa `JMP 0x6006` según el contrato candidato. Las direcciones `0x6003–0x6005` siguen existiendo, pero la CPU cambia su PC y **no ejecuta** la instrucción situada allí.

[[FIG:c14_fig06_ram_salto|Figura 6. El contador de programa salta de 0x6000 a 0x6006 y omite tres bytes de una instrucción, sin mover el contenido de RAM.|Diez direcciones consecutivas muestran JMP, LDI omitida, LDI ejecutada y HALT; una flecha externa indica PC igual a 0x6006.]]

En el libro usaremos esta convención: **filas contiguas para mostrar posiciones físicas y flechas externas para representar el flujo del PC**. Una flecha de programa nunca se interpretará como un cable eléctrico. Cuando un salto vaya mucho más lejos, el dibujo señalará explícitamente el tramo de direcciones omitidas.

## Ejercicios del capítulo 14

Trabaja en papel con la propuesta Aula-8. Indica siempre si calculas un valor matemático o si describes una ejecución todavía hipotética.

**Ejercicio 1 — Tres representaciones.** Convierte el decimal 42 a binario de ocho bits y hexadecimal; identifica sus dos nibbles.

**Ejercicio 2 — ¿Número o texto?** Explica la diferencia entre almacenar el valor `0x2A` y almacenar dos caracteres que se ven como `42`.

**Ejercicio 3 — Bytes de LDI.** Escribe los tres bytes candidatos de `LDI R2,15` y señala cuál es opcode, selector e inmediato.

**Ejercicio 4 — Dirección del PC.** Si `LDI R2,15` empieza en `0x6010`, ¿cuál sería la dirección de la siguiente instrucción?

**Ejercicio 5 — Little-endian.** Obtén los dos bytes de dirección que irían detrás del selector para `ST [0x6F12],R0`.

**Ejercicio 6 — Roles repetidos.** En la secuencia `13 00 00 6F`, ¿por qué aparecen dos bytes `00` con funciones diferentes?

**Ejercicio 7 — Selector de modo.** Descompón el selector `0x0A`: ¿qué modo y qué registro señala? ¿Es correcto usar el modo 3 en esta versión?

**Ejercicio 8 — Desplazamiento firmado.** Interpreta el byte `FF` como disp8 firmado y calcula la dirección efectiva de `[X−1]` si `X=0x6004`.

**Ejercicio 9 — Depósito manual.** Escribe el contenido esperado de las direcciones `6000–6007` del programa LDI/ST/HALT.

**Ejercicio 10 — Error de base.** Si en `6002` se deposita `0x42` creyendo que equivale a 42 decimal, ¿qué valor cargaría R0?

**Ejercicio 11 — Arranque y fin.** Explica por qué no basta con pulsar RESET para ejecutar desde `6000` y por qué HALT no devuelve el control al monitor como RET.

**Ejercicio 12 — Salto condicional.** Interpreta `32 03 60` como instrucción candidata y explica qué cambia si Z vale cero o uno.

## Solucionario del capítulo 14

**1.** `42=00101010₂=0x2A`. El nibble alto es `0010` (`2`) y el bajo es `1010` (`A`=10). `2×16+10=42`.

**2.** El valor `0x2A` es un solo byte numérico. Los caracteres visibles «4» y «2» son símbolos de texto que, con una codificación como ASCII/UTF-8, se representan como `0x34` y `0x32`; ocupan dos bytes.

**3.** `11 02 0F`: opcode `11` para LDI, selector `02` para R2 y valor `0F` para 15 decimal. Es **codificación candidata**, no programa ejecutado.

**4.** Consume tres bytes desde `0x6010`: posiciones `6010`, `6011`, `6012`; la próxima dirección es **0x6013**.

**5.** La dirección `0x6F12` se divide en bajo `12` y alto `6F`; detrás del selector aparecería **12 6F**. La instrucción completa sería `13 00 12 6F`.

**6.** El primer `00` es el selector de **modo absoluto y R0**; el segundo `00` es el byte bajo de la dirección `0x6F00`. Su igualdad numérica es casual; su interpretación proviene del formato.

**7.** `0x0A=10 decimal=2×4+2`: modo **SP** y registro **R2**. El modo 3 está reservado; un formato válido no debe usarlo como si estuviera implementado.

**8.** `0xFF` como disp8 en complemento a dos representa **−1**. La dirección efectiva es `0x6004−1=0x6003`.

**9.** `6000:11`, `6001:00`, `6002:2A`, `6003:13`, `6004:00`, `6005:00`, `6006:6F`, `6007:01`. Hay **ocho posiciones** y tres instrucciones de tamaños 3, 4 y 1 byte.

**10.** `0x42=4×16+2=66` decimal. Cargaría **66**, no 42. El byte correcto para decimal 42 es `0x2A`.

**11.** RESET sigue el vector de ROM de firmware previsto y puede entrar al monitor, no necesariamente al programa de RAM. HALT detiene la CPU; RET recupera la dirección de retorno guardada por una llamada compatible, algo que todavía requiere CPU y pila implementadas.

**12.** `32` es JNZ; `03 60` codifica destino `0x6003`. Si **Z=0**, PC saltaría a `0x6003`; si **Z=1**, continuaría en la dirección siguiente al operando. Es un resultado definido por la propuesta, no una traza de circuito probado.

## Para continuar

Acabamos de recorrer la distancia entre un número escrito en la libreta y un programa listo para depositarse en RAM: **base numérica, opcode, operandos, dirección, orden de bytes y control seguro del bus**. Sabemos además por qué un panel detenido y un monitor de firmware resuelven problemas diferentes. En el **capítulo 15, «La instrucción en movimiento»**, seguiremos un programa desde la lectura de los bytes hasta el efecto que cada orden tendría en registros y memoria, distinguiendo siempre la traza funcional de una ejecución electrónica real.
