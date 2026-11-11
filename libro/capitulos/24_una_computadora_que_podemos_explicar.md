# Capítulo 24. Una computadora que podemos explicar

*Parte VI · Cierre de Aula-Computadora · Aula-8 y Aula-16*

Empezamos este libro mirando el recorrido de una corriente por un conductor. Parecía imposible que un interruptor minúsculo acabara formando una computadora. Sin embargo, dimos un paso cada vez: transistor, compuerta, memoria, registro, sumador, unidad de control, direcciones, ROM, RAM y programas. Al escribir los ejemplos de Euclides y Fibonacci, la máquina empezó a parecerse a un compañero de trabajo: una herramienta que conserva información, toma decisiones y repite operaciones.

Hemos llegado al final del **recorrido escrito**, no al final de la ingeniería. Nuestro logro hoy es un conjunto de **modelos lógicos, decisiones documentadas, cálculos, diagramas y pruebas de referencia reproducibles**. Todavía no hemos construido ni validado una CPU Aula-8 o Aula-16, su ROM ejecutable, sus tiempos eléctricos ni su salida física de vídeo. Un libro honesto tiene que distinguir las cosas que puede explicar de aquellas que de verdad puede demostrar al conectar cables y medir señales.

## 1. La máquina vista de lejos

Una computadora con propósito general combina un camino de datos, una unidad de control y memoria para ejecutar una secuencia de operaciones. La **CPU** decide qué instrucción le toca y realiza sus efectos. La **RAM** conserva valores que el programa puede cambiar. La **ROM de firmware** puede ofrecer el arranque y servicios comunes. Los **periféricos** permiten hablar con el exterior: teclado, pantalla y almacenamiento. Los buses y los decodificadores ayudan a seleccionar qué componente participa en cada operación.

No hay que confundir una **idea arquitectónica** con una realización de hardware. Hemos usado nombres para registros, banderas y operaciones como `LDI` o `ST`, pero algunas codificaciones de instrucciones permanecen candidatas. Esa precaución nos evita una contradicción: un diagrama correcto puede describir qué se desea construir sin demostrar que un circuito comercial concreto lo ejecuta.

| Pieza | Responsabilidad | Evidencia existente | Paso pendiente |
| --- | --- | --- | --- |
| CPU y ALU | Interpretar y operar datos | Modelos, operaciones y ejemplos | Implementar ISA y control |
| RAM | Almacenar bytes | Mapa y pruebas anfitrionas | Conectar y medir chips |
| ROM firmware | Arrancar y ofrecer servicios | Contratos candidatos | Código, imagen y arranque real |
| E/S | Teclado, vídeo, bloques | Direcciones y semánticas lógicas | Controladores y pruebas de enlace |
| Software | Resolver problemas | Modelos matemáticos, ASM educativo | Ejecutar en CPU Aula real |

[[EQ:Espacio CPU = 2^16 direcciones de byte = 65536 bytes]]

La figura separa **explicación**, **verificación de referencia** e **implementación física**. Un algoritmo que produce el resultado correcto en Python no prueba que un procesador inexistente tenga la señal `WRITE` correcta. Y un diagrama de buses no garantiza que una resistencia, un flip-flop o una memoria cumpla requisitos de tiempo.

[[FIG:c24_fig01_alcances_y_evidencias|Figura 1. Entender el diseño, comprobar un modelo y construir hardware son logros diferentes.|Tres etapas de evidencia: teoría escrita, simulación de referencia en anfitrión y montaje físico todavía pendiente.]]

## 2. El mapa completo de direcciones

El espacio lógico de direcciones tiene dieciséis bits y es **direccionable por bytes**. En Aula-8 las operaciones naturales son de ocho bits; en Aula-16 son de dieciséis bits, pero la CPU todavía puede acceder a bytes y sus palabras deben comenzar en una dirección par. El ancho del bus de **datos** no duplica el número de direcciones posibles; eso lo gobierna el bus de **direcciones**.

[[EQ:RAM inicial = 0x8000 bytes = 32768 bytes]]

[[EQ:ROM CPU = 0x2000 bytes = 8192 bytes]]

