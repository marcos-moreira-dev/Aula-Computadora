# Interludio P23V — De los mapas de caracteres al escritorio gráfico

**Estado:** plan editorial histórico **ya ejecutado** en [manuscrito P23V](capitulos/23v_de_mapas_de_caracteres_a_escritorio_grafico.md), [Word](capitulos/23v_de_mapas_de_caracteres_a_escritorio_grafico.docx) y [PDF](capitulos/23v_de_mapas_de_caracteres_a_escritorio_grafico.pdf). Está **después del capítulo 23 y antes del 24**; **no es un capítulo numerado ni altera el total de 24**. Este documento conserva las decisiones de diseño y objetivos de las figuras, no reemplaza la prosa final.

## Pregunta conductora

«Si una computadora conoce números y letras, ¿qué hace falta para que aparezcan puntos, palabras dibujadas y, con el tiempo, ventanas en una pantalla?» La respuesta no debe insinuar que la CPU entiende físicamente un píxel: un programa mueve bits y un dispositivo interpreta esos bits para mostrar una imagen.

## Escalera narrativa — de lo conocido a lo nuevo

1. **De código de carácter a símbolo visible.** El byte ASCII `0x41` puede significar `A`, pero no describe su forma. Terminal externa frente a vídeo de texto controlado por la máquina; un mapa de texto de 32×16 celdas usa 512 B si cada celda tiene un código de un byte.
2. **La fuente tipográfica de píxeles.** Glifo `A` hecho de ocho filas de ocho bits; ROM de caracteres, índice y consulta de cada fila. Distinguir **fuente**, **glifo**, **carácter** y **codificación**. Fuentes 5×7, 8×8 y otras según dispositivo, nunca presentar una como norma universal. Repertorio extendido, acentos y límites de ASCII.
3. **Modo texto y semigráficos.** Muchas máquinas mostraban bordes, barras, bloques y dibujos usando caracteres especiales. Distinguir el carácter almacenado de la retícula visual de puntos. Papel de atributos de color y posición del cursor.
4. **Modo gráfico: cada píxel tiene información propia.** Mapa de bits, resolución, `x/y`, organización por filas, máscaras, orientación de bits, inversión de estado. Contrastar 512 B de un mapa de caracteres con 4096 B de 256×128×1bpp.
5. **¿Quién dibuja?** CPU, RAM, ROM de firmware, ROM de caracteres y controlador de pantalla; distinguir subrutina software `PLOT` y circuito que presenta bits. No proponer nuevos opcodes por necesidad aparente de dibujar.
6. **Color y memoria.** Monocromo (1 bpp), cuatro colores (2 bpp), 16 colores (4 bpp), 256 índices (8 bpp); relación `memoria = techo(anchura × altura × bits_por_pixel / 8)` para formatos empaquetados sin relleno. Paletas frente a RGB directo; aclarar que la cantidad de colores lógicos no especifica un conector ni un monitor.
7. **La tipografía evoluciona.** Glifos almacenados como mapas de bits; fuentes de ancho fijo y proporcional; contornos matemáticos (curvas Bézier) convertidos en píxeles mediante rasterización, suavizado de bordes y escala. Es un cambio de **representación y software**, no necesariamente una instrucción nueva de la CPU.
8. **De pantallas antiguas a escritorios.** Monitores de texto, gráficos basados en píxeles, interfaces de ventanas, memoria de imagen, composición de superficies y aceleración gráfica. Mencionar sistemas como Windows XP/7 como **contexto histórico**, sin simular sus subsistemas ni confundir una interfaz gráfica moderna con la arquitectura Aula-8.
9. **Puente hacia lo actual.** Diferenciar modo gráfico histórico de una API de dibujo moderna; pantallas de microsistemas, paneles monocromos de bajo consumo y protocolos abstractos de visualización. Mencionar conectores/estándares específicos solo con fuentes y alcances verificables.

## Figuras exactas que debemos generar desde datos (no con IA ilustrativa)

| Figura | Contenido y prueba de fidelidad |
| --- | --- |
| A. Byte → letra | Código `0x41`, selección de glifo, matriz 8×8 dibujada según bytes reales; comparar exactamente cada pixel con bits fuente. |
| B. Pantalla en modo texto | 32×16 celdas y un ejemplo «HOLA»; cada carácter mapea a 8×8 píxeles, coordenadas y memoria documentadas. |
| C. Píxel direccionable | Imagen 256×128 1bpp y ampliación de los bytes 0 y 4095; validar esquinas y paso de byte `x=7→8`. |
| D. RAM vs ROM vs controlador | Diagrama que distingue µROM, ROM de firmware, ROM de glifos y VRAM; comparar una **terminal externa histórica** con la pantalla integrada de Aula V1, cuyo **modelo lógico está congelado** pero no se ha construido. |
| G. Modos de direccionamiento y VRAM | CPU con absoluto `C020`, decodificador E/S, registro puntero VRAM `0002` y escritura posterior en `C028`; **no** confundir el offset del periférico con un modo de direccionamiento de la ISA. |
| E. Comparación de colores | Cuatro columnas del mismo patrón renderizado a 1/2/4/8 bpp con tamaños calculados por programa; los colores concretos son paletas de ejemplo. |
| F. Fuente antigua / moderna | Glifo pixelado junto a contorno Bézier original y resultado rasterizado; no atribuir una tipografía comercial ajena sin permiso. |

**Herramienta de reproducción futura:** script determinista (Python o Java) que genere SVG y PNG a partir de matrices de bits y paletas definidas, junto con tests de límites, dimensiones, orden de bits y memoria. En el libro, la figura final no debe afirmar que se obtuvo de circuitos fabricados ni confundir maqueta de interfaz con salida de hardware real.

**Actualización de contexto para autores:** el [contrato lógico vigente de Aula](../simulador-javafx/CONTRATO_VIDEO_AULA_V1.md) incluye una sola pantalla y dos bancos separados. El libro debe enseñar también terminales externos como variante histórica y separar los tres niveles de direccionamiento.

## Ejercicios y modelos de verificación

- Calcular bytes de un modo texto de `32×16` y de un bitmap `256×128` a `1/2/4/8 bpp`.
- Decodificar un glifo de ocho bytes y representar sus 64 posiciones, con lectura de bits reproducible.
- Ubicar el píxel `(8,0)` y `(255,127)` en la VRAM con convenio MSB-primero.
- Comparar una función software para encender píxeles con el acceso directo a un dispositivo por registros; explicar por qué ninguna forma exige un opcode gráfico nuevo.
- Convertir una tabla de caracteres en pantalla semigráfica y distinguirla de imagen real por píxel.
- Interpretar los significados distintos de Unicode/carácter, glifo, fuente, framebuffer, rasterización y paleta.

## Límites editoriales y situación real

- No cambia los capítulos 21–24 ni reemplaza la historia de CPU/RAM/ROM con un libro de diseño gráfico.
- Es independiente del taller virtual; **el contenido puede existir aunque nunca se implemente hardware gráfico**.
- Mantener las fuentes bibliográficas y los derechos de diagramas, logotipos y tipografías en las referencias del libro antes de redactar la versión final.
- No usar imágenes generadas por IA para circuitos, fuentes bit a bit o diagramas de acceso a memoria que necesiten exactitud.
- **El interludio ya está escrito y maquetado**: 10 páginas, siete figuras SVG/PNG exactas, trece OMML y doce ejercicios resueltos. Su comprobador reproduce offsets, bitmaps y lectura documental; no hay electrónica de vídeo certificada.
