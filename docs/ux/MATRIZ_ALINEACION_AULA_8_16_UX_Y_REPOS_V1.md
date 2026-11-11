# Aula-Computadora — matriz de alineación entre UX, libro y modelos técnicos

**Corte de trabajo:** noviembre de 2026 · **Versión:** 1.0 · **Naturaleza:** análisis y propuestas de preproducción, no modificación de la ISA, de los circuitos ni de la aplicación.

## 1. Resultado ejecutivo

La experiencia debe tratarse como **dos recorridos educativos finitos de construcción y comprobación**, no como un CAD electrónico genérico: Aula-8 en placa didáctica 3D más esquemas digitales 2D; Aula-16 desde cero, con esquemas 2D. La duración pretendida es **como máximo cinco horas de uso continuo por recorrido**, algo que deberá medirse con estudiantes; no es una propiedad ya probada.

El libro y el aplicativo representarán **los mismos componentes, relaciones y principios**, pero en medios diferentes. El libro no hablará de JavaFX; la aplicación no sustituirá las explicaciones sustanciales del libro. El dibujo no será una segunda implementación de la lógica: ambas vistas observarán el estado de un modelo digital único. Una placa didáctica conceptual no debe anunciarse como PCB fabricable.

La capa UX se puede especificar ya. La CPU Aula completa, la ISA final, las ROM ejecutables y el hardware aún no están íntegramente probados. **No confundir madurez editorial ni vectores de prueba de una ALU con CPU operativa**.

## 2. Jerarquía de fuentes y vigencia

| Fuente | Autoridad adecuada | Precaución |
|---|---|---|
| `work/Aula-Computadora/DECISIONES.md`, `AGENTS.md`, `ARQUITECTURA.md` | Acuerdos de diseño y estados de aprobación | La copia local se anuncia en C28-T (9 nov.); algunas notas históricas están superadas. No reemplazar decisiones confirmadas tácitamente. |
| `simulador-javafx/CONTRATO_VIDEO_AULA_V1.md` y JSON | Contrato **lógico** congelado de pantalla y MMIO | No certifica controlador ni hardware. |
| `simulador-javafx/MODELO_CIRCUITOS.md`, `ARQUITECTURA_SOFTWARE.md` | Responsabilidades del dominio, motor y UI | Son arquitectura **prevista**, no programa JavaFX ya escrito. |
| C28-AC: `Aula8_ALU359_APP_NETLIST.json`, RTL C28-W y auditorías | Relaciones y comportamientos comprobados de esos subsistemas | 359 NAND de ALU y cuatro flancos no constituyen CPU completa, PCB ni BOM final. |
| C28-AD: `modelo_compartido_libro_app.json`, SVG de placa y auditoría | Correspondencia conceptual de las dos vistas; identificadores y trazas del **primer ejemplo** | Nueve módulos y 61 trazas **no** son netlist del sistema entero ni pinout de chips. |
| Conversación con Marcos (10–11 nov.) | Contrato de experiencia recientemente acordado | Registrar como nueva decisión UX para reconciliarse con D-007, D-008 y D-036 del repo antes de reescribirlos. |
| `marcos-moreira-dev/ReconcileLabWeirdCore` | Gramática GUI inspiradora, con autorización del autor para reutilizar piezas | No copiar su dominio de reconciliación. Se verificó `java-win11/docs/GUI-GRAMMAR.md` en GitHub; coincide con el paradigma MenuBar, ToolBar, paneles y statusbar. |
| `djhworld/simple-computer` | Referencia de estructura de simulador y didáctica | **No autoridad de Aula**. Su 16-bit CPU, ISA, mapa de E/S, pantalla y modelo Go son distintos. No copiar código sin licencia verificable. |

**Estado del remoto:** en la conexión GitHub disponible no se localizó `marcos-moreira-dev/Aula-Computadora` (consulta directa devolvió 404). Hay **una copia documental local** del proyecto y dos paquetes de entregables C28-AC/AD, pero no se ha comprobado sincronización con un remoto de Aula. El propio D-034 deja URL/visibilidad por determinar. No interpretar ese 404 como inexistencia universal del proyecto.

