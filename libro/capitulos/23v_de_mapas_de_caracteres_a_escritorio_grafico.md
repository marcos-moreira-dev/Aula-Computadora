# Capítulo 23B. De los mapas de caracteres al escritorio gráfico

*Parte VI · Un puente visual entre los capítulos 23 y 24 · Aula-Computadora*

Imagina que acabas de encender una computadora que has construido con tus propias manos. El procesador ya sabe sumar, recorrer direcciones y llamar a una rutina de ROM. Escribes `HOLA` y, por fin, cuatro letras aparecen frente a ti. Parece un gesto sencillo. Pero ¿en qué momento se convirtieron cuatro números de ocho bits en trazos que podemos reconocer con los ojos? Y si el aparato puede dibujar una `A`, ¿por qué no podría dibujar un árbol, un gráfico de barras o una ventana?

Responderemos recorriendo tres niveles que debemos mantener separados: **los datos almacenados**, **el dispositivo que los interpreta** y **la imagen percibida**. En nuestro caso ya existe un **contrato lógico** para una pantalla didáctica Aula: texto y gráficos alternativos. El recorrido parte del modelo de memoria y del controlador y llega hasta la imagen visible; el montaje físico de un controlador no forma parte de este capítulo.

## 1. Un carácter es un código, no un dibujo

Escribamos el valor hexadecimal `41` en una celda de memoria de texto. Según ASCII, el código `0x41` se interpreta como la letra mayúscula **A**. No significa que los ocho bits `01000001` contengan la silueta de esa letra: son una **identidad convencional**. La pantalla necesita buscar un dibujo —un *glifo*— asociado a ese código. La colección coherente de glifos y sus medidas es una fuente tipográfica.

| Concepto | Qué responde | Ejemplo |
| --- | --- | --- |
| Carácter | ¿Qué símbolo o elemento textual se desea? | Letra A |
| Codificación | ¿Con qué valor lo representamos? | ASCII 0x41 |
| Glifo | ¿Qué forma concreta se dibuja? | A con trazos de ocho filas |
| Fuente | ¿Qué repertorio de dibujos y métricas usamos? | Diseño monoespaciado de 8×8 |

Un teclado puede producir el carácter A, un programa puede guardarlo como código y el controlador de texto puede localizar su glifo. Los tres pasos son distintos. En una terminal externa clásica, la computadora podía enviar el código por una conexión y **la propia terminal** decidía qué píxeles iluminar. En nuestro dispositivo didáctico, el controlador virtual consulta directamente su ROM de glifos. Ninguna de esas posibilidades contradice la otra: son **arquitecturas diferentes** para resolver la misma necesidad.

## 2. Dibujar una letra con ocho bytes

Para poder comprobar algo con absoluta fidelidad diseñamos nuestra propia A de **8 columnas × 8 filas**. Cada fila es un byte: bit 7 a la izquierda y bit 0 a la derecha. Uno significa tinta; cero significa fondo. Estas son las ocho filas, de arriba abajo: `18 24 42 7E 42 42 42 00`. El valor hexadecimal `18`, por ejemplo, equivale a `00011000` y coloca dos puntos en las columnas 3 y 4 si contamos desde cero.

[[EQ:Fila 0 = 0x18 = 00011000 en binario]]

[[EQ:Índice del byte de glifo = código × 8 + fila]]

La figura siguiente se ha construido desde esos ocho bytes exactos. Puedes comprobarla fila por fila: en la cuarta fila, `7E = 01111110`, se dibuja el trazo horizontal de la A; en la última fila, `00`, no hay tinta.

[[FIG:p23v_fig01_codigo_glifo|Figura 1. El código 41 hexadecimal selecciona una A formada por ocho filas binarias.|Cadena de código 0x41, ROM de glifos y A de 8 por 8; las ocho filas corresponden a 18 24 42 7E 42 42 42 00.]]

Esta forma de representar letras se llama **fuente de mapa de bits**. Hay fuentes históricas de 5×7, 6×8, 8×8 y muchos otros tamaños; **8×8 no es un estándar universal**. En Aula escogimos 8×8 para que cada fila se almacene en un byte sin empaquetados adicionales. La ROM propuesta tiene 256 posiciones de glifo y ocho bytes por posición; su capacidad es de 2048 bytes, es decir, 2 KiB. La ROM de caracteres **no es la ROM de firmware**: una entrega dibujos; la otra contiene programas o subrutinas.

[[EQ:ROM de glifos = 256 × 8 bytes = 2048 bytes]]

## 3. De una letra a una pantalla de texto

