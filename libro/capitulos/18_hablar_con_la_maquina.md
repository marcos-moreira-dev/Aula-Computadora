# Capítulo 18. Hablar con la máquina

*Parte V · Microcomputadora y software · Aula-Computadora*

Al terminar el capítulo anterior, Aula-8 sabía —sobre el papel— cómo empezar en una ROM ya grabada y esperar órdenes del monitor. Pero una computadora que no recibe ni muestra información sigue siendo difícil de utilizar. ¿Cómo llega una tecla al procesador? ¿Qué hace exactamente la orden que imprime una letra? ¿Y qué diferencia hay entre un carácter, su número ASCII y el circuito que lo transporta?

Vamos a avanzar en tres escalones: **mostrar `A`**, **recibir un carácter y devolverlo**, y **guardar ese carácter en una variable de RAM antes de mostrarlo**. Una cuarta práctica imprimirá una cadena. Todos los programas dependen de la **ISA, ROM y periférico candidatos** de Aula-8: los bytes se pueden verificar, pero **todavía no se ejecutan en una CPU construida ni en un monitor real**.

## 1. El terminal no es una dirección de memoria cualquiera

El terminal propuesto recibe y envía **caracteres de ocho bits**. En la memoria mapeada de Aula-8 tiene dos direcciones: `0xC000`, puerto **DATA**, y `0xC002`, puerto **STATUS**. Estas direcciones pertenecen a entrada/salida (**MMIO**), no a la RAM de programas. Un acceso a DATA puede provocar un efecto externo; por eso no se debe tratar como si fuera otra variable ordinaria.

[[EQ:Carácter A en ASCII = decimal 65 = 0x41 = binario 01000001]]

[[EQ:Dirección de DATA = 0xC000; dirección de STATUS = 0xC002]]

No hemos fijado aún el chip controlador, la temporización de las señales, las interrupciones ni la polaridad eléctrica de sus pines. **El código de estado del registro MMIO no está aprobado.** Lo que sí existe en el contrato es una **API de firmware candidata**, `FW_STATUS`, que devuelve en R0 dos bits conceptuales: bit 0, recepción disponible; bit 1, transmisión lista. No debemos copiar esos bits a un supuesto registro físico C002 sin demostrar su implementación.

Antes de mirar el esquema, distingue **dos sentidos independientes**: el byte que llega desde un teclado a la entrada y el byte que sale hacia una pantalla o terminal. El procesador consulta el estado antes de consumir o enviar cada carácter.

[[FIG:c18_fig01_terminal_y_mmio|Figura 1. Un terminal intercambia bytes con Aula-8 a través de los puertos DATA y STATUS candidatos.|La figura distingue flecha de recepción RX hacia Aula-8, flecha de transmisión TX hacia el terminal y lectura de STATUS por polling. C000 es DATA, C002 es STATUS y los bits públicos de FW_STATUS no se confunden con la codificación física del registro.]]

[[EQ:Máscara pública propuesta de FW_STATUS = RX_disponible × 1 + TX_lista × 2]]

## 2. Esperar no significa que la computadora esté averiada

Si todavía nadie ha pulsado una tecla, una lectura de recepción no tiene un carácter válido. Y si el transmisor está ocupado, enviar inmediatamente otro byte puede perder datos. Un programa sencillo consulta un estado y vuelve a consultarlo hasta que el periférico esté listo: a eso se le llama **sondeo o polling**.

| Condición observada por el firmware | Acción lógica |
| --- | --- |
| RX no disponible | Esperar y consultar de nuevo |
| RX disponible | Leer un byte del canal de entrada |
| TX ocupado | Esperar y consultar de nuevo |
| TX listo | Entregar el byte al canal de salida |

[[EQ:TX lista en la API ⇔ (R0 AND 0x02) ≠ 0]]

**No hay un tiempo de espera garantizado.** Un teclado sin actividad puede mantener bloqueada la lectura cuanto sea necesario. La frecuencia de sondeo, el buffer interno y los tiempos reales de llegada de caracteres se decidirán al construir el periférico y la ROM; el dibujo no representa un oscilograma medido.

## 3. Hablar con un servicio estable de ROM

Una aplicación no debería conocer cada detalle de C000/C002. Para eso el borrador del capítulo 17 reservó cuatro **puntos de entrada públicos** en ROM. La dirección permanece estable aunque mañana cambie la rutina interna.

