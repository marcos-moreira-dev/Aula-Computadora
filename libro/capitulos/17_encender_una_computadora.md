# Capítulo 17. Encender una computadora

*Parte V · Microcomputadora y software · Aula-Computadora*

Una computadora recién alimentada no sabe qué palabra escribir en pantalla ni qué instrucciones tenía el usuario ayer. La **RAM es volátil** y el procesador necesita una manera confiable de comenzar. Por eso el encendido no puede consistir en «buscar cualquier byte y ejecutar». Debemos proporcionarle una secuencia de arranque: **RESET**, lectura de una dirección inicial, firmware guardado en memoria no volátil e inicialización de los recursos que ese firmware utilizará.

El capítulo 16 nos dejó una pieza esencial: `CALL` conserva un retorno en la pila, mientras `RET` lo recupera. Ahora veremos cómo se prepara esa pila, de dónde sale el primer PC y cómo un pequeño **monitor hexadecimal** permitiría inspeccionar y modificar RAM. Haremos todo sobre el **contrato candidato Aula-8 R0.11**, no sobre una EEPROM programada o CPU funcionando. Las cifras son expectativas de diseño; todavía faltan imagen de firmware, ensamblador, control eléctrico y pruebas físicas.

## 1. El instante del encendido no es un programa

Al aplicar alimentación, distintas partes de un circuito real pueden estabilizarse en momentos diferentes. No conviene confiar en que PC, SP o RAM contengan cero. Una señal de **reset** debe mantener el control del procesador en un estado definido hasta que las condiciones eléctricas permitan iniciar la secuencia de arranque. Qué niveles, tiempos, oscilador y supervisión de tensión se necesitarán está **pendiente de diseño y medición**.

Una vez liberado reset, Aula-8 necesitaría conocer dónde empieza el firmware. La propuesta reserva dos bytes en la **ROM de firmware**, en las direcciones `0xFFFC` y `0xFFFD`. Forman un **vector de reset** little-endian: primero se lee el byte bajo, luego el alto. Si contuvieran `00 E0`, la dirección de inicio sería `0xE000`.

[[EQ:PC de inicio = (0xE0 × 256) + 0x00 = 0xE000]]

[[EQ:Vector RESET = ROM[FFFD] × 256 + ROM[FFFC]]]

La segunda línea es deliberadamente una pregunta de ubicación: el vector está en ROM, nunca depende de una RAM que podría estar vacía. **No es una instrucción normal** `JMP`: es un convenio que la lógica de reset del procesador tendría que implementar. También necesitamos acceso funcional al bus y al almacenamiento de firmware durante esos pasos.

Mira la secuencia de la figura. Cada bloque representa una obligación de la futura máquina; ninguno representa un número de ciclos ya medido.

[[FIG:c17_fig01_vector_reset|Figura 1. Reset lee dos bytes de ROM y carga la dirección inicial del firmware.|La secuencia funcional parte de RESET, lee ROM FFFC igual 00, lee ROM FFFD igual E0, combina E000 y sitúa PC en E000. Una nota diferencia la ROM de firmware de la ROM interna de control.]]

## 2. Una memoria de firmware tiene que estar grabada antes

La ROM de firmware se propone como una EEPROM de **8 KiB** en `0xE000–0xFFFF`. A diferencia de RAM, conserva los bytes sin alimentación. Pero «ROM» no significa que un programa aparezca por sí solo: **alguien debe preparar y grabar su imagen con herramientas externas antes del primer encendido**. La primera versión necesitará un ensamblador cruzado, verificación de bytes, programador compatible y pruebas de lectura.

[[EQ:Tamaño ROM = 0x10000 − 0xE000 = 0x2000 = 8192 bytes]]

Un firmware real deberá ser codificado para la ISA finalmente aprobada. No basta con llenar la ROM de números escogidos al azar ni con escribir un documento que describa comandos. Por ahora solo tenemos una distribución y unas interfaces **propuestas**. Ninguna rutina del monitor ha sido enlazada ni programada en una EEPROM.

