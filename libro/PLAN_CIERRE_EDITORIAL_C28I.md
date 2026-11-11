# Ruta de cierre editorial del libro Aula-Computadora

**Actualización:** 9 de noviembre de 2026. **Alcance:** el LIBRO, no una
computadora física terminada ni un programa externo.

## Estimación razonada de avance

**88,5 % de madurez editorial estimada (C28-T)**. No es una cifra arrojada por un
verificador automático: es una estimación de gestión del trabajo, basada en
entregables y en los pendientes conocidos. Recalcularla después de las
auditorías de capítulos y figuras; no confundirla con validación electrónica.

**C28-O, 9 de noviembre:** la retroalimentación de esa fase confirma **17/17
controles aprobados en Windows** y **5/5 fotografías históricas descargadas**.
Se han cotejado visualmente las cinco imágenes, registrado sus autores,
licencias, fuentes y SHA-256, y compuesto un **atlas PDF de siete páginas**
con cinco conexiones a conceptos del libro y una página de créditos.
El atlas es un material **suplementario**: el PDF/Word maestro C28-G de
248 páginas sigue intacto. La nueva prueba autónoma de los cinco activos
y el atlas elevó el conjunto a **18 controles**, posteriormente aprobados
**18/18** en la retroalimentación `20261109_162945` de Marcos.
El progreso de aquella fase subió **80 → 82 %**, no por descargar ficheros,
sino por revisión visual, tratamiento didáctico, atribuciones e inventario
de la obra para conservarla y publicarla.

| Frente del libro | Peso | Cumplimiento estimado | Aporte al total |
| --- | ---: | ---: | ---: |
| Redacción de 26 capítulos (24 + 7B y 23B) | 30 % | 100 % | 30,0 |
| Edición maestra Word/PDF e integración | 15 % | 90 % | 13,5 |
| Hilo didáctico concepto → pieza → computadora | 15 % | 96 % | 14,4 |
| Tablas, esquemas 2D y correspondencia circuito/figura | 15 % | 80 % | 12,0 |
| Pruebas digitales de circuitos esenciales del libro | 10 % | 79 % | 7,9 |
| Lectura editorial y control visual de principio a fin | 10 % | 72 % | 7,2 |
| Fuentes, licencias de imágenes y preparación de publicación | 5 % | 70 % | 3,5 |
| **TOTAL** | **100 %** | — | **88,5 %** |

Puntos de partida confirmados: están los 26 capítulos y sus fascículos,
un PDF maestro C28-G de 248 páginas, figuras y ecuaciones; desde C27 existen
20 conexiones narrativas explícitas entre aprendizaje y construcción.
**C28-H permanece como suplemento**, todavía fuera de Word/PDF maestro.
**C28-O suma un atlas histórico complementario** en
`libro/ediciones/C28_O/`, pendiente de decidir dónde integrar sus láminas
en el libro final y de comprobar de nuevo el renderizado completo del maestro.

**Avance de la fase 1, auditoría C28-J:** el nuevo inventario reproducible
`AUDITORIA_PROGRESION_C28J.md` encontró 26 fuentes, 115 referencias a
figuras con sus PNG/SVG, 20 encabezados explícitos «Construimos Aula…»,
y **cero fallos estructurales**. Seis capítulos (01, 02, 04, 7B, 23, 24)
no usan ese encabezado; su desarrollo causal se debe evaluar leyendo el
texto, sin equiparar la falta de título a falta de aprendizaje. La
comprobación no cambia todavía la estimación editorial ponderada de 77 %.

**Auditoría visual de inventario C28-J:** la herramienta histórica de
figuras se actualizó para aceptar los nueve SVG de pilotos C28 que aún no
están citados en el libro. Se verificaron las 115 figuras referenciadas,
se regeneraron diez hojas de contacto y se obtuvieron **cero alertas
geométricas automáticas**. Esto no sustituye cotejar cada diagrama con
su tabla, fuente HDL o requisitos eléctricos. La revisión a detalle
seguirá guiándose por `scripts/c28_auditar_figuras.py` y su matriz.