Ahora coloquemos una retícula de **32 columnas por 16 filas**. Cada celda guarda **un byte de código**. La dirección interna del carácter situado en columna `c` y fila `f` se obtiene contando 32 celdas por cada fila anterior. Si ponemos `H`, `O`, `L`, `A` en las cuatro primeras posiciones, los códigos ASCII son `48 4F 4C 41` hexadecimales. La ROM transforma cada código en su matriz 8×8 cuando se presenta la imagen.

[[EQ:offset_texto = fila × 32 + columna]]

[[EQ:32 × 16 × 1 byte = 512 bytes de texto]]

En la figura se ven las **512 celdas**, no los miles de píxeles individuales. Esa diferencia explica por qué un texto puede ocupar mucho menos espacio que una fotografía: el controlador reutiliza un mismo dibujo de letra dondequiera que aparezca su código.

[[FIG:p23v_fig02_mapa_texto_32x16|Figura 2. HOLA ocupa las cuatro primeras celdas de un mapa de texto de 32 por 16.|Retícula real de 512 celdas, fila cero y columnas cero a tres identificadas como H O L A, sin presentar esas celdas como píxeles de la pantalla.]]

Si cada glifo tiene 8×8 puntos, la imagen completa de esa retícula equivale a **256×128 posiciones visibles**. Eso no convierte la RAM de texto en un framebuffer: un mapa de 512 códigos utiliza repetidamente la ROM de glifos para producir visualmente hasta 32768 puntos. Incluso pueden mostrarse cuadrados, líneas y bloques usando caracteres especiales. Este recurso se llama **semigráfico**: una apariencia de dibujo conseguida con celdas de texto. Los colores de primer plano y fondo también pueden ser globales o por celda según el diseño; **Aula V1 fija dos colores globales para el texto**, no atributos individuales por celda.

¿Y las tildes? ASCII original de siete bits no contiene `á`, `ñ` ni `¿`. Para Aula se reservaron códigos extendidos de un byte, pero **todavía no se ha aprobado una tabla completa ni dibujado su ROM**. Unicode y UTF-8 son tecnologías útiles para un computador anfitrión moderno; integrarlas directamente en un periférico didáctico de 512 celdas requeriría decodificación y reglas adicionales. Un conversor del programa anfitrión podrá traducir caracteres soportados a los códigos Aula y rechazar los demás de forma explícita.

## 4. Cuando un píxel necesita su propia información

Supongamos ahora que queremos dibujar una diagonal que atraviese una letra, o un círculo sin depender de caracteres especiales. En modo gráfico, cada posición `(x,y)` participa en un mapa de bits. Para una pantalla **hipotética** de 256×128 a **un bit por píxel**, cada byte guarda ocho píxeles. La coordenada `(7,0)` cae en el primer byte, bit 0; `(8,0)` comienza el segundo byte, bit 7. El último punto `(255,127)` corresponde al byte 4095, bit 0.

[[EQ:offset_1bpp = y × 32 + piso(x/8)]]

[[EQ:bit_1bpp = 7 - (x mod 8)]]

Pero **1 bpp solo aparece aquí como comparación conceptual**. El dispositivo lógico Aula V1 usa de verdad **2 bits por píxel**, cuatro valores posibles (`00`, `01`, `10`, `11`) y, por tanto, **cuatro píxeles por byte**. Cada fila tiene 64 bytes. La coordenada `(8,0)` va al byte 2 y ocupa los bits 7–6. Si se escribe el color índice 2 (`10` binario) sobre un byte inicialmente cero, queda `0x80`.

[[EQ:offset_2bpp = y × 64 + piso(x/4)]]

[[EQ:desplazamiento_2bpp = 6 - 2 × (x mod 4)]]

La figura separa cuidadosamente los dos convenios para que no confundamos la demostración monocroma con un tercer modo implementado. Es fácil probar el extremo inferior derecho: `(255,127)` ocupa el último byte 8191, bits 1–0.

[[FIG:p23v_fig03_pixeles_y_offsets|Figura 3. Las coordenadas se convierten en offsets distintos en 1 bpp y 2 bpp.|Comparación exacta de 4096 bytes monocromos hipotéticos y 8192 bytes reales del contrato lógico de vídeo de cuatro colores.]]

## 5. ¿Quién dibuja: la CPU, la ROM o un controlador?

Una tentación natural es inventar instrucciones de CPU llamadas `DRAW`, `PIXEL` o `CIRCLE`. No son necesarias para explicar este sistema. El procesador puede realizar **cargas, almacenamientos, desplazamientos, máscaras y sumas ordinarias**. Una función de software `PLOT(x,y,color)` calcula el offset, modifica dos bits del byte correspondiente y vuelve. Una subrutina así podría vivir en RAM o en una ROM de firmware, pero **su presencia no está garantizada**: hace falta escribirla, codificarla y comprobar que cabe en memoria.

