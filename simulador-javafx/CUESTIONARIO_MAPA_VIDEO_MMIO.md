# Cuestionario de decisiones — mapa de vídeo Aula-8

**Registro histórico del debate:** 8 de noviembre de 2026. **CERRADO por delegación de Marcos**; el contrato vigente es [CONTRATO_VIDEO_AULA_V1.md](CONTRATO_VIDEO_AULA_V1.md). Este cuestionario contiene las **alternativas originales no vinculantes**, incluidas cifras de monocromo y VRAM compartida **descartadas**. Respuestas efectivas: **1A adaptada, 2A, 3A, 4A, 5A, 6A, 7B, 8A, 9B adaptada, 10B, 11A, 12A, 13A precisada, 14A, 15A, 16A**.

Responder, por ejemplo: `1A, 2A, 3A, ... 16A`, indicando excepciones. **No se modificarán ISA, E/S, ROM ni hardware hasta aprobar un contrato consolidado.**

## Mapa existente que no se debe romper

| Dirección | Situación |
| --- | --- |
| `0000–7FFF` | RAM CPU, 32 KiB, vigente. |
| `8000–BFFF` | Expansión CPU reservada, 16 KiB. |
| `C000` y `C002` | DATA y STATUS de terminal existente. |
| `C010–C01F` | Controlador de bloques candidato. |
| `C020–C0FF` | Disponible para planificación, **no reservado**. |
| `C100–DFFF` | Reservado. |
| `E000–FFFF` | Firmware ROM, 8 KiB, incluida tabla candidata de 32 entradas, solo cuatro asignadas. |

## Propuesta de registros, sin reservar aún

Si se seleccionan las opciones 2A, 3A y 4A, el controlador ofrece registros **de 8 bits en direcciones pares**:

| Dirección propuesta | Nombre simbólico | Uso previsto (pendiente de semántica fina) |
| --- | --- | --- |
| `C020` | `VIDEO_MODE` | Texto `00`, bitmap monocromo `01`; otros valores sin definir. |
| `C022` | `VIDEO_STATUS` | Estado y errores; bits exactos sin asignar. |
| `C024` | `VRAM_ADDR_LO` | Byte bajo del desplazamiento de memoria de vídeo. |
| `C026` | `VRAM_ADDR_HI` | Byte alto; el rango válido depende de la capacidad real. |
| `C028` | `VRAM_DATA` | Lee/escribe un byte de VRAM en el desplazamiento seleccionado. |
| `C02A` | `VIDEO_CTRL` | Política de incremento de dirección; demás bits sin definir. |
| `C02C`, `C02E` | — | Reservas sin función. |

**No significa** que la CPU tenga una zona adicional de RAM en `C020`, ni que exista VRAM en `8000`. `VRAM_DATA` es un **puerto**, no los 4096 bytes. El controlador tiene sus propios 4 KiB tentativos, seleccionados mediante sus dos registros de dirección. Los accesos 8-bit de Aula-16 deberán respetar el carril correcto de su bus externo de **16 bits**.

## Dieciséis preguntas de opción múltiple

### Arquitectura y mapa de direcciones

**1. ¿Qué integramos en el taller virtual?**

- **A — Recomiendo:** mantener la terminal básica y añadir **después** un módulo educativo de vídeo opcional.
- B: sustituir desde el inicio la terminal por pantalla de caracteres propia de Aula.
- C: explicarlo solo en el libro, sin módulo de vídeo en el taller.

**2. ¿Cómo ve Aula-8 la memoria de vídeo?**

- **A — Recomiendo:** acceso **indirecto por registros de E/S**; VRAM no ocupa el espacio RAM/ROM de la CPU.
- B: VRAM de 4 KiB **mapeada directamente** en expansión `8000–8FFF`; acceso más directo pero consume mapa y exige resolver contención.
- C: combinación de A y B, con un diseño de arbitraje más complejo.

**3. ¿Dónde reservaríamos los registros de vídeo si se integra?**

- **A — Recomiendo:** `C020–C02F`, a continuación del controlador de bloques.
- B: `C040–C04F`, dejando un hueco anterior sin asignar.
- C: aplazar la dirección hasta diseñar una placa real.

**4. ¿Cuántos registros tendrá el primer contrato?**

- **A — Recomiendo:** seis (`MODE`, `STATUS`, dirección baja/alta, `DATA`, `CTRL`) y dos pares libres.
- B: cuatro mínimos (`MODE`, dirección baja/alta, `DATA`), sin estado/control explícitos.
- C: ocho, agregando desde ahora posición de cursor X/Y.

**5. ¿Qué ocurre con direcciones impares del bloque de vídeo?**

- **A — Recomiendo:** no son alias de registros pares; se reservan y ningún programa debe usarlas.
- B: se admiten como alias del registro par anterior (aumenta ambigüedad).
- C: postergar la semántica de las impares hasta decidir controlador.

### Caracteres, RAM y color

**6. ¿Qué resolución pedagógica usamos en el primer modelo?**

- **A — Recomiendo:** 32×16 caracteres × 8×8 píxeles = **256×128**; 512 B de texto, 4 KiB de bitmap 1 bpp.
- B: 40×25 caracteres × 8×8 = **320×200**; 1000 B de texto, 8000 B de bitmap 1 bpp.
- C: 16×16 caracteres × 8×8 = **128×128**; 256 B de texto, 2 KiB de bitmap 1 bpp.

**7. ¿Qué ROM de caracteres proponemos?**

