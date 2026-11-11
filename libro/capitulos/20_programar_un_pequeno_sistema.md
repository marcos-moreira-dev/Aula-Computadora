# Capítulo 20. Programar un pequeño sistema

*Parte V · Microcomputadora y software · Aula-Computadora*

En el capítulo 19 guardamos bytes en bloques. Ahora aparece una pregunta que un panel de interruptores no resuelve cómodamente: **¿cómo escribir, corregir y volver a ejecutar un programa sin introducir a mano cada hexadecimal?** El primer programa mostraba una `A`; una utilidad real podría leer números, sumarlos, compararlos y repetir operaciones hasta resolver un problema. Necesitamos un camino desde las **líneas que entiende una persona** hasta los **bytes que entiende una CPU**.

Construiremos ese camino de forma escalonada: editor de líneas, ensamblador de dos pasadas, código cargado en RAM, biblioteca de servicios de ROM y un monitor sencillo. Después seguiremos dos programas completos: **sumar 13 y 9** y resolver el **máximo común divisor de 48 y 18** por restas sucesivas. Por último estudiaremos dónde encaja Fibonacci y por qué la recursión depende de una pila disciplinada.

**Límite indispensable:** Aula-8 no cuenta aún con CPU, firmware ni ensamblador **nativo** ejecutables. El script Python incluido con este libro **sí ensambla un subconjunto definido de la ISA candidata R0.3 en la PC anfitriona** y permite comprobar direcciones, etiquetas y bytes. Ese hecho es distinto de demostrar que Aula-8 ejecuta el resultado. Las instrucciones, zonas de RAM y ABI siguen siendo propuestas de diseño.

## 1. De una orden manual a una herramienta reutilizable

Una computadora que solo admite `POKE 6000 11` es útil para aprender qué significa cada byte. Sin embargo, un algoritmo con treinta instrucciones tendría decenas de direcciones que calcular y corregir manualmente. Cada inserción desplazará todas las direcciones posteriores. Un **editor de líneas** debe guardar texto; un **ensamblador** debe traducirlo; el **cargador** debe colocarlo en RAM; y la **CPU** debe ejecutarlo.

Observa los distintos productos de cada etapa: la línea `JZ FIN` es texto que contiene una etiqueta; la dirección `6018` es un número asignado a esa etiqueta; los bytes `31 18 60` representan una instrucción candidata. **Texto, dirección y código máquina no son intercambiables.**

[[EQ:Línea fuente «JZ FIN» → dirección de FIN 0x6018 → bytes 31 18 60]]

[[FIG:c20_fig01_herramientas_y_capas|Figura 1. Editor, ensamblador, almacenamiento, cargador, monitor y CPU desempeñan funciones diferentes.|Un editor entrega texto; un ensamblador de dos pasadas produce bytes; un soporte persistente conserva esos bytes; LOADX candidato copiaría payload a RAM; RUN del monitor llamaría a una CPU que aún no existe.]]

La ROM candidata ofrece servicios básicos de terminal y monitor, mientras las utilidades grandes se conciben como **herramientas cargadas a RAM**. El presupuesto provisional reserva una región de herramientas `1000–2FFF` y una región de práctica `6000–6FFF`. Nada asegura todavía que el editor o el ensamblador nativo quepan juntos: hay que implementarlos, medir sus tamaños y quizá alternarlos en una región compartida (*overlay*). No cabe llamar «sistema operativo completo» a cuatro órdenes de monitor.

## 2. Qué guarda el editor de líneas

Imagina que escribimos `LDI R0, 13`, después `LDI R1, 9` y más tarde `ADD R0, R1`. El editor no almacena directamente las instrucciones: almacena caracteres del texto, espacios, comas y saltos de línea. El compilador/ensamblador interpreta esos signos mediante reglas. El carácter `1` ASCII ocupa `0x31`; el operando numérico decimal `13`, una vez traducido, ocupa `0x0D`. Son objetos distintos.

[[EQ:Texto «13» = bytes ASCII 31 33; valor inmediato decimal 13 = 0x0D]]

Un editor mínimo necesita `LIST` para mostrar líneas, `INSERT` para añadirlas, `REPLACE` para corregirlas, `DELETE` para retirarlas y `SAVE`/`OPEN` para persistirlas. **Ninguna de estas órdenes es actualmente parte funcional del monitor R0.11**. Describirlas es precisar un requisito de implementación, no comunicar que ya están instaladas en Aula-8.