## 3. Conciliación de acuerdos de UX y repositorio

| Tema | Texto/documentación previa | Conversación reciente | Resolución para diseño |
|---|---|---|---|
| D-007, «dos modos» | Máquina construida explorable + «hazlo tú mismo» | Predomina construir desde cero mediante rompecabezas con módulos reutilizables | **Compatible si** «Construir» es el recorrido principal y «Explorar» un modo de consulta de la máquina de referencia, sin edición libre ni proyectos. Pendiente definir cuándo se habilita explorar. |
| D-008, 2D/3D | Navegar capas físicas y lógicas | Solo Aula-8 tiene 3D; Aula-16 solo 2D | Registrar explícitamente la restricción por arquitectura. No mostrar tab 3D vacío en Aula-16. |
| D-006, diseñador guiado | Kit limitado, conexiones, pruebas | Sin mesa libre de protoboard ni cables uno a uno en toda la CPU | **Confirmado en UX:** tablero prediseñado, ubicaciones guiadas, cableado de buses por grupo, módulos ensamblados una vez y reutilizados. Detalle transistor por demanda. |
| D-036, herramientas nativas | Editor de líneas y ensamblador ejecutados en **Aula-8**, no en Java | Una sesión breve orientada a construir CPU y observar programa | Mantener el requisito de autenticidad; separar *herramienta cruzada Java* de *utilidad nativa emulada*. No prometer programas nativos hasta disponer de ROM, binarios y CPU ejecutable. |
| D-009 y vídeo V1 | Pantalla fija, ROM/RAM/E/S y bloques | Monitor visible junto al código | Una pantalla virtual, panel de código y estado a la vez; no añadir monitor extra ni GPU. |
| Especificación funcional antigua | Kit potencialmente con MOS, NPN, resistencias, LED, IC | Catálogo cerrado, sin 555 ni chips irrelevantes | Una paleta específica **por desafío**, no un catálogo universal. Selección de piezas exactas pendiente del BOM educativo. |
| Progreso | No era gestor de proyectos CAD | Guardar progreso sin «Guardar proyecto» universal | Autosave por recorrido, con hitos y última sesión. El progreso educativo es distinto del estado RAM en ejecución. |
| Tres mil conexiones | Despliegue jerárquico bajo demanda | Cada recorrido ≤5 horas | Evitar repetir 359 arrastres NAND o miles de celdas RAM. Una instancia de módulo demostrada se multiplica como bloque certificado para la lección. |

## 4. Invariantes técnicos que las capturas deben respetar

| Contrato | Aula-8 | Aula-16 |
|---|---|---|
| Registros generales | R0–R3 de 8 bits | R0–R3 de 16 bits |
| Bus de datos externo | 8 bits, inspeccionables individualmente | 16 bits, inspeccionables individualmente |
| Direcciones / espacio | 16 bits / 64 KiB direccionables **por byte** | 16 bits / 64 KiB direccionables **por byte** |
| PC / SP / X | 16 bits | 16 bits |
| Organización de memoria | ROM/RAM/E/S con partición todavía pendiente | Dos bancos de 8 bits, acceso de palabra alineado a par, little-endian; candidatos físicos |
| Vídeo, común | TEXTO 32×16, 512 B, glifos 8×8 y ROM glifos 2 KiB; GRÁFICOS 256×128 a 2bpp = 8192 B | Idéntico periférico lógico con accesos de byte y selección de carril |
| MMIO de vídeo | C020, C022, C024, C026, C028, C02A; VRAM **indirecta** | Igual contrato y anchura de registro de 8 bits |
| ISA | 36 opcodes **candidatos**, no congelados | Codificación binaria **sin aprobar**; ejemplos del libro son seudolenguaje |

**Vídeo:** modos texto y gráfico excluyentes; memoria de ambos modos se conserva; pantalla única; RESET selecciona texto pero **no implica limpiar VRAM**. `C000/C002` permanecen como terminal y `C010–C01F` es el controlador de bloques candidato. El estilo gráfico del monitor no debe introducir nuevas resoluciones, colores, puertos o semánticas.

