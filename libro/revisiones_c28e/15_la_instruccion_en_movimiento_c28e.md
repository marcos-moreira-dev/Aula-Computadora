# Capítulo 15. La instrucción en movimiento

*Parte IV · Construir Aula-8 · Aula-Computadora*

En el capítulo 14 convertimos tres instrucciones en ocho bytes y los situamos en `0x6000–0x6007`. Ya sabemos **qué** contiene la memoria. Pero cuando devolvemos el bus al procesador y le indicamos por dónde comenzar, surge una pregunta nueva: **¿cómo consigue una CPU leer esos bytes, reconocer una orden y modificar un registro o una celda de RAM?**

Vamos a seguir el programa como si pudiéramos anotar cada movimiento con un lápiz. Esta vez miraremos el **contador de programa (PC)**, los registros de dirección y datos, la unidad de control y el resultado de cada instrucción. **Es una traza funcional de la ISA y las microsecuencias candidatas de Aula-8**, no una ejecución de hardware real. Los tiempos eléctricos, los circuitos y el microcódigo definitivo siguen pendientes. Podremos describir lo que *debería* pasar, nunca afirmar que un procesador construido ya lo hizo.

## 1. El programa está quieto; las direcciones se mueven

Supongamos que el programa fue depositado correctamente, la CPU ya posee el bus y un mecanismo de arranque coloca **PC en `0x6000`**. Los valores iniciales de R0, R1–R3, FLAGS y RAM[`0x6F00`] son desconocidos. No necesitamos inventarlos: la primera instrucción establecerá R0 antes de que la segunda lo use.

| Dirección de código | Byte | Papel previsto |
| --- | --- | --- |
| `6000` | `11` | Opcode `LDI`. |
| `6001` | `00` | Selector R0. |
| `6002` | `2A` | Inmediato, 42 decimal. |
| `6003` | `13` | Opcode `ST`. |
| `6004` | `00` | Selector absoluto y R0. |
| `6005` | `00` | Dirección baja del destino. |
| `6006` | `6F` | Dirección alta del destino. |
| `6007` | `01` | Opcode `HALT`. |

Esos ocho bytes representan **tres instrucciones**, de 3, 4 y 1 byte. El código no cambia durante este ejemplo; lo que cambia es **dónde apunta PC** y qué función atribuye la unidad de control a cada lectura.

## 2. Buscar no significa leer de golpe todos los operandos

Una CPU de programa almacenado inicia cada instrucción buscando un **opcode**. El registro **PC** guarda la dirección del siguiente byte de código; **MAR** presenta una dirección a la memoria; **MDR** recibe un byte; **IR** conserva el opcode; y la unidad de control decide cómo continuar.

[[FIG:c15_fig01_camino_fetch|Figura 1. PC selecciona la dirección, MAR la presenta a RAM, MDR recibe el byte e IR conserva el opcode para el despacho.|Diagrama lógico que parte de PC=6000, pasa por MAR=6000, RAM[6000]=11 y MDR=11, llega a IR=11 y al bloque de despacho LDI. Las flechas no representan ciclos ni conexiones eléctricas verificadas.]]

La primera acción candidata se llama `FETCH_OPCODE`: coloca la dirección de PC en MAR, solicita lectura, espera un dato válido, lo captura en MDR y lo copia a IR. Después incrementa PC para señalar el siguiente byte. El orden exacto de las señales deberá diseñarse, pero el resultado lógico esperado es claro.

[[EQ:PC después de leer el opcode = 0x6000 + 1 = 0x6001]]

En el borrador técnico aparece la abreviatura `READ_PC_TO_IR`. **Una macro de lectura no es necesariamente un ciclo de reloj.** El chip de memoria podría necesitar tiempo para responder y la CPU todavía no tiene señales ni frecuencia definidas. Tampoco hay que confundir PC con MAR: más adelante MAR apuntará a `0x6F00` para escribir un dato, aunque PC continúe recorriendo `0x6000–0x6007`.

## 3. Decodificar es decidir qué ruta seguir

Después del primer fetch, `IR=0x11` y `PC=0x6001`. El bloque de **decodificación (*decode*)** consulta la ISA candidata: `0x11` representa `LDI`, que necesita un selector de registro y un inmediato. Entonces el control deriva a `LDI_SELECTOR`; todavía **no puede cargar R0**, porque desconoce los dos operandos.

