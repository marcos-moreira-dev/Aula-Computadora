# Capítulo 13. La unidad de control

*Parte IV · Construir Aula-8 · Aula-Computadora*

En el capítulo anterior conectamos registros, buses, memoria y una ALU. Ahora aparece una dificultad muy concreta: **los componentes no saben qué orden seguir**. Si el procesador encuentra los bytes de `LDI R0, 42`, alguien debe leerlos, conservar el código de operación, comprobar a qué registro se refieren y permitir la escritura de `0x2A` en R0. Si se activa la escritura antes de preparar el dato, la computadora puede guardar otra cosa. **La unidad de control organiza esas acciones.**

Estudiaremos una propuesta de **control microprogramado** para Aula-8: estados lógicos, señales de carga, selección de fuentes, lectura y escritura, despacho de instrucciones y una pequeña memoria interna de control. Seguiremos las tres instrucciones que el borrador ya describe: `LDI`, `ST` absoluto y `HALT`. Es importante mantener los límites: **no tenemos microcódigo binario, duración de ciclos, señales eléctricas terminadas ni CPU ejecutable**. El objetivo es comprender qué tendría que hacer una futura implementación y por qué.

## 1. Una instrucción no mueve los cables por sí sola

En un programa podemos escribir `LDI R0, 42`. Para la persona significa «dejar 42 en R0», pero la máquina solo ve una secuencia de bytes. Esos bytes no están conectados directamente a la entrada de escritura de R0. Primero hay que leerlos y decidir cuáles son **orden**, **destino** y **dato**. En el formato candidato, la instrucción utiliza tres posiciones consecutivas:

| Dirección | Byte | Interpretación candidata |
| --- | --- | --- |
| `0x6000` | `0x11` | Código de operación de `LDI`. |
| `0x6001` | `0x00` | Selector de R0. |
| `0x6002` | `0x2A` | Número inmediato 42. |

Una **microoperación** es una acción pequeña sobre el camino de datos: por ejemplo, `MAR←PC`, `IR←MDR` o `R0←TMP`. Una **microsecuencia** establece en qué orden se permiten varias de esas acciones. La unidad de control también debe decidir **cuándo no escribir**. Leer un opcode no debe modificar automáticamente R0, RAM ni las banderas.

[[EQ:IR = 0x11 ; SEL = 0x00 ; TMP = 0x2A]]

En este modelo, `IR` recibe la operación, `SEL` el selector y `TMP` el inmediato; esos recursos ya aparecieron en el capítulo 12. No hay una operación aritmética de usuario en `LDI`: la transferencia final es un movimiento controlado.

## 2. Dos contadores que no se deben confundir

El **PC** indica la próxima posición de memoria del programa. La propuesta de control microprogramado añade otro estado, que representaremos por **µPC**, la posición o referencia del **microestado** actual. Sus dominios son diferentes: `PC` recorre instrucciones almacenadas en memoria visible; `µPC` sirve para seleccionar acciones internas de control.

Imaginemos una **ROM de control** cuyas entradas describieran qué señales activar y cómo seleccionar el estado siguiente. Un **microsecuenciador** utilizaría el estado actual, la información de `IR` y condiciones relevantes para elegir esa entrada. El conjunto de señales iría después hacia registros, multiplexores, ALU y memoria.

[[FIG:c13_fig01_unidad_control|Figura 1. El PC recorre bytes del programa; µPC y la ROM de control organizan señales internas. La memoria de firmware es distinta de la memoria de microcontrol.|Dos dominios: PC direcciona RAM/ROM de firmware, IR lleva opcode al despacho; µPC selecciona ROM de control, que emite señales para datapath y memoria. ROM de control y ROM de firmware aparecen separadas; todos son bloques funcionales candidatos.]]

Una consecuencia importante: **la ROM interna de control no está contada dentro de los 8 KiB de ROM de firmware** propuestos para el mapa de memoria del programa. El firmware contendría rutinas y bytes de instrucciones; el microcontrol contendría órdenes internas para realizarlas. Todavía no fijamos el tamaño de µPC, el ancho de cada palabra de control ni la cantidad de entradas de esa ROM.

