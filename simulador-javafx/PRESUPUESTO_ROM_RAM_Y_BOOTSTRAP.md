# Presupuesto de memoria y arranque por etapas

**Estado R0.2:** estudio de capacidad y diseño propuesto, **no** prueba de cabida, código compilado ni asignación de direcciones congelada. Las cifras de esta página son **metas de ingeniería revisables**; R1 fijará las reglas de la ISA/ABI y R5 medirá imágenes reales.

## 1. El problema que hay que resolver

Aula-8 cuenta inicialmente con **32 KiB de RAM**, **8 KiB de ROM de firmware** y un espacio de direcciones de 64 KiB. Es posible construir un editor y ensamblador nativos modestos, pero sería incorrecto dar por sentado que caben sin reservar memoria para entrada/salida, pila, fuente, tabla de símbolos y binario.

La **ROM de microcontrol de la CPU** es distinta de los 8 KiB de ROM de firmware y no puede utilizarse libremente como disco o memoria de programas de usuario.

El diseño preferido conserva un monitor ROM pequeño y carga editor y ensamblador **por turnos** desde el almacenamiento. Una utilidad externa compilada en la computadora anfitriona sirve solamente para generar la primera imagen de esas herramientas.

## 2. ROM de firmware: ejemplo de presupuesto de 8192 bytes

| Concepto | Meta máxima de bytes | Función |
| --- | ---: | --- |
| Vector, tabla de saltos pública y margen de alineación | 512 | Contratos estables y reset |
| Inicialización y comprobaciones mínimas | 768 | Pila, terminal y arranque |
| Rutinas de terminal y conversión hexadecimal | 1280 | Entrada/salida de caracteres y cifras |
| Parser y comandos básicos del monitor | 3072 | HELP, MEM, POKE, RUN y diagnósticos |
| Controlador de bloques y cargador crudo | 1536 | Leer sectores sin sistema de archivos |
| Mensajes, errores y reserva | 1024 | Salidas y pequeños cambios |
| **TOTAL** | **8192** | **Solo presupuesto provisional** |

Notas:

- La región pública actual empieza en `0xFF00`, y el vector de reset ocupa `0xFFFC–0xFFFD`. Las posiciones definitivas de rutinas y espacios libres deben calcularse desde un **mapa de enlace**, no suponiendo que una sección de la tabla cabe en cualquier sitio.
- En la propuesta [R0.11](ROM_MONITOR_AULA8_R0_11_BORRADOR.md) se reservarían 32 ranuras de 4 B en FF00–FF7F, es decir 128 B, y dos bytes de RESET en FFFC–FFFD. Del techo de 512 B reservado a vector/tabla/alineación quedarían aritméticamente 382 B, **sin demostrar todavía dónde colocar el resto de las secciones ni que quepan**.
- La ROM no se llenará intencionalmente al 100 % por diseño; esta suma distribuye **techos orientativos**, no tamaños obtenidos. Si las mediciones los exceden, se reduce el monitor y se trasladan comandos secundarios a RAM.
- Cada CPU puede requerir una ROM de firmware **distinta**, incluso cuando comparten nombres de servicios. La microarquitectura y formatos de instrucción de Aula-8 y Aula-16 no son binariamente compatibles.
- El monitor puede necesitar inicializar solo un subconjunto del controlador de almacenamiento. `DIR`, `SAVE archivo` y editor no son obligaciones de firmware en la primera ROM.
- El [modelo de bloques R0.12](CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md) reserva ocho registros y propone una transferencia de 256 B por operación. El búfer protegido candidato de RAM `0200–0FFF` puede alojar un bloque temporal, pero esto **no mide los 1536 B** asignados a cargador/controlador dentro del presupuesto de ROM ni crea el firmware. La carga múltiple puede quedar incompleta y nunca se ejecuta en ese estado.

### Criterio medible de aceptación

Para cada versión de la imagen exigir: longitud de ROM no superior a 8192 bytes; mapa de secciones sin traslapes; vector valido; tabla pública accesible; comandos nucleares dentro del presupuesto; batería de pruebas de reset, errores y lectura de bloque. **Todavía no se ha probado** ninguno de esos puntos sobre código real.

## 3. RAM de Aula-8: una partición **candidata**, no definitiva

Los rangos siguientes suman exactamente los 32768 bytes disponibles. Permiten razonar sobre los tamaños y las colisiones; **no** forman todavía una ABI ni un mapa obligatorio para programadores.