El dispositivo de presentación tiene otra tarea: interpretar el banco de vídeo y producir la imagen visible. La **ROM de caracteres** aporta la forma de las letras. Una eventual **micro-ROM de control** de la CPU almacenaría microinstrucciones de su unidad de control, no las formas de las letras ni el contenido del firmware. Son memorias con funciones diferentes.

[[FIG:p23v_fig04_rom_controlador|Figura 4. La ROM del programa, la ROM de glifos y el controlador realizan tareas distintas.|La CPU opera con datos e instrucciones, el firmware puede contener rutinas, la ROM de caracteres conserva dibujos y el controlador presenta texto o bitmap.]]

El modelo de Aula sitúa sus periféricos en direcciones de memoria de CPU llamadas **MMIO** (*memory-mapped input/output*). El controlador de vídeo ocupa `0xC020–0xC02F` con seis registros activos en direcciones pares. La RAM de texto de 512 bytes y la RAM de gráficos de 8192 bytes son **internas al controlador**: no ocupan el intervalo de RAM de la CPU `0000–7FFF`.

| Registro CPU | Nombre | Función |
| --- | --- | --- |
| C020 | VIDEO_MODE | 00 texto, 01 gráficos |
| C022 | VIDEO_STATUS | READY y ERROR persistente |
| C024/C026 | VRAM_ADDR_LO/HI | Offset interno de vídeo, bajo/alto |
| C028 | VRAM_DATA | Byte en el plano de acceso seleccionado |
| C02A | VIDEO_CTRL | Plano, autoincremento, colores de texto |

En Aula V1 **una sola pantalla alterna el modo visible**. El texto y el bitmap se conservan por separado. Pasar a gráficos no borra el texto; volver a texto no borra el bitmap. La CPU podría seguir enviando caracteres al buffer de texto mientras los gráficos se ven. **No hay superposición de las dos imágenes.** En RESET se selecciona texto y se inicializan registros; las memorias de vídeo no se suponen limpias y el firmware deberá borrarlas explícitamente.

## 6. Tres significados distintos de «dirección»

Aquí recuperamos los *addressing modes* del capítulo 23. Una **instrucción inmediata** obtiene un valor incluido en su código; una **absoluta** nombra una dirección CPU; una **indexada** calcula una dirección efectiva con un registro y desplazamiento. Esos nombres describen la **ISA y la unidad de control**, no el procedimiento para buscar un píxel. Cuando la dirección efectiva CPU es `C020`, el **decodificador MMIO** selecciona el registro de modo de vídeo. Dentro del controlador, un **puntero VRAM** como `0002` señala un byte del bitmap: es otro espacio, independiente del mapa CPU.

Para imaginar un píxel ámbar en `(8,0)`, suponiendo que el byte gráfico 2 vale cero: escribe `01` en `C020` para mostrar gráficos; `0E` en `C02A` para seleccionar el plano gráfico sin autoincremento, conservando letras blancas y fondo negro; `02` en `C024`; `00` en `C026`; finalmente `80` en `C028`. La notación «escribe» describe **transacciones de E/S esperadas**, no opcodes binarios ya diseñados.

[[EQ:VIDEO_CTRL 0x0E = 00001110 en binario]]

[[EQ:Valor del byte = 2 × 64 = 128]]

[[FIG:p23v_fig05_tres_direcciones|Figura 5. El procesador accede a registros MMIO y estos resuelven un offset de VRAM.|La dirección C020 es una dirección CPU; C024, C026 y C028 seleccionan una memoria interna; la ISA de Aula-16 aún es candidata.]]

La distinción es importante incluso en Aula-16. Su bus externo de datos tiene dieciséis bits, pero estos **registros de vídeo tienen ocho bits** y están situados en direcciones pares. Se requiere una operación de byte y selección correcta de carril; no podemos tratarlos como registros de 16 bits ni dar por construida la electrónica de ese bus. Las direcciones impares del intervalo no son alias de las pares.

## 7. El precio del color

Para una imagen empaquetada de 256×128 sin rellenos de fila ni cabeceras, cada píxel necesita `bpp` bits. Si `bpp=1`, solo caben dos valores posibles: 0 y 1. Con `bpp=2`, caben cuatro índices; con 4 bits, 16; con 8 bits, 256. Esos índices pueden seleccionar colores de una **paleta**: el valor no tiene por qué contener los componentes rojo, verde y azul.