**Referencia externa no transferible:** `djhworld/simple-computer` usa una CPU de 16 bits propia, pantalla **240×160** y otras direcciones de E/S (`0x0007` y `0x000F`), y su CALL carece de pila real. No adoptar esas constantes ni su tabla de instrucciones. Sus cables booleanos Go tampoco implementan por sí solos la resolución completa `0/1/X/Z` prevista en el modelo de Aula.

## 5. Contrato de una sola fuente de verdad (propuesto)

Toda pieza concreta tiene `componentId` estable, definición semántica, pines y terminales; toda señal tiene `netId`, ancho y bits indexados. La lección guarda instancias/colocación; el motor lógico guarda conectividad real y genera instantáneas `tick`/`microestado`; el libro y la UI trazan proyecciones de esos datos. **La coordenada (x,y,z) solo coloca una pieza visual: nunca crea o define por sí sola una conexión eléctrica.**

Separar:

1. **Especificación base:** `CpuSpec`, `ComponentDefinition`, `Pin`, `Circuit/Module`, `Net`, mapa de memorias y buses; incluir versión de modelo.
2. **Montaje del estudiante:** piezas autorizadas, huecos, conexiones y errores de montaje; identidad estable para undo/redo y autosave.
3. **Simulador sin interfaz:** propagación digital `0/1/X/Z`, reloj, RAM/ROM/MMIO y CPU; pruebas programáticas sin JavaFX.
4. **Instantánea de ejecución:** valores, señales y tiempo discreto reproducible; consumir desde renderizador 2D, 3D, inspector y panel inferior.
5. **Progreso didáctico:** etapa, objetivos, pistas consultadas, pruebas pasadas y checkpoints; no se equipara a RAM ni a un proyecto editable arbitrario.

No existe aún un netlist único completo de Aula-8/Aula-16. `modelo_compartido_libro_app.json` es **primer puente visual**, no reemplazo de todas las redes NAND, control, memoria, buses y firmware. Necesita un proceso de integración/validación antes de alimentar cada escena.

## 6. Gramática de la ventana propuesta

| Región | Componente GUI | Función verificable |
|---|---|---|
| Superior, fila 1 | `MenuBar` | **Archivo** (progreso, salir), **Editar** (deshacer/rehacer), **Ver** (paneles, zoom, centrado), **Recorrido** (etapas, pista, retomar), **Simulación** (iniciar/pausar/pulso/paso/reset), **Ayuda** (controles, acerca de, referencias). No mostrar «Nuevo proyecto» o «Exportar PCB». |
| Superior, fila 2 | `ToolBar` **contextual** | Montaje: colocar, inspeccionar, probar, pista, deshacer. Simulación: ejecutar, pausar, paso de reloj, microestado/instrucción. Programa: traducir, cargar y ejecutar cuando el motor y la ISA existan. Los comandos no aplicables se deshabilitan **con razón entendible**. |
| Izquierda | `Sidebar` | Progreso/hitos y piezas del desafío. Replegable, ajustable, no catálogo de componentes infinito. |
| Centro | `Workspace` + `TabBar` | Aula-8: **Placa 3D**, **Esquema 2D**, **Programa**. Aula-16: **Esquema 2D**, **Programa**. Navegación jerárquica con breadcrumb; zoom/pan; selección sincronizada. |
| Derecha | `Inspector` | Foto o símbolo del componente, nombre/modelo exacto, una explicación funcional breve, pines/señales observadas y prueba contextual. Colapsable y redimensionable. |
| Inferior | Dock de `Problemas`, `Pruebas`, `Señales`, `Salida` | «Resultado observado vs esperado» y evidencia de la causa; no fingir detectar raíz del fallo si no está probada. Oculto/compacto hasta ser útil. |
| Borde inferior | `StatusBar` | Aula, etapa, estado de simulación, autosave, zoom y selección. Evitar indicadores optimistas sin pruebas. |

La **vista Programa** divide su área principal entre editor y monitor virtual; la pantalla permanece a la vista. Las pestañas cambian representación o tarea, **no crean tres CPU diferentes**. Doble clic o contexto «Abrir detalle» entra en el módulo seleccionado; breadcrumb para regresar. El esquema puede cambiar el **nivel de detalle** entre símbolo, puerta y transistor sin multiplicar pestañas innecesarias.

