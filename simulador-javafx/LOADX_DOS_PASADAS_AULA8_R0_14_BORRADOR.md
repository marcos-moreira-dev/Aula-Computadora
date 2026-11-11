# Aula-8 R0.14 — LOADX con búfer pequeño y dos pasadas

**PROPUESTA NO APROBADA.** Un modelo Python en el anfitrión demuestra
que se puede **comprobar** un contenedor AEX1 de hasta 8160 bytes útiles
sin retenerlo íntegro en un búfer de RAM de Aula-8. Aún no hay CPU ni
firmware reales y **la carga no es atómica**.

## 1. El problema de los 3584 bytes

En el mapa provisional de Aula-8, el búfer del monitor ocupa
`0x0200–0x0FFF`, es decir:

\[
4096-512=3584\ \text{bytes}.
\]

Una herramienta AEX1 máxima del overlay contiene **8160 bytes útiles**,
y 32 bytes de cabecera, distribuidos en **32 bloques de 256 bytes**. Por
tanto, no podemos prometer almacenar allí una copia íntegra de ese programa.

Se distinguen tres conceptos que no deben confundirse:

1. **Verificar antes de escribir:** confirmar que el archivo parece válido.
2. **Copiar a RAM:** modificar la ventana donde correrá el programa.
3. **Ejecutar:** conceder control a la dirección de entrada.

R0.14 ensaya una ruta viable en espacio de búfer para los dos primeros,
pero **no implementa el tercero en CPU Aula**.

## 2. Dos lecturas completas usando solo un bloque temporal

El controlador de R0.12 entrega un bloque de **256 B** por operación READ.
Para un AEX1 que comienza en el bloque 0002, el algoritmo candidato es:

**Primera pasada: prevalidación**

1. Leer sector 0002 y verificar firma, versión, CPU, tipo, origen,
   entrada, longitud, bloque requerido y CRC16 de cabecera.
2. Confirmar que todos los sectores declarados existen.
3. Leer todos los sectores uno por uno; omitir los primeros **32 B**
   de cabecera del sector inicial y los ceros de relleno al final.
4. Actualizar un CRC16 incremental sobre **solo el programa útil**.
5. Rechazar error de lectura, CRC incorrecto, padding no nulo o
   cambio de la cabecera entre lecturas.
6. Hasta aquí: **cero escrituras en RAM de programa**.

**Segunda pasada: copia controlada**

1. Volver a leer, en el mismo orden, los bloques AEX1.
2. Confirmar que la cabecera no cambió desde el inicio.
3. Copiar al destino autorizado **únicamente** los bytes útiles,
   en fragmentos de como máximo 256 B, calculando otro CRC incremental.
4. Si el CRC final y las demás comprobaciones siguen siendo válidos,
   informar una **entrada candidata** para una ejecución supervisada futura.
5. Si ocurre algún fallo, **no autorizar la ejecución**. Puede quedar
   RAM modificada parcialmente; debe tratarse como programa inválido.

La cabecera no ocupa RAM del programa. No se modifica el formato AEX1,
el protocolo de ocho registros del controlador R0.12 ni el comando `LOAD`
crudo. `LOADX bloque_hex4` continúa **NO DISPONIBLE** en el monitor.

La secuencia consume aproximadamente **una lectura de cabecera adicional**
más dos lecturas completas del AEX1; en un máximo de 32 sectores,
el modelo realiza **65 lecturas de bloque**. Es un conteo del algoritmo,
**no** una medida de ciclos de CPU, tiempo de EEPROM ni ancho de banda.

## 3. Qué garantiza y qué NO garantiza

| Situación | Resultado del modelo de anfitrión |
| --- | --- |
| CRC o sector defectuoso en primera pasada | Se rechaza sin modificar RAM |
| Cabecera cambia antes de copiar | Se rechaza sin copiar bytes de programa |
| Datos cambian en segunda pasada | Puede quedar copia parcial, pero NO entrada habilitada |
| Último bloque falla después de copiar otros | RAM parcial; NO ejecutar |
| Ambos recorridos verifican | Entrada candidata para ejecución **supervisada futura**, sin ejecutar CPU |
| Se corta la energía durante la copia | **No ensayado**; RAM y recuperación no garantizadas |
| Archivo cambia después de la última lectura | **No garantizado**; CRC16 tampoco proporciona autenticidad |
| Programa contiene opcode inválido | Fuera del alcance: sin CPU ni ISA congelada |

Como se puede ver, dos pasadas **no convierten** RAM en una transacción
atómica. La solución evita almacenar 8160 B en el búfer, pero necesita
una regla que **impida ejecutar** un programa si la segunda pasada falló.
El monitor R0.11 todavía **no implementa esa regla en firmware**, por lo
que tampoco se ha demostrado que un usuario no pueda invocar RUN de otra
forma tras un fallo. La carga del overlay además requiere que el controlador
esté ejecutándose desde ROM y que no esté sobrescribiendo instrucciones
actualmente activas.

Una futura implementación con recuperación fuerte deberá decidir entre:

- Invalidar estado de programa previo y usar una bitácora/puntero de
  confirmación, si las memorias y el sistema lo permiten.
- Mantener dos slots de código y conmutar un puntero al final, **lo que
  requiere más memoria** de la presupuestada.
- Aceptar explícitamente cargas fallidas parcialmente y exigir reinicio
  de la carga, con un control efectivo de RUN/entrada supervisada.

Ninguna de estas estrategias está aprobada o validada electrónicamente.
El objetivo actual es **no mentir sobre atomicidad** y preservar el diseño
físicamente razonable de un único búfer de 256 B.

## 4. Modelo Python y pruebas

La referencia [modelo_loadx_aula8_r0_14.py](../scripts/modelo_loadx_aula8_r0_14.py)
reabre bloques desde una imagen del [controlador R0.12](CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md)
y respeta la [cabecera AEX1 R0.13](EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md).
Solo usa un bloque temporal de lectura de 256 B; en Python también
materializa **una copia de 32 KiB de RAM de referencia** para poder comparar
antes y después. Esa copia es un instrumento de prueba del anfitrión,
**no memoria temporal del futuro firmware**.

~~~powershell
python scripts/verificar_loadx_aula8_r0_14_borrador.py
~~~

Las pruebas insertan fallos en ambas pasadas, mutan datos entre lecturas,
comprueban imágenes de 1, 16 y 32 bloques y protegen RAM fuera de las
ventanas permitidas. No hay aún ROM, ensamblador, editor nativo, bus
electrónico o señal de ejecución real. Aula-16 conserva bus externo de
**16 bits** y formato ISA separado.

## 5. Decisión pendiente de R1

Antes de proclamar `LOADX` implementado hacen falta:

- Programar y **medir** el monitor ROM que lee el MMIO de bloques.
- Definir una marca de «programa no ejecutable» que el RUN de práctica
  y la entrada de herramientas realmente respeten en CPU.
- Elegir qué pasa si se sobrescribe código anteriormente válido.
- Comprobar la memoria compartida con terminal, pila, editor, fuente,
  ensamblador y símbolos.
- Probar interrupción real de lectura, reinicio y estabilidad del
  almacenamiento frente a alteraciones durante ambas pasadas.

**Conclusión:** se resolvió la necesidad de retener el paquete entero
para **verificarlo**, pero no la atomicidad de su instalación ni la
ejecución de programas en Aula. No ampliar otra R0 sobre esto sin evidencia
de firmware/CPU: el siguiente paso relevante es el contrato R1 y la
redacción real del libro.
