# Capítulo 16. Subrutinas y pila

*Parte IV · Construir Aula-8 · Aula-Computadora*

Hasta ahora, el contador de programa (PC) ha avanzado casi siempre hacia el byte siguiente. Pero imaginemos una función que imprime un carácter: si tres partes de nuestro programa la necesitan, copiar sus instrucciones tres veces consumiría memoria y multiplicaría las correcciones. Preferimos escribirla una vez y **llamarla desde varios lugares**. El reto no está en saltar hacia la función, sino en **recordar adónde regresar**.

Este capítulo sigue la codificación **candidata** de Aula-8: veremos saltos, llamadas, retornos, una pila descendente y un bucle. Los valores y efectos se verifican como un modelo de escritorio; **no hay CPU, reloj, micro-ROM, firmware ni señales físicas probados**. La pila no es una palabra mágica: son posiciones de RAM y un registro que señala dónde se encuentran sus datos.

## 1. El salto que se olvida de regresar

Una instrucción `JMP 0x6010` sustituye el valor de PC por `0x6010`. Cuando la CPU busque el siguiente opcode, irá allí. Un salto incondicional **no guarda** por sí mismo el valor anterior de PC. Si lo usamos para entrar a una función, necesitamos otra forma de recordar el punto de regreso.

En la ISA candidata, `JMP` usa el opcode `30` y dos bytes de dirección, **primero el bajo y después el alto**. Desde `0x6000`, `30 10 60` ocupa tres bytes; tras leerlos, PC sería `0x6003`, pero `JMP` lo reemplazaría por `0x6010`.

[[EQ:Destino de JMP = (0x60 × 256) + 0x10 = 0x6010]]

[[EQ:PC secuencial tras JMP = 0x6000 + 3 = 0x6003]]

La pregunta cambia: si queremos ejecutar una rutina en `0x6010` y luego reanudar en `0x6003`, ¿dónde guardar esos dos bytes del retorno? Un registro de retorno único podría servir para una sola llamada, pero se perdería cuando una rutina llamara a otra. Por eso necesitamos **una pila**.

## 2. La pila ocupa RAM, no una memoria misteriosa

El **puntero de pila (SP)** es un registro de 16 bits. En el contrato candidato, la pila crece hacia direcciones menores: al reservar espacio, SP disminuye; al liberarlo, aumenta. El ejemplo supone que el firmware ya fijó `SP=0x8000`, una dirección inmediatamente posterior al último byte de la RAM física inicial `0x0000–0x7FFF`. **Nunca escribimos en `0x8000`**: primero reservamos posiciones válidas.

Para guardar un retorno de 16 bits, CALL calcula `SP ← SP−2`. Quedan libres las posiciones `0x7FFE` y `0x7FFF`; la primera recibirá el byte bajo y la segunda el alto.

[[EQ:SP nuevo = 0x8000 − 2 = 0x7FFE]]

[[EQ:Retorno 0x6003 = (0x60 × 256) + 0x03]]

Observa la figura antes de leer la tabla: los números escritos dentro de las celdas son **bytes almacenados**, no direcciones de instrucciones. SP apunta a la dirección de la primera celda ocupada.

[[FIG:c16_fig01_pila_retorno|Figura 1. CALL reserva dos bytes al descender SP y conserva allí el retorno 0x6003 en orden little-endian.|Tres columnas muestran SP antes en 8000 sin escritura allí; SP después en 7FFE, con RAM[7FFE]=03 y RAM[7FFF]=60; y RET que vuelve a SP=8000 sin borrar las dos celdas.]]

| Instante lógico | SP | `RAM[7FFE]` | `RAM[7FFF]` |
| --- | --- | --- | --- |
| Antes de CALL | `8000` | Desconocido | Desconocido |
| Tras CALL | `7FFE` | `03` | `60` |
| Tras RET | `8000` | `03` residual | `60` residual |