Una opción de diseño podría codificar un selector de fuente, permisos de carga de destinos, operación de ALU, solicitud de memoria y forma de avanzar al siguiente microestado. Eso **no equivale a afirmar** que cada campo ya tiene valores binarios o que existe un chip que los produzca.

## 3. Las señales deben obedecer reglas

La unidad de control no puede activar libremente todas las salidas. Del capítulo 7 recordamos que un bus compartido necesita un dueño. Si R1 y MDR intentan imponer valores distintos sobre las mismas líneas internas, habrá **contención**. Del capítulo 12 recordamos otra exclusión: en una lectura externa conduce la memoria seleccionada; en una escritura conduce la CPU.

| Grupo lógico | Acción posible | Restricción indispensable |
| --- | --- | --- |
| Fuente de datos | Seleccionar R0, R1, MDR o TMP | Solo una fuente conduce el segmento compartido. |
| Carga de destino | Habilitar R0, IR, SEL, TMP o MAR | Un registro cambia solo si se autoriza su captura. |
| Memoria externa | Solicitar `RD`, `WR` o reposo | No solicitar lectura y escritura a la vez. |
| Cálculo de dirección | Avanzar PC o usar acarreo interno | Preservar `FLAGS` cuando la orden no las modifica. |
| Flujo de control | Avanzar, saltar, despachar, detener | Cada estado tiene una transición válida y explícita. |

En un circuito real, los permisos dependen también de la temporización: **poner un dato en un bus no significa que ya esté listo para capturarse**. Hay tiempos de propagación, establecimiento y retención. Por eso un borrador de acciones no permite decir «cada fila dura un ciclo» ni elegir una frecuencia de reloj.

Una **palabra de control** sería el conjunto de campos que describe las acciones de un microestado. Sin embargo, la representación `LOAD_R0`, `READ`, `SELECT_TMP` que usamos aquí es un **nombre lógico legible**, no un patrón de pines verificado. Elegir cómo codificar esas señales será trabajo de diseño posterior.

## 4. Desarmemos una lectura de programa

La documentación candidata usa una abreviatura: `READ_PC_TO_IR`, que puede leerse como «leer el byte apuntado por PC y guardarlo en IR». Para entender de verdad el funcionamiento debemos **desplegar sus dependencias**, pues la memoria no entrega instantáneamente un byte porque escribamos una flecha.

Primero se prepara `MAR←PC`, para sostener una dirección externa. Luego se selecciona el dispositivo de memoria y se solicita `RD`. Cuando el dato sea válido, `MDR` lo captura; ya con el dato retenido, IR puede recibirlo y PC puede avanzar a la dirección siguiente. Hay que liberar la lectura cuando corresponda. Este orden es **conceptual**: todavía no hemos definido en qué flancos se capturan los registros o si algunas acciones pueden superponerse.

[[FIG:c13_fig02_macro_lectura|Figura 2. Una lectura de opcode exige preparar la dirección, solicitar lectura, recibir un byte válido y conservarlo antes de decidir qué hacer con él.|Cuatro etapas lógicas conectadas: MAR recibe PC; RAM/ROM entrega un byte bajo RD; MDR captura; IR recibe el opcode y PC avanza. Las etapas expresan dependencias, no cuatro ciclos de reloj ni duraciones medidas.]]

Supongamos `PC=0x6000`. Al leer `0x11`, IR conserva ese byte y el próximo valor del PC pasa a `0x6001`. **PC no se incrementa porque IR valga 0x11**, sino porque la política de lectura secuencial consume un byte. El incremento de una dirección de 16 bits tampoco debe destruir `FLAGS.C`: puede utilizar un incrementador independiente o una rutina interna de dos pasadas, todavía por decidir.

[[EQ:PC antes = 0x6000 ; IR = 0x11 ; PC después = 0x6001]]

