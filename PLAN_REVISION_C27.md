# Plan de revisión C27 — De los conceptos a la construcción de Aula-8

**Actualización tras ejecutar el plan:** los bloques narrativos, nueve figuras
reproducibles, programas de RAM contigua, pinout PDIP-14, portada conceptual,
revisión visual y pruebas Word/PDF **se implementaron en C27-0.1**. La matriz
de trazabilidad está en `MATRIZ_TRAZABILIDAD_C27.md` y el balance real en
`libro/ESTADO_EDITORIAL_C27.md`. Siguen abiertos los esquemas eléctricos
integrales, hardware y firmware, licencias de fotografías históricas y revisión
humana final. Los párrafos siguientes conservan el plan original como registro
de decisiones anterior a su ejecución.

**Fecha de planificación:** 8 de noviembre de 2026.  
**Naturaleza:** plan editorial y técnico, no ejecución de C27 ni aprobación de una ISA.  
**Base protegida:** C26-0.1, 26 capítulos (24 troncales más 7B y 23B), 228 páginas PDF, 106 figuras, 156 ejercicios esenciales en edición maestra y 312 en fuentes/fascículos.

## 1. Diagnóstico y objetivo de aceptación

La estructura actual explica de manera progresiva electricidad, compuertas, memorias, buses, ALU, CPU y programación, pero **el lector no construye suficientemente pronto una misma Aula-8 acumulativa**. En C12 se ve la integración global de piezas que en capítulos anteriores aparecen principalmente como ejemplos conceptuales. La revisión C27 debe añadir conexiones, estado y pruebas de cada etapa, sin borrar los fundamentos.

**Definición de éxito:** tras C07, el lector puede identificar su primer subsistema Aula-8 y distinguirlo de un registro genérico; tras C09, explicar cómo lo conectaría a la memoria; tras C13, reconocer el datapath y la decisión de control; tras C16, seguir PC, SP, bytes y efectos de salto/llamada/retorno dentro de posiciones RAM contiguas; tras C20, entender el recorrido hasta un programa de interés, incluso si el hardware completo sigue siendo candidato.

## 2. Decisiones que C27 no debe alterar

- **Aula-8:** cuatro registros generales R0–R3 de 8 bits, ALU y bus externo de datos de 8 bits; direcciones, PC, SP y X de 16 bits.
- **Aula-16:** registros generales, ALU y bus externo de datos de 16 bits; direcciones de 16 bits, 64 KiB direccionables por byte, bancos alto/bajo, acceso a bytes pares/impares y palabras alineadas en la versión inicial.
- En ambas: convenio little-endian, flags Z/C/N/V y E/S mapeada en memoria. En Aula-16, las palabras impares no se ejecutan; un acceso a byte impar exige selección y direccionamiento del carril alto.
- **Vídeo lógico V1:** una pantalla con modos alternativos texto 32×16 y bitmap 256×128 a 2 bpp/cuatro colores, bancos de memoria separados, ROM de caracteres 256×8 = 2 KiB, interfaz MMIO indirecta por registros pares C020–C02A. No convertirlo en GPU, no usar simultáneamente los dos modos ni confundir VRAM con RAM de CPU.
- El encendido, ROM de firmware, ROM de microcontrol y ROM de caracteres son mecanismos distintos. El vídeo, el firmware y el control físico siguen sin implementar.
- La ISA Aula-8 R0.3, las secuencias de microcontrol, la ABI y los ejemplos binarios son **candidatos**. La ISA Aula-16 todavía no tiene codificación binaria definitiva. Ninguna figura puede insinuar que se ha ejecutado una CPU o verificado una placa física.
- El libro será didáctico y narrativo. La futura aplicación JavaFX reutilizará sus contratos, pero la tecnología de esa aplicación **no debe aparecer como dependencia dentro de los capítulos del libro**.
- La obra tiene 26 capítulos; 7B y 23B ya están titulados como capítulos y no se reabre esa decisión por inercia.

## 3. Trabajo priorizado y criterios de cierre

### P0. Auditoría de integridad y trazabilidad — bloqueante