| Direcciones CPU | Interpretación | Estado |
| --- | --- | --- |
| 0000–7FFF | 32 KiB de RAM | Diseño lógico |
| 8000–BFFF | Expansión | Reservada |
| C000–C002 | Terminal DATA y STATUS pares | Candidata |
| C010–C01F | Controlador de bloques | Candidato |
| **C020–C02F** | Vídeo texto/gráficos, registros pares | **Contrato lógico congelado** |
| C030–DFFF | E/S y regiones futuras | Reservadas según intervalo |
| E000–FFFF | 8 KiB de ROM firmware | Tamaño previsto; código pendiente |

La figura ofrece una fotografía del mapa de 65536 direcciones, mostrando grandes intervalos y sus funciones. Dentro de `C020–C02F` hay seis registros activos de **un byte** y dos posiciones pares reservadas; las impares no reflejan los registros. La RAM interna del vídeo **no** aparece como otro intervalo CPU: el controlador tiene un puntero interno para sus 512 bytes de texto y 8192 bytes gráficos.

[[FIG:c24_fig02_mapa_final|Figura 2. Mapa global de memoria de Aula con RAM, regiones reservadas, MMIO y firmware ROM.|Regiones 0000–7FFF RAM, 8000–BFFF expansión, C000–C0FF E/S, C100–DFFF reservado, E000–FFFF firmware.]]

En Aula-16, una palabra de 16 bits ocupa dos bytes contiguos en **little-endian**. Si se guarda `0x1234` comenzando en `0x2200`, el byte `34` va en `2200` y `12` en `2201`. Aun cuando el bus pueda transferir ambos carriles, la **dirección impar inicial para una operación de palabra** se rechaza en el modelo V1. Así evitamos diseñar de forma invisible una transacción de memoria partida.

[[EQ:Palabra = byte_bajo + 256 × byte_alto]]

[[EQ:Palabra válida si (dirección AND 1) = 0]]

Las direcciones **no asignadas** son un asunto diferente. Que las posiciones impares de vídeo no sean alias no decide qué valor devuelve un bus de CPU si un programa intenta leerlas: esa política todavía debe fijarse a nivel general de memoria, sin inventar comportamiento del periférico.

## 3. Cómo nace una instrucción ejecutable

Escribimos pseudocódigo y vimos bytes de algunos ejemplos educativos de Aula-8 generados en el computador anfitrión. El paso pendiente para afirmar que la CPU ejecuta esos bytes es definir y comprobar toda la cadena: **ISA binaria**, unidad de control, lectura de instrucción, efectos sobre registros, estados de la memoria, pila y buses. El nombre `ADD` en un manuscrito por sí solo no da lugar a un sumador conectado al reloj.

Una dirección efectiva puede nacer de una instrucción **inmediata, absoluta, indexada o relativa a pila**. Primero la ISA determina cómo calcularla; después el decodificador de memoria decide si cae en RAM, ROM o E/S; finalmente, si corresponde, un controlador de vídeo usa un segundo espacio de direcciones dentro de su propia VRAM. El capítulo 23B nos mostró por qué `C028`, registro CPU, es distinto del offset gráfico `0002`.

[[EQ:Dirección efectiva indexada = base + desplazamiento en bytes]]

Si un programador recorre tres palabras desde `2200`, las posiciones iniciales son `2200`, `2202` y `2204`. La suma de `0x01FF`, `0x0001` y `0x0002` da `0x0202`. Podemos reproducir los bytes del resultado, comprobar que no hay acceso impar de palabra y detectar cualquier error en el modelo. **No podemos aún medir cuántos ciclos consume**, porque la implementación física y el control de Aula-16 no existen.

## 4. Una escalera de problemas que crece con la máquina

Para mostrar la capacidad de una computadora conviene empezar por operaciones modestas. Primero **guardar un byte** y recuperarlo. Luego sumar dos números; después recorrer varios elementos usando un índice. Cuando las instrucciones de control estén claras, resolver Euclides por repetición y Fibonacci con límites de representación. Finalmente, una pequeña consola permite ejecutar comandos y observar resultados. Esta es una **escalera pedagógica**: cada programa necesita una capacidad que el anterior ayuda a comprender.

| Escalón | Ejemplo | Recurso que exige | Prueba básica |
| --- | --- | --- | --- |
| 1 | Guardar 42 | RAM y escritura | Leer de vuelta 42 |
| 2 | Sumar 13 y 9 | ALU y registro | Resultado 22 |
| 3 | Recorrer tres palabras | Direcciones y contador | Resultado 514 |
| 4 | Euclides 48 y 18 | Comparación y bucle | MCD = 6 |
| 5 | Fibonacci F14 | Estado y suma repetida | Resultado 377 |
| 6 | Consola/monitor | ROM y E/S | Secuencia observable |

