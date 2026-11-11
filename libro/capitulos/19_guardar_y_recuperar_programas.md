# Capítulo 19. Guardar y recuperar programas

*Parte V · Microcomputadora y software · Aula-Computadora*

El capítulo 18 permitió seguir un carácter desde el terminal hasta una variable en RAM y de vuelta a la pantalla. Funciona como idea, pero plantea un inconveniente cotidiano: **al apagar una RAM volátil, el programa y los datos pueden desaparecer**. Una microcomputadora útil necesita recuperar mañana los bytes que guardamos hoy. No basta con imprimir «guardado» en pantalla: debe existir un soporte persistente y un camino preciso para leerlo.

Vamos a construir ese camino como contrato técnico: **bloque de 256 bytes → controlador de E/S → búfer de RAM → programa cargado**. Después compararemos una carga cruda con un contenedor que declara sus propios límites. Los ejemplos proceden de los borradores R0.12–R0.14; **el modelo Python funciona en la computadora anfitriona, pero no hay un dispositivo de almacenamiento, CPU Aula-8, firmware nativo ni cargador en ROM construidos**.

## 1. Un bloque numérico no es todavía un archivo

Imagina una tarjeta de memoria representada por una imagen binaria, donde cada segmento guarda exactamente **256 bytes**. El bloque `0000` abarca los offsets `0000–00FF`, el `0001` ocupa `0100–01FF`, y el `0002` empieza en `0200`. El número de bloque indica **posición física lógica**, no nombre de documento. No hay aún carpetas, nombres de archivo, extensión ni índice de archivos.

[[EQ:Offset inicial del bloque n = n × 256 bytes]]

[[EQ:Offset inicial del bloque 0x0002 = 2 × 256 = 512 = 0x0200]]

Un programa de **4096 bytes** de contenido crudo necesita dieciséis bloques. Si mide 4097 bytes ya no cabe en dieciséis: el último byte exige un decimoséptimo bloque. Hay que redondear hacia arriba, no al entero más cercano.

[[EQ:Bloques necesarios = techo(bytes útiles / 256)]]

Antes de mirar la figura, localiza dónde termina el bloque 0001 y empieza el 0002: no hay «hueco de separación» de bytes. La imagen, su tamaño y el esquema de nombres de archivos son decisiones distintas.

[[FIG:c19_fig01_bloques_y_offsets|Figura 1. Una imagen persistente se divide en bloques de 256 bytes y cada número determina un offset exacto.|Bloques 0000, 0001, 0002 y 0003 ocupan offsets 0000, 0100, 0200 y 0300; el bloque 0002 abarca 0200–02FF y su longitud es 0100 hexadecimal.]]

[[EQ:Tamaño de cuatro bloques = 4 × 256 = 1024 bytes]]

## 2. El controlador proporciona registros, no magia

El contrato Aula-8 reserva `0xC010–0xC01F` para un periférico de bloques. Todos sus registros públicos son de **8 bits** y están en **direcciones pares**; las impares quedan reservadas. El procesador usa el mismo bus de datos externo de ocho bits que emplea para memoria, pero una escritura en COMMAND no es «guardar un byte de RAM»; ordena al periférico iniciar una operación.

| Dirección | Registro | Uso candidato |
| --- | --- | --- |
| `C010` | `COMMAND` | Escribir `01` READ, `02` WRITE, `03` RESET |
| `C012` | `STATUS` | Leer BUSY, DRQ, DONE o ERROR |
| `C014` | `BLOCK_LO` | Byte bajo del número de bloque |
| `C016` | `BLOCK_HI` | Byte alto del número de bloque |
| `C018` | `DATA` | Puerto secuencial de bytes de lectura/escritura |
| `C01A` | `ERROR` | Código de error |
| `C01C` | `COUNT_LO` | Cuenta de bytes transferidos, byte bajo |
| `C01E` | `COUNT_HI` | Cuenta de bytes transferidos, byte alto |

[[EQ:Número de bloque = BLOCK_LO + (BLOCK_HI × 256)]]

Por ejemplo, elegir el bloque `0102` exige escribir `02` en `C014` y `01` en `C016`: la dirección de cada registro es una dirección **MMIO**, mientras que el número `0102` es un índice **dentro del almacenamiento**. Si los confundimos, una operación acabaría leyendo un registro que no contiene nuestros datos.

[[FIG:c19_fig02_registros_controlador|Figura 2. Ocho registros MMIO controlan bloques persistentes, y el DATA de C018 transfiere un byte por acceso.|Mapa C010 COMMAND, C012 STATUS, C014 BLOCK_LO, C016 BLOCK_HI, C018 DATA, C01A ERROR, C01C COUNT_LO y C01E COUNT_HI; las direcciones impares están reservadas.]]