El ensamblador de referencia incluido funciona inicialmente **fuera** de Aula-8. Recibe un archivo de texto con `.ORG 0x6000`, nombres de instrucciones, registros `R0..R3`, valores decimales o `0x` hexadecimales y etiquetas terminadas por `:`. Está limitado deliberadamente a un subconjunto instructivo; si se escribe una operación no admitida, debe fallar con un mensaje. Una implementación nativa futura deberá alcanzar al menos ese comportamiento y ejecutar **sus dos pasadas sobre Aula-8**, no delegarlas silenciosamente al anfitrión.

## 3. Primera pasada: calcular dónde cae cada etiqueta

Un ensamblador no puede transformar `JZ FIN` en bytes antes de conocer la dirección de `FIN`. En la **primera pasada** recorre el archivo y avanza un contador según el tamaño de cada instrucción. Por ejemplo, `LDI` necesita tres bytes; `CMP`, dos; `JZ`, tres. Cuando encuentra `BUCLE:`, registra la dirección que se haya acumulado. Al encontrar `FIN:`, hace lo mismo.

[[EQ:Dirección siguiente = dirección actual + longitud de instrucción]]

Tomaremos el programa de Euclides de este mismo capítulo. La primera pasada produce una tabla de símbolos verificable:

| Símbolo | Dirección hexadecimal | Qué identifica |
| --- | --- | --- |
| `BUCLE` | `6006` | Comparación de los dos números |
| `RESTAR_A` | `6013` | Rama que resta R1 a R0 |
| `FIN` | `6018` | Almacenar el MCD y retornar |

[[EQ:FIN = 0x6000 + 24 bytes = 0x6018]]

[[FIG:c20_fig02_dos_pasadas_y_etiquetas|Figura 2. Las dos pasadas separan el cálculo de direcciones de la emisión de bytes y resuelven saltos hacia etiquetas posteriores.|En la primera pasada se registran BUCLE=6006, RESTAR_A=6013 y FIN=6018; en la segunda, JZ FIN situado en 6008 emite 31 18 60.]]

La **segunda pasada** vuelve al texto original. Ahora que `FIN=6018`, el salto `JZ FIN` se convierte en el opcode `31` y sus dos bytes de destino en orden little-endian: `18 60`. Si agregamos una instrucción antes de `FIN`, la primera pasada volverá a calcularla: ya no hay que editar a mano todos los saltos que apuntan a la etiqueta.

[[EQ:JZ FIN = opcode 31 + dirección 0x6018 en little-endian → 31 18 60]]

El ensamblador de referencia **rechaza** etiquetas duplicadas, destinos sin resolver, registros fuera de R0–R3 y programas que invaden `6F00`, reservada en estos ejemplos para resultados. Así se puede enseñar una buena disciplina antes de implementar protección de memoria en hardware.

## 4. Primer programa completo: sumar y dejar una evidencia

El ejemplo inicial usa cinco instrucciones: `LDI R0,13`; `LDI R1,9`; `ADD R0,R1`; `ST [0x6F00],R0`; y `RET`. El último `RET` es intencional: si alguna vez lo inicia el monitor mediante `RUN`, debe **regresar al monitor**. `HALT` detendría la CPU en vez de volver al prompt.

| Dirección | Bytes | Explicación |
| --- | --- | --- |
| `6000` | `11 00 0D` | Carga 13 decimal en R0 |
| `6003` | `11 01 09` | Carga 9 decimal en R1 |
| `6006` | `20 01` | ADD R0,R1: selector 0×4+1 |
| `6008` | `13 00 00 6F` | RAM[6F00] recibe R0 |
| `600C` | `02` | RET: regreso al llamador |

[[EQ:13 + 9 = 22 decimal = 0x16 = 00010110 binario]]

[[EQ:Longitud ensamblada = 3 + 3 + 2 + 4 + 1 = 13 bytes]]

El resultado esperado del **modelo semántico** es `R0=0x16`, `RAM[6F00]=0x16` y banderas Z=0, N=0, C=0, V=0 tras ADD. `ST` y `RET` conservarían esas banderas según la propuesta. El archivo `libro/programas/c20_suma_aula8.asm` y su listado de trece bytes se pueden generar con Python. **No hay aún una RAM de Aula-8 ejecutando esa secuencia**.