La ROM que almacena ese firmware **no es la ROM de microcontrol**. La primera guarda instrucciones visibles al programa; la segunda, si finalmente se adopta, guardará señales o microórdenes internas de la unidad de control. Una CPU necesita saber ejecutar su ISA antes de poder seguir instrucciones desde firmware.

## 3. El mapa de memoria evita que dos dispositivos respondan juntos

El diseño base de Aula-8 cuenta con **16 bits de dirección**: hay `65536` posiciones direccionables por byte, pero eso **no garantiza 65536 bytes de RAM instalados**. La RAM inicial presupuestada es de 32 KiB; la ROM de firmware, 8 KiB; el resto incluye huecos, expansión y registros de entrada/salida según el mapa candidato.

[[EQ:Espacio direccionable = 2^16 = 65536 bytes = 64 KiB]]

[[EQ:RAM inicial = 32 × 1024 = 32768 bytes]]

| Región propuesta | Papel | Precaución |
| --- | --- | --- |
| `0000–7FFF` | RAM inicial de 32 KiB | Contenido desconocido al encender. |
| `6000–6FFF` | Ventana de práctica dentro de RAM | Es **subconjunto**, no RAM adicional. |
| `8000–BFFF` | Espacio sin RAM inicial asignada | No tratar como memoria instalada. |
| `C000` y `C002` | Datos y estado del terminal | Registros mapeados, no bytes ordinarios. |
| `C010–C01F` | Controlador de bloques candidato | No hay controlador implementado. |
| `E000–FFFF` | ROM de firmware de 8 KiB | No escribible mediante `POKE`. |

[[FIG:c17_fig02_mapa_memoria|Figura 2. Espacio de 64 KiB con RAM inicial, registros de periféricos y ROM de firmware, sin rellenar artificialmente los huecos.|Mapa vertical esquemático desde 0000 hasta FFFF; separa RAM 0000–7FFF, zona no asignada 8000–BFFF, E/S y zonas por definir C000–DFFF y ROM E000–FFFF. Una nota ubica la ventana de práctica 6000–6FFF dentro de RAM y el vector FFFC/FFFD dentro de ROM.]]

El decodificador físico todavía tendrá que asegurar que **solo el dispositivo seleccionado** entregue datos al bus durante una lectura. Los huecos no se convierten en ceros por decreto; una lectura en una dirección no asignada no tiene un valor garantizado. La selección y temporización deben verificarse con hojas de datos y circuitos reales.

## 4. Lo primero que haría el firmware

Una vez que PC apunte a `0xE000`, el código de firmware —cuando se escriba— deberá establecer condiciones mínimas antes de aceptar comandos. El orden exacto es una decisión de ingeniería, pero hay dependencias necesarias: inicializar la pila **antes** de usar CALL, inicializar los búferes **antes** de confiar en ellos y configurar el terminal **antes** de mostrar el prompt.

| Paso funcional candidato | Razón |
| --- | --- |
| Definir `SP=0x8000` | CALL decrementará a RAM válida antes de guardar retorno. |
| Inicializar variables y búfer de línea | La RAM podría contener cualquier patrón previo. |
| Configurar terminal y esperar TX listo | No se puede suponer que los bytes llegan instantáneamente. |
| Presentar un saludo y un indicador | El usuario distingue firmware activo de silencio eléctrico. |
| Repetir `leer → validar → responder` | Comienzo de un monitor interactivo. |

[[EQ:Primera reserva de retorno = SP − 2 = 0x7FFE]]

El modelo de memoria y el tamaño de esos búferes siguen siendo presupuestos. Tampoco hemos implementado registros de interfaz, controlador de texto, UART ni sincronización. Las entradas o salidas mencionadas son **servicios que habría que programar**, no periféricos construidos.

## 5. Una tabla estable permite llamar servicios de ROM