**Liberar una posición no equivale a borrarla.** RET avanza SP, pero los bytes anteriores permanecen en RAM hasta ser sobrescritos. Leerlos como si todavía fueran un retorno válido sería un error.

## 3. CALL conserva el camino de vuelta

El ejemplo completo usa estos bytes, todos en la ventana candidata de programas `0x6000–0x6FFF`. No inventamos datos para las posiciones intermedias porque la ejecución salta sobre ellas.

| Dirección | Bytes | Significado previsto |
| --- | --- | --- |
| `6000` | `35 10 60` | `CALL 0x6010` |
| `6003` | `01` | `HALT` del llamador |
| `6010` | `11 00 2A` | `LDI R0,42` en la subrutina |
| `6013` | `02` | `RET` |

En el primer fetch, `IR=35`; al leer los dos operandos `10 60`, PC llega a `0x6003`. **Ese PC posterior a CALL es la dirección de retorno**, no `0x6000` ni `0x6001`. Debe copiarse a temporales `RET_LO/RET_HI` antes de que la unidad de control cargue `0x6010` en PC.

[[EQ:Dirección de retorno = 0x6000 + 3 = 0x6003]]

La propuesta de microcontrol sigue este orden: leer destino, guardar PC como retorno, reservar dos bytes de pila, escribir el bajo en `[SP]`, escribir el alto en `[SP+1]` y finalmente cargar PC con el destino. Como **MAR y MDR se reutilizan**, cada escritura requiere preparar primero dirección y dato. Los temporales del retorno son una necesidad funcional; todavía no son chips seleccionados.

[[FIG:c16_fig02_llamar_regresar|Figura 2. CALL llega a la subrutina y RET recupera exactamente la continuación del llamador.|Flujo funcional de 6000 CALL 6010 hacia 6010 LDI, 6013 RET y regreso a 6003 HALT, con nota lateral de retorno 6003 conservado en 7FFE y 7FFF.]]

## 4. RET no busca una dirección nueva en el programa

En `0x6013`, el fetch obtiene `02`, opcode candidato de `RET`, y PC avanza temporalmente a `0x6014`. Pero RET no conserva ese PC: primero lee **dos bytes de pila**. Con `SP=0x7FFE`, toma `03` de `0x7FFE` y `60` de `0x7FFF`, los compone como `0x6003`, incrementa SP dos posiciones y reemplaza PC por el retorno.

[[EQ:PC restaurado = (RAM[SP+1] × 256) + RAM[SP] = 0x6003]]

[[EQ:SP al regresar = 0x7FFE + 2 = 0x8000]]

La próxima búsqueda lee `01` en `0x6003` y entra en HALT; el PC lógico se habrá incrementado a `0x6004`. R0 contiene `0x2A` porque LDI lo cargó, mientras `FLAGS` conserva sus valores iniciales según el contrato de estas instrucciones. Nadie puede deducir que las banderas sean cero.

| Evento externo previsto | Dirección | Byte |
| --- | --- | --- |
| Leer CALL, destino bajo y alto | `6000`, `6001`, `6002` | `35`, `10`, `60` |
| Guardar retorno bajo y alto | `7FFE`, `7FFF` | `03`, `60` |
| Leer LDI, selector e inmediato | `6010`, `6011`, `6012` | `11`, `00`, `2A` |
| Leer RET y dos bytes de pila | `6013`, `7FFE`, `7FFF` | `02`, `03`, `60` |
| Leer HALT | `6003` | `01` |

[[EQ:Transacciones previstas = 10 lecturas + 2 escrituras = 12]]

**Doce transacciones de memoria no son doce ciclos de reloj.** La microsecuencia usa acciones internas adicionales y no existe una temporización física medida. Escribir `RET` sin que hubiera habido un CALL válido tampoco hace aparecer automáticamente una dirección sensata: se leerían los bytes que hubiera en la pila.

## 5. Las llamadas anidadas justifican una pila