[[EQ:Bloque 0x0102 = (0x01 × 256) + 0x02 = 258]]

Un par de bytes en el índice puede representar hasta 65536 números de bloque. **Eso no demuestra capacidad física de 16 MiB**: puede haber, por ejemplo, una imagen con ocho bloques y fallar la selección de `0008` por estar fuera de rango.

## 3. Estado y dirección de los datos

`STATUS` es una **máscara de bits candidata**, no un registro construido. Su bit `01` indica BUSY; `02`, DRQ (*Data Request*: transferir un byte); `04`, DONE; `08`, ERROR. Por eso el valor `03` significa **BUSY y DRQ simultáneamente**. El controlador sigue ocupado con la transferencia completa, pero ya permite acceder al siguiente byte por DATA.

| Momento | STATUS | COUNT | Significado |
| --- | --- | --- | --- |
| Inactivo o tras RESET | `00` | `0000` | Sin transferencia |
| READ/WRITE abierto | `03` | `0000` a `00FF` | BUSY y DRQ; sigue un byte |
| Transferencia completa | `04` | `0100` | DONE tras 256 bytes |
| Operación rechazada | `08` | Parcial | ERROR; consultar `C01A` |

[[EQ:STATUS 0x03 = BUSY 0x01 OR DRQ 0x02]]

[[EQ:COUNT final 0x0100 = 256 bytes = COUNT_HI 01 y COUNT_LO 00]]

El siguiente esquema muestra estados **lógicos**, no tiempos de reloj. Durante una transferencia no está permitido reconfigurar a mitad el bloque: la propuesta detecta y aborta una orden nueva —incluido NOP— o un cambio de BLOCK_LO/HI, salvo RESET que cancela limpiamente el proceso.

[[FIG:c19_fig03_estados_transferencia|Figura 3. El controlador pasa de reposo a transferencia y termina en DONE o ERROR según los 256 accesos.|Secuencia IDLE STATUS00, ACTIVE STATUS03 COUNT0000..00FF, DONE STATUS04 COUNT0100; una configuración ilegal durante ACTIVE lleva a ERROR STATUS08 y RESET vuelve a IDLE.]]

## 4. Leer el bloque 0002 sin inventar un sistema de archivos

**READ** comienza seleccionando el bloque: `BLOCK_LO=02`, `BLOCK_HI=00`; luego escribe `COMMAND=01`. Si el bloque existe, STATUS pasa a `03` y el programa debe leer el puerto `C018` **exactamente 256 veces**. En cada lectura incrementa el contador y deposita el dato en RAM de destino segura. Tras el último byte, COUNT=`0100` y STATUS=`04`.

No confundas leer un bloque y ejecutar código. Los 256 bytes podrían representar una foto, texto, bytes de un programa o basura. **Solamente el programador sabe qué significan** y qué validaciones corresponden antes de utilizarlos.

[[EQ:RAM destino al leer 2 bloques desde 0x1000 = 0x1000..0x11FF]]

Si se solicita un bloque que no existe, ERROR tiene el código candidato `02`; si se intenta leer/escribir DATA en el estado equivocado, el código sería `03`. Estos valores no son mensajes de un dispositivo real: servirían para diagnosticar la implementación futura.

## 5. Escribir 255 bytes no equivale a haber guardado 256

Para **WRITE**, el programa selecciona bloque y escribe `COMMAND=02`. El controlador admite los bytes de DATA uno por uno. El contrato establece que **no se da por válido el nuevo bloque hasta el byte número 256**: la escritura incompleta debe descartarse. El modelo anfitrión reemplaza de forma controlada la imagen después de completar el bloque, y los ensayos automatizados abren de nuevo el archivo para comprobar la persistencia **en la PC anfitriona**.

[[EQ:Bytes pendientes tras escribir 255 = 256 − 255 = 1]]

Esa demostración no prueba resistencia física ante apagones, condensadores agotados o memoria flash cortada a mitad de operación. La **atomicidad es por bloque en el modelo de archivo** y está limitada por la semántica del sistema anfitrión; una implementación real necesita protocolos de recuperación y pruebas de pérdida de energía. Tampoco se promete que una carga de varios bloques sea una operación indivisible.

## 6. Cargar a RAM no significa ejecutar

El monitor actual solo dispone en su contrato base de `HELP`, `MEM`, `POKE` y `RUN`; **`LOAD` sigue marcado NO DISPONIBLE**. Para preparar el diseño posterior, se propone una sintaxis exclusivamente hexadecimal: `LOAD bloque destino cantidad`. La orden hipotética `LOAD 0002 1000 02` copiaría los bloques `0002` y `0003` a `RAM[1000..11FF]`.

