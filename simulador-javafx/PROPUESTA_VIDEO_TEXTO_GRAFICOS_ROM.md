# Propuesta de vídeo educativo: texto, píxeles, ROM y firmware

**Estado histórico:** **SUPERADO por el [contrato lógico V1 congelado](CONTRATO_VIDEO_AULA_V1.md)** el 8 de noviembre de 2026 tras delegación explícita de Marcos. Este archivo conserva el **debate previo**, incluidas recomendaciones de monocromo/VRAM compartida que **no son la decisión vigente**. Prevalece el contrato nuevo: **2 bpp, cuatro colores, 8192 B de bitmap más 512 B de texto**, seis registros MMIO `C020–C02F`. **No existe hardware ni firmware implementados.**

**Propósito:** conservar la propuesta de Marcos sobre un *text mode* con ROM de caracteres y estudiar si el mismo Aula-8 podría ofrecer un *graphics mode* sencillo **sin tarjeta gráfica, GPU, VGA ni nuevas instrucciones gráficas de CPU**. La obra escrita tratará ambos conceptos; que el taller virtual los implemente permanece pendiente.

## 1. No confundir tres memorias de solo lectura

| Elemento | Qué contiene | Quién lo consulta | Situación Aula |
| --- | --- | --- | --- |
| **Micro-ROM de control (µROM)** | Microinstrucciones para coordinar ALU, registros y buses; no son subrutinas del usuario. | Secuenciador interno de la CPU. | Microarquitectura candidata; tamaño y contenido binario pendientes. |
| **ROM de firmware (8 KiB, E000–FFFF)** | Arranque, monitor y posibles **subrutinas software** de ayuda. | CPU por instrucciones normales, mediante `CALL`/`RET`. | Mapa conceptual existente; 32 ranuras públicas candidatas, **solo cuatro asignadas**: `FW_PUTC`, `FW_GETC`, `FW_PUTS`, `FW_STATUS`. |
| **ROM de caracteres o generador de glifos** | Patrón de bits de cada fila de una letra o símbolo. | Controlador de vídeo/texto que transforma códigos de carácter en puntos visibles. | **Propuesta nueva**, no presente en el diseño base ni necesariamente direccionable por la CPU. |

La intuición de Marcos sobre subrutinas en ROM es correcta **para el firmware**: una función hipotética `PLOT(x,y)` podría calcular dónde está un píxel y escribirlo. Sin embargo, el código de esa función **no enciende el píxel por sí mismo**: necesita un dispositivo de salida que lea memoria de vídeo y produzca la imagen. La ROM de glifos no sustituye ese dispositivo y tampoco equivale a la ROM de firmware.

**Dos situaciones distintas:**

1. **Terminal externo ya previsto:** Aula-8 envía códigos de caracteres por `DATA=C000` y consulta `STATUS=C002`. La terminal anfitriona o periférica genera la imagen y puede usar su **propia** fuente, ROM, RAM o software. Aula-8 no controla una matriz de píxeles ni necesita almacenar fuentes.
2. **Módulo de vídeo integrado, opcional:** un controlador recibe direcciones, códigos, atributos o píxeles; tiene memoria de vídeo y consulta una ROM de caracteres en modo texto. En modo mapa de bits consulta directamente píxeles de vídeo. Se plantea como **periférico aparte**, no una tarjeta GPU.

No debemos llamar *text mode* de vídeo direccionable a una mera terminal de caracteres sin aclarar esa distinción.

## 2. Mismo procesador, salida distinta

La CPU **no precisa** una instrucción `DRAW`, `PIXEL` ni `GRAPHICS`. Sus operaciones ordinarias —cargar, almacenar, operaciones de bits, suma, desplazamientos y saltos— bastan para hablar con un dispositivo conectado a sus buses. La dificultad pasa al **controlador de vídeo**, que selecciona el modo de salida, mantiene el barrido o actualización, obtiene bits de la memoria de vídeo y los presenta al dispositivo físico.