Una pregunta útil: ¿qué ocurriría si una memoria tardase más de lo previsto en entregar datos? La controladora tendría que cumplir la temporización real y, quizá, incorporar espera o una entrada de «listo». **Aula-8 aún no tiene definida una señal READY ni tiempos de memoria efectivos**. No se debe inventar un mecanismo para declarar que la prueba ya existe.

## 5. Del opcode a una secuencia: despachar

Una vez retenido el opcode en IR, la unidad de control consulta la operación reconocida y selecciona la **primera acción** de la microsecuencia correspondiente. Esta decisión se denomina **despacho**. Para nuestro ejemplo, el borrador propone `0x11 → LDI_SELECTOR`, `0x13 → ST_SELECTOR` y `0x01 → HALT_ENTER`.

[[FIG:c13_fig03_despacho|Figura 3. El estado DECODE despacha un opcode a LDI, ST o HALT; una ruta prevista sin microsecuencia no equivale a un opcode ilegal.|Diagrama funcional: FETCH_OPCODE alimenta DECODE; códigos 11,13,01 se dirigen a estados iniciales LDI_SELECTOR, ST_SELECTOR y HALT_ENTER; opcode no conocido va a FAULT y operación reconocida pero todavía no descrita va a PENDING_ROUTE. No se asignan direcciones binarias a los microestados.]]

Es importante distinguir dos situaciones. Si el byte no representa **ninguna instrucción** del borrador, la ruta propuesta es `FAULT`. Si la ISA candidata **sí reconoce** esa instrucción pero todavía no hemos escrito sus acciones internas, el documento marca `PENDING_ROUTE`. Eso no es un error del programa: **es una parte incompleta de nuestro diseño de control**.

La ROM de control podría incluir un mecanismo de salto condicionado por el resultado de una comprobación o una bandera. Pero el despacho no implica que los 36 opcodes candidatos estén implementados: solo **tres** tienen aquí microsecuencias descriptivas.

## 6. Seguir `LDI R0, 42` sin saltarse verificaciones

Después de leer el opcode `11` en `0x6000`, el PC apunta a `0x6001`. Ya estamos en la ruta `LDI` y debemos leer el selector de registro, comprobarlo y después leer el valor inmediato. El orden propuesto es el siguiente:

| Estado lógico | Trabajo que solicita | Resultado esperado |
| --- | --- | --- |
| `LDI_SELECTOR` | Leer byte en PC hacia SEL | `SEL=00`; `PC=6002`. |
| `LDI_CHECK` | Comprobar SEL entre 00 y 03 | R0–R3 válidos; si no, fallo antes de escribir. |
| `LDI_IMMEDIATE` | Leer byte en PC hacia TMP | `TMP=2A`; `PC=6003`. |
| `LDI_COMMIT` | Escribir `TMP` en `R[SEL]` | `R0=2A`; `FLAGS` no cambian. |
| `LDI_END` | Volver a búsqueda de opcode | La próxima instrucción empieza en `6003`. |

Observa que **la validación precede a la escritura**. Supongamos que el selector leído fuese `0x07`: este formato solo admite cuatro registros generales (`00`, `01`, `02`, `03`). El control no debería intentar escribir un registro inexistente; la propuesta dirige ese caso a `FAULT` sin alterar R0–R3. Los efectos de fallo más amplios todavía requieren una especificación física.

[[EQ:0x6000 + 3 posiciones = 0x6003]]

[[EQ:SEL válido ∈ {00, 01, 02, 03}]]

No confundamos el **estado** `LDI_COMMIT` con un ciclo de reloj de duración conocida. El estado describe el propósito de cargar un registro en el momento permitido; la circuitería concreta todavía tiene que demostrar las señales de selección, captura y estabilidad.

## 7. Guardar en memoria exige no perder la dirección

La segunda instrucción candidata es `ST [0x6F00], R0`. Ocupa los bytes `13 00 00 6F` desde `0x6003`: opcode, selector R0, dirección baja y dirección alta. El **orden little-endian del formato** coloca `00` antes de `6F`, aunque la dirección que escribimos normalmente es `0x6F00`.