| Orden futura | Resultado pretendido, no ejecutado |
| --- | --- |
| `LOAD 0002 1000 02` | Copiar 512 bytes crudos al área de herramientas |
| `LOAD 0001 6000 01` | Copiar 256 bytes crudos al área de práctica |
| `MEM 6000 07` | Verificar siete bytes de un programa ya depositado |
| `RUN 6000` | Llamar al programa desde el monitor; aún sin CPU/ROM real |

[[EQ:Destino final de LOAD 0002 1000 02 = 0x1000 + 512 − 1 = 0x11FF]]

El cargador futuro solo debe aceptar destinos **alineados a 256 bytes** dentro de las ventanas `1000–2FFF` (herramientas) o `6000–6FFF` (práctica). Su búfer de etapa `0200–0FFF` permite verificar un bloque completo antes de copiarlo. Si falla el segundo bloque después de copiar el primero, **el destino puede quedar parcialmente sobrescrito**: el programa no debe ejecutarse en ese estado.

## 7. Un programa conservado en un bloque

Para enlazar con el capítulo 18, supongamos que el bloque persistente `0001` comienza con estos siete bytes: `11 00 41 35 00 FF 02`. El resto de ese bloque crudo contiene **249 bytes adicionales**. Si un cargador futuro copiara ese bloque a `0x6000`, los siete primeros bytes serían `LDI R0,0x41`, `CALL FW_PUTC` y `RET`.

[[EQ:Espacio restante del bloque crudo = 256 − 7 = 249 bytes]]

La prueba de aceptación que deseamos algún día es sencilla: cargar el bloque, comprobar con `MEM 6000 07`, ejecutar con `RUN 6000`, observar `A` y recuperar el prompt mediante RET. **Hoy no ocurre en Aula-8**: falta el cargador nativo, el firmware, la CPU, la terminal y su interacción eléctrica. Sí podemos comparar la representación binaria y el contenido de una imagen de bloques en el anfitrión.

## 8. El contenedor AEX1 evita adivinar qué es cada binario

El bloque crudo carece de metadatos. No explica qué arquitectura debe ejecutarlo, en qué RAM cabrá, dónde empieza la primera instrucción o cuántos bytes útiles existen. Para resolverlo se propuso **AEX1**, un encabezado de 32 bytes que precede al programa y declara versión, destino Aula-8, tipo, origen, entrada, longitud y verificaciones CRC16.

[[EQ:Bloques AEX1 = techo((32 + bytes de programa) / 256)]]

Un programa de siete bytes necesita `32+7=39` bytes y se rellena el bloque hasta 256. **Los 32 bytes de la cabecera no deben copiarse a la RAM del programa**; el código real comienza en la dirección de origen indicada. El CRC detecta algunos errores accidentales, pero no demuestra que el código sea seguro ni que se corresponda con las instrucciones de una CPU construida.

[[EQ:Relleno para AEX1 de 7 bytes = 256 − 32 − 7 = 217 bytes]]

Antes de estudiar la figura, distingue las dos rutas: `LOAD` interpreta bytes crudos sin cabecera; `LOADX` reconocerá un AEX1, comprobará formato/CRC/rangos y copiará **solo el payload**. Ambos comandos **siguen sin existir como órdenes nativas del monitor**.

[[FIG:c19_fig04_carga_cruda_y_aex1|Figura 4. LOAD crudo copia bloques completos, mientras LOADX candidato separa cabecera AEX1 y copia solo código validado.|Ruta izquierda LOAD de 256 bytes hacia RAM 6000 con siete bytes significativos y 249 adicionales; ruta derecha LOADX con cabecera 32 bytes, payload 7 y relleno 217, donde solo los siete bytes útiles irían a RAM.]]

[[EQ:Programa útil ejemplo = 7 bytes; cabecera AEX1 = 32 bytes]]

El modelo R0.14 propone validar toda la imagen con CRC en una primera pasada y copiar durante una segunda lectura por bloques de 256 bytes. Evita necesitar un búfer del tamaño máximo, **pero la RAM puede quedar modificada parcialmente si falla la segunda pasada**. Tampoco garantiza que el almacenamiento permanezca idéntico entre pasadas ni que un corte de energía sea seguro. El código modelo Python permite reproducir escenarios, no constituye un cargador de firmware implementado.

## 9. Del editor de líneas a los programas complejos

Para no introducir cada opcode con POKE toda la vida, Aula-8 necesitará un **editor de líneas** y después un **ensamblador nativo**. El editor conserva líneas de texto con números, permite corregirlas y guardarlas como datos. El ensamblador transforma símbolos y mnemónicos en opcodes/direcciones, posiblemente en dos pasadas: primero determina posiciones y etiquetas; después emite bytes.