- En hardware real, el controlador requiere señales y temporización compatibles con una pantalla **todavía sin seleccionar**; no está construido ni validado.
- En el futuro taller virtual, un renderizador del anfitrión podría **modelar** el periférico sin prometer que existe un circuito físico equivalente.
- La interfaz propuesta es acceso **indirecto por registros mapeados**: `MODE`, `VRAM_ADDR_LO`, `VRAM_ADDR_HI`, `VRAM_DATA`, quizá `STATUS`. Son nombres **ilustrativos**; **no asignarles direcciones** hasta aprobar mapa y protocolo. No invadir `C000/C002` ni `C010–C01F`.
- La RAM de vídeo propuesta pertenece al controlador y **no consume** la RAM central `0000–7FFF` si se consulta mediante esos registros. Si se optara por una VRAM mapeada directamente, habría que revisar la distribución de 64 KiB: **no está autorizado**.
- `FW_SETMODE`, `FW_PLOT`, `FW_CLS` o `FW_TEXT` serían subrutinas **opcionales** en ROM de firmware o software cargado en RAM; no se reservan ranuras públicas ni se declara que caben en 8 KiB. También es posible operar directamente con registros mapeados.

## 3. Resolución didáctica de referencia, aún no elegida

Para poder comparar magnitudes sin inventar una pantalla concreta se usa el **ejemplo hipotético** de 32 columnas × 16 filas de caracteres, cada glifo de 8 × 8 píxeles:

- Resolución gráfica: `32 × 8 = 256` píxeles por fila; `16 × 8 = 128` filas, **256 × 128**.
- Buffer de texto si cada celda almacena **un código de 8 bits**: `32 × 16 = 512 B`.
- ROM de caracteres de **256 glifos** por **8 filas**, un byte por fila: `256 × 8 = 2048 B = 2 KiB`. Con 128 glifos serían 1024 B. **No existe un estándar universal de 5×5 u 8×8**: cada máquina o fuente define sus dimensiones y repertorio.
- Modo de texto con atributos independientes de un byte por celda (colores/estilo): `512 + 512 = 1024 B` de buffer; es otro diseño opcional, no adquirido.

El patrón de una `A` en una ROM de glifos se guarda fila a fila como ocho grupos de ocho bits. Un bit `1` puede representar tinta encendida y un `0` fondo; el significado visual se fija por el controlador y su paleta.

## 4. Debate verificable: monocromo o color

Se compara **la misma** imagen de 256 × 128 = 32 768 píxeles, sin contar cabeceras, paleta, doble buffer, alineación ni estructuras auxiliares.

| Formato | Valores por píxel | Memoria de mapa de bits | Ventaja | Coste didáctico |
| --- | ---: | ---: | --- | --- |
| **1 bit/píxel** | 2 (apagado/encendido) | **4096 B = 4 KiB** | Píxel, fila, máscara y bit visibles de inmediato. | Solo dos índices; luz/fondo pueden ser del color físico elegido, pero no cuatro colores independientes. |
| **2 bits/píxel** | 4 índices de paleta | **8192 B = 8 KiB** | Introduce color, paleta y píxeles empaquetados sin demasiada complejidad. | Doble memoria, lógica de dos bits y selección de colores. |
| **4 bits/píxel** | 16 índices de paleta | **16 384 B = 16 KiB** | Útil para explicar paletas históricas. | Más memoria y controles. |
| **8 bits/píxel** | 256 índices de paleta | **32 768 B = 32 KiB** | Puente a imágenes indexadas y sistemas posteriores. | Muy exigente para un periférico educativo sencillo. |

**Recomendación técnica, no decisión cerrada:** comenzar por **1 bit/píxel**, con dos colores lógicos (fondo y tinta), y **dejar 2 bits/píxel / cuatro colores como ampliación posterior** si Marcos lo aprueba. Esto respeta el valor de estudiar cada bit, la ROM de glifos y las máscaras. Las tablas de colores y el concepto de RGB **sí** pueden explicarse en el libro incluso sin implementarlos en el taller.

La VRAM propuesta sería de **4 KiB independientes**, **reutilizables entre modos** (512 B efectivos de texto o 4096 B del mapa de bits); no hacen falta 4 KiB + 512 B simultáneos si los modos se excluyen. La futura opción de 2 bits/píxel requeriría **8 KiB de VRAM**, capacidad distinta y pendiente. La ROM de glifos de 2 KiB va **aparte**.