Considera una segunda situación: la función en `0x6010` llama a otra situada en `0x6020`. La primera llamada (`6000 → 6010`) ya guardó `0x6003` en `7FFE–7FFF`. La segunda, desde `6010`, tiene tres bytes y debe regresar a `0x6013`. Reservará otras dos posiciones, dejando `SP=0x7FFC`. Allí escribirá `13 60`.

[[EQ:SP con dos retornos = 0x8000 − 2 − 2 = 0x7FFC]]

[[FIG:c16_fig03_llamadas_anidadas|Figura 3. Dos CALL anidados apilan dos direcciones de retorno diferentes y RET recupera la última primero.|Mapa de cuatro celdas: 7FFC=13, 7FFD=60 para regresar al primer nivel; 7FFE=03, 7FFF=60 para regresar al llamador. Una secuencia muestra SP 8000→7FFE→7FFC→7FFE→8000.]]

El RET de la segunda función recuperará `0x6013`; otro RET recuperará `0x6003`. Esta política se llama **último en entrar, primero en salir (LIFO)**. Si todos los CALL guardaran el retorno en un único registro, la segunda llamada reemplazaría al primero y no podríamos regresar correctamente a ambos sitios.

La pila real también puede guardar parámetros, registros y variables locales. Pero **ninguna de esas capacidades es automática**: el programador o compilador debe decidir qué coloca y retira en cada posición, sin solapar datos y sin alterar incorrectamente el retorno.

## 6. Saltar condicionalmente permite repetir tareas

Una subrutina resuelve reutilización; un **bucle** resuelve repetición. La ISA candidata incluye `JZ`, `JNZ`, `JC` y `JNC`. Son saltos absolutos con opcode y dos bytes de destino. Incluso si no se toma el salto, **se consumen sus dos operandos** para que PC quede al comienzo de la siguiente instrucción.

| Salto | Pregunta que decide |
| --- | --- |
| `JZ` | ¿Z vale 1? |
| `JNZ` | ¿Z vale 0? |
| `JC` | ¿C vale 1? |
| `JNC` | ¿C vale 0? |

La bandera **Z** indica resultado cero según la operación que la actualiza. La bandera **C** significa acarreo en suma y préstamo en resta dentro de esta propuesta; por eso un `JC` no significa simplemente «mayor» en todas las circunstancias.

Un ejemplo didáctico con un contador carga inicialmente tres en R0 y lo decrementa. Tras cada `DEC`, `JNZ 0x6003` vuelve al decremento si Z=0. En la tercera disminución el resultado es cero, Z=1 y el salto **no** se toma.

[[EQ:R0 sucesivo = 3 → 2 → 1 → 0]]

[[EQ:JNZ se toma cuando Z = 0; no se toma cuando Z = 1]]

[[FIG:c16_fig04_bucle_jnz|Figura 4. JNZ vuelve al decremento dos veces y continúa hacia HALT cuando el contador llega a cero.|Tres iteraciones de DEC R0 con resultados 2, 1 y 0; Z=0 conduce a JNZ tomado las dos primeras veces, Z=1 a JNZ no tomado y HALT al final. Se recuerda que los bytes destino del salto siempre se leen.]]

Aquí hay una frontera: **el contrato de DEC y sus flags es una propuesta**, y su microsecuencia física sigue sin implementarse. La tabla permite verificar el razonamiento semántico, no afirmar que una placa ya ejecuta tres vueltas.

## 7. Parámetros y registros: el contrato de una función

Una subrutina útil suele recibir datos y devolver algún resultado. Podemos pasar un byte en un registro; para funciones más complejas hay que elegir una **convención de llamadas (ABI)**: quién coloca parámetros en pila, qué registros deben conservarse y quién limpia la pila al regresar.

El borrador de **MiniC-Aula** propone argumentos en ranuras de dos bytes y limpieza de argumentos por el llamador; por separado, el **firmware de ROM** propone otra ABI pública que conserva R2, R3 y X. **No son la misma convención**, y ninguna se puede considerar probada en un compilador o CPU actuales. Lo importante para este capítulo es entender por qué CALL/RET por sí solos no determinan cómo pasan los parámetros.

