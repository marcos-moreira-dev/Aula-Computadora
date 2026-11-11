# C28-AC — De la teoría del libro a los planos reutilizables en la aplicación

**Estado:** planos vectoriales y modelo lógico listos para inspección; la CPU completa y el circuito eléctrico físico siguen sin estar cerrados. Estos activos amplían la etapa C28-AB sin modificar el Word/PDF maestro.

## Qué abrir primero

1. `activos_app/Visor_PASO_A_PASO_C28W.html` — abre con doble clic: muestra qué registra Aula-8 en cada flanco del reloj. Cambia operandos y operación; START, CLK, RESET.
2. `activos_app/AULA8_C28W_BUS_DATAPATH_8_LINEAS.svg` — plano editable en Inkscape, con las ocho conexiones del bus visibles en los tramos principales, captura A/B, ALU y registro del resultado.
3. `activos_app/ALU_BIT0_NAND_DESPLEGADO.svg` — abre en Inkscape el subcircuito real que influye en el bit S0 de la ALU. No es un dibujo inventado: procede de las conexiones del JSON C28-U.
4. `activos_app/Visor_ALU359_ZOOM.html` — visor ampliable, arrastrable y con buscador de las 359 NAND2. `ALU359_DIAGRAMA_COMPLETO.svg` es su original vectorial.
5. `activos_app/CMOS_NAND2_4_MOS.svg` — transistor a transistor **una sola** NAND2 de CMOS estático, dibujo de topología, no huella para protoboard.
6. `activos_app/AULA16_MEMORIA_DOS_BANCOS_16_LINEAS.svg` — ejemplo de dos bancos de RAM de ocho bits para Aula-16; arquitectura **candidata**, todavía no un circuito ensamblado.

Todas las figuras anteriores tienen PNG para revisión rápida. Los SVG son los originales editables; el HTML es demostrativo y funciona sin internet.

## 1. Cálculos comprobados: ALU Aula-8

Entrada de autoridad: `c28_u/netlists/alu8_seis_rutas_359nand.json`. La app consume una serialización del **mismo circuito** en `activos_app/Aula8_ALU359_APP_NETLIST.json` (`aula.circuito.logico.v1`), no una segunda topología escrita a mano.

| Magnitud | Cálculo | Resultado |
|---|---|---:|
| Entradas externas | A[7:0] + B[7:0] + 6 selectores ONE-HOT | 22 |
| Lógica aritmética ADD/SUB | Presupuesto del netlist original | 134 NAND2 |
| Lógica AND/OR/XOR/NOT A | Presupuesto del netlist original | 64 NAND2 |
| Selección de una de seis rutas | Presupuesto del netlist original | 136 NAND2 |
| Cálculo de Z | Presupuesto del netlist original | 22 NAND2 |
| Validez de C/V | Presupuesto del netlist original | 3 NAND2 |
| Total combinacional | 134 + 64 + 136 + 22 + 3 | **359 NAND2** |
| Terminales de entrada a compuertas | 359 × 2 | **718** |
| Terminales de salida del circuito serializado | S[7:0] + N + Z + C + V + CV_valid | 13 |
| Arcos de entrada + salidas publicados | 718 + 13 | **731** |
| Fuentes de señales nombradas | 22 entradas + 359 resultados NAND | **381** |
| MOS equivalentes solo en CMOS estático NAND2 | 359 × 4 | **1.436 transistores** |
| Mayor profundidad combinacional (ruta a salida) | Caminata sobre DAG de dependencias | **38 NAND2 consecutivas** |
| Fan-out lógico máximo | Conteo de patillas consumidoras de una señal | **30** (selector SUB) |

**Interpretación del número 1.436.** En NAND2 CMOS estático ideal se emplean dos PMOS en paralelo y dos NMOS en serie. Multiplicar **no** añade el coste de registros, flip-flops, buses de salida, buffers de señal, oscilador, controlador, memoria, protección y fuentes. Tampoco es una lista de compra de 1.436 transistores discretos: un diseño físico debe elegir familia, tecnología, encapsulados o celdas, etc. Hay compuertas que comparten una misma entrada en ambos pines; son dos conexiones a patillas en el cómputo anterior.

**Sobre la velocidad.** Treinta y ocho niveles es un número lógico, **no** 38 nanosegundos ni 38 ciclos de reloj. Para calcular tiempo real hacen falta modelos de transistor/celda, cargas y retardos de cableado, tensión, temperatura y buffers (el fan-out de 30 es una alerta). No es legítimo deducir frecuencia máxima ni disipación a partir del JSON ideal.

### Comprobación más amplia realizada

Se ha recorrido el producto cartesiano de A=0..255 y B=0..255 para las seis selecciones: `256 × 256 × 6 = 393.216` vectores. Se contrastaron S, N, Z, CV_valid y, cuando CV_valid=1, C y V contra un cálculo independiente. El resultado quedó registrado en `auditoria/C28_AC_RESULTADOS.json`.

Ejemplos de seguimiento:

| Operación | A decimal / binario | B decimal / binario | S decimal / binario | N | Z | C | V |
|---|---|---|---|---:|---:|---:|---:|
| ADD | 13 / `00001101` | 9 / `00001001` | 22 / `00010110` | 0 | 0 | 0 | 0 |
| SUB | 9 / `00001001` | 13 / `00001101` | 252 / `11111100` | 1 | 0 | 1 (préstamo) | 0 |
| XOR | 13 / `00001101` | 9 / `00001001` | 4 / `00000100` | 0 | 0 | no válida | no válida |

