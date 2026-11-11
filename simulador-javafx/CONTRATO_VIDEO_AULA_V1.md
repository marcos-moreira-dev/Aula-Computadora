# Contrato de vídeo Aula V1 — diseño lógico congelado

**Fecha:** 2026-11-08 (Ecuador). **Autoridad:** Marcos delegó expresamente en el asistente la elección de las opciones de arquitectura de vídeo. **Estado: CONGELADO PARA DISEÑO LÓGICO**, **NO IMPLEMENTADO NI CERTIFICADO FÍSICAMENTE**. No congela ISA, ROM de firmware, temporización, fuente de alimentación ni conector de una pantalla real.

**Fuente legible por máquinas:** [VIDEO_AULA_V1_CONTRATO.json](VIDEO_AULA_V1_CONTRATO.json). **Revisión documental:** `python3 scripts/verificar_contrato_video_aula_v1.py` desde raíz.

## 1. Decisión principal

**Una sola pantalla didáctica**, no una terminal física junto a otro monitor. El mismo dispositivo visible presenta **texto** o **mapa de bits** según `VIDEO_MODE`.

- Los accesos de teclado/terminal acordados permanecen en `C000` (DATA) y `C002` (STATUS): el software y las cuatro entradas candidatas de ROM (`FW_PUTC`, etc.) no cambian.
- Las **salidas** de caracteres de `C000` alimentan el buffer de texto de la **misma pantalla** aunque el mapa de bits esté visible; las entradas siguen la ruta de teclado prevista. No se suman dos adaptadores físicos; se integra la función de consola en el controlador virtual.
- `VIDEO_MODE=00`: se ve el buffer de caracteres, interpretado con ROM de glifos 8×8.
- `VIDEO_MODE=01`: se ve el framebuffer 2bpp de cuatro colores lógicos.
- Conservar **ambos buffers separados** hace que la pantalla de texto reaparezca al regresar de gráficos. Un cambio de modo **no borra** por sí solo ninguna memoria. No existen capas simultáneas, división de pantalla, sprites ni texto proporcional en V1.
- El videojuego/taller modelará esto lógicamente; **no hay GPU, VGA, controlador electrónico diseñado ni salida de señales físicas** comprometidos para V1.

La pantalla no exige a la CPU instrucciones `DRAW` o `PIXEL`. La CPU usa `LD/ST`, constantes, aritmética y operaciones de bits ordinarias de su ISA **todavía candidata**. El control de vídeo accede a su VRAM interna y a la ROM de glifos.

## 2. Mapa único de CPU y registros

Las direcciones CPU son de **16 bits y se refieren a bytes**. En Aula-8 el bus de datos externo es de 8 bits; en Aula-16, **16 bits** con operaciones de byte y selección de carril. Los registros del periférico son **de 8 bits ubicados en direcciones pares**.

| Intervalo / dirección | Uso congelado en el modelo lógico |
| --- | --- |
| `0000–7FFF` | RAM CPU de 32 KiB, inalterada. |
| `8000–BFFF` | Expansión reservada: **no** se mapea VRAM aquí. |
| `C000` | Terminal DATA bidireccional, consola del monitor visible. |
| `C002` | Terminal STATUS existente, sin redefinir sus bits aquí. |
| `C010–C01F` | Controlador de bloques, según R0.12 candidato anterior. |
| **`C020–C02F`** | **Reservado para controlador de vídeo Aula V1**; seis registros pares activos, dos pares libres, impares no alias. |
| `C030–C0FF` | E/S restante sin nuevas asignaciones. |
| `C100–DFFF` | Reservado. |
| `E000–FFFF` | ROM de firmware CPU 8 KiB; tabla pública FF00–FF7F, cuatro entradas candidatas existentes. |

**Los 8192 bytes de bitmap y los 512 bytes de texto no ocupan direcciones CPU.** La CPU accede a ellos indirectamente mediante el par `VRAM_ADDR` y el registro `VRAM_DATA`. El desplazamiento es **dentro de la memoria de vídeo**, no una dirección absoluta de CPU.