El microsecuenciador puede tener su propio contador **µPC** para recorrer acciones internas. El PC del programa, en cambio, recorre direcciones visibles de RAM o ROM. Ambos contienen direcciones, pero **apuntan a espacios conceptualmente distintos**. La ROM de control propuesta tampoco es la ROM de firmware del monitor.

Si el opcode no existe en los 36 candidatos, el borrador propone `FAULT`. Si está asignado pero aún no tiene microsecuencia desarrollada, la ruta se considera **pendiente**, no una instrucción demostrada ni necesariamente ilegal. No debemos confundir una lista de nombres de operaciones con su implementación.

## 4. Ejecutar LDI requiere dos lecturas y una carga

La primera instrucción permite distinguir las tres etapas habituales: **buscar (*fetch*)**, **decodificar (*decode*)** y **ejecutar (*execute*)**. La última etapa tampoco es indivisible: hay que obtener los operandos, validarlos y habilitar la escritura del registro correcto.

| Acción lógica candidata | Lectura o movimiento | Estado esperado |
| --- | --- | --- |
| `FETCH_OPCODE` | `RAM[6000]=11` → IR. | `IR=11`, `PC=6001`. |
| `DECODE` | Elegir ruta LDI. | R0 sigue sin modificarse. |
| `LDI_SELECTOR` | `RAM[6001]=00` → SEL. | `SEL=00`, `PC=6002`. |
| `LDI_CHECK` | Validar R0–R3. | Si es inválido, no se escribe. |
| `LDI_IMMEDIATE` | `RAM[6002]=2A` → TMP. | `TMP=2A`, `PC=6003`. |
| `LDI_COMMIT` | `R[SEL] ← TMP`. | **R0=2A**, FLAGS intactas. |

[[EQ:Longitud de LDI = 1 opcode + 1 selector + 1 dato = 3 bytes]]

[[EQ:PC al finalizar LDI = 0x6000 + 3 = 0x6003]]

El inmediato `2A` **es el número 42**, no una dirección de memoria. LDI no ha escrito todavía en `0x6F00`. Además, IR debe conservar `11` aunque MDR sea reutilizado para recibir primero `00` y luego `2A`. El registro `TMP` preserva el dato que finalmente se copia a R0.

Si en lugar de `00` el selector fuese `07`, `LDI_CHECK` debería impedir el cambio de registro e ir a la ruta de fallo candidata. Primero se valida, **después** se permite `LDI_COMMIT`. Esta regla está en el borrador; aún no se ha probado un circuito de detección de errores.

## 5. ST debe recordar dos bytes de dirección

Con PC en `0x6003`, el siguiente fetch lee el opcode `13`, lo deja en IR e incrementa PC a `6004`. La ruta `ST` absoluta quiere guardar un registro en RAM. Debe descubrir **qué registro**, **qué modo de direccionamiento** y **cuál es la dirección**.

| Acción candidata | Byte leído | Resultado después de la acción |
| --- | --- | --- |
| `ST_SELECTOR` | `RAM[6004]=00` | SEL absoluto/R0, PC=`6005`. |
| `ST_CHECK` | Ninguno | Validación del formato absoluto. |
| `ST_ADDR_LOW` | `RAM[6005]=00` | `ADDR_LO=00`, PC=`6006`. |
| `ST_ADDR_HIGH` | `RAM[6006]=6F` | `ADDR_HI=6F`, PC=`6007`. |
| `ST_BUILD_MAR` | Ninguno | `MAR=0x6F00`. |

[[EQ:0x6F00 = (0x6F × 256) + 0x00]]

[[EQ:Longitud de ST absoluto = 1 + 1 + 2 = 4 bytes]]

[[FIG:c15_fig02_direccion_st|Figura 2. La dirección de ST se construye con dos bytes retenidos mientras MAR se usa para leer el programa.|Tres momentos ilustrativos: leer 00 de RAM 6005 y guardarlo en ADDR_LO; leer 6F de RAM 6006 y guardarlo en ADDR_HI; unir 6F y 00 para formar MAR=6F00. MDR cambia en cada lectura.]]