Si en la práctica futura `RAM[6F00]` contuviera `0D`, sabemos que el programa probablemente almacenó antes de sumar; si contuviera `00`, verificaríamos la codificación de selector, las banderas y la escritura en memoria. Una prueba buena incluye **resultado, estado intermedio y diagnóstico**, no solo un mensaje de «correcto».

## 5. Segundo programa: Euclides añade decisiones y ciclos

El **máximo común divisor** de dos enteros positivos puede encontrarse sin multiplicación ni división: si son iguales, hemos terminado; si uno es mayor, le restamos el otro; repetimos. Este algoritmo encaja en la ISA candidata porque dispone de `CMP`, `SUB` y saltos. **No inventaremos una instrucción MOD/DIV que no está en la tabla R0.3**.

[[EQ:mcd(48,18) = mcd(30,18) = mcd(12,18) = mcd(12,6) = mcd(6,6) = 6]]

Aquí `CMP R0,R1` actualiza Z si son iguales y C como **préstamo de la resta R0−R1**. `JZ FIN` termina cuando Z=1. Si no son iguales, `JNC RESTAR_A` se toma cuando **no** hubo préstamo, es decir, cuando R0 es mayor que R1 sin signo. En caso contrario ejecuta `SUB R1,R0`. Después vuelve a `BUCLE`.

| Dirección | Bytes | Operación candidata |
| --- | --- | --- |
| `6000` | `11 00 30` | R0 = 48 |
| `6003` | `11 01 12` | R1 = 18 |
| `6006` | `24 01` | BUCLE: CMP R0,R1 |
| `6008` | `31 18 60` | JZ FIN |
| `600B` | `34 13 60` | JNC RESTAR_A |
| `600E` | `22 04` | SUB R1,R0 |
| `6010` | `30 06 60` | JMP BUCLE |
| `6013` | `22 01` | RESTAR_A: SUB R0,R1 |
| `6015` | `30 06 60` | JMP BUCLE |
| `6018` | `13 00 00 6F` | FIN: ST [6F00],R0 |
| `601C` | `02` | RET |

[[EQ:Longitud de Euclides = 29 bytes; última dirección ocupada = 0x601C]]

[[FIG:c20_fig03_euclides_estados|Figura 3. El algoritmo de Euclides avanza por restas entre dos registros positivos hasta obtener 6.|Pares de estados (48,18), (30,18), (12,18), (12,6), (6,6); el valor final 6 se guarda hipotéticamente en RAM[6F00].]]

La referencia Python realiza **dos verificaciones separadas**: (1) la traducción textual por longitudes y etiquetas, y (2) un recorrido semántico independiente que aplica comparaciones y restas a los registros. La segunda comprobación no se limita a leer los mismos bytes y dar por supuesto el resultado. Aun así, ninguna de ambas sustituye la ejecución de fetch/decodificación en una CPU real.

La precondición es `a>0` y `b>0`. Con un cero, la versión por restas puede quedarse repitiendo sin progresar; el programa didáctico actual **no admite ceros**. Una aplicación terminada tendría que comprobar entrada, informar el caso y resolver `mcd(a,0)=a` separadamente.

## 6. Fibonacci: primero iteración, después recursión

Fibonacci no es una instrucción, sino una **definición matemática** de una sucesión. Comienza `0, 1, 1, 2, 3, 5, 8...`. Un programa iterativo mantiene dos variables (`anterior` y `actual`), calcula una suma y las actualiza. Es una prueba natural de registros, bucles y conservación de resultados.

[[EQ:F(0)=0; F(1)=1; F(n)=F(n−1)+F(n−2) para n≥2]]

| n | F(n) | ¿Cabe en 8 bits sin signo? |
| --- | --- | --- |
| 0 | 0 | Sí |
| 1 | 1 | Sí |
| 2 | 1 | Sí |
| 3 | 2 | Sí |
| 4 | 3 | Sí |
| 5 | 5 | Sí |
| 6 | 8 | Sí |
| 13 | 233 | Sí |
| 14 | 377 | No |

[[EQ:F(6)=8; F(13)=233≤255; F(14)=377>255]]

La versión recursiva describe `F(6)` como llamadas a `F(5)` y `F(4)`, que llaman otras funciones hasta alcanzar los casos base. Es más expresiva para aprender CALL/RET y ABI, pero trabaja más: incluso con argumentos pequeños se duplican cálculos. La ABI MiniC-Aula R0.10 propone ranuras de parámetros de **dos bytes**, retorno u16 en `R1:R0`, prólogo que salva X/R2/R3 y pila descendente. **Esta recursión todavía es un experimento aritmético en el anfitrión**, no un binario Aula generado ni ejecutado.