| Servicio público candidato | Dirección | Entrada o salida de la llamada |
| --- | --- | --- |
| `FW_PUTC` | `FF00` | Recibe un byte en R0 y lo transmite |
| `FW_GETC` | `FF04` | Espera una tecla y devuelve su byte en R0 |
| `FW_PUTS` | `FF08` | Recibe en X una cadena terminada en `00` |
| `FW_STATUS` | `FF0C` | Devuelve máscara pública candidata en R0 |

`CALL FF00` se codifica como `35 00 FF`: opcode `35`, byte bajo `00` y alto `FF`. El firmware ofrece en `FF00` una ranura ilustrativa `30 00 E1 00`: `JMP E100`, seguido de `NOP`. **E100 no es una rutina grabada ni ejecutable**: es una dirección ficticia que permite entender cómo la ROM podría reubicar una función sin modificar el programa del usuario.

[[EQ:Ranura FF00 = 30 00 E1 00; longitud = 4 bytes]]

Mira la trayectoria de la siguiente figura: el programa ejecutaría CALL hacia la dirección pública, la ranura saltaría a la implementación y el servicio regresaría mediante RET al byte posterior a CALL. El retorno no nace en el JMP de la ranura; fue guardado por CALL en la pila.

[[FIG:c18_fig02_llamada_publica_rom|Figura 2. CALL llega a una ranura pública, JMP salta a la implementación y RET vuelve al programa.|Programa en 6003 llama a FF00; los bytes 30 00 E1 00 realizan un salto conceptual a E100; un RET ilustrativo retorna a 6006 mediante el retorno guardado en pila, sin ejecutar el NOP de relleno.]]

[[EQ:Retorno después de CALL desde 0x6003 = 0x6003 + 3 = 0x6006]]

La **ABI pública candidata** exige conservar R2, R3 y X, pero permite modificar R0, R1 y FLAGS. Así que un programa no debe confiar en R0 después de `FW_PUTC`, salvo que la rutina prometa expresamente un resultado. En cambio, `FW_GETC` sí promete entregar el carácter leído en R0.

## 4. Primer escalón: imprimir una sola letra

Escribimos el menor programa del capítulo. `LDI` coloca en R0 el número hexadecimal `41`, que representa `A`. `CALL` invoca el servicio público, y `RET` regresa al monitor si el monitor lanzó el programa con CALL, como estableció el capítulo 17.

| Dirección | Bytes hex | Acción candidata |
| --- | --- | --- |
| `6000` | `11 00 41` | `LDI R0,0x41` |
| `6003` | `35 00 FF` | `CALL FW_PUTC` |
| `6006` | `02` | `RET` al monitor |

[[EQ:Longitud del programa A = 3 + 3 + 1 = 7 bytes]]

El resultado **esperado cuando haya CPU, firmware y pantalla** es una `A`. No afirmamos haberla visto. Si en lugar del último `02` colocáramos `01` (`HALT`), la CPU se detendría en vez de recuperar el prompt. Esta distinción se conservará en todos los ejemplos de interacción.

## 5. Segundo escalón: recibir y repetir una tecla

En lugar de decidir nosotros qué letra imprimir, llamamos a `FW_GETC` (`FF04`), que devolvería el byte recibido en R0. A continuación `FW_PUTC` enviaría el mismo byte. El usuario observaría un **eco**: teclea `B` y recibe `B`, por ejemplo. Esta aplicación demuestra entrada y salida, pero **todavía no conserva el dato** para utilizarlo más adelante.

| Dirección | Bytes hex | Efecto esperado |
| --- | --- | --- |
| `6000` | `35 04 FF` | GETC deposita carácter en R0 |
| `6003` | `35 00 FF` | PUTC transmite R0 |
| `6006` | `02` | Regresar al monitor |

[[EQ:Eco mínimo = 3 + 3 + 1 = 7 bytes de programa]]

Aunque en esta descripción decimos «tecla», el teclado físico puede enviar códigos de control, un retorno de carro o caracteres no imprimibles. **El byte no significa automáticamente una letra visible.** La codificación de teclado, los saltos de línea y los códigos mayores que 127 deben especificarse antes de prometer comportamiento uniforme.

## 6. Tercer escalón: una variable en RAM sobrevive a la llamada

Agregamos un `ST` entre GETC y PUTC para que el byte recibido quede almacenado en `RAM[0x6F00]`. Aquí aparece una capacidad útil: el programa recuerda una entrada aunque después vuelva a consultar otra tecla. `ST` absoluto utiliza `13 00 00 6F`: opcode, selector de R0, dirección baja y dirección alta.