[[EQ:MCD(48,18)=6]]

[[EQ:F14=377 y F25=75025]]

Hay un aprendizaje importante en el último ejemplo. `F14` necesita más de ocho bits y `F25` rebasa incluso el valor máximo sin signo de dieciséis bits. La computadora no sabe por intuición que el número matemático esperado es 75025: si el programa usa un registro de 16 bits y aritmética modular, retiene otro patrón. Debemos enseñar las condiciones de error igual que enseñamos el resultado correcto.

[[EQ:75025 mod 65536 = 9489 = 0x2511]]

El paso de mostrar un carácter por consola o un punto de color depende de un periférico, de una representación de datos y de un programa adecuado. No transforma al videojuego didáctico en una computadora con tarjeta gráfica. El objetivo del taller virtual es **experimentar con reglas explícitas y recibir retroalimentación**, no simular una interfaz moderna completa.

## 5. Dos arquitecturas para los mismos problemas

Aula-8 enseña el trabajo fino de un byte, del acarreo y de una CPU con registros generales de ocho bits. Aula-16 amplía el dato natural y el bus externo a dieciséis bits, sin abandonar el direccionamiento de 16 bits. Ambas tienen cuatro registros generales de su respectivo ancho y registros de control de dieciséis bits según el diseño conceptual. **No son binarias compatibles**: una ISA de Aula-16 necesitará codificación, convenios de llamada y herramientas propios.

[[EQ:2^8 = 256; 2^16 = 65536]]

Un mismo problema permite comparar el esfuerzo del programador: sumar 511+1 requiere varias operaciones de byte cuando los registros naturales son de ocho bits, mientras una suma de palabra puede expresarlo directamente en Aula-16. Eso no significa automáticamente que la segunda máquina sea más rápida, barata o de menor consumo. La velocidad y el coste requieren decisiones físicas y medidas, no solo el número de bits del nombre.

[[FIG:c24_fig03_dos_arquitecturas_un_metodo|Figura 3. Aula-8 y Aula-16 conservan los algoritmos de estudio, pero no comparten código máquina.|Dos arquitecturas con datos naturales distintos convergen en una misma secuencia de problemas verificables.]]

## 6. Lo que una prueba demuestra de verdad

Un verificador escrito en Python puede recorrer todas las combinaciones de una tabla de verdad, calcular valores esperados o comprobar bytes exactos de una imagen. Un comprobador de formato puede confirmar que el PDF contiene ejercicios y que las figuras tienen texto alternativo. Son pruebas útiles, pero pertenecen a **capas específicas**. No prueban que una señal de reloj alcance a cada flip-flop ni que una EEPROM sea programable con la fuente escogida.

| Evidencia | Conclusión permitida | Conclusión prohibida |
| --- | --- | --- |
| Modelo matemático | Salida esperada calculada | CPU física validada |
| Diagrama SVG generado | Convención y etiquetas reproducibles | PCB fabricable |
| Ensamblador educativo | Bytes emitidos por herramienta anfitriona | Binario ejecutado en Aula |
| Simulador futuro | Semántica implementada del modelo | Comportamiento eléctrico |
| Prototipo medido futuro | Comportamiento bajo condiciones ensayadas | Funcionamiento universal sin límites |

[[EQ:Prueba de ejemplo: 511 + 1 + 2 = 514]]

La figura siguiente dispone las etapas en un orden de trabajo. Antes de soldar o comprar componentes se deben congelar contratos coherentes, demostrar las operaciones en un modelo, ensamblar programas que correspondan exactamente a la ISA y comprobar trazas del ciclo de instrucción. Después se fabrican módulos y se miden tensiones, tiempos y márgenes térmicos. Se pueden visitar etapas en paralelo, pero ninguna evidencia debe declararse equivalente a otra.

[[FIG:c24_fig04_escalera_verificacion|Figura 4. El paso desde un modelo a un prototipo añade validaciones distintas.|Semántica, herramientas, simulación de CPU y prototipo medido en una secuencia de evidencia creciente.]]

## 7. Un arranque que aún tiene que hacerse realidad