En operaciones lógicas, el campo `CV_valid=0` indica que no hay que interpretar las banderas C/V, aunque físicamente los pines tengan un valor binario. No hemos definido la política de FLAGS de una futura instrucción de CPU.

## 2. Qué se ha construido de la parte secuencial

C28-V dispone de tres registros RTL de 8 bits (`A_Q`, `B_Q`, `RESULT_Q`) y cinco bits de banderas. C28-W agrega controlador de cinco fases codificadas en **tres bits** y un bit para `RESULT_VALID`. **Hay 24 + 5 + 3 + 1 = 33 bits de estado RTL** en este módulo educativo. Esto no determina cuántos MOS serán los flip-flops físicos.

El controlador adopta flancos positivos:

| Flanco | Estado después del flanco | Consecuencia |
|---|---|---|
| t₀ | CAPTURA_A | Se acepta START; aún no se carga A_Q. |
| t₁ | CAPTURA_B | A_Q captura A_IN. |
| t₂ | CALCULA | B_Q captura B_IN. |
| t₃ | TERMINO | Se captura ALU→RESULT_Q y flags; DONE=1. |

Durante este proceso A_IN, B_IN y SEL deben mantenerse estables. RESET es **síncrono y solo resetea control/validez**; no deja registros A/B/RESULT a cero. START durante BUSY se ignora. Esto está representado en el visor de pasos, no se ha inventado un pipeline ni una CPU completa.

## 3. Aula-16: aritmética de capacidad candidata

Si se confirma memoria de **16 líneas de dirección por bytes**: `2^16 = 65.536` ubicaciones de byte = **64 KiB** de espacio direccionable. Dos bancos de 8 bits (par/impar) con **32.768 bytes por banco** constituyen la misma capacidad total, no el doble. A[15:1] son 15 señales compartidas; A0 distingue el byte par/impar. En acceso a palabra de 16 bits con alineación par, hay **32.768 palabras alineadas**. Ejemplo little-endian: palabra `0x1234` en `0x6000` → byte `0x34` en `0x6000` y `0x12` en `0x6001`.

El área de direcciones disponible no obliga a instalar físicamente 64 KiB de RAM; podrían existir ROM, E/S u otros bloques. La semántica definitiva de acceso de 8/16 bits y la ISA todavía deben confirmarse.

## 4. Cómo aprovechar esto en la aplicación futura

Arquitectura propuesta —aún sujeta al debate de UX/UI y tecnologías:

- **Modelo de dominio**: nodos `IN`, `NAND2`, `OUT`; cables `from`/`to` y nombre de señal, selectores ONE-HOT. El JSON de C28-AC sirve de punto de partida verificable.
- **Simulador lógico**: evaluación topológica de cada NAND y estados de registro por flanco; los mismos casos del verificador sirven para impedir regresiones.
- **Vista de circuito**: capas de esquemático (zoom, búsqueda y señal activa), diagrama de sistema CPU/RAM, pantalla de registro/ensamblador cuando esté definida la ISA. SVG editables para iconografía y diagramas estáticos; componentes interactivos de JavaFX (o tecnología aún por decidir) para animar y editar.
- **Edición de protoboard**: arrastrar, girar y encajar un transistor o compuerta, mostrar patillas **reales** y orificios conectados por filas/rieles, detectar conexiones abiertas y cortocircuitos. Este nivel requiere modelos eléctricos y geometría, y **no se ha implementado todavía**.
- **Reutilización**: el circuito se representa en datos estables; el dibujo puede cambiar sin reescribir las operaciones. Posibles acciones `colocar`, `rotar`, `conectar`, `desconectar`, `simular`, `retroceder`, más serialización de proyecto.
- **Trabajo colaborativo**: cuando comience el aplicativo, organizar repositorio, ramas, commits pequeños, pruebas automáticas y pull requests revisados con IA en GitHub; sus decisiones y la interfaz se discutirán contigo primero.

### Pendientes reales antes de hablar de circuito físico completo

1. Determinar componentes físicos, VDD, tecnologías PMOS/NMOS, modelo de retardo/consumo y requisitos de alimentación/tierras.
2. Elegir cómo materializar flip-flops, mux, reset, reloj y control; corregir/aislar cargas elevadas como el selector SUB.
3. Cerrar mapa de memoria, E/S, ISA y microcódigo si se pretende ejecutar programas de extremo a extremo.
4. Establecer si el aplicativo tendrá simulación **digital ideal**, simulación analógica de transistores o ambas; la segunda no se obtiene únicamente del diagrama NAND.
5. Debatir UX/UI de las vistas y validaciones didácticas contigo, antes de programar el editor de protoboard.

## 5. Reproducibilidad

Para verificar conexiones y resultados en Windows, haz doble clic en `PROBAR_C28AC_SOLO.cmd`. Equivale a `python scripts/c28ac_verificar_modelo_app.py`. Para la comprobación exhaustiva opcional: `python scripts/c28ac_verificar_modelo_app.py --exhaustivo` (requiere NumPy). Para regenerar planos: `python scripts/c28ac_generar_activos_app.py`, `python scripts/c28ac_generar_planos_sistema.py`, `python scripts/c28ac_generar_visor_pasos.py` (requiere Graphviz/Inkscape). El control global `PROBAR_TODO_GLOBAL_C28H.cmd` incorpora asimismo el nuevo chequeo portable cuando se disponga del proyecto completo.

**Criterio editorial:** incluir en el libro solo lo validado como circuito real o RTL y conservar el resto etiquetado `candidato`, para que el lector siga literalmente cómo nace la computadora sin confundir una maqueta de la interfaz con una placa eléctrica construida.