### Máquina de estados mínima para comandos

- **Montaje:** incompleto → completo pero no probado → pruebas superadas. Una estructura válida no garantiza funcionamiento.
- **Simulación:** parada → ejecutando ↔ pausada; detener/reiniciar tiene semántica definida de RESET, RAM y señales.
- **Programa:** editando → traducido → cargado → ejecutándose. Si ISA/binario no existe, el mockup marca los comandos como **propuesta**, nunca como hecho.
- **Recorrido:** pendiente → en curso → superado; una etapa pasa solo tras pruebas exigidas, no al «ver» el esquema.

**Corrección física:** un MOSFET «conduce/no conduce» y una *red* porta `0/1/X/Z`; no son literalmente la misma variable. Se pueden usar halos y líneas coloreadas como metáfora didáctica, con una etiqueta que distinga conducción del transistor y valor digital del nodo.

## 7. Flujo pedagógico y aceptación

1. **Elegir CPU:** Aula-8 o Aula-16, avances independientes; Aula-16 visible desde el principio con recomendación de cursar Aula-8.
2. **Montar desafío:** área con huecos predefinidos, transparencia del objetivo o pista graduada, kit pequeño, arrastrar/soltar. Conectar buses como unidad cuando el problema se haya abstraído a módulos.
3. **Probar componente:** permitir colocar mal dentro de ubicaciones válidas; ejecutar vectores. Si se comprueba la causa, señalar pieza/red; si no, decir la discrepancia y mostrar entradas/salidas. No prometer detección exhaustiva de daños eléctricos.
4. **Promover módulo:** tras superar pruebas, registrar el subcircuito y convertirlo en pieza semántica reutilizable; continuar sin reconstruir docenas de copias.
5. **Inspeccionar:** placa 3D cuando procede, esquema 2D hasta puertas y transistores, monitor de valores binarios; selección cruzada.
6. **Ejecutar programa:** solo cuando exista máquina completa y contrato ISA probado; distinguir `traducido por herramienta Java anfitriona`, `ensamblado dentro de Aula` y `ejecutado por Aula`.
7. **Finalizar:** test integrado y lectura de logros concretos, no un supuesto certificado de hardware físico.

**Prueba de duración:** diseñar hitos y contabilizar pasos, pistas y tiempo real de 2–3 usuarios; el tope de cinco horas **por CPU** queda como criterio de diseño, no como estimación certificada. No exigir cientos de conexiones idénticas.

## 8. Riesgos de inconsistencia y acciones antes de hacer capturas

| Prioridad | Riesgo | Acción mínima |
|---|---|---|
| P0 | Diseñar una pantalla de programa basada en opcodes imaginados | Congelar Aula-8 ISA/semántica de pruebas, y definir qué parte de Aula-16 es ejecutable en V1. Hasta entonces mostrar seudocódigo etiquetado. |
| P0 | Llamar «simulación eléctrica» a 0/1 digital o «PCB» a un esquema conceptual | Especificar tres niveles: digital lógico probado; físico didáctico ilustrativo; eléctrico/temporización pendiente. |
| P0 | Libro, SVG y app crean copias diferentes de un bus | ID de componente/red/bit común; validar todas las conexiones entre cada netlist de etapa y su representación. |
| P0 | Ignorar D-007 «Explorar vs construir» | Proponer cómo se navega a máquina terminada sin eliminar un acuerdo confirmado. Solicitar aprobación del autor. |
| P1 | Prometer editor/ensamblador nativos que en realidad ejecuta el anfitrión | Probar binario en CPU digital; presentar funciones no nativas como *herramientas externas*. |
| P1 | Poner millones de instancias gráficas para memoria | LOD, módulos colapsados e inspección por dirección, sin duplicar celdas de RAM como mallas 3D. |
| P1 | Romper flujo de cinco horas con la construcción de cientos de NAND | Piezas reutilizables y desafíos representativos con máximo de acciones a medir. |
| P1 | Copiar semántica del repo de Scott | Usarlo como inspiración, no como libro de especificaciones: no reutilizar ISA, puertos ni framebuffer. |
| P2 | Diseño visual precioso pero sin gramática de escritorio | Respetar ReconcileLab: menú persistente, toolbar contextual, canvas dominante, paneles ajustables y feedback de status. |