| Dirección | Registro | Lectura/escritura | Contrato de V1 |
| --- | --- | --- | --- |
| `C020` | `VIDEO_MODE` | R/W | `00` texto, `01` bitmap cuatro colores; otros valores inválidos. |
| `C022` | `VIDEO_STATUS` | R | Bit 0 `READY`; bit 7 `ERROR` persistente; demás bits a 0. |
| `C024` | `VRAM_ADDR_LO` | R/W | Ocho bits bajos del desplazamiento de vídeo. |
| `C026` | `VRAM_ADDR_HI` | R/W | Ocho bits altos del desplazamiento de vídeo. |
| `C028` | `VRAM_DATA` | R/W | Un byte del **plano de acceso** elegido en `VIDEO_CTRL`; autoincremento opcional. |
| `C02A` | `VIDEO_CTRL` | R/W | Banco de acceso, autoincremento y colores globales del texto. |
| `C02C`, `C02E` | Sin asignar | — | Reservados, sin lecturas/escrituras válidas. |

Todas las direcciones impares de `C020–C02F` están **sin asignar y no reflejan registros pares**. La política de fallo de lectura en direcciones CPU **no asignadas** se decidirá en el contrato general de buses; no simularlas como puertos de vídeo.

## 3. Codificación exacta de registros

### `VIDEO_MODE` (`C020`)

El valor **completo** debe ser `00` o `01`; los bits 7..1 son cero. Escribir otro valor deja el modo anterior intacto y activa `VIDEO_STATUS.ERROR`. Una lectura devuelve `00` o `01`.

### `VIDEO_STATUS` (`C022`)

| Bit | Nombre | Semántica |
| --- | --- | --- |
| 0 | `READY` | 1 mientras el dispositivo lógico acepta accesos (V1 siempre listo después de RESET). |
| 7 | `ERROR` | 1 después de modo inválido, operación de datos fuera de banco o escritura indebida a un registro de vídeo de solo lectura. Se conserva hasta RESET o limpieza explícita. |
| 1..6 | — | Siempre 0; reservados. |

Es de **solo lectura**, no elimina `ERROR` al leerlo. Una escritura directa a `VIDEO_STATUS` no modifica el estado y activa `ERROR`.

### `VIDEO_CTRL` (`C02A`)

| Bits | Nombre | Significado |
| --- | --- | --- |
| 0 | `AUTO_INC` | 0: mantener dirección tras acceso `DATA`; 1: incrementar **después de un acceso válido**. |
| 1 | `ACCESS_PLANE` | 0: texto (512 B); 1: bitmap (8192 B). Es **independiente** del modo visible. |
| 3..2 | `TEXT_FG` | Índice de color global de caracteres, entre 0 y 3. |
| 5..4 | `TEXT_BG` | Índice de fondo global del texto, entre 0 y 3. |
| 6 | — | Reservado, debe escribirse 0. Escritura con bit6=1 se rechaza y activa `ERROR`. |
| 7 | `CLEAR_ERROR` | **Solo escritura**: escribir 1 limpia el error previo. Se lee siempre 0. |

Escribir `CTRL` con bit6=0 actualiza bits 0..5, además de limpiar `ERROR` si bit7=1. RESET: `CTRL=0C` (autoincremento desactivado, acceso al texto, letra blanca índice 3, fondo negro índice 0). La paleta lógica de la primera presentación será `0=negro, 1=verde, 2=ámbar, 3=blanco`. Los valores RGB concretos del renderizador **no** forman parte del bus ni de una señal física.

### Dirección y datos

- `VRAM_ADDR = (ADDR_HI << 8) | ADDR_LO`, 16 bits de desplazamiento dentro del banco.
- `ACCESS_PLANE=0`: válido `0000–01FF` (512 bytes de códigos de caracteres).
- `ACCESS_PLANE=1`: válido `0000–1FFF` (8192 bytes de mapa de bits).
- `VRAM_DATA`: lectura devuelve el byte del banco; escritura lo sustituye; acceso válido con `AUTO_INC=1` incrementa la dirección en **una unidad** después de completar, sin circular por el final del banco.
- Fuera del banco, un `VRAM_DATA` leído devuelve `FF`, una escritura se ignora, `ERROR=1`, y `VRAM_ADDR` **no avanza**. Puntero `0200` en texto y `2000` en gráficos son inválidos; la CPU puede escribir estos valores en `ADDR` pero no acceder a `DATA` con ellos.
- Al acceder a un banco no se altera el otro, esté o no visible. **Cambiar `VIDEO_MODE` no modifica el plano de acceso** del registro `CTRL`.