- A: 128 glifos de 8×8 = **1 KiB**; caracteres básicos solamente.
- **B — Recomiendo:** 256 glifos de 8×8 = **2 KiB**, con repertorio de acentos y semigráficos aún por diseñar.
- C: fuente modificable en RAM desde el primer prototipo; más flexible, más complejo.

**8. ¿Cómo se guarda una celda de texto?**

- **A — Recomiendo:** un byte de **código de glifo**; 512 B si se eligió 6A.
- B: dos bytes (**glifo + atributo**), 1024 B si se eligió 6A; facilita color por carácter.
- C: texto UTF-8 directamente interpretado por controlador; implica decodificador complejo e introduce caracteres de ancho variable.

**9. ¿Cómo se reparte la memoria de vídeo?**

- **A — Recomiendo:** una VRAM de **4 KiB compartida por modos** (6A + 10A); la representación cambia al alternar, sin dos imágenes simultáneas.
- B: buffer de texto **512 B aparte** y gráfico **4 KiB aparte** (6A + 10A); conserva ambos al cambiar, pero emplea más memoria/control.
- C: usar una región de RAM principal de Aula-8; altera el presupuesto de RAM y acceso de memoria.

**10. ¿Qué profundidad de color implementamos primero?**

- **A — Recomiendo:** **1 bpp, dos índices** (fondo y tinta), con cuatro colores en una ampliación posterior.
- B: **2 bpp, cuatro índices de paleta** desde el principio; para 6A necesita **8 KiB** de bitmap, incompatible con la VRAM de 4 KiB de 9A sin ampliarla.
- C: solo texto, sin bitmap en el primer prototipo del módulo.

**11. ¿Cómo conviven los modos de texto y gráficos?**

- **A — Recomiendo:** selección **exclusiva**: modo texto o modo bitmap; los gráficos con caracteres especiales (semigráficos) se estudian en texto.
- B: ambos superpuestos en una pantalla (capas/mezcla; considerablemente más complejo).
- C: pantalla dividida en zonas de texto y bitmap simultáneas (control extra).

### Operación, firmware y límites

**12. ¿Cómo se leen/escriben los bytes de VRAM?**

- **A — Recomiendo:** puerto `DATA` de lectura/escritura y un bit en `CTRL` que **activa o desactiva autoincremento**, inicialmente desactivado.
- B: `DATA` siempre autoincrementa; más simple, más incómodo para operaciones sobre un mismo byte.
- C: `DATA` nunca autoincrementa; firmware debe actualizar dirección para cada byte.

**13. ¿Qué pasa al arrancar y al cambiar de modo?**

- **A — Recomiendo:** arranca en texto; contenido inicial de VRAM **indefinido** hasta que el firmware/programa lo limpie; cambiar modo no lo borra automáticamente.
- B: circuito o controlador limpia VRAM automáticamente en RESET/cambio (más lógica y temporización).
- C: arrancar directamente en bitmap con memoria inicial indeterminada.

**14. ¿Dónde ponemos las rutinas auxiliares de dibujo?**

- **A — Recomiendo:** primero enseñar `LD/ST` y máscaras mediante E/S; después probar biblioteca en RAM; **no asignar todavía** nuevas entradas ROM.
- B: reservar **ya** servicios `FW_SETMODE`, `FW_PLOT`, `FW_CLS` en la tabla ROM, aunque falte medir firmware.
- C: obligar a usar solo ROM para gráficos; no permitir acceso directo por el programa (requiere un control más amplio).

**15. ¿Hasta dónde llega el hardware de visualización en V1?**

- **A — Recomiendo:** **modelo lógico** reproducible en el taller y libro; señal eléctrica/placa física de pantalla para etapa posterior. Mantener GPU y VGA fuera del alcance V1.
- B: diseñar un circuito eléctrico de salida de vídeo y sincronización ahora; **amplía el alcance** y requiere redefinir D-035.
- C: elegir ya un display comercial concreto (OLED/LCD) y su protocolo, antes de cerrar la CPU.

**16. ¿Qué hacemos con Aula-16?**

- **A — Recomiendo:** futuro acceso al **mismo módulo de registros de 8 bits**, con operaciones de byte y validación de carriles; no añadir lógica ahora.
- B: diseñar un vídeo específico Aula-16 desde cero.
- C: dejar los gráficos solo en Aula-8 y no planificarlos para Aula-16.

## Coherencia de respuestas

- Si marcas **1C**, las preguntas 2–5 y 9–16 quedan como **investigación teórica**, no compromisos del taller.
- Si marcas **2B**, elegir **3A** no significa que VRAM esté indirectamente en C020: un bloque de registros de control y la VRAM directamente mapeada son cuestiones diferentes; hay que especificar la compatibilidad.
- Si marcas **6B**, el framebuffer 1 bpp necesita **8000 B**, no 4 KiB. Si marcas **10B**, se duplica la necesidad de bits por píxel. Por eso 9A solo significa 4 KiB si se eligieron también **6A y 10A**.
- Si marcas **8B** y **9A**, los atributos ocupan parte de la misma VRAM; conviene definir la partición exacta de texto antes de codificar el controlador.
- Ninguna elección modifica todavía la ROM de firmware E000–FFFF, las cuatro rutinas candidatas FF00–FF0C ni los registros de terminal/almacenamiento existentes.

**Pasos posteriores a la respuesta:** actualizar estados en `DECISIONES.md`, crear **contrato de mapa con direcciones y semánticas exactas**, revisar arquitectura y ROM/ISA, definir pruebas de acceso inválido y solo después considerar implementación o maquetación de diagramas.