| Dirección | Bytes hex | Efecto esperado |
| --- | --- | --- |
| `6000` | `35 04 FF` | `CALL FW_GETC` |
| `6003` | `13 00 00 6F` | `ST [0x6F00],R0` |
| `6007` | `35 00 FF` | `CALL FW_PUTC` |
| `600A` | `02` | `RET` |

[[EQ:Dirección RAM del dato = 0x6F00 = 28416]]

[[EQ:Longitud del programa eco con variable = 3 + 4 + 3 + 1 = 11 bytes]]

Si llegara el byte `0x42` (`B`), el estado esperado **antes de PUTC** sería R0=`42` y RAM[`6F00`]=`42`. Después de PUTC no suponemos que R0 conserve ese valor, pero la RAM sí lo conserva si la rutina ROM no pisa la dirección de práctica. Verifica en la figura que **el almacenamiento se realiza antes de transmitir**.

[[FIG:c18_fig03_eco_con_variable|Figura 3. GETC entrega un byte, ST lo guarda en RAM y PUTC lo envía.|Secuencia de instrucciones 6000 CALL FF04, 6003 ST [6F00],R0, 6007 CALL FF00 y 600A RET; ejemplo ilustrativo B igual a 42 hexadecimal en R0 y RAM[6F00] antes de salida.]]

Esta es la misma idea de «guardar una variable» que usarás en programas mayores. Antes de Euclides o Fibonacci, una computadora debe poder mover datos, actualizar estados y regresar correctamente de una función. **Un algoritmo no se vuelve ejecutable por tener nombre conocido.**

## 7. Cuarto escalón: imprimir una cadena sin duplicar llamadas

Llamar a PUTC cuatro veces funciona para imprimir `HOLA`, pero no es cómodo para mensajes más largos. El servicio `FW_PUTS` recibe en X la dirección de una cadena y transmite cada byte hasta encontrar el terminador `00`.

En `0x6100` reservaríamos los bytes `48 4F 4C 41 00`. El programa de `0x6000` hace `SETX 0x6100` (`14 00 61`), `CALL FW_PUTS` (`35 08 FF`) y `RET` (`02`). **El cero final no se imprime**: solo marca el final para la rutina.

[[EQ:Tamaño de HOLA con terminador = 4 caracteres + 1 = 5 bytes]]

[[EQ:SETX 0x6100 = 14 00 61; CALL FW_PUTS = 35 08 FF]]

[[FIG:c18_fig04_cadena_terminada|Figura 4. FW_PUTS recorre cuatro caracteres ASCII y se detiene ante el terminador 00.|RAM 6100–6104 contiene 48 H, 4F O, 4C L, 41 A y 00 FIN; X apunta inicialmente a 6100 y la terminal muestra HOLA, sin mostrar el terminador.]]

[[EQ:Salida prevista = bytes 48 4F 4C 41 → texto HOLA]]

Un dato de seguridad: si falta el `00`, el servicio podría continuar leyendo direcciones contiguas. Una rutina robusta necesitaría reglas de límites; Aula-8 **todavía no dispone de protección hardware de memoria** ni de una implementación probada de PUTS.

## 8. El monitor convierte una entrada en una orden

El monitor teórico reconoce `HELP`, `MEM`, `POKE` y `RUN` sin distinguir mayúsculas. **No ejecuta directamente la palabra escrita**: primero recibe bytes, los guarda, identifica la orden, valida la cantidad de argumentos y comprueba sus rangos. El número `10` en `MEM 6000 10` es **hexadecimal** y significa 16 bytes, no diez.

| Línea escrita | Interpretación candidata |
| --- | --- |
| `MEM 6000 10` | Leer 16 bytes desde `6000` |
| `POKE 6000 2A` | Escribir byte `2A` en RAM de práctica |
| `RUN 6000` | Entrar por CALL en un programa de práctica |
| `POKE FF00 30` | Rechazar: intenta modificar ROM |
| `REG`, `LOAD` | No disponibles en R0.11 |

[[EQ:MEM 6000 10 consulta 0x10 = 16 posiciones]]

El editor hexadecimal del monitor permite cambiar **bytes**, no «variables con nombre». Para saber que `6F00` guarda la última tecla, el programador todavía debe llevar un mapa de sus datos. Nombrarlos y calcular sus direcciones corresponde más adelante al ensamblador.

## 9. Diagnóstico: separar problemas de CPU, firmware y terminal

Si no aparece `A`, habría que preguntar en orden: ¿la CPU fue realmente construida y llegó a `0x6000`? ¿Está grabada la tabla pública `FF00`? ¿Existe código efectivo del servicio? ¿La pila conserva el retorno? ¿El terminal tiene alimentación, conexiones y estado TX listo? Un `RUN` aceptado por un **parser de Python** no demuestra ninguna de esas condiciones físicas.