El problema se vuelve visible al leer esos bytes. Cada nueva lectura pasa por `MDR`, de modo que guardar ahí únicamente el primer byte de dirección sería un error: la lectura siguiente lo sustituiría. La microarquitectura candidata propone dos retenedores de ocho bits, `ADDR_LO` y `ADDR_HI`. Son **funciones de almacenamiento temporal**; todavía no está decidido si necesitan chips independientes.

[[EQ:ADDR_HI = 0x6F ; ADDR_LO = 0x00 ⇒ MAR = 0x6F00]]

[[FIG:c13_fig04_escritura_segura|Figura 4. La escritura ST retiene por separado los bytes de la dirección y prepara MDR con R0 antes de activar WR hacia RAM.|Secuencia funcional en tres paneles: captura ADDR_LO=00 y ADDR_HI=6F mientras MDR se reutiliza; forma MAR=6F00; copia R0=2A a MDR y solo entonces activa WR para almacenar 2A. Se advierte que escribir antes de preparar MDR grabaría el dato equivocado.]]

La secuencia lógica completa incluye leer selector, validarlo, leer bajo, leer alto, formar MAR, **preparar MDR con R0** (`ST_STAGE_DATA`) y finalmente solicitar `WR` (`ST_WRITE`). ¿Por qué debemos volver a cargar MDR con R0? Porque la última lectura dejó en MDR el byte `0x6F`, no el valor `0x2A` que queremos almacenar. Activar la escritura demasiado pronto podría grabar un byte incorrecto en `0x6F00`.

[[EQ:MDR antes de preparar = 0x6F ; MDR para WR = R0 = 0x2A]]

Después de leer los cuatro bytes de `ST`, `PC=0x6007`. Durante la escritura, el dueño del bus de datos externo es la CPU; el circuito debe impedir que RAM conduzca simultáneamente. El panel manual tampoco puede adueñarse del bus mientras la CPU lo utiliza. **Nada de esto se ha medido eléctricamente.**

## 8. Detenerse, fallar y reiniciar no son lo mismo

En `0x6007` el ejemplo coloca el opcode candidato `0x01`, que representa `HALT`. Al leerlo, PC avanzaría a `0x6008` y el control entraría en `HALT_ENTER`: desactivaría transacciones externas y propondría `HALTED=1`. **No habría una nueva búsqueda automática de instrucciones** ni un retorno espontáneo al monitor.

[[EQ:PC tras HALT = 0x6008 ; HALTED = 1]]

`FAULT` designa una condición de fallo del modelo y no es sinónimo de HALT solicitado por el programa. `RESET`, a su vez, debería conducir al procedimiento de arranque definido por el hardware y el firmware. Depositar bytes en RAM y pulsar RESET **no garantiza** que el procesador empiece justamente en esos bytes: podría empezar en un vector de ROM, ejecutar un monitor y requerir una orden explícita para saltar al programa.

El comportamiento definitivo de fallo, depuración, reanudación, temporización de RESET y aislamiento del panel debe diseñarse y comprobarse en una etapa futura. Aquí solo debemos identificar la distinción funcional para no introducir falsas capacidades en los ejercicios.

## 9. ¿Cuánto trabajo representa nuestro programa de ejemplo?

Podemos contar **transacciones externas** en la traza escrita. `LDI` lee tres bytes, `ST` lee cuatro y escribe uno, y `HALT` lee un byte. En total se **esperan ocho lecturas de memoria de programa y una escritura de datos**. Esta cuenta no es una medición de velocidad: una lectura puede exigir varios pasos internos, esperas y condiciones de reloj aún sin especificar.

| Instrucción | Lecturas de bytes | Escrituras de datos | PC al terminar su lectura |
| --- | ---: | ---: | --- |
| `LDI R0,42` | 3 | 0 | `0x6003` |
| `ST [0x6F00],R0` | 4 | 1 | `0x6007` |
| `HALT` | 1 | 0 | `0x6008` |
| **Total** | **8** | **1** | **8 posiciones consumidas** |

