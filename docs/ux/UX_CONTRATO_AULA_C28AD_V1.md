# Aula-Computadora — contrato de experiencia y correspondencia técnica

**Versión:** UX-V1 (10–11 de noviembre de 2026)  
**Carácter:** especificación de producto y UX propuesta; no equivale a una aplicación implementada, una placa fabricable ni una ISA terminada.

## 1. Propósito y límites

Producto educativo de escritorio JavaFX con dos recorridos cerrados: Aula-8 y Aula-16. El estudiante construye, comprueba y hace funcionar una computadora hipotética siguiendo desafíos delimitados. Meta de diseño: cada recorrido completo debe poder finalizarse en hasta cinco horas de actividad continua; esto requiere validación posterior con usuarios.

- **Aula-8:** construcción guiada con placa didáctica 3D y esquema digital 2D.
- **Aula-16:** construcción guiada desde cero, en 2D; reutiliza conocimientos y patrones de Aula-8, no necesariamente sus programas binarios.
- **Fuera de alcance V1:** editor de PCB de fabricación, simulador analógico universal, protoboard libre con infinitas piezas, familias arbitrarias de CPU, proyectos abiertos, 3D de Aula-16, cursos gamificados con distracciones.
- **Distinción pedagógica:** el esfuerzo necesario para aprender una operación es legítimo; repetir centenares de conexiones idénticas no lo es.

## 2. Decisiones de usuario confirmadas

1. **Piezas incorrectas:** pueden permanecer en posiciones admitidas; el resultado se observa y comprueba. Solo se diagnostican causas con evidencia suficiente.
2. **Programación:** editor y pantalla virtual a la vista simultáneamente.
3. **Acceso:** Aula-16 disponible desde el principio, recomendando pasar antes por Aula-8; progresos independientes.
4. **Continuidad:** guardar avance automáticamente, no implementar por ahora un gestor general de proyectos.
5. **Catálogo:** únicamente componentes pertinentes al diseño; no exhibir piezas arbitrarias, como temporizadores no utilizados.
6. **Observación:** zoom en 2D y 3D; selección e inspección coherentes; vistas físicas y digitales sincronizadas.

## 3. Gramática espacial de ventana

| Zona | Papel | Comportamiento |
| --- | --- | --- |
| Menu bar | `Archivo`, `Editar`, `Ver`, `Recorrido`, `Simulación`, `Ayuda` | Comandos generales y estables; evitar ribbon innecesario. |
| Toolbar contextual | Acciones de la etapa | Montaje: deshacer, pista, probar. Ejecución: iniciar, pausar, pulso, instrucción. Programación: traducir, cargar, ejecutar. |
| Izquierda | Etapas y piezas admitidas | Panel plegable/redimensionable. En programación se repliega para dar espacio al código. |
| Centro | `Placa 3D`, `Esquema 2D`, `Programa` para Aula-8; solo `Esquema 2D` y `Programa` para Aula-16 | Estado compartido; pestañas de vistas, no instancias separadas de CPU. |
| Derecha | Inspector del elemento seleccionado | Nombre, pequeña imagen, función breve, terminales y estado; plegable y redimensionable. |
| Abajo | `Problemas`, `Pruebas`, `Señales`, `Salida` | Dock plegable, normalmente cerrado si no se necesita. |
| Inferior estrecho | Status bar | Aula, etapa, simulación, guardado, zoom; no reportar éxito no comprobado. |

**Navegación:** selección por clic, inspección profunda por doble clic o menú contextual; breadcrumbs para regresar de transistor/compuerta a módulo y computador. En programación, editor y pantalla visibles a la vez; inspector/dock en segundo plano. En 3D, arrastrar una pieza no debe confundirse con girar la cámara. Controles de zoom, centrar y paneo visibles para ratón y touchpad.

## 4. Modelo de estado — cuatro dimensiones independientes

| Dimensión | Valores de referencia | Regla |
| --- | --- | --- |
| Recorrido | pendiente / en curso / superado | Avance educativo, no estado de ejecución. |
| Montaje | incompleto / evaluable / pruebas superadas | Un montaje completo todavía puede funcionar mal. |
| Simulación | detenida / en ejecución / pausada | Pausar antes de cambiar conexiones. |
| Programa | vacío / editando / traducido / cargado | Error de traducción no implica fallo de circuito. |