[[EQ:Llamadas recursivas ingenuas para F(6) = 25, contando casos base]]

La primera meta es comprobar que `F(6)=8` por iteración y recursión. Luego habría que instrumentar SP, conservar registros, vigilar que la pila no sobrescriba el programa y medir espacio real de cada marco. Saltar directamente a `F(40)` en un procesador de ocho bits **sin definir tipo numérico y presupuesto de pila** no sería una prueba responsable.

## 7. Dónde entra MiniC-Aula

El ensamblador conoce instrucciones y direcciones; un compilador de un lenguaje pequeño permitiría escribir funciones, variables locales y tipos como `u8` y `u16`. Por ejemplo, una expresión en MiniC podría describir `return a + b;`, pero el compilador debe convertirla en cargas, suma, tratamiento del acarreo, retorno y respeto de la ABI. Una **suma `u16` en Aula-8** requiere operar primero el byte bajo mediante ADD y después el alto mediante ADC usando el acarreo retenido; no basta con agregar dos números y asumir que entran en R0.

[[EQ:0x01FF + 0x0001 = 0x0200: bajo FF+01→00 con C=1; alto 01+00+C→02]]

El orden de trabajo acordado es **MiniC-Aula cruzado primero en la PC anfitriona**, y editor/ensamblador **nativos en Aula-8** como objetivo de implementación. El compilador MiniC nativo es una extensión posterior, no una condición de la primera versión. El lenguaje deberá limitarse a lo que pueda traducir y verificar, con mensajes de error cuando una característica no exista.

## 8. Qué hace pequeño a este sistema

Una arquitectura de software modesta puede ofrecer monitor, editor, ensamblador, cargador y unas pocas aplicaciones. No necesita aparentar ventanas gráficas ni procesos paralelos. Pero sí necesita contratos: qué direcciones protege, cómo informa errores, cómo retorna al prompt, cómo guarda herramientas y cuándo se niega a ejecutar un programa parcialmente cargado.

[[FIG:c20_fig04_mini_sistema_y_pruebas|Figura 4. El sistema propuesto distingue monitor ROM, herramientas RAM, programa de usuario y soporte persistente.|ROM E000–FFFF aloja el monitor candidato; RAM 1000–2FFF herramientas futuras; RAM 6000–6EFF programa de práctica; 6F00 datos de ejemplo; bloques persistentes con protocolo de carga futuro.]]

| Acción deseada | Existe como diseño | Existe ejecutándose en Aula-8 |
| --- | --- | --- |
| POKE / MEM / RUN | Gramática candidata ROM R0.11 | No |
| LOAD / LOADX | Contratos de bloques R0.12–R0.14 | No |
| Ensamblar dos pasadas | Referencia Python de un subconjunto | No; Python corre en PC |
| Editor de líneas y MiniC cruzado | Alcance y ABI propuestas | No |
| Ejecutar MCD / Fibonacci | Resultados calculables y probables | No |

Antes de proclamar «mini sistema funcionando», exigiremos iniciar desde RESET, obtener prompt, editar, ensamblar, cargar, ejecutar, retornar, guardar, reiniciar y recuperar sin ayuda oculta del anfitrión. El modelo de bloques por sí solo **no** satisface ese circuito completo.

## 9. Diagnóstico y criterio de aprobación

Una primera prueba de ensamblador debe detectar etiqueta repetida; la segunda, etiqueta ausente; la tercera, un programa que pisa `6F00`; la cuarta, una referencia hacia una región que el monitor no permite ejecutar. Un buen rechazo vale tanto como producir bytes correctos. En la ejecución futura registraremos PC/SP, R0/R1, FLAGS, lecturas/escrituras RAM y salida de terminal; cada instrucción tendrá precondiciones y efectos observables.

[[EQ:Capacidad de práctica reservada para código = 0x6F00 − 0x6000 = 3840 bytes]]

Para estudiar el artefacto de hoy, ejecuta en una PC con Python `python3 scripts/ensamblador_dos_pasadas_aula8_educativo.py libro/programas/c20_euclides_aula8.asm`. Producirá el listado de **29 bytes** y la tabla de etiquetas sin requerir Aula-8. Cuando la CPU sea implementada, se comparará esa imagen con una ejecución instrumentada. **La prueba actual acredita la representación, no el hardware.**

