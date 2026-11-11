# C28-P · Auditoría técnica del tramo final del libro

**Fecha:** 9 de noviembre de 2026. **Base:** global C28-H + atlas C28-O.
**Entrada real de Windows:** `Retroalimentacion_GLOBAL_C28H_20261109_162945.zip`.

## 1. Qué autorizó la retroalimentación

- **18/18 controles APROBADOS**, ninguno fallido o pendiente.
- Icarus Verilog compiló y simuló el controlador PC/MAR de C28-F y ambas
  políticas de lectura del piloto C28-H, en los vectores que registran
  sus testbenches.
- Se recuperaron **5/5 fotografías históricas**, con informe de licencia,
  procedencia y hash. El atlas C28-O se verificó como PDF de siete páginas.
- En el global recibido, el maestro **Word/PDF sigue siendo C28-G**, de
  248 páginas. El suplemento de lectura secuencial C28-H no fue insertado.

## 2. Qué se agregó en este avance

Se revisaron la progresión y los ejemplos representativos de los capítulos
**15–24, incluyendo 23B**, y se implementó
`scripts/c28p_auditar_tramo_final.py`. Este script usa solo Python estándar:

1. Lee 11 lecciones, detecta sus 50 referencias FIG y comprueba que
   existen PNG legibles en formato y SVG parseables, con pies descriptivos.
2. Enumera las **65.536 direcciones de byte**, separando RAM, expansión,
   MMIO, reserva y ROM; comprueba los ocho registros de bloques, seis de
   vídeo, 32 ranuras públicas y el vector RESET.
3. Contrasta el modelo CALL/RET con pila descendente y retorno little-endian
   para 14.337 posiciones iniciales de SP; comprueba anidamiento y la traza
   de 10 lecturas y 2 escrituras del capítulo 16.
4. Verifica el bucle `DEC/JNZ` para valores iniciales 1–255, incluidos el
   número de saltos tomados y la llegada final a cero.
5. Contrasta tamaños AEX1, bloques de 256 B, 4.096 pares positivos de
   Euclides por restas y valores relevantes de Fibonacci.
6. Examina los dos carriles de RAM de Aula-16, 16.384 direcciones de palabra
   par, las **32.768 posiciones de píxel** de 256×128 a 2 bpp, 512 celdas
   de texto y ROM de glifos de 2.048 B.

Se genera un JSON de evidencia en `c28_p/auditoria/C28_P_RESULTADOS.json`
y una matriz de figuras por capítulo en
`libro/MATRIZ_FIGURAS_C28P_15_A_24.md`. La matriz enlaza el propósito de
cada dibujo con su figura, pero **no equipara XML/PNG válido a netlist
eléctrica**.

## 3. Continuidad concreta de los 11 capítulos

| Cap. | Elemento nuevo que se integra | Regla examinada o riesgo abierto |
| --- | --- | --- |
| 15 | Fetch, decodificación, escritura | MDR recibe el dato R0 antes de WR; el piloto C28-H no decide PC anticipado/diferido |
| 16 | Pila y control de flujo | CALL guarda PC posterior a operandos; RET restaura little-endian y no borra RAM |
| 17 | Vector RESET y firmware | FFFC/FFFD forman E000; tabla pública no implica ROM compilada |
| 18 | Terminal, servicios y texto | C000/C002 son MMIO, distintos de API de FW_STATUS |
| 19 | Controlador de bloques | Transferencia completa de 256 B; LOAD/LOADX siguen indisponibles |
| 20 | Ensamblador y programas | 13 B de suma, 29 B de Euclides; referencia en anfitrión, no código ejecutado por Aula |
| 21 | Registros y ALU de 16 bits | 16 bits de datos no expanden automáticamente las 16 líneas de dirección |
| 22 | Bus externo Aula-16 | Dos carriles de ocho bits, palabras alineadas y bytes direccionables |
| 23 | Programación Aula-16 | Algoritmos sin codificación de ISA ni ejecutable Aula-16 |
| 23B | Texto y gráficos | 512 B de texto, 8192 B de bitmap, 2048 B de glifos y VRAM indirecta |
| 24 | Síntesis del recorrido | Modelo lógico, simulación HDL y hardware medido son evidencias diferentes |

## 4. Revisión visual focalizada

Se examinaron a escala de lectura siete gráficos de este tramo:

- `c15_fig03_preparar_escritura`: dato `6F` frente a `2A` antes de WR.
- `c16_fig03_llamadas_anidadas`: cuatro celdas de retorno y LIFO.
- `c17_fig02_mapa_memoria`: RAM 32 KiB, E/S y ROM 8 KiB.
- `c19_fig02_registros_controlador`: ocho registros pares de bloque.
- `c22_fig05_dos_bancos_aula16`: dos carriles de ocho bits en Aula-16.
- `p23v_fig03_pixeles_y_offsets`: 1 bpp pedagógico frente a 2 bpp V1.
- `c24_fig02_mapa_final`: partición ilustrativa de 64 KiB.

No se observaron cortes, solapamientos evidentes ni valores manifiestamente
ilegibles en estas siete muestras. **No** se afirma que las 50 imágenes
sean correctas transistor por transistor, ni que se haya inspeccionado
todavía cada página de las 248 del maestro.

## 5. Puertas pendientes antes del 100 % del libro

1. **Matriz circuito → tabla → HDL → dibujo:** para compuertas, latch,
   registro, selector, sumador, PC/MAR, lectura/escritura. La nueva matriz
   C28-P cubre localización editorial, no prueba topológica de cables.
2. **Decidir política del PC:** ambas alternativas del piloto C28-H han
   pasado pruebas bajo sus propios contratos; conservarlas como candidatas.
3. **Integrar el suplemento y atlas en el maestro:** actualizar tanto Word
   como PDF y el índice, sin reproducir fotografías sin atribución.
4. **QA íntegra:** lectura de estilo, ecuaciones, gráficos y paginación en
   las 248 páginas y las que se añadan.
5. **Publicación:** confirmar licencias de las fotos y coautorías; la
   creación y administración del repositorio remoto queda para después.

## 6. Barra de progreso explicada

El avance editorial pasa de **82 % a 84 % estimados** por auditoría dirigida
de los últimos once textos, la matriz de 50 figuras, las siete inspecciones
y la nueva suite de contratos. El desglose exacto está en
`libro/PLAN_CIERRE_EDITORIAL_C28I.md`. No es el porcentaje de una CPU
terminada, ni una medición automática; **el libro todavía no está cerrado**.

**Nueva prueba Windows esperada:** `LIBRO_C28P_TRAMO_FINAL`. Con los 18
controles previos, el próximo paquete podrá informar **19/19** si todos
vuelven a aprobar. Los resultados de Windows aún no han sido recibidos
para esta nueva prueba.