**Auditoría parcial C28-L (capítulos 1–7B):** se revisó el puente entre
electricidad, transistores, compuertas, realimentación, flancos y registro.
`AUDITORIA_LOGICA_C28L_01_A_07B.md` documenta la lectura; un script
reproducible superó **131.144 comparaciones de lógica ideal** sobre NAND,
XOR, funciones construidas con NAND, latch SR, latch D, flip-flop D y
registro de ocho bits. La cifra está dominada por la enumeración exhaustiva
del registro; **no demuestra cableado eléctrico ni correspondencia de todos
los trazos de las figuras**. Quedan el examen detallado de los circuitos,
la lectura de capítulos 8–24 y la actualización editorial del maestro.
En la etapa C28-L la estimación ponderada **permaneció en 77 %**,
porque aquellas pruebas cubrían solo los fundamentos iniciales.

**C28-M — avance real hasta 80 %:** después de confirmar en Windows los
15/15 controles anteriores, se inspeccionó la progresión dirigida de los
capítulos 8–14 y figuras representativas, además de sus contratos
matemáticos. El informe `AUDITORIA_C28M_MEMORIA_ALU_ISA_08_A_14.md`
documenta **196.620 vectores** de decodificación, ADD, SUB y sumadores,
el programa de ocho bytes LDI/ST/HALT y la consistencia de los 36 opcodes
del borrador ISA. Se añade la comprobación de ejemplo de 8 lecturas,
1 escritura y PC=0x6008, **sin presentarlo como CPU simulada**.

La subida de **77 a 80 puntos** se obtiene revisando tres frentes:

- Continuidad didáctica **80 % → 90 %**, aporta **+1,5 puntos** por
  contrastar la progresión concepto → pieza de capítulos 8–14.
- Pruebas matemáticas **55 % → 65 %**, aporta **+1,0 punto** por modelos
  exhaustivos del sumador, ALU y mapa de memoria.
- Revisión editorial/visual **55 % → 60 %**, aporta **+0,5 puntos** por
  lectura técnica dirigida y cuatro láminas inspeccionadas.

Los demás pesos no cambian. El número es **estimativo y reproducible en
su desglose**, no una certificación física o el porcentaje de páginas
aprobadas por un corrector automático.

**C28-O — de 80 a 82 puntos:** el frente de permisos y fuentes pasa del
30 al 70 %: cinco fotografías recibidas de la máquina de Marcos, con
metadatos y huellas completos, examinadas visualmente y reutilizadas en un
atlas didáctico de siete páginas. Faltan el montaje definitivo de imágenes
en el maestro, referencias cruzadas, revisión global y requisitos de
publicación. **Los demás frentes permanecen constantes**.

**C28-P — de 82 a 84 puntos:** recibido el control **18/18 aprobado**,
se recorrieron los once textos 15–24 (incluido 23B), se relacionaron sus
**50 figuras** con las fuentes PNG/SVG y se inspeccionaron visualmente siete
diagramas representativos. Un nuevo verificador independiente contrasta
casos de CALL/RET, JNZ, memoria/ROM/MMIO, bloques/AEX1, Euclides, Fibonacci,
bancos Aula-16 y offsets de vídeo. El incremento de **+2,0 puntos** se divide
en continuidad didáctica **90 → 95 %** (+0,75), pruebas de contratos
**65 → 72,5 %** (+0,75) y lectura/inspección visual **60 → 65 %** (+0,50).
No se presenta la estructura de 50 figuras como certificación de circuitos,
ni se modifica el maestro C28-G. La prueba adicional se llamará
`LIBRO_C28P_TRAMO_FINAL`; el nuevo conjunto espera **19 controles** en Windows.