[[EQ:Bytes = techo(ancho × alto × bpp / 8)]]

| Profundidad | Valores posibles | Bytes para 256×128 | ¿Forma parte de Aula V1? |
| --- | ---: | ---: | --- |
| 1 bpp | 2 | 4096 | No, comparación |
| **2 bpp** | **4** | **8192** | **Sí** |
| 4 bpp | 16 | 16384 | No |
| 8 bpp | 256 | 32768 | No |

La paleta lógica fijada para Aula es `0 negro`, `1 verde`, `2 ámbar`, `3 blanco`. Esto no especifica los valores RGB físicos, el tipo de panel, una tarjeta gráfica ni un conector VGA. En la figura siguiente aparecen cuatro versiones de un mismo patrón como **ilustración de profundidades**, y se indica el tamaño real de almacenamiento. El patrón solo necesita cuatro colores o menos, aunque los paneles de 4/8 bpp admitirían más. No debemos confundir esta comparación de representaciones con cuatro modos disponibles en nuestro ordenador.

[[FIG:p23v_fig06_profundidad_color|Figura 6. Duplicar los bits por píxel aumenta la memoria necesaria.|Cuatro paneles didácticos de 1, 2, 4 y 8 bits por píxel y tamaños 4096, 8192, 16384 y 32768 bytes.]]

Una fuente de mapa de bits también puede dibujarse sobre un framebuffer de colores; eso no cambia la identidad del carácter. Lo que cambia es **cómo se construye cada píxel final**. Por eso, aunque texto y gráficos sean mutuamente excluyentes en el contrato Aula V1, en el mundo de la computación sí existen interfaces que combinan texto dibujado y gráficos en un mismo lienzo. No estamos obligados a implementar aquí esa mezcla.

## 8. Cuando las letras dejan de ser cuadrículas fijas

En el texto de 8×8 todas las letras ocupan el mismo ancho de celda. Esa familia se denomina **monoespaciada**. En fuentes proporcionales, una `i` puede ocupar menos que una `W`; esto requiere **métricas** y un sistema de colocación de glifos. Una tipografía moderna además puede representar sus contornos como curvas, incluidas las **curvas de Bézier**, que se escalan y luego se convierten en puntos del dispositivo mediante *rasterización*.

[[EQ:B(t) = (1-t)² P0 + 2(1-t)t P1 + t² P2; 0≤t≤1]]

La fórmula anterior describe una curva Bézier cuadrática en términos de tres puntos de control, no una instrucción de CPU. Para dibujarla en pantalla, el software o hardware de representación calcula qué cobertura corresponde a cada píxel. El **antialiasing** suaviza bordes usando coberturas o intensidades intermedias. Nuestro ejemplo gráfico enseña una A de píxeles, un contorno vectorial de diseño propio y su apariencia rasterizada. No reproduce una fuente comercial.

[[FIG:p23v_fig07_tipografia_y_contornos|Figura 7. Una letra puede almacenarse como filas de bits o describirse con contornos geométricos.|Matriz A original 8×8 comparada con un contorno A original y una representación de líneas convertidas en imagen.]]

Este puente permite comprender, en pequeño, el camino hacia un escritorio de ventanas. Una aplicación escribe texto o superficies; un sistema de ventanas ordena y combina las superficies; un dispositivo presenta el resultado. **Windows XP y Windows 7 no emplean exactamente la misma arquitectura de composición**: el Administrador de ventanas de escritorio se introdujo con Vista y la composición de Aero en Windows 7 dependía de sus condiciones de activación. Para este libro importa la continuidad **conceptual** entre caracteres, bitmaps y superficies, no reproducir el subsistema gráfico de cada versión de Windows.

## 9. Lo que significa «activar gráficos» hoy

En un microcontrolador moderno, una pantalla puede tener su propia memoria interna y recibir comandos por una interfaz serial; en un computador de escritorio el sistema operativo y sus controladores suelen presentar interfaces de dibujo de mucho más nivel. Son ejemplos de tecnologías y compromisos distintos. No hay un único «modo VGA» universal que debamos emular en Aula, ni una instrucción de procesador que por sí sola convierta una terminal en un escritorio gráfico.

El punto de cierre es más simple y más potente: **los píxeles son datos representados según un convenio**. La computadora los calcula; un controlador los interpreta. Se puede escribir y probar el convenio aunque el aparato físico todavía no exista. Y con esa comprensión podemos regresar al último capítulo para preguntar, sin magia ni nostalgia mal interpretada, qué significa haber diseñado realmente una computadora.