[[EQ:3 + 4 + 1 = 8 lecturas ; 0 + 1 + 0 = 1 escritura]]

Un diagnóstico inicial del control consiste en preguntar en cada acción: **¿qué registro conserva la dirección?, ¿quién conduce el dato?, ¿qué destino captura?, ¿en qué estado se permite avanzar?** Esas cuatro preguntas detectan muchos errores de secuencia antes de que exista un simulador de transistores.

## Construimos Aula-8: una instrucción es una serie de autorizaciones

Hasta el capítulo 12 podíamos dibujar una ruta por la que **podría** circular un dato. Para que una instrucción la utilice, la unidad de control deberá ordenar movimientos concretos: habilitar una salida, cargar un registro, elegir operación de ALU, preparar dirección en MAR, copiar dato a MDR y activar lectura o escritura. Estas órdenes no deben confundirse con los bytes que el programa almacena en RAM.

En particular, para escribir `0x2A` en `RAM[0x6F00]` la CPU primero debe conservar la dirección `6F00`, colocar **el valor `2A`** en el camino de datos y solo entonces solicitar la escritura. Si MDR todavía contiene el último byte alto de dirección `6F`, una señal `WR` prematura almacenaría el dato equivocado. Esta comprobación de **causalidad y orden** es parte de construir Aula-8, aunque la secuencia física de ciclos y la ROM interna de microcontrol aún estén por diseñar.

## Ejercicios del capítulo 13

Para cada ejercicio, explica tanto **lo que debe ocurrir** como lo que **todavía no queda demostrado** por un dibujo lógico. Trabaja con la codificación candidata de este capítulo, no con una CPU real.

**Ejercicio 1 — Funciones.** Diferencia una instrucción de programa, una microoperación y una microsecuencia usando el ejemplo `LDI R0,42`.

**Ejercicio 2 — Dos contadores.** Indica para qué sirven PC y µPC. ¿Por qué las direcciones de RAM del programa no son las mismas que las posiciones de la ROM de control?

**Ejercicio 3 — Fuente compartida.** Explica qué falla si se habilitan simultáneamente R1 y MDR como fuentes del mismo bus interno y sus bits no coinciden.

**Ejercicio 4 — Leer opcode.** Ordena preparar MAR, solicitar RD, capturar MDR, copiar a IR y avanzar PC para leer el byte `11` desde `0x6000`.

**Ejercicio 5 — Una macro no es un ciclo.** ¿Por qué no podemos afirmar que `READ_PC_TO_IR` tarda exactamente un ciclo de reloj?

**Ejercicio 6 — Despacho.** Indica las rutas iniciales propuestas para `11`, `13` y `01`, y diferencia `FAULT` de `PENDING_ROUTE`.

**Ejercicio 7 — Comprobación de selector.** Si una instrucción LDI candidata lee `SEL=07`, ¿debe cargar R0 antes de detectar un error? Justifica.

**Ejercicio 8 — LDI completo.** A partir de `11 00 2A` en `0x6000`, muestra IR, SEL, TMP, R0 y PC después de consumir la instrucción y preparar la carga.

**Ejercicio 9 — Dirección en dos bytes.** Para `ST [0x6F00],R0`, identifica los bytes de dirección, el orden de lectura y los registros temporales candidatos que deben conservarlos.

**Ejercicio 10 — El dato que no corresponde.** Explica por qué no conviene activar WR inmediatamente después de leer el byte alto `6F` de la dirección de ST si queremos guardar `2A`.

**Ejercicio 11 — Detención y arranque.** Tras `HALT` en `0x6007`, indica el PC candidato y explica por qué RESET no significa necesariamente «ejecutar desde `0x6000`».

**Ejercicio 12 — Recuento y límites.** Suma las lecturas y escrituras externas del programa LDI/ST/HALT. ¿Por qué ese total no determina cuántos ciclos, puertas lógicas o microinstrucciones físicas tendrá Aula-8?

