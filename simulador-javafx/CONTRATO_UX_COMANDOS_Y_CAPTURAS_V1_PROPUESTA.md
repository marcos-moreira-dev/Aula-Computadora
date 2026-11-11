# Aula-Computadora — contrato mínimo de comandos, estados y capturas UX

**Estado:** propuesta de integración para la carpeta `simulador-javafx/`, sin alterar ISA, buses, firmware ni contratos eléctricos.  
**Propósito:** detener la expansión de ideas y disponer de un único guion verificable para futuras imágenes de la interfaz.

## A. Alcance congelado para la preproducción

- Dos recorridos independientes de construcción, Aula-8 y Aula-16. Meta: **terminar montaje, pruebas y un programa observable en cinco horas o menos por CPU**, mediante validación de uso futura; no obliga a construir centenares de NAND repetidas.
- `Construir`: recorrido guiado, piezas pertinentes al desafío, slots, pruebas y promoción de subcircuitos a módulos reutilizables. `Explorar`: máquina de ejemplo completa, **accesible desde el inicio**, sin modificar el avance del recorrido.
- Aula-8 dispone de **Placa 3D**, **Esquema 2D** y, al llegar al nivel adecuado, **Programa**. Aula-16 dispone de **Esquema 2D** y **Programa**; 3D queda fuera de V1, con arquitectura extensible.
- La vista 3D es una **placa didáctica original**, no una PCB fabricable. Los diagramas 2D y las figuras del libro derivan de las mismas IDs y topología comprobada. Ninguna imagen puede adelantar una ISA o un circuito aún sin aprobar.
- Java 21 + JavaFX + Maven, monolito modular y motor lógico sin interfaz. Una definición de transistor no contiene nodos `Shape`, `MeshView` ni widgets de JavaFX: la presentación usa un `VisualSpec`/renderer por tipo e instancia.

## B. Ventana y regiones fijas

| Región | Nombre | Política |
|---|---|---|
| Superior 1 | `MenuBar` | Archivo, Editar, Ver, Recorrido, Simulación, Ayuda. Conserva posición entre etapas. |
| Superior 2 | `ToolBar` contextual | Agrupa solo comandos pertinentes a la actividad actual; texto corto e icono sobrio. |
| Izquierda | `Sidebar` | Etapas y piezas permitidas. Colapsable y redimensionable; puede estrecharse al programar. |
| Centro | `Workspace` + `TabPane` | Escena 3D/diagrama 2D/programa, según CPU y etapa; zoom, pan, selección y breadcrumbs. |
| Derecha | `Inspector` | Foto/símbolo, nombre preciso, función, terminales y valores actuales. Breve; colapsable y redimensionable. |
| Abajo | Dock | Pestañas: **Problemas**, **Pruebas**, **Señales**, **Salida**. Normalmente retraído; aparece al ejecutar prueba o cuando una salida sea relevante. |
| Inferior fijo | `StatusBar` | CPU, recorrido, etapa, simulación, autosave, zoom y selección. Sin mensajes engañosos de éxito. |

**Atención:** la barra de herramientas indica qué puede hacerse **ahora**; el menú mantiene comandos estables, aunque alguno no esté disponible. El inspector es el panel derecho; los errores de ejecución van al dock inferior. Las tres vistas comparten selección, valores e identidad del circuito, pero no comparten instancias de nodos gráficos.

## C. Menús de V1 — propuesta concreta

