# Aula-8 R0.13 — formato mínimo AEX1 para programas cargables

> **PROPUESTA NO APROBADA.** AEX1 es una cabecera binaria experimental, un
> empaquetador y un verificador Python **del anfitrión**. No hay ensamblador,
> firmware, LOADX nativo, CPU ejecutable ni interfaz de almacenamiento físico.

## 1. Por qué un binario crudo no basta

En R0.12 podemos leer el sector 0002 y copiar 256 bytes a RAM. Sin embargo,
los bytes no nos dicen si son de Aula-8, dónde deberían empezar, cuánto
programa es útil ni qué instrucción constituye la entrada. Peor aún:
podríamos copiar por accidente un archivo dañado sobre el futuro editor.

**AEX1** es una etiqueta de 32 bytes delante de un programa de Aula-8 que
declara estos datos. No es un sistema de archivos: el propietario todavía
debe saber **en qué bloque numérico** empieza la imagen.

Un ejemplo original: los cuatro bytes candidatos de Aula-8
`11 00 2A 02` se quieren depositar en `0x6000`. El contenedor guarda
primero 32 bytes de cabecera y luego el programa: `32 + 4 = 36` bytes;
se completa el primer bloque de **256 bytes** con 220 ceros.
Cuando se cargue, la cabecera **no se copia** a RAM; los bytes de instrucción
empiezan exactamente en `0x6000`.

## 2. Cabecera AEX1, offsets contados desde cero

Todos los enteros de 16 bits se escriben **little-endian** (octeto bajo
primero). Los offsets siguientes son hexadecimales.

| Offset | Bytes | Campo | Regla |
| --- | ---: | --- | --- |
| `00–03` | 4 | Firma ASCII | `AEX1` = `41 45 58 31` |
| `04` | 1 | Versión | `01` |
| `05` | 1 | CPU destino | `08` = Aula-8; rechazo de otras |
| `06` | 1 | Tipo | `01` práctica, `02` herramienta |
| `07` | 1 | Flags reservados | `00` obligatorio |
| `08–09` | 2 | Origen RAM | u16, alineado a 256 bytes |
| `0A–0B` | 2 | Entrada | u16, dentro del programa |
| `0C–0D` | 2 | Bytes útiles | u16, mayor que cero |
| `0E–0F` | 2 | CRC programa | CRC-16/CCITT-FALSE sobre bytes útiles |
| `10–11` | 2 | Número de bloques | incluye cabecera y relleno |
| `12–13` | 2 | CRC cabecera | CRC-16/CCITT-FALSE de offsets `00–11` |
| `14–1F` | 12 | Reserva | doce bytes `00` obligatorios |

La función matemática del número de bloques es:

\[
N_{\text{bloques}}=\left\lceil\frac{32+L_{\text{programa}}}{256}\right\rceil.
\]

Por ejemplo, 384 bytes útiles ocupan `ceil(416/256) = 2` bloques;
la cabecera ocupa solo el comienzo del primer bloque. El resto
del último bloque tiene que estar relleno de ceros.

**CRC elegido:** CRC-16/CCITT-FALSE, polinomio `0x1021`,
estado inicial `0xFFFF`, sin reflexión ni XOR final. El texto
ASCII `123456789` produce `0x29B1`. Es detección de errores
accidentales, **no** firma criptográfica ni prueba de autenticidad.

## 3. Dos ventanas de RAM; ninguna otra

| Tipo | Código | Ventana de RAM | Máximo útil comenzando al inicio |
| --- | --- | --- | ---: |
| Programa de práctica | `01` | `6000–6FFF` | 4064 bytes (16 bloques) |
| Editor o ensamblador candidato | `02` | `1000–2FFF` | 8160 bytes (32 bloques) |

No basta con que el último byte quede en RAM: **la ventana y el tipo deben
coincidir**. El origen ha de acabar en `00`, el tamaño útil debe ser al menos
un byte, y la entrada debe cumplir `origen ≤ entrada < origen + tamaño`.
Se rechazan ROM, MMIO, pila, código que cruce el fin del espacio reservado,
tipo desconocido, origen desalineado y cabecera con bits no definidos.

El máximo útil es menor que el tamaño de ventana porque los 32 bytes
del encabezado **consumen almacenamiento en bloques**, aunque no RAM:
una práctica de 4096 bytes útiles necesitaría 17 bloques con AEX1.
El objetivo es restringir también el presupuesto de sectores del paquete.
Se podrá definir otro empaquetado más adelante, previo análisis de capacidad.
Estos límites no prueban que el editor o ensamblador vayan a caber.