Los dos latches candidatos `ADDR_LO` y `ADDR_HI` no son adorno: **MDR cambia en cada lectura**. Cuando obtiene el byte alto `6F`, el bajo `00` ya no puede depender de MDR. La arquitectura necesita retener los operandos hasta reconstruir MAR. La implementación podría escoger otra organización interna, pero debe demostrar la misma conservación de información.

En el programa se almacena primero el byte bajo y después el alto: **little-endian**. Eso no altera cómo escribimos `0x6F00` en papel: seguimos mostrando el byte más significativo a la izquierda.

## 6. La escritura necesita el dato correcto en MDR

Ya sabemos dónde escribir: `MAR=0x6F00`. Sin embargo, **MDR contiene `6F`**, porque fue el último dato leído al construir la dirección. Si el circuito solicitara escritura inmediatamente, guardaría el **byte alto de la dirección**, no el contenido de R0.

La microsecuencia candidata incluye `ST_STAGE_DATA`: **MDR ← R0**, que en nuestro ejemplo dejaría `MDR=0x2A`. Solo después `ST_WRITE` podría pedir una escritura externa con dirección y dato correctos.

[[EQ:MDR antes de preparar = 0x6F ; MDR después = R0 = 0x2A]]

[[EQ:RAM[0x6F00] después de ST = 0x2A]]

[[FIG:c15_fig03_preparar_escritura|Figura 3. ST debe sustituir en MDR el byte de dirección 6F por el dato 2A de R0 antes de habilitar una escritura.|Panel de peligro con MAR=6F00 y MDR=6F; panel intermedio ST_STAGE_DATA con R0=2A y MDR=2A; panel de escritura con RAM[6F00] recibiendo 2A solo si el bus y la señal WR son seguros.]]

Durante la lectura, la memoria es la **fuente de datos** del bus; en la escritura, lo es la CPU. Nunca deberían conducir ambas al mismo tiempo. El esquema no decide todavía la polaridad de señales, el tiempo de acceso ni el retardo necesario antes de habilitar `WR`.

La escritura en `0x6F00` **no incrementa PC**: tras leer el byte alto de dirección, PC ya se encuentra en `0x6007`. Esa es la dirección del próximo opcode. No se necesita volver a buscar el opcode `ST` para completar su efecto.

[[EQ:PC después de ST = 0x6007]]

## 7. HALT se busca, pero no vuelve al monitor

La tercera búsqueda obtiene `RAM[6007]=01` y deja el opcode `HALT` en IR. La lectura incrementa PC a `0x6008`. Esta orden no tiene operandos; la ruta candidata `HALT_ENTER` debe impedir nuevas búsquedas y dejar el estado `HALTED`.

[[EQ:PC después de leer HALT = 0x6007 + 1 = 0x6008]]

Detenerse **no** significa volver a un monitor hexadecimal. Si una rutina fuese llamada desde firmware mediante `CALL`, necesitaría conservar la pila y ejecutar `RET` para recuperar la dirección de retorno. Aquí usamos `HALT` deliberadamente; reiniciar o reanudar requerirá controles que aún no están construidos.

## 8. Contemos accesos, no ciclos imaginarios

La traza propuesta permite enumerar todas las **transacciones externas**. En esta tabla hay lecturas de opcodes y operandos, y una sola escritura de datos. El paso interno de `DECODE` no es otra lectura de RAM.

| Orden | Operación | Dirección | Dato | Significado |
| ---: | --- | --- | --- | --- |
| 1 | Leer | `6000` | `11` | Opcode LDI. |
| 2 | Leer | `6001` | `00` | Selector R0. |
| 3 | Leer | `6002` | `2A` | Inmediato; luego R0. |
| 4 | Leer | `6003` | `13` | Opcode ST. |
| 5 | Leer | `6004` | `00` | Selector absoluto/R0. |
| 6 | Leer | `6005` | `00` | Dirección baja. |
| 7 | Leer | `6006` | `6F` | Dirección alta. |
| 8 | **Escribir** | `6F00` | `2A` | R0 → RAM, tras preparar MDR. |
| 9 | Leer | `6007` | `01` | Opcode HALT. |

[[EQ:Lecturas previstas = 3 de LDI + 4 de ST + 1 de HALT = 8]]

[[EQ:Transacciones externas previstas = 8 lecturas + 1 escritura = 9]]