**C28-Q — de 84 a 85 puntos:** llegó la evidencia Windows **19/19
APROBADO**. Se definieron y probaron desde los JSON de conexiones las
redes NAND de XOR (4 puertas), latch SR (2), selector PC C28-D (51) y
PC/MAR C28-F (177). Se contrastaron cuatro vectores XOR, trece casos
ideales SR, 8.336 combinaciones C28-D y 32.768 C28-F. El cotejo
dirigido de rutas SVG y tabla de patillas se documenta en
`INFORME_C28_Q_RED_NAND_Y_RTL.md` y la matriz
`libro/MATRIZ_CIRCUITOS_C28Q.md`. La correspondencia de circuitos y
figuras sube de **60 a 65 %** (+0,75 puntos) y las pruebas digitales
de **72,5 a 75 %** (+0,25 puntos). El global añade una auditoría
Python y dos pares de compilación/simulación Icarus, por lo que su
**siguiente objetivo es 24/24 controles en Windows**, todavía por
confirmar. Ni los dibujos ni los netlists constituyen fabricación,
mediciones de electricidad o CPU integrada. El maestro C28-G sigue
intacto.

**C28-R/S — de 85 a 87,3 puntos:** Marcos confirmó **24/24 controles
Windows en C28-Q**. C28-R desarrolla una red combinacional explícita de
**134 NAND** para la ruta aritmética ADD/SUB de ocho bits, con **131.072
vectores** exhaustivos sobre resultado, C7/Cout, C (acarreo/préstamo),
V, N y Z. El Verilog derivado del mismo modelo y su testbench quedan
pendientes de compilar/simular en Windows. No se implementó el selector
de operaciones lógicas ni la CPU. C28-S inspecciona automáticamente las
**248 páginas PDF**, **17.216 fragmentos textuales** y **127 bloques de
imagen** del maestro: cero cajas fuera de página o caracteres U+FFFD.
Se abrieron ocho hojas de contacto; **no equivale a leer 248 páginas
al tamaño final**. La edición Word/PDF original no se modificó.
La nueva suite tiene **28 controles previstos**: +1 Python C28-R,
+1 Python C28-S y +2 para compilación/simulación Icarus C28-R.
Incrementos ponderados: correspondencia circuito/figura **65 → 73 %**
(+1,2 puntos), pruebas digitales **75 → 79 %** (+0,4 puntos) y revisión
global **65 → 72 %** (+0,7 puntos). El nuevo 87,3 % sigue siendo una
estimación de libro, no de hardware construido ni páginas certificadas.

**C28-T — de 87,3 a 88,5 puntos, sin nuevas pruebas:** se añadieron
dos láminas originales en SVG y PNG, la topología etiquetada de las
nueve NAND de un sumador completo y la ruta completa de ADD/SUB de
ocho bits con presupuesto 32+72+4+4+22. El suplemento
`SUPLEMENTO_C28T_DEL_BIT_A_134_NAND.md` recorre las señales y
los acarreos con ejemplos, la interpretación de C/V/N/Z, y el límite
entre netlist digital y circuito eléctrico; un mapa de inserción
registra dónde encajaría en C4/C10/C11. La continuidad didáctica
**95 → 96 %** aporta **+0,15** y la correspondencia circuito/figura
**73 → 80 %** aporta **+1,05**. Las otras categorías permanecen iguales.
**No se ejecutó una nueva ronda de pruebas, no se modificó el Word/PDF
maestro C28-G ni se certificó hardware.** La suite prevista de 28 controles
continúa sin confirmación Windows.

## Fases que quedan para considerar cerrado el libro

### 1. Matriz didáctica y lectura causal de los 26 capítulos

Recorrer cada capítulo con una hoja de control de cinco preguntas:

1. ¿Qué concepto nuevo comprende el lector, en lenguaje accesible?
2. ¿Qué **pieza concreta de Aula-8 o Aula-16** construye o utiliza gracias a él?
3. ¿Qué señales entran y salen, qué estado conserva y cómo se interconecta?
4. ¿Qué figura y qué tabla/ejercicio permiten comprobarlo en papel?
5. ¿Qué pieza reaprovechamos en el capítulo siguiente, sin contradicciones?

Completar los enlaces faltantes y eliminar referencias prematuras a módulos
todavía no explicados. Proteger la diferencia entre Aula-8 y Aula-16.

### 2. Auditoría lógica y gráfica de circuitos didácticos prioritarios

Establecer una matriz con **identificador único de cada circuito**, definición
funcional, tabla de verdad/transiciones, archivo HDL/modelo, testbench,
resultado de pruebas y figura de libro. Priorizar:

- Puertas NAND/NOT/AND/OR y ejemplos combinacionales elementales.
- Latch/flip-flop, registro, contador y selector de señales.
- ALU, indicadores y selección de bus.
- PC, MAR, MDR, memoria y protocolo de lectura con espera.
- Trayecto ilustrativo de fetch/decode/execute y saltos/pila.

Una figura 2D puede mostrar un **bloque funcional**, un **esquema lógico
de puertas**, o un **esquema eléctrico**: deben etiquetarse de forma distinta.
Icarus Verilog permite simular HDL y guardar formas de onda; un flujo de
síntesis/diagramación puede convertir la descripción en conexiones 2D.
**Renderizar un dibujo no demuestra por sí solo su funcionamiento**. No
afirmar que un esquema funcional es un cableado fabricable. No todas las
ilustraciones conceptuales necesitan un netlist eléctrico.

### 3. Reconciliar los pilotos C28 con el manuscrito

- Contrastar los resultados C28-A/D/E/F/G/H con los ejemplos del libro.
- Mantener **PC anticipado** y **PC diferido** como alternativas candidatas,
  sin canonizar una de ellas antes de que Marcos decida.
- Integrar el suplemento C28-H al capítulo 15 únicamente cuando su explicación
  y alcance hayan sido revisados; actualizar entonces el Word/PDF maestro,
  el índice y las referencias cruzadas.
- Distinguir explícitamente pruebas de modelo Python, simulaciones Verilog,
  dibujos vectoriales y pruebas físicas, que son cuatro evidencias diferentes.

### 4. Revisión integral de la edición

Leer los 26 capítulos en orden; revisar precisión, terminología, progresión,
ejemplos hexadecimales, figuras legibles, pies de figura, tablas y ejercicios.
Renderizar todas las páginas del Word/PDF regenerado y revisar páginas de
alto riesgo a resolución de lectura. No basta con que el PDF abra.

### 5. Derechos, bibliografía y entrega final

Verificar procedencia y licencia de fotografías históricas, citas y elementos
ajenos; sustituir por dibujos propios cuando corresponda. Preparar una
edición final descargable, con fuentes Word/Markdown, PDF maestro, activos
gráficos reproducibles y registro de las pruebas que efectivamente pasaron.

## Criterios de cierre: cuándo decir «libro terminado»

- El lector logra seguir el paso **concepto → circuito/pieza → integración**
  sin saltos esenciales en los 26 capítulos.
- Las figuras electrónicas importantes coinciden con su fuente de diseño y
  tienen estados de verificación honestos; las no validadas están identificadas.
- El PDF final se inspecciona página por página y coincide con el Word y el
  índice, sin ecuaciones rotas, texto cortado ni imágenes ilegibles.
- Las fuentes y permisos están documentados y los errores críticos cerrados.
- Se delimita expresamente lo que es **modelo educativo** y lo que todavía
  requiere diseño, construcción y pruebas de electrónica real.

La **construcción física de la computadora, el firmware ejecutable y el
software complementario** tienen sus propias hojas de ruta. Su ausencia
no impide cerrar una edición pedagógica si se describe con honestidad su
alcance y no se presentan prototipos ficticios como certificados.