1. Inventariar por capítulo: objetivo, ejemplo decisivo, figura, circuito o relación con Aula-8/Aula-16, pruebas documentales y nociones pendientes.
2. Contrastar cada mención técnica con `ARQUITECTURA.md`, datos estructurados de ISA/ROM/vídeo y hojas de datos cuando sea un componente comercial.
3. Separar evidencia en cuatro estados: documentado, verificado lógicamente, integrado en simulación y validado físicamente. No promover el estado de una pieza por la calidad de su dibujo.
4. Crear un índice de incidencias por capítulo con tipo, prioridad y resolución. Diferenciar defecto demostrado de ampliación voluntaria.

**Salida:** matriz de trazabilidad «concepto → componente Aula → figura → caso de prueba → estado de evidencia». No se generan todavía nuevos Word/PDF.

### P1. Hilo narrativo «Construimos Aula-8» — imprescindible

En puntos seleccionados, insertar una secuencia natural y recurrente, sin convertir cada sección en una plantilla repetitiva:

1. Qué pieza acaba de entender el lector y **por qué** la necesita Aula-8.
2. Qué entradas y salidas posee, y a qué pieza anterior se conectan.
3. Qué cambia en el circuito acumulado y qué todavía no puede hacer.
4. Una comprobación pequeña (tabla de verdad, dato conservado, transferencia o traza) con resultado y límites.

**Puntos de inserción:**

| Capítulos | Construcción acumulativa que debe verse | Límite de la afirmación |
| --- | --- | --- |
| 1–2 | Alimentación y conmutación mediante montajes didácticos independientes. | No construir toda la CPU con transistores discretos. |
| 3–4 | Señales combinacionales que servirán para selección/habilitación. | Compuerta comercial y tabla de verdad, no placa CPU. |
| 5–6 | Un bit almacenado, versión de D y reloj con niveles/flancos definidos. | Sin inventar timing de un chip no elegido. |
| 7 y 7B | Primer banco Aula-8 de 8 flip-flops, carga, conservación y significado del byte. | Distinguir registro del contenido y de su codificación. |
| 8–9 | Bus de 8 datos, 16 direcciones, decodificación y lectura/escritura RAM. | Selección exclusiva, triestado y requisitos eléctricos por confirmar. |
| 10–11 | Sumador, ALU y banderas unidos al banco de registros. | Comportamiento lógico independiente de velocidad física. |
| 12–13 | Repetir el circuito acumulado completo con datapath y unidad de control. | Microcontrol todavía candidato, no micro-ROM ejecutada. |
| 14–16 | Programa en RAM, fetch, PC, saltos, pila, CALL/RET. | Bytes provisionales claramente etiquetados. |
| 17–20 | RESET/monitor, texto de terminal, almacenamiento, herramienta de programación. | Modelo documental/anfitrión, no firmware nativo implementado. |
| 21–23B | Aula-16 como arquitectura distinta, bancos de 8 bits, vídeo V1 y registros. | No reciclar inadvertidamente buses u opcodes de Aula-8. |
| 24 | Síntesis de capacidades conseguidas y trabajo de ingeniería aún abierto. | No llamar «construida» a una CPU que sigue en proyecto. |

**Salida:** el lector puede señalar, en una figura acumulativa de cada hito, qué elemento se añadió y qué mecanismo lo utiliza. Evitar repetir una vista compleja si un acercamiento local enseña mejor.

### P2. Memoria contigua y flujo de programas — imprescindible

Basarse en los programas que ya aparecen en C14–C20 y en `ESCALERA_DE_PROGRAMAS_AULA8.md`, no inventar bytes independientes del contrato. Diseñar un lenguaje gráfico repetible:

- Columna vertical de direcciones RAM **consecutivas** y byte por dirección; al lado, opcode/operando o dato según el caso. Las direcciones omitidas se señalan expresamente con corte/continuación, nunca se aparenta que dos celdas distantes son contiguas.
- Flechas externas de flujo del **PC**, diferentes de líneas eléctricas de bus, sin atravesar etiquetas ni celdas.
- Indicadores de «leída», «ejecutada», «omitida», «destino» y «escritura»; leyenda breve en cada primera aparición.
- Mostrar bytes de destino en little-endian; por ejemplo `06 60` produce `0x6006` en un salto candidato de Aula-8.
- Programas pequeños para `JMP`, salto condicional tomado/no tomado, `CALL/RET` con pila descendente, `LD/ST` con dirección efectiva y acceso al firmware. Señalar en qué regiones hay código, datos, pila, MMIO y ROM.
- Para el caso CALL/RET, incluir **dos vistas sincronizadas**: instrucciones RAM con flechas PC y celdas contiguas de pila con SP, bytes de retorno y orden de escritura/lectura.
- Si el ensamblador o codificación no se ha aprobado, cada figura debe decir «ISA candidata», y el generador deberá tomar opcodes y longitudes de los JSON vigentes.