Un programa como `SUMA` requiere registros, instrucciones aritméticas y almacenamiento; el **algoritmo de Euclides** añade bucles y decisiones; **Fibonacci recursivo** necesita llamadas anidadas, parámetros, pila y límites contra desbordamiento. No debemos prometerlos ejecutables ahora. En el siguiente capítulo creceremos hacia un sistema pequeño donde estos escalones puedan verificarse **de uno en uno**, con salidas esperadas y diagnósticos cuando fallen.

Sin nombres de archivo ni directorios, el usuario todavía necesita conocer «bloque 0001». Agregar nombres, tabla de asignación, reserva de espacio y recuperación ante corrupción requiere un diseño de sistema de archivos que no está definido. No llamemos «archivo» a cualquier bloque numérico antes de haber especificado esa estructura.

[[PAGEBREAK]]
## Construimos Aula-8: un programa conserva su orden al salir de RAM

Durante una ejecución, el PC puede saltar hacia atrás, avanzar o entrar a una subrutina. Pero el almacenamiento persistente no guarda esos recorridos como flechas: debe guardar **los bytes mismos y su orden**. Un bloque de 256 bytes es una secuencia de posiciones; al recuperarlo hacia un destino autorizado, cada byte vuelve a ocupar su dirección correspondiente. Eso permite reconstruir el programa que antes vimos en el mapa `0x6000–0x6007`.

Al comprobar una carga, no basta que el último byte sea correcto: hay que verificar origen, destino, tamaño, integridad y región permitida. El modelo anfitrión puede demostrar esa correspondencia y detectar fallos, pero todavía no constituye una rutina LOAD ejecutada dentro de Aula-8. Las flechas de la futura figura de transferencia deberán distinguir **orden de almacenamiento**, **orden de carga** y **recorrido posterior del PC**.

## Ejercicios del capítulo 19

**Ejercicio 1 — Bloque.** ¿Cuál es el offset inicial del bloque `0002` en una imagen de 256 B por bloque?

**Ejercicio 2 — Redondeo.** ¿Cuántos bloques crudos requieren 4097 bytes?

**Ejercicio 3 — Registro.** ¿Dónde se escribe el comando READ y qué valor lleva?

**Ejercicio 4 — Índice.** Escribe BLOCK_LO/BLOCK_HI para seleccionar `0102`.

**Ejercicio 5 — Estado.** ¿Qué significa STATUS=`03` durante la transferencia?

**Ejercicio 6 — Cuenta.** ¿Cuál es COUNT al transferir 256 bytes y cómo se divide en LO/HI?

**Ejercicio 7 — ERROR.** ¿Qué ocurre si se reconfigura el bloque a mitad de una operación activa?

**Ejercicio 8 — Persistencia.** ¿Una escritura de 255 bytes debe cambiar el bloque persistente?

**Ejercicio 9 — Destino.** Calcula la última dirección de `LOAD 0002 1000 02`.

**Ejercicio 10 — Programa.** ¿Cuántos bytes adicionales tiene un bloque crudo de 256 B si el programa útil ocupa siete?

**Ejercicio 11 — AEX1.** ¿Cuántos bytes de relleno requiere un AEX1 de siete bytes útiles dentro de un bloque?

**Ejercicio 12 — Garantía.** ¿Por qué una segunda pasada con CRC no garantiza carga atómica ante un fallo?

[[PAGEBREAK]]
## Solucionario del capítulo 19

**1.** `0x0200`, porque `2×256=512` bytes.

**2.** `ceil(4097/256)=17` bloques.

**3.** Escribir `01` en `COMMAND`, dirección `C010`.

**4.** `BLOCK_LO=02` en C014 y `BLOCK_HI=01` en C016.

**5.** BUSY=`01` más DRQ=`02`: transferencia activa y byte siguiente permitido.

**6.** COUNT=`0100`, con LO=`00` y HI=`01`.

**7.** El contrato rechaza/aborta la transferencia y señala ERROR; no mezcla bytes de dos bloques.

**8.** No. El modelo solo confirma el bloque al recibir el byte 256; una escritura incompleta se descarta.

**9.** `0x1000 + 0x0200 − 1 = 0x11FF`.

**10.** `256−7=249` bytes.

**11.** `256−32−7=217` bytes.

**12.** Después de validar, la segunda lectura puede fallar o cambiar el soporte. Algunos bloques podrían haberse copiado ya sobre RAM y no habría rollback.

## Para continuar

El **capítulo 20** enlazará editor, ensamblador y sistema pequeño, con programas que evolucionen desde guardar un número y sumarlo hasta bucles y procedimientos. La complejidad debe aumentar **solo cuando los mecanismos anteriores funcionen**: no saltaremos directamente a recursión o a un sistema de archivos antes de dominar la representación de bytes, los retornos y la persistencia.