[[FIG:c15_fig04_transacciones|Figura 4. La traza tiene ocho lecturas y una escritura; el último opcode se lee después de almacenar el dato.|Nueve casillas numeradas muestran LDI con tres lecturas, ST con cuatro lecturas y una escritura, y HALT con una lectura. La escritura número 8 lleva 2A a 6F00; el conjunto no representa nueve ciclos de reloj.]]

**Nueve transacciones no son nueve instrucciones ni nueve ciclos de reloj.** Cada acceso puede necesitar varias acciones internas y esperas eléctricas. Para hablar de frecuencia, duración o consumo necesitaríamos un diseño implementado y mediciones, no únicamente esta tabla.

## 9. Qué queda al final, y qué no cambia

Si finalmente se construyen la CPU y la memoria según estos contratos, la ejecución debería dejar `R0=0x2A`, `RAM[0x6F00]=0x2A`, `IR=0x01`, `PC=0x6008` y estado `HALTED`. Los ocho bytes del programa permanecerían intactos. Los valores de R1–R3 y del resto de RAM siguen siendo desconocidos, porque este programa no los define.

[[EQ:R0 final = RAM[0x6F00] = 0x2A]]

`LDI`, `ST` y `HALT` están especificadas para **conservar Z, C, N y V**. Por ello las banderas finales serían iguales a las iniciales, sean cuales sean; no podemos dibujarlas como cero por comodidad. Tampoco debemos esperar que MAR siga en `0x6F00` después del último fetch: para leer HALT tuvo que presentar `0x6007`.

Una traza funcional es una **expectativa que se puede contrastar**. Un futuro prototipo necesitará un modo seguro de inspección, medidas de control de memoria, registros y señales, y comprobaciones eléctricas de contención y temporización. Hasta entonces no podemos certificar que Aula-8 ejecutó los nueve accesos.

### Una decisión que sí podemos expresar con puertas NAND

En la lámina complementaria del capítulo 14 el salto `JNZ` presentaba dos destinos posibles. Tras leer **opcode y dos operandos**, el control dispone de una dirección secuencial, `PC_SEQ=0x6003`, y de la dirección reconstruida desde el programa, `TARGET=0x6009`. Si estamos ejecutando `JNZ`, el indicador `Z` determina cuál de las dos llega a la entrada candidata del registro PC.

| JNZ activada | Z | TAKE | Entrada candidata de PC |
| --- | --- | --- | --- |
| 0 | 0 | 0 | `PC_SEQ` |
| 0 | 1 | 0 | `PC_SEQ` |
| 1 | 0 | 1 | `TARGET` |
| 1 | 1 | 0 | `PC_SEQ` |

**Ojo con la primera columna.** Cuando `JNZ=0`, este pequeño circuito deja pasar la secuencia normal; eso no pretende implementar `JMP`, llamadas, retornos ni todas las decisiones de control. Es solamente el **selector condicional de JNZ**. El destino incondicional de `JMP` necesitará otra orden de selección o una ampliación del circuito.

En un bit cualquiera, construimos el selector usando puertas **NAND**, que reciben dos señales y producen la negación de su AND. Primero calculamos la condición compartida por los dieciséis bits; después repetimos tres NAND por cada bit de dirección. Es el mismo principio que empleamos al construir multiplexores con compuertas sencillas:

[[EQ:TAKE = JNZ ∧ NOT Z]]

[[EQ:D_i = (NOT TAKE ∧ PC_SEQ_i) ∨ (TAKE ∧ TARGET_i)]]

[[FIG:c28d_selector_pc_nand|Lámina complementaria 15A. El selector JNZ tiene 51 puertas NAND: tres de control compartido y tres por cada uno de los dieciséis bits de la dirección candidata.|La red de control calcula NZ, TAKE_N y TAKE. Una celda genérica utiliza NAND de PC_SEQ_i con TAKE_N y NAND de TARGET_i con TAKE; una tercera NAND une ambas salidas y obtiene D_i. Las redes con nombres iguales están conectadas.]]

La palabra **«entrada candidata»** importa. El dibujo calcula `D[15:0]`; **no hemos dibujado aquí el registro de PC** que capturará ese valor en un flanco, ni los controles de carga, ni los tiempos de memoria. También debemos cuidar que `Z` y las direcciones estén estables antes de la captura. Un combinacional correcto no garantiza por sí solo una computadora temporizada correctamente.