### Ejemplo matemático de un píxel en blanco y negro

Para `0 ≤ x < 256` y `0 ≤ y < 128`, con filas consecutivas y orden de bit más significativo primero:

```text
ancho_fila_bytes = 256 / 8 = 32
indice = y * 32 + floor(x / 8)
mascara = 0x80 >> (x mod 8)
pixel = (VRAM[indice] & mascara) != 0
```

Para encenderlo: `VRAM[indice] = VRAM[indice] | mascara`; para borrarlo: `VRAM[indice] = VRAM[indice] & ~mascara`, limitando el resultado a un byte. Así, `(x=0,y=0)` usa el bit 7 del byte 0; `(7,0)` el bit 0 del byte 0; `(8,0)` el bit 7 del byte 1; `(255,127)` el bit 0 del byte **4095**. **Son índices de la VRAM interna hipotética**, no direcciones CPU.

En **2 bpp** el byte contiene cuatro píxeles; para una fila de 64 B: `indice = y*64 + floor(x/4)` y `desplazamiento = 6 - 2*(x mod 4)`. La máscara de campo es `0b11 << desplazamiento`. El índice del color no equivale todavía a la tensión RGB física: hace falta definir una paleta y un método de salida.

### Ejemplo matemático del texto

Si un código `c` ocupa la celda `(col, fila)` y cada glifo es 8×8, `buffer_texto[fila*32+col] = c`. Para el píxel local `(u,v)` del glifo, `0 ≤ u,v < 8`:

```text
fila_glifo = ROM_GLIFOS[c * 8 + v]
encendido = (fila_glifo & (0x80 >> u)) != 0
```

El controlador puede aplicar el mismo glifo a muchas posiciones; el buffer de texto **no guarda 64 bits por cada carácter**, solo su código. Las fuentes modernas pueden ser **proporcionales, vectoriales y suavizadas**: por eso esta ROM representa únicamente el caso didáctico de fuentes de mapa de bits.

## 5. Qué queda en piedra y qué no

### Confirmado como intención pedagógica

- El libro explicará el paso de caracteres a píxeles y la noción de fuente; comparará texto, mapas de bits y evoluciones posteriores.
- El proyecto principal sigue centrado en CPU, memoria y software; ni tarjeta gráfica compleja, ni VGA, ni Windows real, ni GPU son requisitos de Aula-8 o del primer taller.
- No modificar ahora ISA, micro-ROM, ROM pública, mapa de memoria ni el contrato de la terminal vigente.

### Propuesta sujeta a aprobación

1. ¿Agregar a la **herramienta didáctica** un módulo de vídeo integrado además de la terminal ya acordada, o mostrarlo únicamente como lección interactiva fuera de la CPU?
2. Si se agrega, ¿conservar 32×16 caracteres, glifo 8×8, VRAM de 4 KiB y ROM de glifos de 2 KiB como dimensiones del **primer prototipo**?
3. ¿Autorizar **monocromo 1 bpp** para el prototipo y reservar **cuatro colores 2 bpp** para una versión posterior?
4. ¿Cómo se conectará su controlador al bus, qué direcciones/puertos se emplearán, qué sincronización habrá y qué comandos serán públicos? No decidido.
5. ¿Qué caracteres contendrá la ROM? ASCII básico, repertorio extendido, caracteres de bloques/semigráficos y glifos diseñados desde cero; sin importar sin licencia fuentes comerciales.

**Prohibido tratar esta propuesta como implementada.** Las cifras son hipótesis reproducibles para planificación y no mediciones de hardware. Los circuitos concretos dependerán de la pantalla que se elija, de sus niveles de señal y de las hojas de datos.

**Verificación reproducible de las cuentas (solo en PC):** `python3 scripts/verificar_modelo_video_texto_grafico.py` desde la raíz del repositorio. Comprueba el empaquetado de bits de **todos** los 32 768 píxeles a 1 y 2 bpp, las esquinas, la ROM de glifos de ejemplo y los presupuestos de memoria. **No** es una implementación de vídeo en Aula-8 ni una prueba eléctrica.