[[PAGEBREAK]]
## Construimos Aula-8 y Aula-16: del byte a una pantalla compartida

El controlador lógico V1 amplía la misma idea que usamos con el terminal: el programa escribe **registros mapeados** y un dispositivo interpreta los bytes. No añadimos una tarjeta gráfica comercial ni suponemos que la CPU lea directamente cada píxel de VRAM. Los registros en direcciones pares `0xC020–0xC02A` permiten seleccionar un modo y acceder indirectamente a bancos de memoria de vídeo separados del mapa principal.

La pantalla física o virtual es **una sola**: en modo texto utiliza 32×16 caracteres y la ROM de glifos de 2 KiB; en modo gráfico, una matriz de 256×128 píxeles con dos bits por píxel y cuatro colores. Los bancos conservan sus contenidos al cambiar de modo, pero el controlador muestra **uno u otro**, no ambos simultáneamente. El puente con los primeros capítulos es tangible: un bit ya podía conservar un estado; ahora muchos bits coordinados forman caracteres, colores y finalmente una imagen.

## Ejercicios del capítulo 23B

**Ejercicio 1 — Código y forma.** ¿Por qué el byte ASCII `41` hexadecimal no reproduce por sí solo una letra A?

**Ejercicio 2 — Fila binaria.** Escribe como ocho bits `0x7E` e indica cuántos puntos tienen tinta.

**Ejercicio 3 — Glifos.** ¿Qué offset de la ROM de glifos selecciona la fila 3 del código `0x41`?

**Ejercicio 4 — Texto.** ¿Cuántos bytes ocupa un mapa de 32×16 si se almacena un código por celda?

**Ejercicio 5 — Coordenadas de texto.** ¿Cuál es el offset de fila 3, columna 5, contando ambas desde cero?

**Ejercicio 6 — Tildes.** ¿Por qué ASCII original y Unicode no obligan a añadir UTF-8 al controlador Aula V1?

**Ejercicio 7 — Monocromo hipotético.** ¿En qué byte y bit queda el punto `(8,0)` a 1 bpp, MSB primero?

**Ejercicio 8 — Mapa V1.** ¿En qué byte y bits queda el punto `(255,127)` a 2 bpp?

**Ejercicio 9 — Color.** Un byte gráfico inicialmente a cero debe poner color índice 2 en `(8,0)`. ¿Qué valor toma el byte 2?

**Ejercicio 10 — Acceso MMIO.** Explica qué diferencia hay entre la dirección CPU `C028` y el offset VRAM `0002`.

**Ejercicio 11 — Capacidad.** Calcula la memoria de la misma imagen 256×128 a 1, 2, 4 y 8 bpp empaquetados.

**Ejercicio 12 — Tipografía.** ¿Qué cambia entre una fuente de mapa de bits 8×8 y un contorno Bézier escalable? ¿Hace falta un opcode de CPU nuevo?

[[PAGEBREAK]]
## Solucionario del capítulo 23B

**1.** El byte representa el **código** del carácter; el dibujo procede del glifo definido por la fuente.

**2.** `01111110`; hay seis bits con valor uno.

**3.** `0x41×8+3 = 65×8+3 = 523` decimal (`0x020B`), si cada glifo ocupa ocho bytes y las filas empiezan en cero.

**4.** `32×16 = 512 bytes`.

**5.** `3×32+5 = 101`, o `0x65`.

**6.** ASCII original no contiene tildes; el diseño Aula usa códigos locales de ocho bits aún por completar. La conversión desde Unicode puede realizarse fuera del dispositivo.

**7.** Segundo byte: offset `1`, bit `7`.

**8.** Offset `127×64+255//4 = 8191`, bits `1–0`.

**9.** `0x80` porque `10` se coloca en bits 7 y 6 de un byte inicialmente nulo.

**10.** `C028` selecciona un registro del periférico en el espacio de CPU; `0002` es la dirección local dentro del banco de vídeo seleccionado.

**11.** `4096`, `8192`, `16384` y `32768` bytes; solo el caso de 2 bpp pertenece a Aula V1.

**12.** En 8×8 hay puntos discretos de tamaño fijo; el contorno expresa geometría escalable que se rasteriza a cada resolución. La CPU puede realizar cálculos y escrituras habituales; no exige un opcode gráfico.

## Para continuar

Ya podemos contar una historia coherente desde un byte en RAM hasta una letra o un punto de color. El último capítulo retomará las dos familias Aula, el mapa de memoria, los programas y el método experimental. No proclamará que poseemos un prototipo físico: mostrará qué sabemos, qué hemos comprobado y qué queda pendiente.