Si un programa necesita imprimir una letra, no debería depender de la posición interna de la rutina de impresión. El borrador reserva **32 ranuras de cuatro bytes** entre `0xFF00` y `0xFF7F`. Por ahora solo **cuatro** reciben nombre: `FW_PUTC`, `FW_GETC`, `FW_PUTS` y `FW_STATUS`. Las otras 28 quedan sin asignar, **no son funciones disponibles**.

[[EQ:Ranuras reservadas = 32 × 4 = 128 bytes]]

[[EQ:Ranuras sin asignar = 32 − 4 = 28]]

Una ranura candidata empieza con un `JMP` absoluto. La de `FW_PUTC` en `0xFF00` podría contener `30 00 E1 00`: el byte `30` es opcode `JMP`, `00 E1` compone `0xE100`, y el último `00` es relleno NOP. **`E100` es un destino ficticio de enseñanza**: no contiene una función real de impresión.

| Entrada pública | Servicio | Entrada o salida propuesta |
| --- | --- | --- |
| `FF00` | `FW_PUTC` | Recibe carácter en R0. |
| `FF04` | `FW_GETC` | Devuelve carácter en R0. |
| `FF08` | `FW_PUTS` | Lee cadena terminada en `00` apuntada por X. |
| `FF0C` | `FW_STATUS` | Devuelve máscara de estado candidata en R0. |

[[EQ:Destino de la ranura PUTC = (0xE1 × 256) + 0x00 = 0xE100]]

La figura muestra por qué un programa haría `CALL FF00`, no `JMP E100`. CALL guarda la continuación; la ranura salta a una implementación que, si existiera, terminaría en RET y devolvería el control. Así se podrían mover las rutinas internas sin cambiar la dirección pública.

[[FIG:c17_fig03_ranuras_rom|Figura 3. Una ranura de ROM fija enlaza mediante JMP con una rutina que terminaría en RET.|Diagrama funcional: programa CALL FF00 → ranura 30 00 E1 00 → destino ilustrativo E100 → RET vuelve a la dirección posterior al CALL; la ranura se etiqueta como contrato no ejecutado.]]

## 6. Del reset al prompt del monitor

El **monitor hexadecimal** sería un programa pequeño residente en ROM que permite introducir comandos para inspeccionar memoria y modificar zonas de práctica. El flujo básico es recibir una línea de texto, dividirla en palabras, validar sintaxis y límites, realizar la operación y presentar una respuesta. Si la línea es inválida, debe comunicar el error **sin escribir RAM**.

El contrato R0.11 utiliza números hexadecimales **sin prefijo**: direcciones de cuatro cifras, bytes de dos y longitudes desde `1` hasta `100` hexadecimal. El valor `10` de longitud significa **dieciséis bytes**, no diez. Un ejemplo de futura orden sería `MEM 6000 10`.

[[EQ:Longitud hexadecimal 0x10 = 16 bytes decimales]]

| Orden candidata | Ejemplo | Comportamiento o límite |
| --- | --- | --- |
| `HELP` | `HELP` | Mostrar ayuda y funciones pendientes. |
| `MEM` | `MEM 6000 10` | Leer 16 bytes solo si todo el rango es legible. |
| `POKE` | `POKE 6000 2A` | Escribir un byte solo en `6000–6FFF`. |
| `RUN` | `RUN 6000` | Llamar al programa desde el monitor. |
| `REG` | `REG` | **No disponible**: falta captura de estado real. |
| `LOAD` | `LOAD` | **No disponible**: faltan firmware/controlador. |

No confundas `MEM` con `POKE`. La primera operación es lectura; la segunda modifica RAM y por eso se limita intencionalmente a una ventana de práctica. El monitor **no** tendría permiso para programar la EEPROM con `POKE` ni para leer ciegamente registros de periféricos como si fueran RAM.

## 7. Validar antes de tocar la memoria

