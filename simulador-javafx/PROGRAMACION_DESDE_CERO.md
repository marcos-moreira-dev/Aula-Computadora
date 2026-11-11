# Programación desde cero: panel, monitor, editor y ensamblador

**Estado:** R0.1, contrato pedagógico y plan técnico. **No** hay firmware ni herramientas ejecutables todavía. La sintaxis de los ejemplos es ilustrativa mientras la ISA y el ABI permanezcan pendientes en R1.

## 1. Propósito verificable

Una persona debe poder entender cómo se pasa de una computadora que solo ejecuta instrucciones binarias a otra que **permite escribir, ensamblar, guardar y ejecutar programas utilizando sus propios recursos**.

El orden de aprendizaje es deliberado:

1. Introducción manual de bytes en RAM, con CPU detenida.
2. Arranque desde ROM y monitor hexadecimal por terminal.
3. Carga de utilidades desde almacenamiento persistente a RAM.
4. Editor de líneas y ensamblador **nativos** ejecutándose en Aula-8.
5. Mini sistema de archivos y un intérprete de comandos simple.
6. Compilación cruzada de MiniC-Aula en el anfitrión. Un compilador MiniC *nativo* es ampliación posterior, no requisito de V1.

La progresión también se documentará en Aula-16, reusando algoritmos y recompilando para su ISA distinta. No se supone que un ejecutable de Aula-8 funcione sin cambios en Aula-16.

## 2. Una distinción que no se puede perder

| Capa | Dónde reside el programa | Quién ejecuta su lógica | ¿Qué aprende el alumno? |
| --- | --- | --- | --- |
| Panel manual | Circuito de entrada / interfaz de enseñanza | Lógica de depósito independiente de CPU detenida | Direcciones, datos, RAM y señales de control |
| Monitor de ROM | 0xE000–0xFFFF | **CPU Aula** tras RESET | Firmware, bus y operaciones por teclado |
| Editor de líneas | RAM, cargado desde almacenamiento | **CPU Aula** | Texto, buffers y edición mínima |
| Ensamblador nativo | RAM, cargado desde almacenamiento | **CPU Aula** | Símbolos, traducción y binario |
| MiniOS y comandos | ROM mínima + utilidades en RAM | **CPU Aula** | Archivos, servicios y programas |
| Ensamblador o MiniC cruzado | Equipo anfitrión | CPU anfitriona durante compilación; Aula ejecuta el resultado | Toolchain, ABI y archivo ejecutable |

El simulador podrá ofrecer un editor **del anfitrión** como comodidad para importar ejemplos, pero debe marcarlo como herramienta externa. No atribuir a la CPU Aula trabajo de análisis, ensamblado o compilación ejecutado en Java.

## 3. Etapa 0: consola de interruptores

### Comportamiento didáctico

- Panel con dirección de 16 bits, dato de 8 bits, indicadores luminosos y controles conceptuales `EXAMINAR`, `DEPOSITAR`, `SIGUIENTE`, `EJECUTAR` y `DETENER`.
- `DEPOSITAR` escribe **un byte** en RAM; el usuario observa dirección, dato y pulso de escritura.
- `SIGUIENTE` aumenta dirección; permite cargar un programa byte a byte.
- `EXAMINAR` muestra el contenido sin escribir ni ejecutar.
- `EJECUTAR` arranca en una dirección RAM seleccionada cuando exista un programa válido.
- Si se intenta escribir en ROM o en un registro de E/S por el mecanismo de depósito, mostrar un error explícito; el panel educativo inicialmente solo deposita en RAM.

### Limitación eléctrica real

Un conjunto de interruptores **no** puede escribir arbitrariamente la memoria mientras la CPU conduce los mismos buses. En una implementación física se necesita detener o aislar a la CPU y conceder el control de dirección, dato y `WE` a la lógica del panel. El esquema exacto —bus grant, multiplexores o controlador de depuración— es **PENDIENTE de R1**. En el simulador, la operación debe registrar la misma regla de propiedad exclusiva del bus.

Para Aula-16 el panel puede conservar una entrada de datos **de 8 bits** y depositar bytes sucesivos; el bus externo del procesador sigue siendo **de 16 bits**, con selección de banco/carril. No simular que esa interfaz convierte el bus principal en uno de 8 bits.

### Práctica inicial

Una vez congelados los opcodes, preparar un programa de pocos bytes (por ejemplo, escribir en un LED mapeado o emitir un carácter). Entregar tabla `dirección / byte hexadecimal / significado / estado esperado`. **No** inventar bytes de máquina antes de R1.

## 4. Etapa 1: monitor residente en ROM

### Secuencia de arranque