[[EQ:SP equilibrado después de función = SP previo a preparar la llamada]]

Si una función guarda un registro, debe restaurarlo en el orden inverso. Si reserva variables locales, debe liberarlas antes de RET. Un error de un solo byte en SP puede hacer que RET mezcle el byte bajo de un retorno con el alto de otro: el programa no vuelve a donde el autor esperaba.

## 8. Qué pasa si el programa termina con HALT

Una función llamada desde el monitor debe **volver por RET** si la intención es regresar a la consola. `HALT` detiene la CPU; no desapila un retorno ni invoca un monitor por arte de magia. Este principio será indispensable al encender la computadora y escribir un monitor de ROM.

La protección real de la pila sigue pendiente: no hemos construido una unidad que detecte automáticamente desbordamiento, subdesbordamiento o una dirección de retorno falsa. Los modelos pueden **rechazar casos** como política educativa, pero eso no demuestra que un circuito ya posea esas protecciones.

## 9. Cómo diagnosticar una llamada que no vuelve

Ante una traza inesperada, pregunta en este orden: ¿CALL leyó exactamente dos bytes de destino? ¿Guardó como retorno el PC **posterior** a esos operandos? ¿Restó dos a SP antes de escribir? ¿Puso bajo en `[SP]` y alto en `[SP+1]`? ¿Preparó MAR/MDR antes de cada escritura? ¿RET leyó esos mismos dos bytes y sumó dos a SP?

Un segundo nivel de diagnóstico revisa si una subrutina modificó la pila por accidente, si una llamada anidada pisó un retorno anterior, si el programa ejecutó HALT en vez de RET y si la región de RAM prevista realmente está disponible. Son condiciones que habrá que comprobar cuando existan circuitos y firmware funcionales.

## Construimos Aula-8: dos ventanas de programa y la pila real

La llamada del ejemplo ocupa `0x6000–0x6002`; su continuación en `0x6003` contiene HALT. La rutina comienza en `0x6010`, tras un tramo que la figura **omite de forma explícita**. Son direcciones de una misma RAM, no dos memorias distintas. CALL utiliza un salto como JMP, pero primero reserva `0x7FFE` y `0x7FFF` en la pila para conservar los bytes `03 60` de la dirección de regreso.

[[FIG:c16_fig05_ram_y_pila_call_ret|Figura 5. CALL y RET conectan dos tramos de RAM de programa con las dos celdas contiguas donde se guarda el retorno.|El llamador 6000–6003 contiene CALL y HALT; la rutina 6010–6013 contiene LDI y RET; la pila 7FFE–7FFF almacena 03 60 para volver a 6003.]]

RET no busca una etiqueta textual llamada «volver»: lee esas dos celdas, reconstruye `0x6003` y cambia PC. También restaura SP a `0x8000` sin borrar el contenido residual. Al dibujar el proceso con flechas del PC y con celdas de la pila, se hace evidente que **la secuencia de instrucciones y los datos de retorno comparten el mismo sistema de direcciones**, pero cumplen funciones distintas.

El bucle de decremento ofrece un segundo recorrido: la CPU vuelve de `0x6005–0x6007` a `0x6003` mientras Z=0, aunque los bytes de RAM no cambien de sitio. Al alcanzar R0=0, el PC continúa hacia HALT.

[[FIG:c16_fig06_ram_bucle_jnz|Figura 6. El bucle de tres decrementos vuelve a 0x6003 mientras JNZ se toma y avanza a HALT cuando Z vale 1.|Mapa RAM 6000–6008 con LDI, DEC, JNZ y HALT, y flecha de regreso desde el operando de JNZ hacia DEC.]]

No asignamos a estas flechas duración eléctrica ni ciclos de micro-ROM: muestran el **orden lógico** que un futuro procesador deberá respetar.