**Regla de veracidad:** `Pieza colocada`, `Montaje listo para probar`, `Prueba superada` y `CPU ejecutando` son afirmaciones diferentes. Si una salida no coincide, mostrar entrada, salida observada y esperada. Indicar una causa solo si una regla comprobable la identifica.

## 5. Correspondencia de recursos técnicos disponibles

Los hallazgos proceden de `Aula_Computadora_C28AC_PLANOS_Y_APP.zip`, `Aula_Computadora_C28AD_LIBRO_Y_DOS_VISTAS.zip` y del candidato `Aula_Computadora_C28_AB_MAESTRO_CANDIDATO.pdf`. Las cantidades de pruebas se han leído de los informes de auditoría incluidos, no se han vuelto a ejecutar durante esta revisión.

| Elemento | Recurso | Estado comprobado/documentado | Consecuencia UX |
| --- | --- | --- | --- |
| NAND2 CMOS | `CMOS_NAND2_4_MOS.svg`, tabla JSON | Topología de 4 MOS; sin modelo analógico | Primer desafío; símbolos, terminales y tabla de verdad. No fingir voltajes físicos. |
| ALU Aula-8 | `Aula8_ALU359_APP_NETLIST.json`, diagramas SVG/DOT | **359 NAND2**; auditoría reporta 393.216 vectores de seis operaciones correctos | Zoom, búsqueda por ID, despiece del bit 0, señales interactivas. No arrastrar 359 compuertas a mano. |
| Camino de datos y control C28-W | `operacion_controlada_c28w.v`, visor HTML | 33 bits de estado RTL, cuatro flancos ejemplificados; sin implementación física | Botones START/CLK/RESET, línea temporal, estado de registros y flags. No confundir con CPU completa. |
| Placa didáctica conceptual | `AULA8_MAINBOARD_CONCEPTUAL_8_BITraces.svg` y `modelo_compartido_libro_app.json` | 9 módulos, 8 rutas de buses, 61 trazas visuales; **no PCB**, sin huellas ni alimentación completa | Referencia de composición inicial para 3D/2D, no afirmar precisión de pinout o fabricar desde ella. |
| Aula-16 memoria | `AULA16_MEMORIA_DOS_BANCOS_16_LINEAS.svg` | Dos bancos de 8 bits, arquitectura **candidata** | Ejemplo de vista 2D de RAM par/impar y acceso a palabras alineadas. |
| ISA Aula-8 | Manuscrito C28-AB, capítulos de programación | ISA candidata, no ejecución completa certificada | Editor y controles visuales propuestos; comandos reales sujetos a contrato final. |
| ISA Aula-16 | Manuscrito C28-AB, capítulo 23 | **ISA binaria no aprobada**; instrucciones del capítulo son seudolenguaje | No inventar botones de compilación o bytes ejecutables como si existieran. |
| Vídeo Aula V1 | Manuscrito C28-AB, capítulo de presentación | Contrato lógico especificado; hardware y software todavía pendientes | Monitor de texto/gráficos con reglas exactas abajo, sin prometer GPU física. |

### Pantalla virtual: reglas del documento

- Texto: **32 columnas × 16 filas**, glifos **8×8**, mapa de **512 bytes** y ROM propuesta de **256 glifos × 8 bytes = 2 KiB**.
- Gráficos: **256×128 píxeles**, **2 bits por píxel**, **8192 bytes** de memoria gráfica, paleta lógica **negro, verde, ámbar, blanco**.
- Modos texto y gráficos: alternativos, **no superpuestos**; buffers separados conservan su contenido al alternar.
- Registros de vídeo MMIO: `0xC020` modo, `0xC022` estado, `0xC024/26` dirección VRAM, `0xC028` datos, `0xC02A` control. La VRAM es interna al controlador, no RAM general de la CPU.
- En edición visual, una pantalla de programa puede incluir una inspección del buffer/VRAM, pero no una paleta de 256 colores ni efectos gráficos fuera de este contrato.

### Anchos y direccionamiento

