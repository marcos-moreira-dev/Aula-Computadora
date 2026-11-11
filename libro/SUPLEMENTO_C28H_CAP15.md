# Suplemento para el capítulo 15: La memoria también tiene su ritmo

El contador de programa puede tener preparada la dirección del siguiente
byte; eso no significa que la memoria ya haya entregado el byte anterior.
Pensemos en una biblioteca. Colocamos sobre la mesa una ficha con el número
del libro que queremos. El bibliotecario busca la estantería, pero nosotros
no podemos fingir que el libro ya está sobre la mesa. Conservamos la ficha
y aguardamos una respuesta.

En nuestra computadora esa ficha es MAR, la orden de lectura se representa
por RD y el resultado llega a MDR. PC nos dice dónde buscar la próxima
instrucción. Al contrario que una función booleana instantánea, los tres
registros dependen de los flancos del reloj.

Hasta ahora hemos construido funciones lógicas y registros capaces de
guardar bits. ¿Qué nos falta para usarlos como una memoria de verdad? Un
acuerdo sobre el tiempo: cuándo enviamos la dirección, cuánto esperamos y
en qué momento una respuesta puede considerarse válida. El componente nuevo
no sustituye al registro de ocho bits: lo utiliza como el lugar donde
guardar el byte recibido. Así los conceptos dejan de ser una lista aislada
y se convierten en nuevas piezas de la misma computadora.

## Tabla de transición del controlador de lectura

| Estado previo | Condición | Acción en el flanco | Estado siguiente |
| --- | --- | --- | --- |
| Libre | `req=0` | Conservar registros; ignorar READY | Libre |
| Libre | `req=1` | Capturar MAR, activar RD, invalidar MDR anterior | Esperando |
| Esperando | `ready=0` | Mantener MAR y RD; conservar MDR | Esperando |
| Esperando | `ready=1` | Capturar MDR, desactivar RD, señalar aceptación | Libre |
| Cualquiera | `rst_n=0` | Reiniciar controlador y registros | Libre |

Si la solicitud era FETCH hay dos alternativas posibles. En C28-F se
incrementa PC al pedir el byte; en C28-G se hace al aceptarlo. El nuevo
piloto compara ambas y **todavía no convierte una en diseño final**. Si
pedimos un dato ordinario, como el byte de `0x6F00`, PC no avanza.

## Una escena con valores concretos

Partimos de PC=`0x6000`. Pedimos un byte de instrucción y MAR conserva
`0x6000`. Si READY permanece en cero durante dos flancos, MDR no puede
declarar que el dato es válido. Cuando READY pasa a uno y el byte `0x32`
se captura, MDR vale `0x32`; en la alternativa diferida PC pasa a `0x6001`.
Una segunda lectura puede comenzar entonces.

La tabla de estados muestra **qué sucede**; el diagrama temporal muestra
**cuándo**. El esquema funcional muestra **qué elementos intervienen**.
Las tres ilustraciones contestan preguntas distintas y se necesitan juntas
cuando queremos construir algo verificable.

## Del concepto a una prueba que podemos repetir

1. La tabla anterior define el comportamiento esperado de la lectura.
2. El modelo Python aplica miles de secuencias de entrada y guarda los
   valores que deberían tener PC, MAR, MDR y las señales de control.
3. El archivo Verilog describe registros que cambian de estado en un
   flanco; Icarus contrasta las mismas entradas con el resultado esperado.
4. El SVG dibuja el recorrido de la solicitud y del dato. Más adelante,
   sintetizar el RTL permitirá dibujar puertas y conexiones concretas;
   el dibujo funcional actual todavía no es ese esquema de puertas.

Cuando los resultados se correspondan, habremos comprobado el **protocolo
digital ideal** de este bloque, no que una memoria comercial responde en un
tiempo determinado. Después usaremos el mismo método para escribir datos,
unir los buses y completar una instrucción de principio a fin.

## Lo que hemos comprobado y lo que no

El modelo de Python produjo 24.248 comprobaciones y vectores de referencia.
En la auditoría digital C28-H de Windows del 9 de noviembre de 2026,
Icarus Verilog confirmó 12.124 vectores por cada una de las dos políticas
de PC, sin discrepancias. Esta evidencia sí valida el comportamiento
digital ideal descrito por ese RTL bajo los casos ensayados; no valida la latencia
de una SRAM comercial, la retención eléctrica, el arbitraje de un bus,
los retardos del reloj ni un montaje físico. Antes de construir una placa
habrá que seleccionar componentes, leer sus hojas de datos y medir.

*Nota editorial*: el piloto HDL ya se simuló en Windows. Integrar la
explicación al Word/PDF maestro cuando se revise su encaje didáctico y
se decida la política de avance del PC. Hasta entonces, ambas son candidatas.