Si el eco imprime un signo extraño, revisa el byte recibido y la codificación. Si PUTS no termina, revisa el `00`. Si el prompt desaparece tras ejecutar, comprueba que el programa termina en **RET** y no en **HALT**. Todas estas verificaciones son criterios de aceptación para una futura implementación, no resultados ya obtenidos.

[[PAGEBREAK]]
## Construimos Aula-8: un byte abandona la memoria y llega a la pantalla

Los capítulos 14–17 siguieron bytes de programa, direcciones y retorno. Ahora la misma CPU necesita distinguir **una celda RAM** de un **registro de periférico mapeado en memoria**. Escribir un carácter en la dirección lógica `0xC000` no significa necesariamente almacenar un byte en RAM; el decodificador selecciona el terminal. Antes de escribir, el programa debe consultar el estado previsto en `0xC002` y respetar el protocolo del dispositivo.

Una letra `A` se codifica aquí como `0x41`. El dato puede proceder de un registro o de RAM, atravesar la ruta de datos del procesador y terminar en el controlador del terminal. El capítulo describe ese contrato sin asumir una UART, pantalla física ni firmware probado. Más adelante el modo texto del capítulo 23B usará caracteres y una ROM de glifos **distintos de la ROM del firmware**.

## Ejercicios del capítulo 18

**Ejercicio 1 — Dirección.** ¿Qué diferencia hay entre DATA `C000` y una variable en `6F00`?

**Ejercicio 2 — ASCII.** Convierte `0x41` a decimal y explica qué carácter ASCII representa.

**Ejercicio 3 — Estado.** ¿Por qué no se puede asegurar que el bit 1 de C002 sea el mismo bit 1 de `FW_STATUS`?

**Ejercicio 4 — Espera.** ¿Qué debe hacer GETC si todavía no se recibió un carácter?

**Ejercicio 5 — Ranura.** ¿Cuántos bytes ocupa CALL FF00 y qué guarda en pila?

**Ejercicio 6 — Retorno.** En el programa de siete bytes, ¿a qué dirección vuelve el RET de la rutina PUTC?

**Ejercicio 7 — Programa.** ¿Qué salida correspondería a `11 00 41 35 00 FF 02` si existieran los servicios?

**Ejercicio 8 — Eco.** ¿Qué dos servicios usa el programa que repite una tecla?

**Ejercicio 9 — Variable.** Si GETC devolviera `0x42`, ¿qué contenido quedaría en `RAM[6F00]` tras ST?

**Ejercicio 10 — Cadena.** Escribe los cinco bytes de `HOLA` con terminador.

**Ejercicio 11 — Hexadecimal.** ¿Cuántos bytes pide `MEM 6000 10`?

**Ejercicio 12 — Diagnóstico.** ¿Por qué HALT no permite asumir que el monitor recupera el prompt?

[[PAGEBREAK]]
## Solucionario del capítulo 18

**1.** C000 es un registro MMIO del terminal: una lectura/escritura puede significar recibir/transmitir; 6F00 es una celda de RAM de práctica.

**2.** `0x41=4×16+1=65`; corresponde a `A` en ASCII.

**3.** El contrato da bits **públicos de API**, pero no define aún el cableado ni el registro físico de STATUS en C002.

**4.** Seguir esperando y consultar el estado hasta que RX esté disponible; no inventar un byte.

**5.** Tres bytes (`35 00 FF`); CALL apila PC posterior a esos tres bytes.

**6.** Regresa a `6006`, siguiente byte posterior a CALL de `6003`.

**7.** Mostraría la letra `A` y regresaría al monitor si RUN entró mediante CALL y la pila está equilibrada.

**8.** `FW_GETC` recibe y `FW_PUTC` transmite.

**9.** `RAM[6F00]=0x42`; en ASCII es `B`.

**10.** `48 4F 4C 41 00`.

**11.** Dieciséis bytes: `0x10=16` decimal.

**12.** HALT detiene la CPU y no recupera la dirección de retorno; RET sí desapila PC.

## Para continuar

Ya conseguimos seguir, en un contrato escrito, datos que llegan del terminal, se guardan en RAM y salen de nuevo. Pero si desconectamos la energía, esa RAM puede perderlos. El **capítulo 19** introduce el almacenamiento persistente por bloques y distingue **guardar bytes**, **cargarlos en RAM** y **ejecutar un programa**; son tres operaciones diferentes.