Cuando diseñamos el arranque propusimos que la CPU pudiera empezar a leer instrucciones desde ROM y que un monitor ofreciera comandos. Pero **el vector de RESET, la codificación final, el contenido de firmware y los tiempos eléctricos deben concordar en un sistema ejecutable**. Una tabla de servicios como `FW_PUTC` describe una interfaz pública candidata, no demuestra que el byte llegue a un monitor.

La pantalla Aula V1 comienza lógicamente en modo **texto**, con controlador listo y sin error. Sus bancos de memoria conservan contenido indeterminado tras RESET: la rutina de arranque debe inicializar el texto antes de anunciar que la consola está lista. Cambiar al modo de gráficos mediante `C020=01` selecciona el framebuffer; regresar con `C020=00` devuelve la vista de caracteres sin destruir el buffer anterior. Esto **no añade** una instrucción especial del CPU ni reserva automáticamente una rutina pública de ROM para dibujar.

[[EQ:Video texto = 512 B; video bitmap = 8192 B]]

[[EQ:Memoria interna de video = 512 + 8192 = 8704 B]]

El lector puede imaginar un futuro prototipo con una pantalla física, un microcontrolador auxiliar o un generador de señales dedicado. Son **posibilidades de ingeniería**, no elecciones tomadas por el contrato V1. Para decidirlas harían falta pinout, sincronización, interfaz, consumo, memoria, ancho de banda, precio y pruebas. Una elección didáctica de cuatro colores no especifica por sí sola un puerto VGA ni obliga a construir una GPU.

## 8. La hoja de ruta que sigue después del manuscrito

El manuscrito puede cerrarse sin disfrazar las tareas restantes. Para transformar Aula en una herramienta técnica ejecutable queda por diseñar o implementar: una ISA estable y su ensamblador, microarquitectura de CPU, modelos de RAM/ROM/E/S que pasen pruebas, firmware de arranque y consola, mapa completo de glifos, interfaz virtual del taller y, si más adelante se desea, montaje físico. El texto de ocho bits tiene un ejemplo exacto de A; **no tenemos aún los 256 glifos completos**. Los protocolos de teclado y los detalles de cursor, retorno de carro y desplazamiento de líneas también necesitan contratos precisos.

| Prioridad | Entregable verificable | Criterio de aceptación |
| --- | --- | --- |
| 1 | ISA + ensamblador Aula-8 | Programa, bytes y traza coinciden |
| 2 | CPU virtual lógica | Tests de LD/ST/ADD/CALL/RET |
| 3 | ROM monitor + consola | Arranque y eco observables |
| 4 | Vídeo V1 | Matrices, colores y registros exactos |
| 5 | Aula-16 y herramientas | Bancos, alineación y pruebas |
| 6 | Prototipo opcional | Mediciones con instrumentos |

No todo es tarea del mismo día ni del mismo proyecto. El libro, el simulador de aprendizaje y el hardware físico **tienen criterios de cierre distintos**. La publicación final todavía necesitará una edición maestra consolidada: índice, referencias, normalización de figuras, revisión de términos y una lectura completa que detecte contradicciones entre capítulos.

## 9. Cerrar el círculo

Al encender una computadora real, normalmente solo vemos un cursor o una pantalla. Tras ese gesto hay miles de decisiones: qué significa un cero, cómo se retiene, cuándo avanza un registro, por dónde viaja una dirección, cómo se calcula un resultado y cómo un dispositivo convierte bits en una imagen. Ninguno de esos pasos requiere magia; sí requiere **precisión y paciencia**.

La buena noticia es que incluso una computadora pequeña puede enseñarnos lo esencial. Ya sabemos formular preguntas suficientemente precisas para comprobar una ALU, una memoria y un mapa de píxeles. Sabemos qué hace falta aprender para que una subrutina de ROM sea real. Sabemos que **explicar un circuito no equivale a fabricarlo**, pero también que diseñarlo con pruebas nos acerca de manera legítima a construirlo.

Esta es la promesa cumplida del recorrido editorial: no una máquina imaginaria proclamada terminada, sino una computadora que **podemos explicar** desde sus fundamentos y un camino verificable para convertir esa explicación en algo que funcione.

[[PAGEBREAK]]
## Nuestra computadora, vista desde el primer bit