## 4. Dos formas de carga, separadas

- `LOAD 0002 1000 02` sigue siendo la **propuesta cruda R0.12**:
  copia dos bloques de 256 bytes sin cabecera. Permanece NO DISPONIBLE.
- `LOADX 0002` es una **nueva sintaxis candidata**: lee primero el
  encabezado de AEX1 en el bloque `0002`; comprueba todos los bloques
  requeridos, los CRC, las posiciones, la CPU y el relleno; solo después
  dejaría copiar **únicamente el programa útil** a la RAM indicada.
  Permanece igualmente NO DISPONIBLE.

Ejemplo de prevalidación de `LOADX 0002`:

1. Leer bloque 0002 y descifrar los 32 primeros bytes. No escribir RAM.
2. Rechazar tipo/CPU/versión desconocidos, rango RAM prohibido y bloque
   de origen fuera del dispositivo.
3. Calcular bloques necesarios y comprobar que existan desde 0002.
4. Leer **todo el contenedor** y comprobar CRC y relleno antes de copiar.
5. Solo si todos los controles pasan, copiar el **payload**, jamás cabecera.
6. Informar dirección de entrada. **No ejecutar automáticamente**.

Este planteamiento evita **una carga parcial causada por un bloque corrupto
dentro de un mismo AEX1** si el cargador dispone de un área temporal íntegra
suficiente. **Hay una dificultad pendiente importante:** el búfer `0200–0FFF`
del presupuesto R0.2 tiene **3584 bytes**, menor que los 8160 bytes útiles
máximos del editor/ensamblador candidato. El modelo anfitrión puede retener
todo AEX1 en memoria, pero una ROM real con RAM limitada **no puede prometer
carga íntegramente atómica** sin resolver esto. Se deberá optar entre un
contenedor menor, otra estrategia de staging/rollback, o verificar cada
bloque antes de copiar con una segunda lectura estable. No se fija
la solución ni se afirma que LOADX sea implementable con ROM/RAM actual.
Tampoco hay protección frente a la modificación simultánea de la imagen,
fallos de alimentación, código malicioso o colisiones con programas residentes.

El monitor `RUN` de R0.11 solo admite `6000–6FFF`. Un editor cargado en
`1000–2FFF` necesita **mecanismo supervisado de entrada diferente**;
el encabezado AEX1 no concede permisos de ejecución ni convierte un byte
arbitrario en una instrucción válida. Incluso una entrada dentro del payload
podría señalar al medio de una instrucción: sin CPU/ISA definitivas no se
certifica el código.

## 5. Packer y verificación reproducibles, únicamente en el anfitrión

Crear un paquete desde un `programa.bin` que ya exista:

~~~powershell
python scripts/empaquetar_aex_aula8_r0_13.py crear --bin programa.bin --out programa.aex --origen 6000 --entrada 6000 --tipo practica
python scripts/empaquetar_aex_aula8_r0_13.py inspeccionar --archivo programa.aex
python scripts/verificar_ejecutable_aula8_r0_13_borrador.py
~~~

El empaquetador no fabrica instrucciones, no ensambla MiniC, **no sobrescribe
archivos de salida existentes** y produce únicamente una secuencia de bloques.
No inserta esta secuencia en una imagen de disco por defecto: se pueden
escribir sus bloques secuenciales en la imagen de referencia R0.12 durante
pruebas. Ni la función `preview_load_ram` ni `stage_from_block_image` son
firmware: validan y generan una **nueva copia de RAM simulada en Python**.

## 6. Qué debe revisarse antes de R1

- Confirmar nombres y bytes del formato AEX1, CPU target, CRC y tipo.
- Resolver el desfase entre área de staging y tamaño máximo del overlay,
  sin borrar fuente, símbolos, pila ni otras regiones residentes.
- Dimensionar rutinas de carga, verificación y reporte de errores en ROM
  con mapa de enlace **real**, y no adjudicar slots públicos ROM sin ABI.
- Completar ISA/CPU Aula-8; después ejecutar de verdad un programa cargado
  desde la imagen y comparar contra un intérprete independiente.
- Especificar imágenes de Aula-16 **por separado** con bus externo de
  **16 bits**. El byte `08` en AEX1 **no** autoriza cargarlo en Aula-16.

**Resultado R0.13:** formato y modelo validables en anfitrión, no binario
ejecutable certificado, no loader en la CPU y no editor nativo implementado.
