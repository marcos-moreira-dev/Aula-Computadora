# Auditoría visual y de progresión — C28-A

**Fecha:** 8 de noviembre de 2026  
**Base preservada:** Aula-Computadora C27-0.1, PDF maestro de 236 páginas  
**Alcance de esta entrega:** inventario completo, primera inspección visual, piloto lógico R0 y prioridades; **no reedición del PDF maestro**.

## Qué se comprobó de manera efectiva

1. Se recuperó una copia separada del ZIP global C27; su estructura ZIP fue
   comprobada y no se alteró la edición original.
2. En los capítulos hay **115 referencias a figuras**, correspondientes a
   **115 SVG y 115 PNG** del mismo identificador. Los PNG se abrieron y
   verificaron. No se detectaron rótulos fuera de los límites del lienzo ni
   colisiones texto-texto mediante el análisis geométrico aproximado.
3. Se generaron **10 hojas de contacto** que muestran las 115 figuras y se
   hizo una **primera lectura visual de todas**. La matriz CSV identifica
   por separado las imágenes que necesitan inspección individual.
4. Se amplió `c13_fig01_unidad_control.png` a su resolución original. En la
   edición C27 consultada, «despacho y condiciones» aparece **debajo** de
   la línea de conexión, sin cruzarla; la captura anterior de Marcos mostró
   un defecto que no debe reaparecer en una futura composición del PDF.
5. Se diseñó y probó el piloto R0; ver `../piloto_registro8/LEEME_C28_A.md`.
6. Se rasterizaron y revisaron las páginas físicas **78, 119 y 205** del
   maestro C27. La 78 presenta una lectura razonablemente clara; en la 119
   se detecta tipografía matemática problemática para literales hexadecimales
   (por ejemplo, `0x12FF` aparece espaciado como `0 x12 FF`). En la **205**
   aparecen expresiones con nombres completos convertidos a seudovariables
   matemáticas con guiones bajos, como
   `Dirección_de_palabra_válida_en_V1`: la idea es comprensible, pero la
   presentación no es apta para un libro final. Son **defectos confirmados**
   del propio PDF C27, no solo sospechas de las capturas antiguas.

**Limitación expresa:** el detector automático no busca intersecciones entre
**líneas eléctricas y texto** ni verifica distancias tras escalar los gráficos
al PDF. La revisión de miniaturas sirve para clasificar; **no certifica**
que las 115 figuras estén libres de problemas al imprimirse o verse en el
libro. Faltan comprobaciones individuales a escala de la página final.

## Correcciones prioritarias para la siguiente pasada

| Prioridad | Figura o zona | Acción editorial o técnica |
|---|---|---|
| 1 | **Capítulo 7**, `c07_fig01`, `c07_fig05` | Insertar/componer los dos esquemas R0 del piloto: celda detallada y ocho carriles, con texto narrativo. Los cuadrados antiguos pueden quedar como resumen, no como única descripción del circuito. |
| 1 | **Capítulo 13**, `c13_fig01` | Mantener resuelta la distancia de «despacho y condiciones» respecto al conductor; inspeccionar el PDF una vez que las figuras se vuelvan a colocar. |
| 1 | **Capítulo 1**, `c01_fig01` y `c01_fig04` | Comprobar rótulos junto al cable y continuidad real de los contactos de protoboard; no representar una tira continua como filas independientes. |
| 1 | **Capítulos 8 y 22**, buses | Conservar los buses agrupados para una visión general, pero añadir vistas por carriles cuando se explique qué cable transmite qué bit. Diferenciar siempre Aula-8 (datos 8) y Aula-16 (datos 16; dos carriles de 8). |
| 1 | **Capítulo 14**, `c14_fig05` y `c14_fig06` | Preservar el mapa RAM contiguo y las flechas de salto que ya existen; verificar al ampliar que el PC, el opcode y las filas objetivo correspondan exactamente. |
| 2 | **Capítulo 6**, `c06_fig01` | Examinar los caminos del latch D y el inversor: prevenir cruces de texto, líneas sin nodo y una falsa apariencia de conexión eléctrica. |
| 2 | **Capítulos 10, 11 y 16** | Inspeccionar a tamaño completo sumadores, recorridos de pila, saltos y rótulos pequeños, con verificación de aritmética y direcciones. |
| **1** | **PDF C27, páginas físicas 119 y 205** | Corregir la maquetación de expresiones como `0x12FF` y nombres textuales con `_` forzados a notación matemática. Evitar que la `x` de hexadecimal parezca una multiplicación; usar estilo monoespaciado para bytes y direcciones. |
| 2 | **Todas las páginas con fórmulas** | Comprobar exponentes, subíndices y ceros de expresiones en base 16; revisar la antigua incidencia de página 78 después de repaginar. |
| 3 | **Todo el volumen** | Encontrar secciones demasiado breves, ejercicios redundantes, fuentes incrustadas en el discurso y transiciones que hablan del concepto sin mostrar su uso en Aula-8. |

## Política de figuras para el libro definitivo

- **Circuitos didácticos muy simples:** símbolos claros, suficiente espacio,
  unidad o polaridad indicadas, sin necesidad de SPICE ni protoboard ficticio.
- **Circuitos reutilizables:** esquema lógico fiel, misma semántica que el
  simulador, nombre de señales y casos de prueba de cambios de estado.
- **Circuitos físicos o de temporización compleja:** elegir integrados,
  dibujar en un EDA, comprobar reglas eléctricas, simular cuando el modelo
  lo permita y documentar las hipótesis. Un render bonito no sustituye eso.
- **Prototipo en protoboard:** solo si se puede dibujar la distribución real
  de nodos y carriles sin errores; junto al esquema, no en su lugar.

Las ilustraciones históricas y la portada generada por IA se dejan para una
fase visual posterior: no deben intervenir en diagramas donde la posición
de una línea o un bit tenga significado técnico exacto.

## Secuencia de trabajo sin cerrar el libro prematuramente

1. **C28-A, ahora:** inventario completo + lectura de miniaturas + modelo de
   un registro R0 con esquemas y pruebas (realizado como piloto).
2. **C28-B:** inspección del PDF página a página, reparación de diagramas y
   fórmulas, integración didáctica del registro y revisión de las transiciones
   concepto → pieza construida.
3. **C29:** completar contratos de módulos siguientes (ALU, MAR/MDR, señales
   de buses, árbitro, RAM y control); distinguir explícitamente propuestas
   de elementos ya probados. Si se cambia ISA, buses, ABI o mapa de memoria,
   solicitar acuerdo previo.
4. **C30:** simulación digital progresiva y esquema EDA por módulos, más
   verificaciones automatizadas; solo después, primeros módulos del taller
   JavaFX, que representarán esos mismos contratos.
5. **Cierre editorial:** nuevas capturas técnicas verificadas, portada IA,
   ilustraciones históricas, legibilidad integral, licencia, índices y PDF
   final. No publicar como «circuito probado físicamente» lo que es lógica
   simulada.

## Archivos útiles

- `matriz_115_figuras.csv`: 115 filas, estados de inspección y prioridades.
- `contactos_01.jpg` … `contactos_10.jpg`: diez hojas de miniaturas.
- `alertas_texto.txt`: salida del filtro geométrico (vacía cuando no halló
  colisiones aproximadas; **no** implica ausencia de cruces cable-texto).
- `../../scripts/c28_auditar_figuras.py`: regeneración de esta inspección.
- `../piloto_registro8/`: contrato, dibujos y código de comprobación.