1. Se programa previamente la EEPROM de firmware con una imagen compilada fuera de Aula, mediante un programador apropiado; una ROM vacía no genera herramientas espontáneamente.
2. RESET consulta el vector de 0xFFFC–0xFFFD y transfiere control al firmware.
3. Firmware inicializa pila, terminal, variables y búferes imprescindibles. No depende de ceros iniciales en RAM.
4. Firmware presenta prompt y acepta órdenes en texto.
5. El monitor interpreta comandos e invoca rutinas reales de lectura/escritura, arranque y E/S.

### Conjunto mínimo de comandos

| Comando conceptual | Función | Disponibilidad |
| --- | --- | --- |
| `HELP` | Mostrar ayuda breve | ROM |
| `MEM addr [longitud]` | Inspeccionar bytes | ROM |
| `POKE addr byte` | Modificar un byte de RAM | ROM |
| `REG` | Mostrar registros/flags si el mecanismo de depuración lo permite | ROM, contrato pendiente |
| `RUN addr` | Ejecutar en dirección indicada | ROM |
| `LOAD` | Cargar un tramo o utilidad desde bloques | ROM o servicio auxiliar, según presupuesto |
| `SAVE`, `DIR`, `TYPE` | Guardar/listar/leer archivos | **Posteriores** a la capa de almacenamiento y directorio |

En el [borrador R0.11](ROM_MONITOR_AULA8_R0_11_BORRADOR.md) se propone `RUN` mediante `CALL` a la ventana de práctica `6000–6FFF`; **RET** con pila equilibrada regresa al prompt y **HALT** detiene la CPU sin retorno automático. `POKE` interactivo solo admite esa ventana provisional para evitar daños sobre búferes del monitor y pila; `MEM` admite RAM/ROM dentro de un único rango legible. REG/LOAD permanecen sin implementación. Esta propuesta deberá confirmarse en R1/R5 con CPU real.

### Ejemplo de sesión **ilustrativo**

~~~text
AULA-8 MONITOR
AULA> MEM 6000 04
6000: A4 00 7F 91
AULA> POKE 6000 A5
AULA> MEM 6000 01
6000: A5
~~~

Los bytes iniciales son arbitrarios: no se presupone RAM con ceros al encender. El monitor debe rechazar `POKE` en ROM, direcciones fuera de rango, entrada hexadecimal inválida y comandos incompletos. Un `POKE` de byte es también válido en dirección impar de Aula-16 si el carril está correctamente implementado.

## 5. Etapa 2: cargar herramientas desde almacenamiento

- El almacenamiento lógico usa bloques de **256 bytes** respaldados por imagen persistente.
- El [borrador R0.12](CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md) propone ocho registros MMIO en C010–C01E y `LOAD bloque_hex4 destino_hex4 cantidad_hex2`. Sería necesario leer el bloque completo en el búfer protegido antes de copiarlo; la orden sigue **NO DISPONIBLE** hasta escribir el firmware Aula y comprobar CPU/bus. Si falla un bloque, no ejecutar el programa parcialmente cargado.
- Primer ejercicio: leer **bloques crudos** a un rango RAM previamente reservado, verificar integridad y ejecutar un programa cuyo punto de entrada es conocido.
- Segundo ejercicio: introducir un encabezado de ejecutable y un directorio mínimo **cuando** estén definidos los campos, longitudes, validación de rangos y reserva de memoria.
- Tercer ejercicio: permitir `LOAD EDITOR` y `LOAD ASM` mediante nombres o identificadores de archivo; no prometer nombres hasta implementar el directorio.
- Las herramientas se generan originalmente con **ensamblador cruzado** y se copian a la imagen. Una vez cargado el ensamblador nativo, debe poder producir los mismos bytes que el ensamblador cruzado para un subconjunto común.

Sin almacenamiento o sin sistema de archivos, `SAVE HOLA.ASM` todavía no tiene semántica real. Las lecciones pueden conservar primero el texto solo en RAM y advertir que se perderá al cortar energía.

## 6. Etapa 3: editor de líneas nativo

### Diseño funcional mínimo

- Terminal de texto ASCII y **edición por líneas numeradas**. No teclado de flechas, ratón, pantalla de ventanas ni editor de pantalla completa.
- `NEW`: borrar **el documento activo en RAM** previa confirmación. No borrar archivos persistentes sin autorización.
- `EDIT nombre` o `EDIT`: abrir un documento cargado o nuevo, según exista la capa de archivos.
- `10 ...`, `20 ...`: introducir/reemplazar líneas con número.
- `LIST [inicio] [fin]`: listar texto.
- `DELETE numero`: borrar línea seleccionada, con confirmación opcional en el contexto de aprendizaje.
- `SAVE nombre` y `LOAD nombre`: solo cuando exista capa de archivos.
- `QUIT`: regresar al monitor, con aviso si hay cambios no guardados.