Si volvemos al comienzo, el camino ya no es una lista de tecnologías. La corriente permite una señal eléctrica; las compuertas representan decisiones; la realimentación conserva un bit; ocho elementos de memoria forman un registro; los buses llevan direcciones y datos; la RAM almacena programas; la ALU transforma valores; la unidad de control ordena movimientos; y el PC recorre bytes concretos de instrucciones, saltando cuando el programa lo indica. Aula-16 muestra después qué cambia al ampliar la palabra sin abandonar las direcciones de byte.

La pregunta final para el lector no es «¿cuántos esquemas he memorizado?», sino: **si el PC, los registros y la memoria muestran ciertos valores, ¿podría seguir el siguiente movimiento y explicar por qué ocurre?** Si puede hacerlo, los capítulos han construido un modelo comprensible de computadora. Si no, conviene regresar al circuito o transferencia que todavía no resulta clara. Esto **no** certifica una CPU física: el siguiente trabajo de ingeniería será convertir esas relaciones en una netlist, ejecutar pruebas digitales independientes, definir temporización y verificar los componentes elegidos.

## Ejercicios del capítulo 24

**Ejercicio 1 — Direcciones.** ¿Cuántos bytes distintos puede identificar un bus de 16 bits de direcciones cuando cada dirección nombra un byte?

**Ejercicio 2 — RAM.** ¿Cuántos bytes comprende el intervalo `0000–7FFF`, ambos extremos incluidos?

**Ejercicio 3 — ROM.** ¿Cuántos bytes ocupa `E000–FFFF`?

**Ejercicio 4 — Palabra.** Si en `2200` y `2201` hay `34 12`, ¿qué palabra little-endian se lee?

**Ejercicio 5 — Alineación.** ¿Se permite una lectura de palabra iniciada en `2201` en Aula-16 V1?

**Ejercicio 6 — MMIO.** ¿Por qué la RAM de vídeo no ocupa el rango de RAM de CPU?

**Ejercicio 7 — Pantalla.** ¿Qué dirección CPU selecciona el modo y qué valor muestra bitmap?

**Ejercicio 8 — Estado de RESET.** ¿Es correcto afirmar que la pantalla está necesariamente en blanco apenas se produce RESET?

**Ejercicio 9 — Euclides.** Calcula el MCD de 48 y 18 por restas.

**Ejercicio 10 — Desbordamiento.** ¿Por qué `F25=75025` no cabe en `u16`? ¿Qué residuo deja una operación modular?

**Ejercicio 11 — Evidencia.** Un script de Python valida un mapa de caracteres. ¿Qué puede garantizar y qué no garantiza?

**Ejercicio 12 — Cierre.** Explica la diferencia entre un manuscrito completado, un simulador funcional y un prototipo electrónico certificado.

[[PAGEBREAK]]
## Solucionario del capítulo 24

**1.** `2^16 = 65536 direcciones = 64 KiB` de espacio direccionable.

**2.** `0x8000 = 32768 bytes = 32 KiB`.

**3.** `0x10000-0xE000 = 0x2000 = 8192 bytes`.

**4.** `0x1234`, porque `0x34` es el byte menos significativo.

**5.** No. Las lecturas de palabra requieren direcciones pares en el contrato lógico V1.

**6.** Es memoria **interna del periférico**. La CPU usa registros MMIO como `C024/C026/C028` para seleccionar y leer o escribir sus bytes.

**7.** `VIDEO_MODE` en `C020`, valor completo `01` para gráficos.

**8.** No. RESET fija registros y modo texto, pero el contenido de los buffers puede ser indeterminado. Hace falta inicializarlo explícitamente.

**9.** `(48,18)→(30,18)→(12,18)→(12,6)→(6,6)`; MCD `6`.

**10.** Supera `65535`. `75025 mod 65536 = 9489 = 0x2511`.

**11.** Garantiza propiedades del **modelo de referencia** y sus entradas de prueba; no prueba circuitos físicos, tiempos eléctricos ni firmware inexistente.

**12.** El manuscrito demuestra coherencia editorial y matemáticas; el simulador demostraría semántica ejecutada en software; el prototipo certificado requiere fabricación, pruebas instrumentales y límites de operación publicados.

## Epílogo

Desde un transistor hasta una palabra impresa en una pantalla, todas las etapas son preguntas que podemos convertir en experimentos. La última página no es la última prueba: es la invitación a construir, medir y seguir aprendiendo sin perder la costumbre de distinguir un resultado esperado de un resultado observado.