## Solucionario del capítulo 13

**1.** La instrucción expresa un efecto visible para el programador (`R0←42`). Una microoperación sería `SEL←MDR`, `TMP←MDR` o `R0←TMP`. La microsecuencia reúne esas acciones en un orden y comprueba el destino antes de escribir. Los nombres son lógicos, no señales físicas fijadas.

**2.** PC, de 16 bits, señala el próximo byte del **programa**; µPC seleccionaría la próxima acción del **control interno**. La ROM de control no forma parte del mapa visible de RAM/ROM de firmware y todavía no tiene tamaño ni codificación definitiva.

**3.** Dos salidas podrían imponer niveles contradictorios sobre el mismo conductor: contención eléctrica. El control debe habilitar **una sola fuente** por segmento de bus; los destinos se autorizan por separado.

**4.** `MAR←PC=0x6000`; seleccionar memoria y solicitar RD; esperar un byte válido; `MDR←0x11`; transferir `IR←MDR`; avanzar `PC←0x6001` sin modificar FLAGS. La temporización real de estas dependencias sigue abierta.

**5.** La macro oculta preparar dirección, habilitar memoria, esperar dato, capturarlo y avanzar PC. Esos eventos necesitan tiempos y flancos concretos. No tenemos aún el circuito ni el reloj que permitan demostrar cuántos ciclos requieren.

**6.** `11→LDI_SELECTOR`, `13→ST_SELECTOR`, `01→HALT_ENTER`. `FAULT` corresponde a un opcode inexistente en el contrato; `PENDING_ROUTE` indica una instrucción candidata conocida cuya microsecuencia todavía no se ha descrito.

**7.** No. Los selectores admitidos para R0–R3 son `00` a `03`. El control valida antes de `LDI_COMMIT`; con `07` iría a la ruta de fallo propuesta **sin escribir el registro destino**.

**8.** `IR=0x11`, `SEL=0x00`, `TMP=0x2A`; la escritura propuesta deja `R0=0x2A=42`. Al consumir tres bytes, `PC=0x6003`. Los indicadores `FLAGS` permanecen igual si así lo exige la instrucción candidata.

**9.** La dirección `0x6F00` se representa en ese formato por el byte bajo `00` seguido del alto `6F`. Se conservarían como `ADDR_LO=00` y `ADDR_HI=6F`; después se forma `MAR=0x6F00`, sin depender del contenido cambiante de MDR.

**10.** La lectura del byte alto deja `MDR=0x6F`. Si se activa WR con ese dato, RAM podría recibir `6F` en lugar de `2A`. Hay que preparar `MDR←R0=0x2A`, asegurar dirección estable y conducción exclusiva del bus, y solo después solicitar escritura.

**11.** Tras leer el opcode HALT en `0x6007`, el siguiente PC candidato es `0x6008` y se entra en detención. RESET sigue la ruta de arranque establecida por ROM/firmware; no coloca mágicamente PC en el programa de RAM.

**12.** `LDI`: 3 lecturas. `ST`: 4 lecturas y 1 escritura. `HALT`: 1 lectura. Total **8 lecturas + 1 escritura = 9 transacciones externas**. Una transacción no tiene duración de reloj fijada y los microestados son descripciones; hacen falta esquemas, señales, codificación, temporización y pruebas reales.

## Para continuar

Ya sabemos que una instrucción necesita **dos niveles de interpretación**: los bytes del programa y las pequeñas acciones del control que hacen posible su efecto. También vimos que una lectura requiere preparar y conservar datos, y que un fallo de secuencia puede escribir en el lugar equivocado. En el **capítulo 14, «De números a instrucciones»**, estudiaremos con detalle los opcodes, los formatos de bytes y cómo una persona podría depositar un programa en memoria con un panel detenido. Más adelante, en el capítulo 15, recorreremos la ejecución completa sin suponer ciclos que todavía no existen.