El piloto que acompaña a estas láminas genera una descripción de **51 puertas NAND y sus redes**, compara sus salidas con la ecuación del multiplexor mediante **160.144 casos de prueba** y recorre el programa de trece bytes con los dos valores posibles de `Z`. La prueba se ejecuta en Python sobre el anfitrión: **no se ha ejecutado Verilog, una netlist eléctrica con retardos, ni la CPU Aula-8**. Aun así, ya sabemos qué piezas concretas deberá conservar una implementación posterior.

### La dirección siguiente ya está calculada; ahora debemos guardarla

El selector anterior produce dieciséis señales, una por bit. Pero si sus entradas cambian, sus salidas pueden cambiar también. **Eso no significa que el PC deba obedecer inmediatamente**. Recuerda el registro de ocho bits del capítulo 7: primero preparamos la entrada y después un flanco del reloj decide si el dato se conserva o se reemplaza. Ahora repetimos la idea con **dieciséis bits**, porque el PC de Aula-8 debe poder señalar cualquiera de sus direcciones de `0x0000` a `0xFFFF`.

Llamemos `PC_NEXT` a la propuesta de dirección, `PC_Q` a lo que el registro conserva y `LOAD` a la autorización de capturar. Añadiremos un control didáctico `CLR_TEST` que pone el registro a cero **en el siguiente flanco ascendente**. Es una prueba de laboratorio del banco de flip-flops, **no el RESET verdadero de Aula-8**: para arrancar la computadora real todavía habrá que consultar su vector en ROM, sin fingir que el procesador arranca ejecutando la dirección cero.

| ¿Llegó un flanco ascendente de CLK? | `CLR_TEST` | `LOAD` | Nuevo `PC_Q` | Interpretación |
| --- | --- | --- | --- | --- |
| No | Cualquiera | Cualquiera | El anterior | Cambiar cables no equivale a escribir. |
| Sí | `1` | `0` o `1` | `0x0000` | La limpieza de prueba tiene prioridad. |
| Sí | `0` | `1` | `PC_NEXT` | Captura la dirección candidata. |
| Sí | `0` | `0` | El anterior | Retención o *HOLD*. |

Observa que esta es una **tabla de transición de estado**, no una tabla de verdad de una puerta sin memoria. Hay que conocer el estado anterior y saber si llegó un flanco. Si acabamos de encender el banco sin haberlo inicializado, su contenido se representa como `X` (*desconocido*); aplicar `HOLD` a `X` no lo convierte mágicamente en cero. Una captura válida o `CLR_TEST` sí permite conocerlo en el modelo.

Para un bit `i`, la red que alimenta su flip-flop es:

[[EQ:D_i = (NOT CLR_TEST) ∧ ((LOAD ∧ NEXT_i) ∨ ((NOT LOAD) ∧ Q_i))]]

Podemos obtener la misma función con **cinco puertas NAND por bit** y otras **dos NAND compartidas** que invierten `LOAD` y `CLR_TEST`: en total, **82 NAND combinacionales y dieciséis flip-flops D de flanco ascendente**. La cifra cuenta *solo* las NAND que preparan `D`, no las puertas internas que un integrado emplearía para construir cada flip-flop. Tampoco incluye generación de reloj, protección contra rebotes ni selección del origen de `PC_NEXT`.

[[FIG:c28e_pc16_red_y_dff|Lámina complementaria 15B. El selector de 82 NAND prepara las entradas de dieciséis flip-flops; CLK determina cuándo cambia PC_Q.|Vista general del banco PC16 con realimentación y señales LOAD/CLR_TEST; debajo, celda genérica con cinco NAND y conexiones por nombre. El dibujo representa una red lógica ideal, no un esquema eléctrico completo ni un reset físico.]]

**Probemos una equivocación frecuente.** Imagina `PC_Q=0x6000`; el combinacional recibe de pronto `PC_NEXT=0x6009`. Si `LOAD=0`, el siguiente flanco conserva `0x6000`. Si ponemos `LOAD=1` mientras el reloj ya está alto, tampoco cambia inmediatamente. Solo una transición posterior **de CLK bajo a CLK alto** permite capturar `0x6009`. De este modo el destino del salto entra en el registro en un momento definido.

Para comprobarlo sobre papel, sigue algunos momentos de una secuencia de laboratorio. La columna de la derecha muestra **el valor retenido después del evento**, no el que simplemente llega al cable.