**Salida:** una familia de esquemas validados contra programas fuente y volcados de bytes, con una muestra piloto ya creada `aula8_memoria_contigua_salto_prototipo.svg`, aún **no incorporada** al PDF C26.

### P3. Diagramas fieles por niveles — imprescindible, alcance acotado

Los niveles se presentarán como objetos distintos:

1. **Funcional:** bloques CPU–registros–ALU–RAM; especificar anchos, direcciones y sentido de datos.
2. **Lógico:** compuertas, FF, MUX, lógica de decodificación, habilitación y casos de conflicto. Debe coincidir con tabla de verdad y estado.
3. **Esquema electrónico de componente seleccionado:** referencias, alimentación, pines, niveles, entradas no utilizadas, desacoplo y señales, conforme a hoja de datos. Requiere chequeos eléctricos y de temporización separados de los dibujos.
4. **Montaje de protoboard opcional:** solo para circuitos pequeños que realmente enseñan; numeración exacta de patillas, rieles, resistencias y advertencias sobre su naturaleza experimental.

**Selección inicial de casos ricos:** transistor+LED, NAND de integrado comercial, latch/FF, registro de 8 bits, decodificador de memoria, medio/full adder y arbitraje de bus. El conjunto completo de una CPU cableada con número de chip exacto **no** es condición editorial de C27. Las partes todavía no diseñadas se llaman «lógicas propuestas», no «esquema definitivo».

**Salida:** fuente estructurada de señales/conexiones reutilizable y validadores; SVG/PDF/PNG derivados de ella. Asegurar que el futuro taller y el libro no mantienen dos circuitos distintos.

### P4. Reescritura editorial selectiva — imprescindible

- Revisar los 26 capítulos como una historia causal; ampliar subapartados escuetos **solo cuando falten explicación, ejemplo o conexión con la máquina**.
- Reducir, fusionar o relegar ejercicios redundantes. No imponer seis por capítulo como cuota: los 156 de C26 son un techo provisional, no un objetivo de relleno. Mantener solución de todo ejercicio conservado.
- Añadir como mínimo una lectura de figura y una consecuencia práctica cuando se introduce un componente fundamental. El dibujo **no** reemplaza la explicación.
- Priorizar modos de direccionamiento inmediato, absoluto, indexado X+desplazamiento y relativo a SP con ejemplos de dirección efectiva. Diferenciarlos de regiones del mapa de memoria y del MMIO de vídeo.
- Fuentes externas reunidas en sección bibliográfica y `FUENTES_CONSULTADAS.txt`; citas puntuales en el cuerpo solo cuando hagan falta para atribución, seguridad, hechos históricos o cifras específicas. No escribir párrafos de justificación del propio proyecto.
- Evitar «ensayo experimental» y metaexplicaciones sobre agentes, herramientas, números de pruebas o producción dentro del texto narrativo. Conservar datos de auditoría en anexos/documentos técnicos.

**Salida:** capítulos didácticos con profundidad proporcionada a la importancia del tema, sin aumentar páginas por sí mismo.

### P5. Diseño visual, documentación histórica y portada — posterior al texto técnico

- Tomar como referencias de tono, **no para copiar diseños**: *De las matemáticas a la computadora* (Altair/maquinaria real, composición editorial sobria) y *El espacio de lo posible* (atmósfera cálida, tecnología material y sentido narrativo).
- Priorizar ilustraciones históricas en lugares donde el lector se beneficie del contexto: primeras microcomputadoras, panel frontal, memoria/computación de época y evolución de integración. Cada imagen llevará pie que identifique el objeto y procedencia.
- Portada original: microcomputadora didáctica retro Aula-8/Aula-16, mesa técnica, conexiones plausibles y elementos de época con interés humano. No representar la máquina como fotografía documental de una construcción que no existe.
- Verificar derechos/licencias y atribuciones antes de incorporar fotografías históricas; las imágenes técnicas **no** se generan con IA cuando exige precisión de patillas o cableado.