Una implementación sencilla puede conservar pares `(número de línea, longitud, bytes ASCII)` ordenados, más un búfer de entrada. Fijar límites explícitos de líneas, caracteres por línea y tamaño del texto, y notificar `OUT OF MEMORY` sin corrupción. Cadenas con números decimales son únicamente una **interfaz del editor**, no direcciones RAM ni opcodes.

### Sesión ilustrativa

~~~text
AULA> EDIT HOLA.ASM
10 INICIO:
20   LDI R0, 65
30   CALL FW_PUTC
40   HALT
.LIST
10 INICIO:
20   LDI R0, 65
30   CALL FW_PUTC
40   HALT
.SAVE
~~~

Los nombres `FW_PUTC` y `LDI` son simbólicos; operandos finales, formato, bytes y política de retorno están pendientes de ISA/ABI. No atribuir tamaños binarios ficticios al ejemplo.

## 7. Etapa 4: ensamblador nativo de Aula-8

### Alcance de primera versión

1. Un fichero de entrada ASCII a la vez.
2. Instrucciones de Aula-8 ya definidas en ISA.
3. Números hexadecimales/decimales y referencias a etiquetas.
4. Directivas esenciales de byte, palabra, reserva y origen; sintaxis exacta pendiente.
5. Traducción **en dos pasadas**: asignación de direcciones/etiquetas y generación de bytes con resolución de referencias.
6. Diagnósticos con número de línea: instrucción desconocida, literal inválido, símbolo duplicado/no resuelto, operandos incompatibles, exceso de memoria y dirección ROM no escribible.
7. Resultado binario en RAM, con dirección inicial y límites identificados; `RUN` solo después de validar el resultado.

No exigir macros, enlazador general, bibliotecas complejas, optimización, depuración simbólica completa ni lenguaje C dentro de Aula-8.

### Dificultad y presupuesto de RAM

Los **32 KiB** de RAM deben repartirse entre firmware mutable/búferes, monitor, pila, código de editor/ensamblador, texto fuente, símbolos, binario de salida y área para ejecutar el programa. No fijar particiones con direcciones absolutas sin medir tamaño de binarios. Exigir un **mapa de memoria del proceso**, no solo la afirmación «cabe».

Una línea de trabajo viable es ejecutar el editor y el ensamblador **por turnos** y reutilizar parte de su memoria; el fuente se mantiene en un área de trabajo común. La estrategia concreta requiere tamaños reales, protección frente a solapamientos y pruebas de casos límite.

La propuesta numérica de *overlay*, y sus limitaciones, está en [PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md](PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md). Sigue siendo una **hipótesis** hasta disponer de código máquina y mapas de enlace.

### Criterio de autenticidad

El código del ensamblador nativo debe ser leído como instrucciones del **CPU Aula** y alterar RAM mediante sus propias operaciones. El anfitrión puede comparar el resultado como oráculo, pero **no** sustituir silenciosamente las dos pasadas del ensamblador dentro del modo nativo.

## 8. Etapa 5: mini sistema operativo

Objetivo modesto: cargar programas, mostrar directorio y leer/escribir archivos, sin multitarea ni aislamiento de procesos.

- Protocolo de bloque con errores/estado definidos.
- Directorio mínimo y política de nombres; bloque libre/ocupado y persistencia ante reinicio.
- Formato ejecutable: versión, CPU destino, punto de carga, entrada, longitud y control de integridad por definir.
- Comandos orientativos: `DIR`, `TYPE`, `LOAD`, `RUN`, `SAVE`, `DEL` (con confirmación) y ejecución de utilidades.
- Programas de usuario pueden llamar a la tabla estable de firmware; utilidades posteriores usan wrappers para evitar acoplarse a direcciones internas.

No llamar «SO» al monitor mínimo por el mero hecho de mostrar un prompt. Distinguir **monitor de firmware**, **cargador**, **sistema de archivos** y **shell**.

## 9. MiniC-Aula: alcance conservado

- **Primera entrega:** compilador **cruzado** que corre en la Dell G3; produce ejecutables para Aula-8 o Aula-16.
- **Al ampliarse el proyecto:** explorar compilador MiniC reducido *nativo* o intérprete compacto, después de medir RAM, velocidad y representación del código fuente.
- Nunca prometer un compilador C completo, ni alterar la ISA, la pila o el mapa de memoria para acomodarlo sin registrar una decisión.

## 10. Lecciones y pruebas de aceptación