| Evento | CLK | LOAD | CLR_TEST | PC_NEXT | PC_Q después |
| --- | --- | --- | --- | --- | --- |
| Encendido sin inicializar | bajo | 0 | 0 | 1111 | X |
| Flanco ascendente, sin carga | ↑ | 0 | 0 | 1111 | X |
| Cambiamos LOAD con CLK alto | alto | 1 | 0 | 6000 | X |
| Siguiente flanco ascendente | ↑ | 1 | 0 | 6000 | 6000 |
| Cambia la entrada, HOLD activo | ↑ | 0 | 0 | 6003 | 6000 |
| Preparado el destino del salto | ↑ | 1 | 0 | 6009 | 6009 |
| CLR_TEST aparece con CLK alto | alto | 1 | 1 | 7777 | 6009 |
| Próximo flanco: domina CLR_TEST | ↑ | 1 | 1 | 7777 | 0000 |

Los valores de dirección de la tabla están en **hexadecimal**. El calendario digital de doce observaciones incluido entre los materiales del libro permite revisar también los flancos de bajada.

Unamos esta pieza al salto del capítulo 14. Al acabar de leer los **tres bytes** de `JNZ`, el modelo anterior ofrece `PC_SEQ=0x6003` y `TARGET=0x6009`. Si `Z=0`, el selector devuelve `0x6009`; si `Z=1`, devuelve `0x6003`. **Con `LOAD=1` en un flanco ascendente**, el banco PC16 conserva el destino elegido. Si no hay ese flanco, solo tenemos una propuesta en sus entradas. La unión entre el selector de 51 NAND y el banco de 82 NAND se probó en el anfitrión, sin confundirla con una CPU completa.

Para cerrar esta etapa distinguimos tres cosas. El **modelo lógico** decide el valor que debe llegar a `D`; el **flip-flop ideal** determina cuándo ese valor se vuelve estado; el **circuito físico** tendrá que garantizar tiempos de establecimiento y retención, retardos, señales de reloj limpias y carga eléctrica admisible. Esa tercera parte continúa pendiente. La prioridad de `CLR_TEST` es válida para este piloto, pero la secuencia real de RESET, lectura del vector de ROM y entrega del bus **todavía requiere diseño y discusión**.

## 10. Dónde podría fallar un diseño

Si PC avanza dos veces tras leer un opcode, se pierde un operando. Si IR es sobrescrito con el inmediato, el despacho deja de identificar la instrucción. Si no se valida SEL, podría escribirse el registro equivocado; si se pierde `ADDR_LO`, se forma una dirección errónea; y si no se ejecuta `ST_STAGE_DATA`, terminaríamos guardando `6F` en lugar de `2A`.

Hay fallas que el papel no modela: señales con niveles eléctricos insuficientes, memorias más lentas que el pulso aplicado, dos salidas que conducen el mismo bus y comportamientos indeterminados al encender. **Los modelos Python no detectan esas fallas físicas**. El diseño R1 tendrá que resolverlas con esquemas, componentes, temporización y pruebas de laboratorio.

## Construimos Aula-8: relacionar el bus con las celdas del programa

Volvamos a la figura de RAM contigua del capítulo 14. Durante el primer fetch, `PC=0x6000` selecciona la celda del opcode `11`; después, la búsqueda del selector toma `0x6001` y la del inmediato, `0x6002`. **Son tres lecturas externas diferentes**, aunque la frase en ensamblador ocupe una sola línea. La unidad de control conserva esos bytes en registros internos pertinentes y el PC acaba preparado para el próximo opcode.

En el momento de ST, las posiciones `0x6003–0x6006` contienen código, pero `0x6F00` es el **destino de escritura**. La dirección de destino no se convierte en el nuevo valor del PC por aparecer en la instrucción: solo indica qué celda debe cambiar. La misma representación nos ayuda a no confundir un salto (`JMP`, que altera PC) con un almacenamiento (`ST`, que altera RAM). Al enseñar las dos acciones mediante flechas, cada una tendrá su significado y su condición de control propios.

## Ejercicios del capítulo 15

Trabaja con el programa `11 00 2A 13 00 00 6F 01` que comienza en `0x6000`.