**Salida:** guía artística breve, inventario de imágenes con fuentes/derechos, portada y PDF maquetado **después** del cierre de capítulos y figuras técnicas.

### P6. QA del libro maestro y publicación — puerta final

1. Regenerar desde las fuentes reproducibles; ejecutar pruebas de capítulos y verificadores de contratos del repositorio.
2. Revisar diagramas completos en SVG, exportación PNG y páginas PDF reales: legibilidad, flechas, unidades, cruces y etiquetas no superpuestas.
3. Renderizar **todas** las páginas PDF y revisar un mosaico completo, luego páginas individuales de alto riesgo y una muestra distribuida por capítulos. No confundir contactos visuales pequeños con inspección detallada.
4. Revalidar los defectos corregidos en C26: circuito del capítulo 1, fórmulas `16⁰` (incidencia antigua de la p. 78) y figura de control con texto cruzado (incidencia antigua de la p. 119). La numeración puede desplazarse tras C27; localizar también por contenido.
5. Control de texto seleccionable, matemáticas, acentos, tablas, índice, saltos de página, portada, figuras y bibliografía. Asegurar que las soluciones corresponden al enunciado que finalmente quedó.
6. Contrastar ejemplos de RAM/ROM e ISA con fuente de datos; validar little-endian, saltos, PC/SP, números de bytes y ausencia de solapamientos de regiones. Revisar en particular los anchos **8/16** de cada bus.
7. Revisión manual de principio a fin y reporte de incidencias abiertas, cerradas y expresamente postergadas. Si hay defectos bloqueantes, C27 permanece «candidata».
8. Preparar ZIP global + parche, PDF/Word maestro, archivos fuente, inventario de figuras, resultados reproducibles y guía PowerShell de prueba/retroalimentación. No borrar C26 ni fascículos anteriores.

**Salida:** libro C27 verificable y acompañado de informe honesto de pruebas, limitaciones y pendientes.

## 4. Orden de trabajo y puertas de paso

| Fase | Qué se hace | Condición para avanzar |
| --- | --- | --- |
| A. Auditoría | P0 y selección de ejemplos/figuras de alto rendimiento. | Matriz de trazabilidad y lista de huecos reales, no intenciones vagas. |
| B. Prototipos | P1–P3 en C05–C09 y en un programa de C14–C16. | Un hilo de construcción y 2–3 figuras de memoria/circuito técnicamente coherentes. |
| C. Propagación | Aplicar el patrón aprobado al resto de C01–C24 y 7B/23B. | Conexiones acumulativas sin contradicciones ni excesos de longitud. |
| D. Pulido | P4, coherencia de ejemplos, ejercicios, terminología y fuentes. | Relectura continua satisfactoria. |
| E. Arte | P5: ilustraciones históricas, estilo y portada. | Calidad editorial y derechos documentados. |
| F. Cierre | P6: regeneración y auditoría Word/PDF, entrega y feedback. | Sin defectos bloqueantes; pruebas y estado de hardware honestos. |

No iniciar el trabajo E antes de B–D; el arte no debe esconder una incongruencia de circuitos. Tampoco iniciar la implementación JavaFX como atajo para producir ilustraciones antes de aprobar los contratos técnicos relevantes.

## 5. Qué NO es C27

- No es rediseñar Aula-8/Aula-16, agregar una GPU o alterar el mapa de vídeo V1.
- No es aprobar sin pruebas 36 opcodes candidatos o inventar el binario de Aula-16.
- No es certificar circuitos eléctricos, placa o rendimiento con diagramas bonitos.
- No es escribir un tutorial de KiCad/JavaFX/ensamblador de PC dentro del libro.
- No es duplicar bibliografías, ejercicios ni páginas solo para aparentar volumen.
- No es una reescritura ciega: conservar las buenas explicaciones y los defectos ya corregidos en C26.

## 6. Estado después de esta planificación

**Planeado, no ejecutado:** se ha fijado el orden de revisión y los criterios de aceptación. El PDF C26, sus fuentes y sus decisiones siguen intactos. No se ha regenerado ni publicado C27; los esquemas eléctricos completos, CPU ejecutable, firmware y taller todavía están pendientes.