| Menú | Comandos visibles y útiles | Exclusión deliberada |
|---|---|---|
| **Archivo** | Elegir computadora, Reanudar recorrido, Guardar avance ahora, Preferencias, Salir | «Nuevo proyecto CAD», abrir proyecto arbitrario, publicar PCB. |
| **Editar** | Deshacer, Rehacer, Quitar pieza seleccionada, Restablecer etapa (con confirmación) | Duplicar miles de chips, operaciones CAD genéricas. |
| **Ver** | Ajustar a ventana, Centrar selección, Zoom +/−, Mostrar/ocultar paneles, Modo concentración | Menús para vistas no soportadas por esa CPU. |
| **Recorrido** | Etapa actual, Ver objetivo, Pista, Construir, Explorar máquina de referencia, Volver al progreso | Misiones ajenas al currículo. |
| **Simulación** | Probar módulo, Iniciar, Pausar, Detener, Un pulso, Una instrucción, Reiniciar CPU | Controles de analizador analógico/temperatura. |
| **Ayuda** | Cómo usar el programa, Controles de navegación, Conceptos del elemento, Fuentes, Acerca de | Enciclopedia emergente no solicitada. |

**No crear un menú `Programa` por ahora:** las acciones **Traducir**, **Cargar** y **Ejecutar** viven en la toolbar de la pestaña Programa. Pueden revisarse si el uso real demuestra necesidad de comandos globales.

## D. Disponibilidad de acciones según contexto

| Estado del usuario | Toolbar principal | Trabajo habilitado | Qué impide el sistema |
|---|---|---|---|
| Inicio / selector | Continuar, Construir, Explorar | Elegir Aula-8/Aula-16 y restaurar progreso | No se ejecuta una CPU no seleccionada. |
| Construir pieza | Seleccionar, Colocar, Quitar, Deshacer, Pista, Probar | Snap a ubicaciones **admisibles**, incluso si una pieza es incorrecta | Probar no significa aprobar; no se modifica la CPU si corre. |
| Inspeccionar circuito | Abrir detalle, Subir nivel, Centrar, Zoom | Navegar símbolo/puerta/transistor sin destruir montaje | El inspector nunca edita la conectividad por sí solo. |
| Probar circuito | Probar, Ver entradas, Abrir resultados | Entradas de prueba y comparación observado/esperado | No se inventa una causa raíz sin verificación estructural. |
| Simulación de CPU | Iniciar/Pausar/Detener, Pulso, Instrucción, Reset | Ver buses, registros, memoria y monitor **cuando exista CPU ejecutable** | No editar estructura mientras se ejecuta; los botones nativos no se habilitan por una mera maqueta. |
| Programa | Traducir, Cargar, Ejecutar, Detener | Editor y pantalla virtual **visibles juntos**, inspección del estado | Diferenciar compilador/ensamblador del anfitrión y utilidades que realmente corren en Aula. |
| Explorar referencia | Ejecutar, Pausar, Pulso, Inspeccionar, Volver a construir | Examinar la máquina terminada, sin afectar progreso guardado | No arrastrar piezas ni guardar proyecto libre. |

**Regla sobre edición:** la propuesta más simple es permitir cambios estructurales solo en modo **Detenido**. La pausa conserva valores para observar; se debe detener explícitamente antes de modificar. Esto es todavía una decisión operativa propuesta, no una propiedad física certificada.

## E. Estados que no debemos mezclar

1. **Montaje:** incompleto / estructuralmente completo / pruebas superadas.
2. **Recorrido:** pendiente / en curso / terminado.
3. **Motor:** detenido / ejecutando / pausado, con `tick` y snapshot.
4. **Programa:** editado / traducido / cargado / ejecutándose / fallido.
5. **Guardado:** cambios pendientes / guardando / guardado / error de persistencia.

Un error de programa no hace «fallar» la placa; una puerta colocada no implica que el test haya pasado. El `StatusBar` usa etiquetas concretas: **«Etapa: registro», «CPU: detenida», «Último guardado: correcto», «Zoom: 125 %»**. No muestra porcentajes inventados de avance técnico.

**Diagnóstico:** dos niveles. *Hecho comprobado*: «Entrada A=1, B=1; salida observada=1, esperada=0». *Causa verificada*: «Pin Y conectado a la red equivocada», únicamente si un chequeo de netlist lo demuestra. El dock conserva detalles; el tooltip ofrece una frase breve, no una explicación extensa.