**Ejercicio 1 — Estado inicial.** ¿Qué necesitamos establecer antes del primer fetch y qué registros no hace falta poner a cero?

**Ejercicio 2 — Buscar.** Después de buscar el primer opcode, ¿qué contienen PC e IR y qué dirección usó MAR?

**Ejercicio 3 — Dos direcciones.** Explica por qué PC puede contener `0x6007` mientras MAR contiene `0x6F00`.

**Ejercicio 4 — LDI en detalle.** Anota las tres direcciones leídas y el valor de R0 y PC después de la instrucción.

**Ejercicio 5 — Selector incorrecto.** ¿Qué debería pasar si el selector de LDI fuera `07`?

**Ejercicio 6 — ST absoluto.** ¿Qué significan los bytes de `6004`, `6005` y `6006`, y qué dirección forman?

**Ejercicio 7 — Error en MDR.** ¿Qué valor hay en MDR después de leer el byte alto de dirección y cómo evita ST escribirlo?

**Ejercicio 8 — Bus compartido.** ¿Quién conduce los datos en lectura y quién en escritura?

**Ejercicio 9 — Flags.** Si FLAGS empezara en `1010`, ¿cómo terminaría? ¿Y si comenzara en `0101`?

**Ejercicio 10 — Accesos.** Cuenta las lecturas y escrituras externas. ¿Por qué no equivale al número de ciclos de reloj?

**Ejercicio 11 — Parada.** Tras buscar HALT, ¿qué valen IR y PC? ¿Por qué no retorna al monitor?

**Ejercicio 12 — Evidencia física.** Propón tres mediciones para comprobar esta traza en un prototipo.

## Solucionario del capítulo 15

**1.** Los ocho bytes deben estar en RAM, el bus debe pertenecer a CPU y PC debe iniciarse explícitamente en `0x6000`. No necesitamos presuponer R0, R1–R3, FLAGS o RAM en cero: LDI establecerá R0 antes de ST.

**2.** Durante la lectura, MAR usa `0x6000`; después `IR=0x11` y `PC=0x6001`. El resto de valores depende de cuándo se observen.

**3.** PC señala el siguiente byte de código después de los operandos de ST. MAR representa la dirección efectiva de **datos** `0x6F00`; son funciones diferentes.

**4.** Lee `6000:11`, `6001:00` y `6002:2A`; luego `R0=0x2A` y `PC=0x6003` según el contrato candidato.

**5.** `07` no está permitido para LDI con R0–R3. `LDI_CHECK` debe ir a fallo antes de permitir `LDI_COMMIT`, sin alterar registros generales.

**6.** `6004:00` es selector absoluto/R0; `6005:00` es dirección baja; `6006:6F` es alta. Forman `0x6F00`, no `0x006F`.

**7.** MDR puede contener `0x6F`. `ST_STAGE_DATA` lo reemplaza por el dato `R0=0x2A` antes del pulso de escritura.

**8.** En lectura, la memoria conduce el dato; en escritura, debe conducirlo la CPU. Conducir ambos a la vez causaría contención.

**9.** `1010` se conservaría como `1010`; `0101` como `0101`. Las tres instrucciones no escriben las banderas en esta propuesta.

**10.** Son **8 lecturas** y **1 escritura**. Una transacción puede requerir varias microacciones y ciclos físicos, todavía no implementados ni medidos.

**11.** `IR=0x01` y `PC=0x6008`. HALT se detendría; RET, con una pila válida, sería la instrucción que permitiría recuperar el retorno de una llamada.

**12.** Por ejemplo: seguir PC/IR y los pulsos de lectura; observar el dato y la dirección durante WR y confirmar RAM[`0x6F00`]=`0x2A`; verificar con instrumento los tiempos y que solo un circuito conduce el bus. Sin prototipo son condiciones pendientes, no pruebas realizadas.

## Para continuar

Acabamos de unir las piezas: **PC localiza, MAR solicita, MDR transporta, IR identifica, SEL y TMP conservan operandos, y la unidad de control coordina**. La secuencia muestra por qué buscar, decodificar y ejecutar son ideas distintas, incluso cuando un libro las dibuja como tres cajas. En el **capítulo 16, «Subrutinas y pila»**, reutilizaremos ese mecanismo para estudiar llamadas, retornos, saltos y bucles: el programa ya no se limitará a avanzar siempre a la dirección siguiente.