## Ejercicios del capítulo 16

Trabaja con el mapa de programa `6000:35 10 60`, `6003:01`, `6010:11 00 2A` y `6013:02`, usando `SP=8000` antes de CALL.

**Ejercicio 1 — Salto.** ¿Qué pierdes al usar JMP en lugar de CALL para entrar en una función?

**Ejercicio 2 — Longitud.** ¿Cuántos bytes consume CALL y qué PC debe recordar?

**Ejercicio 3 — Pila.** ¿En qué dirección se guarda cada byte de `0x6003`?

**Ejercicio 4 — Orden.** ¿Qué ocurriría si se guardaran `60 03` en lugar de `03 60`?

**Ejercicio 5 — Retorno.** ¿Qué valores tienen SP y PC después de RET?

**Ejercicio 6 — Residuos.** ¿RET convierte automáticamente en cero las celdas liberadas?

**Ejercicio 7 — Bus.** ¿Qué debe cambiar entre leer los operandos y escribir la pila?

**Ejercicio 8 — Contabilidad.** Cuenta los accesos externos de CALL, LDI, RET y HALT.

**Ejercicio 9 — Anidamiento.** ¿Qué retorno queda en `7FFC–7FFD` si `6010` llama a `6020`?

**Ejercicio 10 — Bucle.** Para R0 igual a 3, anota los tres resultados de DEC y si JNZ salta.

**Ejercicio 11 — ABI.** ¿Por qué CALL/RET no bastan para decidir cómo pasar parámetros?

**Ejercicio 12 — Fallo.** Da dos causas distintas de que el programa no regrese al llamador.

## Solucionario del capítulo 16

**1.** JMP reemplaza PC sin conservar una continuación. CALL debe guardar la dirección a la que RET regresará.

**2.** Tres bytes (`35 10 60`). Debe recordar `0x6003`, la dirección posterior al opcode y los dos operandos.

**3.** SP pasa a `0x7FFE`; en `RAM[7FFE]` se guarda `03` (bajo) y en `RAM[7FFF]` `60` (alto).

**4.** Con el contrato little-endian, RET compondría `0x0360` en vez de `0x6003`; el flujo sería incorrecto.

**5.** Tras leer y liberar el retorno, `SP=0x8000` y `PC=0x6003`.

**6.** No. Los bytes `03 60` permanecen físicamente en RAM como residuos, aunque la pila los considere fuera de uso.

**7.** MAR debe pasar de direcciones de código a `0x7FFE` y `0x7FFF`; MDR debe contener `03` o `60`, y el dueño del bus debe cambiar de lectura a escritura sin contención.

**8.** CALL: 3 lecturas + 2 escrituras; LDI: 3 lecturas; RET: 3 lecturas; HALT: 1 lectura. Total: 10 lecturas y 2 escrituras, sin inferir ciclos de reloj.

**9.** El retorno de la llamada en `6010` es `0x6013`; en `7FFC` queda `13` y en `7FFD` `60`. El retorno anterior `03 60` permanece en `7FFE–7FFF`.

**10.** Resultados 2, 1 y 0. Con Z=0 se toma JNZ dos veces; con Z=1 no se toma y continúa al final.

**11.** CALL/RET conservan una dirección de retorno. La ubicación y anchura de parámetros, registros preservados y limpieza corresponden a una ABI acordada.

**12.** Por ejemplo, ejecutar HALT en vez de RET o alterar SP y sobrescribir los bytes del retorno. También fallaría un RET sin CALL válido.

## Para continuar

Ya sabemos cómo una función puede entrar, trabajar y volver sin perder a su llamador. Nos falta responder una pregunta anterior a todas ellas: **¿quién coloca el primer programa en PC cuando encendemos una máquina real?** En el capítulo 17, «Encender una computadora», seguiremos RESET, una ROM grabada de antemano, la inicialización de la pila y el monitor que permitiría trabajar sin volver a cargar todo a mano.