Una orden incompleta como `POKE 6000`, un byte imposible como `1FF`, una dirección con caracteres inválidos o una escritura `POKE FF00 2A` deberían rechazarse. Para `MEM`, si una lectura solicitada atraviesa el final de RAM hacia una zona no asignada, conviene rechazar **toda la petición**, no entregar un resultado parcialmente fiable.

[[EQ:Direcciones permitidas por POKE = 0x6000 … 0x6FFF]]

[[EQ:Tamaño de ventana POKE = 0x6FFF − 0x6000 + 1 = 4096 bytes]]

Este filtro es una **política candidata del programa monitor**, no protección de memoria impuesta por hardware. Un programa ejecutando opcodes con acceso directo podría escribir en otras regiones de RAM si la CPU y el bus lo permitieran. La ROM se protege mediante sus características físicas y señales de control, no porque el monitor diga «no».

## 8. RUN debe regresar por RET

Considera el siguiente programa candidato de siete bytes, ubicado en RAM mediante `POKE` cuando ya exista un monitor funcional:

| Dirección | Bytes | Significado |
| --- | --- | --- |
| `6000` | `11 00 41` | `LDI R0,0x41` (carácter A). |
| `6003` | `35 00 FF` | `CALL 0xFF00` (ranura PUTC). |
| `6006` | `02` | `RET` para volver al monitor. |

El comando `RUN 6000` **no sería simplemente un salto irreversible**. La implementación candidata usa CALL desde el monitor para guardar el retorno a su propia continuación. El programa a su vez llama a la ranura PUTC, que saltaría a una rutina de firmware. Esa rutina terminaría en RET y regresaría al **programa** en `0x6006`; el RET del programa regresaría al **monitor**. Son **dos niveles de retorno diferentes**.

[[FIG:c17_fig04_run_dos_ret|Figura 4. RUN crea un retorno al monitor y CALL PUTC crea otro retorno dentro del programa.|Recorrido lógico: monitor CALL 6000 → programa LDI y CALL FF00 → firmware JMP a rutina ficticia → primer RET a 6006 → segundo RET al monitor. Ruta lateral HALT muestra que no vuelve al prompt.]]

Si en `0x6006` se colocara `HALT`, la CPU se detendría: **no aparecería un prompt nuevo por arte de magia**. Para retomar el monitor haría falta RESET o una futura capacidad explícita de depuración. La diferencia entre `HALT` y `RET` es observable en el flujo esperado aunque todavía no haya ejecución física.

## 9. Qué sigue sin funcionar todavía

No hemos fabricado la CPU ni escrito el monitor. Las cuatro direcciones de servicio, el vector `00 E0` y el mapa son **contratos provisionales**; las direcciones internas `E100/E140/E180/E1C0` son marcadores ficticios. No hay funciones detrás de esos bytes. Tampoco conocemos los tamaños finales del firmware: disponer de 8192 bytes teóricos no demuestra que el monitor, las rutinas, los búferes y las tablas quepan después de ensamblar.

La próxima etapa de ingeniería exige cerrar la ISA y ABI, definir el circuito de reset y selección de memoria, elaborar una imagen realmente enlazable, programar la EEPROM, construir un terminal probado y ejecutar pruebas sobre la CPU. La verificación documental no mide tiempos de memoria, alimentación, recuperación ante apagones o compatibilidad de los chips.

[[PAGEBREAK]]

## Construimos Aula-8: del vector de RESET a la primera instrucción

Un procesador recién encendido no puede suponer que el primer byte de RAM contiene un programa ni que todas las posiciones empiezan en cero. En el contrato candidato, el circuito de inicio debe tomar de la ROM las dos celdas del vector `0xFFFC` y `0xFFFD`, interpretarlas en little-endian y formar la dirección inicial `0xE000`. A partir de ahí el PC ya puede **buscar un opcode**, y solo el firmware decidirá qué memoria inicializa y cómo ofrece un monitor de comandos.