| ID | Lección / estímulo | Evidencia exigida |
| --- | --- | --- |
| BP-01 | Depositar byte y examinarlo | Escritura solo en RAM con CPU detenida y bus sin doble conductor |
| BP-02 | Intentar depósito en ROM | Rechazo visible, contenido ROM sin cambios |
| BP-03 | Depositar byte en dirección impar de Aula-16 | Banco/carril correcto sin rebajar ancho del bus |
| MON-01 | RESET con RAM arbitraria | Monitor inicia sin suponer RAM inicial en cero |
| MON-02 | POKE ROM o comando inválido | Error reproducible, sin escritura indebida |
| MON-03 | RUN y retorno/fin | Transición definida, no prompt ficticio tras HALT |
| ED-01 | Crear, reemplazar, listar y borrar una línea | Texto intacto y ordenado |
| ED-02 | Límite de memoria y salida sin guardar | Error controlado y aviso, sin corrupción |
| ASM-N-01 | Dos pasadas, etiquetas hacia delante | Mismos bytes que ensamblador cruzado |
| ASM-N-02 | Etiqueta indefinida/duplicada | Diagnóstico con línea y sin ejecutar resultado inválido |
| ST-01 | Guardar, apagar, reiniciar y cargar | Archivo recuperable íntegro de imagen de bloques |
| ST-02 | Archivo con CPU destino incompatible | Rechazo antes de escribir/ejecutar memoria |
| BOOT-01 | Editor/ensamblador cargados desde imagen | Se ejecutan efectivamente sobre la CPU Aula |

## 11. Dependencias para el libro y trabajo futuro

- **R1:** congelar ISA/ABI, operación exacta de RUN/HALT, mecanismo de parada y propiedad del bus, acceso del controlador de bloques y formato de programas.
- **R4, capítulo 14:** primeros bytes máquina y panel manual.
- **R5, capítulos 17–20:** ROM ya programada, monitor, editor de líneas, ensamblador nativo, archivo persistente y MiniC cruzado; explicar las dependencias, no enumerarlas sin mostrar una sesión completa.
- **R6:** recompilar herramientas para Aula-16, comprobar bancos y compatibilidad de datos/archivos.
- **R7 y R8:** modelo lógico y luego interfaz 2D/3D del panel/terminal con pruebas de que las herramientas nativas ejecutan instrucciones de Aula.

### Fuentes históricas de contraste

- MITS, [*Altair 8800 Operators Manual* (1975)](https://vtda.org/docs/computing/MITS/MITS_Altari8800OperatorsManual_1975.pdf): `DEPOSIT NEXT`, carga manual por interruptores.
- MITS, [*Altair 8800 Theory of Operation* (1975)](https://vtda.org/docs/computing/MITS/MITS_Altair8800TheoryOperation_1975.pdf): el circuito real del panel interviene en los buses y la CPU; no son interruptores «mágicos».
- Apple Computer, [*Apple-1 Operation Manual* (1976)](https://device.report/m/52627e26d76bf7b0639394eca3b3471d97580b7e6f2e743a079ccd4fede03833): monitor hexadecimal de ROM, consulta, depósito y ejecución por terminal.
- MOS Technology, [*KIM-1 User Manual* (1976)](https://www.kim-1.com/docs/usrman.htm): teclado hexadecimal, ejecución, programas volátiles y persistencia histórica externa.

Los manuales son referencias históricas, **no** licencias para copiar sus textos, esquemas, interfaces exactas o código de firmware. Aula usa ISA, rutinas, gráficos y ejemplos propios.

# Carga ejecutable AEX1 R0.13: propuesta posterior al LOAD crudo

La [cabecera AEX1](EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md) podría acompañar
programas nacidos del ensamblador cruzado o del futuro ensamblador nativo.
Permite indicar CPU Aula-8, dirección de carga, entrada, tamaño y CRC16.
El comando futuro `LOADX` prevalidaría estos datos antes de copiar solo los
bytes útiles. **No existe hoy ensamblador que emita código Aula ni ROM que
ejecute LOADX**; el packer Python únicamente envuelve un binario preexistente.
RUN R0.11 no sirve para el overlay y el búfer de 3584 B es insuficiente
para retener la herramienta máxima de 8160 B: ambos puntos requieren una
decisión de ingeniería en R1.

## R0.14: nueva propuesta de LOADX de dos pasadas

La [verificación/copia incremental](LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.md)
separa **validez del archivo** de **permiso para ejecutar**. Su
referencia anfitriona ya puede prevalidar un paquete AEX1 grande
sin retenerlo completo: usa un bloque temporal de 256 B y luego
relee antes de copiar. Una falla tardía obliga a recargar y
**prohibir** el salto al código parcial. Esto todavía no está
implementado en el monitor de ROM; RUN permanece restringido
y la entrada del overlay requiere supervisión. No hay editor
ni ensamblador nativos ejecutándose en Aula-8.