En la práctica el programador selecciona el banco con `VIDEO_CTRL`, escribe desplazamiento bajo/alto y usa `DATA`. Es acceso a un periférico, no un nuevo *addressing mode* del procesador.

## 4. Memoria y píxeles

| Elemento del controlador | Cantidad | Cálculo |
| --- | ---: | --- |
| Buffer de texto | **512 B** | 32 columnas × 16 filas × 1 B. |
| Buffer gráfico | **8192 B = 8 KiB** | 256 × 128 píxeles × 2 bits / 8. |
| Total RAM de vídeo | **8704 B** | Dos bancos separados, se conservan al cambiar de modo. |
| ROM de caracteres | **2048 B = 2 KiB** | 256 glifos × 8 filas × 1 B; fuera de ROM de firmware. |

Cada carácter usa un byte y referencia un glifo de 8×8. Se reserva el repertorio `00–7F` para un subconjunto ASCII/control y `80–FF` para españoles acentuados, símbolos y semigráficos. **La tabla completa de códigos y sus 2048 bytes de dibujos están pendientes de elaborar y verificar**; la capacidad y el tamaño del glifo sí quedan congelados. No se requiere UTF-8 ni fuente Unicode dentro del controlador. Las entradas Unicode del anfitrión deberán convertirse explícitamente a códigos Aula compatibles o rechazarse con diagnóstico.

El bitmap es **2 bpp, cuatro índices de paleta**, cuatro píxeles por byte, **MSB primero**, 64 bytes por fila:

```text
para 0 <= x < 256, 0 <= y < 128:
    indice_byte = y * 64 + (x // 4)
    shift       = 6 - 2 * (x % 4)
    color       = (bitmap[indice_byte] >> shift) & 0b11
```

Por ejemplo, `(8,0)` se encuentra en el **byte de VRAM gráfica 2**, bits 7–6. El índice de color `2` se escribe allí como `10` binario; sobre el byte previamente a cero, deja `80` hexadecimal. El último píxel `(255,127)` ocupa los bits 1–0 del **byte 8191**.

El modo texto toma `codigo = texto[fila*32+col]` y consulta `rom_glifos[codigo*8+fila_pixel]`; el bit de columna selecciona tinta o fondo conforme a `TEXT_FG/TEXT_BG`.

La comparación con bitmap monocromo de **1 bpp = 4096 B** sigue apareciendo en el **libro**, pero `VIDEO_MODE` V1 **no añade un tercer modo monocromo**. De esta manera la máquina virtual no duplica innecesariamente implementaciones.

## 5. Encendido, cambio de modo y consola

1. RESET lógico restablece `VIDEO_MODE=00`, `VIDEO_STATUS.READY=1`, `ERROR=0`, `ADDR=0000`, `CTRL=0C` y cursor de consola inicial en la esquina superior izquierda. **No presupone que las dos RAM de vídeo empiecen a cero.**
2. El monitor/firmware aún por implementar deberá inicializar explícitamente el buffer de texto antes de anunciar `AULA-8 READY`; el programa que use gráficos debe inicializar su bitmap antes de mostrar información significativa. Esto será especificación de arranque, **no prueba de que cabe en los 8 KiB de ROM**.
3. Escribir `VIDEO_MODE=01` muestra bitmap, **sin borrar el texto**. Escribir `VIDEO_MODE=00` muestra texto, sin borrar bitmap. No hay interruptor físico; lo decide el programa por E/S.
4. La salida por la terminal `C000` sigue actualizando el contenido de texto aunque los gráficos sean visibles. El formato exacto de retorno de carro, tabulación, scroll, cursor y cola de teclado permanece en el contrato futuro del terminal; no se modifica aquí la ABI ROM candidata.
5. No se reserva una entrada `FW_PLOT`, `FW_SETMODE` ni `FW_CLS` por esta decisión. Se enseñarán operaciones normales de CPU y, si conviene, una biblioteca en RAM. Cualquier servicio ROM nuevo exige código compilado y presupuesto verificado.

## 6. ¿Qué son los modos de direccionamiento?

Los **modos de direccionamiento de la ISA** (aún candidatos) calculan la **dirección efectiva CPU**; la **decodificación de memoria** selecciona qué responde a esa dirección; el puntero de VRAM es un **segundo espacio de direcciones** dentro del periférico:

| Nivel | Ejemplo | Interpretación |
| --- | --- | --- |
| Inmediato `LDI R0,1` | El 1 viaja como dato en la instrucción. | No se lee una posición de RAM por el operando. |
| Absoluto `ST [C020],R0` | Dirección efectiva CPU = `C020`. | El decodificador selecciona el registro `VIDEO_MODE`. |
| Indexado `LD R1,[X+2]` | Dirección efectiva CPU = `X+2` (según ISA candidata). | Si cae en RAM lee RAM; si cae en MMIO actúa un dispositivo. |
| Relativo a pila `LD R1,[SP-1]` | Dirección efectiva CPU = `SP-1`. | Se aplica la misma lógica de decodificación; no es un modo gráfico. |
| Puntero de VRAM `0002` | Desplazamiento local dentro del banco gráfico. | La CPU accede a **`C024/C026/C028`** para operar sobre él. `0002` no reemplaza al PC ni a la dirección CPU. |

**Ejemplo documental:** `LDI R0,1; ST [0xC020],R0` seleccionaría gráficos al implementarse la ISA candidata. La acción `ST` del procesador sería una escritura de bus ordinaria hacia un registro de periférico; no se inventa `SETGRAPHICS` como opcode. Los microdetalles y tiempos de señales permanecen sin demostrar.

## 7. Respuestas congeladas a las 16 preguntas

| Pregunta | Elegida | Motivación |
| ---: | :---: | --- |
| 1 | **A adaptada** | Un solo dispositivo visible con consola integrada y modos alternativos, conservando `C000/C002`. |
| 2 | **A** | Acceso indirecto por registros; VRAM fuera del mapa CPU. |
| 3 | **A** | Reservar `C020–C02F`. |
| 4 | **A** | Seis registros activos, dos pares reservados. |
| 5 | **A** | Direcciones impares sin alias. |
| 6 | **A** | Texto 32×16, glifos 8×8, imagen 256×128. |
| 7 | **B** | ROM de 256 glifos × 8 B, 2 KiB, apoyo a acentos. |
| 8 | **A** | Un byte de código por celda; sin decodificador UTF-8 en pantalla. |
| 9 | **B adaptada** | RAM texto 512 B y bitmap **8192 B**, independientes. |
| 10 | **B** | Cuatro índices de color, 2bpp, para el bitmap inicial. |
| 11 | **A** | Texto y bitmap son modos exclusivos, no capas. |
| 12 | **A** | `DATA` de lectura/escritura con autoincremento opcional. |
| 13 | **A precisada** | RESET en texto, RAM inicial indeterminada, limpieza explícita, cambio sin borrado. |
| 14 | **A** | Acceso directo a MMIO y biblioteca en RAM; sin ranuras ROM nuevas. |
| 15 | **A** | Modelo lógico virtual; sin hardware gráfico físico en V1. |
| 16 | **A** | Aula-16 usaría el mismo dispositivo mediante operaciones de byte compatibles con bus externo de 16 bits. |

Las adaptaciones 1/9 reflejan la petición posterior de **una única pantalla y recuperación del texto al volver de gráficos**. La elección de detalles fue **delegada explícitamente** por Marcos. El cuestionario anterior se conserva como historia de la decisión, pero **este documento prevalece** ante contradicciones.

## 8. Pendientes técnicos que no invalidan el contrato

- Firmware ejecutable, presupuesto ROM y pruebas de monitor/terminal nativos.
- Codificación completa de glifos españoles/semigráficos y derechos de autor de tipografías; no copiar una ROM comercial.
- Esquema de vídeo electrónico, pantalla concreta, reloj, sincronización, arbitraje y pruebas físicas.
- Semántica detallada del teclado, cursor, scroll y tratamiento de controles de consola (`CR/LF/BS`).
- Ancho, decodificador y comportamiento general de accesos a **direcciones CPU no asignadas**; la no-aliasedad de los registros de vídeo sí está fijada.
- Implementación real de la ISA Aula-8/Aula-16, incluidas operaciones de byte correctamente dirigidas al carril externo de Aula-16.

**Regla de continuidad:** estos puntos pendientes no autorizan alterar silenciosamente `C020–C02F`, los tamaños de memoria ni 2bpp. Una revisión requiere explicar el conflicto y registrar nueva decisión con migración.