## F. Seis capturas representativas que se producirán

| ID | Escenario | Qué debe verse exactamente | Validación técnica |
|---|---|---|---|
| IM-01 | Inicio / selector | Aula-8, Aula-16, Continuar, Construir, Explorar; dos progresos separados; estilo corporativo | No inventar proyectos abiertos o arquitecturas adicionales. |
| IM-02 | Aula-8, placa 3D a medio construir | Sidebar con piezas de **una** etapa, placa didáctica con slots, inspector de pieza, toolbar contextual, statusbar | Geometría conceptual etiquetada; no presentarla como PCB física. |
| IM-03 | Aula-8, esquema 2D al abrir una NAND/registro | Pistas de 8 bits separadas, puertas/transistores y breadcrumb, inspector de componente seleccionado | Derivar de C28-AC/AD, sin inventar cables ni números de patas. |
| IM-04 | Prueba de un módulo con error | Circuito, prueba 00/01/10/11, una discrepancia y dock **Problemas/Pruebas** expandido | Error reproducible, sin culpar una pieza si el motor no demostró la causa. |
| IM-05 | Aula-8, Programa + monitor | Editor y **una sola pantalla virtual** juntos, controles de traducción/carga/ejecución, registros y señales contextualizados | Pantalla: texto 32×16 o gráficos 256×128 2bpp; código solo si ISA real aprobada o rotular «ejemplo conceptual». |
| IM-06 | Aula-16, memoria y ejecución 2D | Dos bancos de 8 bits, bus de datos de 16, dirección de 16 y estado de lectura de palabra alineada | Sin tab 3D; little-endian y sin asumir 64 KiB de RAM instalada. |

**Método visual:** dibujar primero la UI y los circuitos **precisos mediante recursos vectoriales/programación**. La IA visual puede servir para acabados o inspiración estética, pero nunca se confiará en texto ilegible ni se le delegará inventar conexiones. Las capturas indicarán **«Diseño de interfaz propuesto»** mientras no exista una aplicación JavaFX real.

## G. Puerta de salida de planificación y GitHub

Antes de producir las seis capturas: comprobar que IM-01 a IM-06 no violan el contrato visual, la arquitectura Aula, el mapa de vídeo ni los estados; no hace falta cerrar el color definitivo de cada icono o un futuro modo libre.

Antes de publicar un repo **público**: resolver D-033 sobre licencias, imágenes históricas y coautorías. Antes de crear incluso el repo **privado**: confirmar cuenta GitHub, nombre y acceso de escritura, y la relación con la copia documental actual. No decir «subido» sin comprobar commit y URL.

**Propuesta para primer repositorio:** `Aula-Computadora`, visibilidad **privada por defecto**, ramas convencionales y una sola fuente de verdad para libro/código; preparar un `.gitignore`, README de estados reales, `DECISIONES.md` y las especificaciones de UX en una primera entrega. **No cargar** automáticamente todo el archivo histórico ni imágenes con derechos no revisados.

**Criterio práctico de «planificado»**: existen (1) alcance, (2) arquitectura de modelos, (3) flujo de aprendizaje, (4) comandos/UI, (5) inventario de capturas y (6) trazabilidad de contratos técnicos; lo demás se resuelve al implementar y probar, sin fingir precisión futura.

### Documentación relacionada

- `AGENTS.md`, `DECISIONES.md`, `ARQUITECTURA.md`, `HOJA_DE_RUTA.md`.
- `simulador-javafx/MODELO_CIRCUITOS.md`, `ARQUITECTURA_SOFTWARE.md`, `ESPECIFICACION_FUNCIONAL.md`, `CONTRATO_VIDEO_AULA_V1.md`.
- Entregables gráficos C28-AC/C28-AD y especificaciones UX ya guardadas por separado.

*Este archivo es una propuesta de integración y no declara implementadas escenas, programa ni circuitos nuevos.*