| Dirección inicial | Final | Tamaño | Uso propuesto |
| --- | --- | ---: | --- |
| `0x0000` | `0x01FF` | 512 B | Variables de firmware y estado global |
| `0x0200` | `0x0FFF` | 3584 B | Búferes de terminal y servicio de carga |
| `0x1000` | `0x2FFF` | 8192 B | **Overlay**: editor **o** ensamblador, nunca ambos a la vez |
| `0x3000` | `0x4FFF` | 8192 B | Documento fuente y su representación interna |
| `0x5000` | `0x5FFF` | 4096 B | Tabla de símbolos y área de las dos pasadas |
| `0x6000` | `0x6FFF` | 4096 B | Binario generado o programa del alumno |
| `0x7000` | `0x7FFF` | 4096 B | Pila descendente y reserva de ejecución |
| **TOTAL** | | **32768 B** | **Hipótesis de cabida a medir** |

### Cómo funciona el overlay

1. El monitor carga un binario de **editor** en su región de herramienta.
2. El editor modifica el documento en un **área de fuente aparte**.
3. Al solicitar `ASM`, se vuelve al cargador y se reemplaza en esa misma región el editor por el **ensamblador**. El documento permanece intacto en su propia región.
4. El ensamblador construye la tabla de símbolos, da dos pasadas y escribe el resultado en la región de salida.
5. El monitor puede ejecutar el resultado solo después de validar longitud, dirección de entrada, rangos y estado de la pila. Para volver a editar, recarga el editor.

Un editor con números de línea puede almacenar `(numero, longitud, contenido ASCII)`; los números son metadatos de edición, **no** instrucciones ni bytes que deban pasar al ensamblador. El conversor/editor debe entregar al ensamblador texto con las líneas de fuente correctamente delimitadas.

### Límites que deberán declararse al usuario

- Máximo de fuente inicial: hasta **8192 B incluyendo índices**, solo si la prueba de carga lo confirma.
- Binario inicial: hasta **4096 B** en el área temporal propuesta, si no necesita reubicar o solapar utilidades.
- Tabla de símbolos: **4096 B** totales; cantidad real de etiquetas depende del formato final.
- Editor/ensamblador: cada uno requiere **no más de 8192 B** para ocupar el overlay de ejemplo; si el tamaño real lo excede, rediseñar la partición o reducir prestaciones.
- La pila requiere límites y protección frente al resto de memoria. Definir la dirección inicial exacta y los efectos de `PUSH`, `CALL` y `RET` según ABI. No asumir que `HALT` salta al monitor.

Estos son límites **de una primera implementación nativa mínima**, no límites intrínsecos de la arquitectura Aula-8. Los programas MiniC compilados fuera de Aula podrían utilizar otra distribución de RAM documentada.

## 4. Un arranque que no oculta herramientas externas

### Fase A — Máquina desnuda

- Se demuestra el panel de depósito byte a byte con CPU detenida y propietario exclusivo del bus.
- Al principio el usuario introduce un programa **muy corto**; no se le exige teclear miles de bytes para cargar un editor completo.
- El mecanismo físico para que el panel tenga control del bus es un problema de electrónica a resolver; la interfaz virtual debe explicitarlo.

### Fase B — Primera ROM

1. En el anfitrión se escribe el firmware original de Aula en su propio ensamblador cruzado.
2. El firmware se convierte en imagen binaria y se programa en EEPROM con un dispositivo externo si se construye físicamente.
3. Al resetear, la CPU Aula lee el vector de firmware y ejecuta el monitor.
4. `MEM`, `POKE`, `RUN` y servicios mínimos son instrucciones reales de Aula, no comandos mágicos de Java.

### Fase C — Bloques y herramientas

1. En el anfitrión se compila primero un editor y un ensamblador **para la ISA de Aula-8**.
2. Se colocan esos **binarios de destino** dentro de una imagen de almacenamiento con bloques de 256 B.
3. El monitor lee bloques y copia el código a RAM, comprobando límites y que no invada el firmware mutable ni la pila.
4. La CPU Aula ejecuta el editor y el ensamblador cargados. A partir de aquí se pueden crear programas nuevos en la propia Aula.
5. Un directorio de archivos con nombres, persistencia y protección se añade después de demostrar carga por bloques crudos.

La introducción de software a partir de herramientas cruzadas **no invalida la ejecución nativa**; es el paso de bootstrap que permite crear el primer conjunto de utilidades.

### Fase D — Autosuficiencia razonable

- Escribir fuente desde terminal de Aula.
- Ensamblarlo en Aula; cotejar el resultado con el ensamblador cruzado durante pruebas.
- Guardar texto y binario en el almacenamiento persistente.
- Reiniciar la máquina, recuperar el archivo y ejecutar otra vez.
- Reservar MiniC compilado nativamente para una ampliación: no se necesita para alcanzar esta autosuficiencia de ensamblador.

## 5. RUN, CALL, RET y HALT: contrato pendiente

No basta decir «al terminar aparece el prompt». Son eventos diferentes:

| Evento | Significado esperado | Pendiente de definir |
| --- | --- | --- |
| `RUN direccion` | Transferir ejecución a un programa válido en RAM | ¿Se invoca vía CALL desde el monitor o se modifica PC mediante un trampolín? |
| `RET` | Recuperar la dirección de retorno desde la pila | ¿Qué marco, registros y flags debe conservar la aplicación? |
| `HALT` | Detener el procesador o la ejecución | ¿La UI se queda detenida hasta RESET, STEP o una acción explícita? |
| Fallo o programa colgado | No equivale a finalización normal | ¿Cómo recuperar la consola sin fingir retorno? |

Una opción coherente es ejecutar aplicaciones retornables mediante **CALL controlado por monitor**, de modo que un `RET` legítimo regrese a éste. Es una **propuesta** sujeta a la ISA/ABI; programas que ejecutan HALT se muestran detenidos, no de vuelta al shell por arte de magia.

## 6. Qué significa verificar una herramienta nativa

Protocolo de comparación entre implementaciones, cuando ambas existan:

1. Compilar un mismo archivo fuente con ensamblador cruzado del anfitrión y con ensamblador nativo de Aula.
2. Igualar el origen de carga, versión de ISA, endianness, convenciones de expresión y directivas del subconjunto compartido.
3. Comparar **byte por byte** los binarios generados, tamaños, direcciones de entrada y símbolos.
4. Ejecutar ambos en la CPU de referencia y comprobar salida, registros y cambios de RAM.
5. Provocar errores de etiqueta hacia delante, duplicada, indefinida, overflow y agotamiento de fuente/símbolos.
6. Confirmar con traza que el ensamblador nativo realizó lecturas, escrituras y ciclos reales de Aula; si el resultado lo construyó Java, la prueba falla.
7. Repetir los casos de persistencia después de cerrar y volver a cargar la imagen de bloques.

Una comparación correcta no certifica el montaje **físico** de la CPU. Cada nivel de evidencia conserva su significado.

## 7. Riesgos y reducción de alcance

| Riesgo | Indicio | Respuesta preferida |
| --- | --- | --- |
| Monitor ROM supera 8 KiB | Imagen real más grande que EEPROM | Mover `DIR`, `TYPE`, mensajes extensos y herramientas a RAM |
| Editor o ensamblador supera su overlay | Binario mayor que región asignada | Simplificar parser/directivas, ampliar overlay o reducir documento disponible |
| Fuente y binario chocan | Mapa de carga y salida se solapan | Rechazar programa, guardar fuente, reubicar y reconstruir mapa |
| No existe retorno de programa | HALT/infinite loop no devuelve control | Detención explícita, RESET y monitor con estado documentado |
| Memoria no inicializada | Bootstrap depende de bytes aleatorios | Inicializar estructuras antes de usarlas |
| Imagen de almacenamiento se corrompe | Fallo a mitad de escritura | Errores detectables y política de escritura consistente, aún por especificar |
| Depósito manual «mágico» | Dos agentes conducen el bus | Definir arbitraje/parada y pruebas eléctricas antes de afirmar viabilidad física |

## 8. Criterio de salida de esta planificación

**Documentado:** mapa de gasto propuesto, arranque cruzado→nativo, límites de herramientas, razones del overlay y pruebas de aceptación.

**Pendiente y no certificable:** medidas reales de ROM/RAM, código de firmware y assembler, circuitos de panel, tabla de opcodes, ABI, archivos ejecutables y prueba de persistencia. Estos pendientes son parte de **R1/R5/R7**, no de R0.2.

# R0.13: deuda de memoria del cargador AEX1

El [formato AEX1 propuesto](EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md)
establece 32 B de cabecera por contenedor (en almacenamiento, no RAM útil),
máximo de práctica 4064 B y máximo de herramienta 8160 B. Para no copiar
un programa incompleto, el modelo Python valida todo el contenedor en RAM
del **anfitrión** antes de crear una copia de RAM. El búfer de Aula-8
propuesto `0200–0FFF` ocupa **3584 B**, así que **no cabe** una imagen
completa de herramienta. Esto es una incompatibilidad explícita del diseño
provisional: habrá que medir alternativas de staging en bloques, recarga,
rollback o acotar imágenes antes de llamar «cargador real» a LOADX.
No se ha medido ROM ejecutable, mapas de enlace ni pila.

## R0.14: staging por bloque frente a atomicidad

El [modelo LOADX R0.14](LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.md)
calcula CRC16 del payload completo en primera pasada sin copiar,
y usa solo 256 B temporales en segunda pasada. **Es viable respecto
al presupuesto de búfer** de 3584 B, aunque no demuestra que la rutina
quepa realmente en 8192 B de ROM de firmware. Un fallo durante
la segunda copia **puede invalidar el código anterior** y dejar RAM
parcial: faltan compuerta real de ejecución, recuperación, mapa
de enlace y pruebas sobre CPU.