Ambas CPU documentadas mantienen **16 bits de dirección**, **65.536 direcciones por byte = 64 KiB de espacio direccionable**. Aula-8 tiene cuatro registros generales de 8 bits, ALU de 8 y bus externo de datos de 8; Aula-16 proyecta registros generales y ALU de 16, bus externo de datos de 16. Para Aula-16 V1, lectura de palabra alineada a dirección par y bancos par/impar, pendientes de concretar electrónicamente. **El espacio direccionable no significa RAM instalada de 64 KiB.**

## 6. Estructura didáctica derivada

1. **Primer circuito:** distinguir señal, transistor y NAND2; montaje corto y tabla de verdad.
2. **Memoria mínima:** conservar un bit y luego un byte; detalle de registro, no SRAM simplificada falsamente como flip-flop.
3. **Transferencia:** buses individuales visibles, conexión por grupo; MUX, registro A/B y captura.
4. **Cálculo:** las seis rutas de la ALU359 y banderas; visualizar bit 0 y composición de ocho bits.
5. **Control:** reloj, START, fases y transferencia; caso C28-W antes de CPU completa.
6. **Sistema:** memoria, instrucciones, reset, E/S y pantalla cuando el contrato completo esté listo.
7. **Programación:** editar, traducir, cargar, ejecutar y observar en el mismo estado de CPU; alcance real conforme se aprueben las ISA.
8. **Aula-16:** reconstrucción en 2D desde cero mediante patrones ya aprendidos y nuevos desafíos de buses, palabras, bancos, instrucciones y pantalla.

La secuencia es un **mapa curricular candidato**; faltan dependencias exactas y presupuesto de interacción por etapa. El objetivo de cinco horas se debe contrastar con una prueba de recorrido, no estimarlo a partir del número de capítulos del libro.

## 7. Pendientes bloqueantes para capturas fidedignas

1. Elegir circuito físico/encapsulado de las piezas del ejercicio de montaje y distinguir 3D didáctico de huella verificable.
2. Cerrar CPU Aula-8 ejecutable de extremo a extremo, mapa de memoria y semántica de los opcodes que efectivamente se podrán ejecutar.
3. Cerrar ISA binaria y convención de llamadas de Aula-16 antes de representar compilación o código máquina real.
4. Precisar el subconjunto MiniC-Aula y si el compilador inicial será anfitrión o nativo; no presentarlo como implementado sin pruebas.
5. Finalizar los gestos, niveles de detalle, reglas de colocación equivocada y pruebas didácticas sin prometer simulación analógica.
6. Establecer capturas con contenido técnico verificable: primer módulo, placa a medio construir, bit ALU, fase de reloj, programa y monitor, memoria Aula-16, estados de error y concentración.

**Regla de producción visual:** primero generar diagramas a partir de `modelo_compartido_libro_app.json` y los netlists/RTL verificables. El libro recibe SVG/PNG; JavaFX recibe representación interactiva 2D/3D del mismo estado. Una composición conceptual se etiqueta como tal hasta que exista diseño físico comprobado.

## 8. Fuentes y límites de esta revisión

- `Aula_Computadora_C28AD_LIBRO_Y_DOS_VISTAS.zip` (`LEEME_C28AD_LIBRO_DOS_VISTAS.md`, `modelo_compartido_libro_app.json`, auditoría).
- `Aula_Computadora_C28AC_PLANOS_Y_APP.zip` (`LEEME_C28AC_ASSETS_APP.md`, auditoría y recursos gráficos).
- `Aula_Computadora_C28_AB_MAESTRO_CANDIDATO.pdf` (capítulos 23 y presentación de vídeo; versión candidata, no certificación).
- `ISAN Manual.docx` (ergonomía semántica, costo de interacción, veracidad de la retroalimentación).
- `UXUI aplicaciones autocontenidas.docx` (responsabilidad de menu bar, toolbar, sidebar, workspace, inspector, panel inferior, status bar y accesibilidad).
- `ReconcileLabWeirdCore-main.zip` (`GUI-GRAMMAR.md`: escritorio sobrio, paneles, barra de estado y canvas).

**Separación editorial:** este documento es específico de Aula-Computadora. El PDF genérico futuro de «Arquitectura de experiencia UX/UI y definición funcional del producto» es un artefacto distinto y aún no se ha redactado.