[[PAGEBREAK]]
## Construimos Aula-8: de la tabla de bytes a un programa mantenible

Depositar ocho bytes a mano enseña qué hace el hardware, pero se vuelve incómodo cuando necesitamos etiquetas, saltos y varias funciones. El ensamblador resuelve esa dificultad sin eliminar la realidad de la memoria: convierte una descripción simbólica en **una secuencia de bytes situada en direcciones concretas**. Una etiqueta de salto termina codificada como una dirección o un desplazamiento según la ISA elegida; no queda un nombre escrito dentro de la RAM.

El programa de suma y el de Euclides se deben leer en ambos sentidos: desde el algoritmo hasta las instrucciones, y desde el **volcado contiguo de memoria** hasta lo que ejecutaría el PC. Los binarios actuales son generados por herramientas del anfitrión y se comprueban documentalmente; queda por demostrar su ejecución en una CPU Aula. El próximo escalón será un editor y ensamblador **nativos**, que deben funcionar como código máquina del procesador y no como una interfaz de PC que imita sus resultados.

## Ejercicios del capítulo 20

**Ejercicio 1 — Texto frente a dato.** ¿Por qué la cadena ASCII `13` no es el mismo byte que el número decimal 13?

**Ejercicio 2 — Primera pasada.** ¿Qué dirección obtiene `BUCLE` después de dos LDI de tres bytes desde `6000`?

**Ejercicio 3 — Etiqueta adelantada.** ¿Cuáles son los bytes de `JZ FIN` si FIN=`6018`?

**Ejercicio 4 — Suma.** Calcula 13+9 y representa el resultado en hexadecimal y binario de ocho bits.

**Ejercicio 5 — Longitud.** ¿Cuántos bytes necesita el programa de suma completo y dónde se sitúa su RET?

**Ejercicio 6 — Regreso.** ¿Por qué el programa lanzado por RUN termina en RET en vez de HALT?

**Ejercicio 7 — Flags.** Después de comparar R0=12 con R1=18 sin signo, ¿qué ocurre con C y JNC?

**Ejercicio 8 — Euclides.** Escribe los cinco pares de valores que llevan de (48,18) a (6,6).

**Ejercicio 9 — Restricción.** ¿Qué caso debe tratarse aparte para no bloquear Euclides por restas?

**Ejercicio 10 — Fibonacci.** ¿Cuánto vale F(6) y cuál es el primer F(n) que no cabe en `u8`?

**Ejercicio 11 — ABI.** ¿Por qué una función `u16` que usa una CPU de ocho bits necesita conservar el acarreo entre bytes?

**Ejercicio 12 — Garantía.** ¿Qué demuestra el ensamblador Python y qué falta para afirmar que el mini sistema funciona en Aula-8?

[[PAGEBREAK]]
## Solucionario del capítulo 20

**1.** El texto contiene los caracteres `1` (`31` hexadecimal) y `3` (`33`); el valor decimal 13 se codifica como `0D` en un byte.

**2.** `6006`: dos instrucciones de tres bytes ocupan `6000–6005`.

**3.** `31 18 60`: opcode JZ y dirección little-endian.

**4.** `22` decimal = `16` hexadecimal = `00010110` binario.

**5.** Trece bytes, con `RET=02` en `600C`.

**6.** RUN usa una llamada; RET restaura la dirección del monitor guardada en la pila. HALT detendría la CPU.

**7.** Como 12 es menor que 18, CMP señala préstamo `C=1` y JNC **no salta**.

**8.** (48,18) → (30,18) → (12,18) → (12,6) → (6,6).

**9.** El cero: el programa de restas exige operandos positivos; `mcd(a,0)=a` se resuelve separadamente.

**10.** `F(6)=8`. `F(14)=377` es el primero de la sucesión que supera 255.

**11.** Una suma del byte bajo puede generar un acarreo que se debe incluir en la suma del byte alto, mediante ADC.

**12.** Python comprueba longitudes, etiquetas, bytes, rangos y cálculos semánticos de anfitrión. Faltan CPU digital/real, firmware, herramientas nativas y ejecución observable tras RESET.

## Para continuar

Con este capítulo terminamos la **primera ruta de software de Aula-8** como diseño comprobable: de un byte a una variable, una suma, un ciclo y una función. En el capítulo 21 cambiaremos de perspectiva: ¿qué gana y qué cuesta ampliar de ocho a dieciséis bits el ancho natural de los registros y la ALU, sin confundirlo con duplicar memoria?