### Orden de cierre y entregables

**Etapa UX-1 — Contrato y navegación.** Aprobar recorrido principal/consulta, operaciones del menú, barra de estado, acoplamiento de paneles y reglas de selección. Resultado: navegación y microcopy sin código.

**Etapa UX-2 — Modelo interactivo mínimo.** Prototipo preciso de NAND2, un registro y el bus; mismo componente en 3D/2D/inspector; prueba y error honesto. Validar con las fuentes C28-AC/AD, antes de añadir la CPU entera.

**Etapa UX-3 — Presupuesto de recorrido.** Inventariar los desafíos necesarios para que cada arquitectura pueda montarse y probarse en ≤5 h; fijar qué se arrastra y qué se colapsa en módulo.

**Etapa UX-4 — Capturas hipotéticas.** Solo entonces diseñar imágenes fieles de: bienvenida, reto NAND, placa Aula-8 parcial, esquema NAND/registro, detalle ALU, reloj, código+monitor, error y pruebas, Aula-16 memoria y final. Las escenas que dependan de ISA incierta deben etiquetarse como conceptuales.

**Etapa técnica independiente.** Consolidar netlist completo, CPU, ISA/ABI, memoria, ROM, vídeo y ejecutables con pruebas sin pantalla. La evolución editorial e implementación puede progresar a distinta velocidad sin inventar «funciones completas».

## 9. Tres decisiones estratégicas restantes para Marcos

1. **Explorar la CPU completa.** ¿Debe estar disponible desde el inicio como referencia —con riesgo de adelantar respuestas— o solo tras terminar el montaje? **Recomendación:** disponible desde inicio como modo *demostración de lectura*, claramente separado del avance para que el estudiante no pierda orientación.
2. **Qué cuenta como «terminar» una CPU en cinco horas.** **Recomendación:** terminar el montaje guiado, superar un programa sencillo y observar la pantalla; aprender el editor/ensamblador nativos y MiniC en una sección posterior opcional, pero mantener su implementación futura como contrato del producto.
3. **Realismo de placa 3D.** ¿Placa **didáctica original** con encapsulados aproximados y conexiones correctas de alto nivel, o réplica fiel de placa fabricable con huellas comerciales? **Recomendación:** didáctica original, con leyenda explícita de que no constituye plano de fabricación. Una placa de fabricación requiere otros planos, costos y validación.

## 10. Fuentes concretas consultadas

- Copia de trabajo `work/Aula-Computadora/{AGENTS.md,README.md,DECISIONES.md,ARQUITECTURA.md,HOJA_DE_RUTA.md}` y `simulador-javafx/{ESPECIFICACION_FUNCIONAL.md,MODELO_CIRCUITOS.md,ARQUITECTURA_SOFTWARE.md,CONTRATO_VIDEO_AULA_V1.md}`.
- Entregables `Aula_Computadora_C28AC_PLANOS_Y_APP.zip`, `Aula_Computadora_C28AD_LIBRO_Y_DOS_VISTAS.zip`; modelo y lectura C28-AD.
- `Aula_Computadora_C28_AB_MAESTRO_CANDIDATO.pdf` y el informe de UX existente `UX_CONTRATO_AULA_C28AD_V1.md`.
- `ISAN Manual.docx`, `UXUI aplicaciones autocontenidas.docx`, `Arquitectura_Conceptual_de_Aplicaciones_de_Software_1.0.pdf`.
- GitHub `marcos-moreira-dev/ReconcileLabWeirdCore`, `java-win11/docs/GUI-GRAMMAR.md`; GitHub `djhworld/simple-computer`, `README.md`, `arch/arch.go`, `circuit/wires.go`, `io/display.go`, `computer/computer.go` y `asm/opcodes.go`.

**Regla de gobernanza:** si una propuesta altera una decisión `CONFIRMADO` del repositorio, se registra la motivación y se solicita acuerdo; nunca se edita silenciosamente la arquitectura o el libro a partir de una captura atractiva.