Este recorrido aprovecha exactamente la misma representación de **celdas contiguas** utilizada para JMP y CALL: leer dos bytes de una dirección no significa que esos bytes sean instrucciones. Son datos que determinan **dónde** comienza la ejecución. Hasta que exista una ROM realmente grabada y una CPU capaz de leerla, `E000` es un destino documental del firmware, no una prueba de encendido físico.

## Ejercicios del capítulo 17

**Ejercicio 1 — Arranque.** ¿Por qué no puede depender el PC inicial de una RAM sin inicializar?

**Ejercicio 2 — Vector.** ¿Qué dirección forman los bytes `00 E0` leídos de `FFFC–FFFD`?

**Ejercicio 3 — Capacidad.** ¿Cuántos bytes ocupa el rango ROM `E000–FFFF`?

**Ejercicio 4 — Pila.** ¿Por qué el firmware debe fijar SP antes de ejecutar CALL?

**Ejercicio 5 — ROM y control.** ¿En qué se diferencia firmware ROM de micro-ROM?

**Ejercicio 6 — Mapa.** ¿La ventana `6000–6FFF` aporta 4 KiB adicionales a los 32 KiB de RAM?

**Ejercicio 7 — Ranura.** Interpreta `30 00 E1 00` en `FF00`.

**Ejercicio 8 — Servicio.** ¿Por qué un programa llama a `FF00` en vez de depender de `E100`?

**Ejercicio 9 — Hexadecimal.** ¿Cuántos bytes leería `MEM 6000 10`?

**Ejercicio 10 — Seguridad.** ¿Debe aceptarse `POKE FF00 2A`? ¿Y `POKE 6000 2A`?

**Ejercicio 11 — Retornos.** ¿Por qué hay dos RET en la ruta RUN → PUTC → monitor?

**Ejercicio 12 — Diagnóstico.** Menciona tres condiciones que faltan antes de afirmar que el encendido funciona físicamente.

## Solucionario del capítulo 17

**1.** La RAM es volátil y sus bytes iniciales no están garantizados. Reset debe obtener un PC definido de un mecanismo y memoria no volátil preparados para ello.

**2.** `0xE000`, porque `00` es bajo y `E0` alto en little-endian.

**3.** `0x10000−0xE000=0x2000`, es decir, 8192 bytes u 8 KiB.

**4.** CALL necesita dos posiciones válidas de RAM donde guardar el retorno. Con `SP=0x8000` primero descendería a `0x7FFE`.

**5.** Firmware ROM contiene instrucciones visibles para la ISA y ejecutadas por la CPU; micro-ROM, si se adopta, describe acciones internas de control que hacen posible ejecutarlas.

**6.** No. La ventana 6000–6FFF está dentro de 0000–7FFF; es una restricción de uso del monitor, no RAM adicional.

**7.** `30` significa JMP absoluto; `00 E1` compone `E100`; el último `00` es relleno NOP. E100 es una dirección ficticia y no una rutina existente.

**8.** La ranura FF00 es una interfaz pública que podría mantenerse estable aunque cambie la dirección interna; CALL conserva el retorno.

**9.** Dieciséis bytes, porque `10` es hexadecimal `0x10`.

**10.** `POKE FF00 2A` debe rechazarse: FF00 pertenece a ROM. `POKE 6000 2A` está dentro de la ventana candidata, siempre que la sintaxis sea válida.

**11.** El RET del servicio devuelve el control al programa en 6006. El RET del programa libera el retorno que había creado RUN y vuelve al monitor.

**12.** Por ejemplo, reloj y reset estables medidos; CPU capaz de leer ROM y ejecutar la ISA; EEPROM realmente grabada con firmware enlazado. También faltan terminal, pila y pruebas de bus.

## Para continuar

Tenemos el arranque explicado como una cadena de obligaciones técnicas: **ROM previamente grabada → vector de reset → firmware → pila y terminal → monitor**. En el capítulo 18, «Hablar con la máquina», nos concentraremos en la parte visible: cómo una letra viaja entre el procesador, sus registros de entrada/salida y una terminal, antes de imaginar editores o sistemas más complejos.
