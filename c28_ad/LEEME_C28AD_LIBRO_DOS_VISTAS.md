# C28-AD — Una computadora, dos representaciones, cuatro primeras etapas

## Regla editorial y de producto

**El libro y el aplicativo comparten conceptos, topología e identificadores; cambia únicamente la forma de presentación.**

- **Libro:** dibujos claros de la evolución real: componente → transistor → puerta → registro → bus → ALU → control → memoria → CPU → instrucciones. Cada imagen debe incluir explicación y señalar lo que está comprobado frente a lo que es candidato.
- **Aplicativo, vista electrónica digital:** esquema desplegable hasta compuertas y conexiones; señales binarias por bit, flancos, registros, memorias e instrucciones cuando correspondan.
- **Aplicativo, vista hardware:** mesa/placa tridimensional con componentes y cableado seleccionables, cámara, acercamiento, niveles de detalle. Para empezar, una placa didáctica; los encapsulados, el protoboard exacto, sus contactos y la simulación eléctrica se debatirán al entrar en UX/UI.
- **Sin duplicar circuitos:** el documento `modelo_compartido_libro_app.json` tiene las mismas IDs y enlaces para el libro y las dos vistas. El circuito lógico probado permanece en el JSON C28-AC de 359 NAND; las posiciones en pantalla **no definen** conectividad ni propiedades electrónicas.

## La imagen C28-AD

`figuras/AULA8_MAINBOARD_CONCEPTUAL_8_BITraces.svg` es una imagen **original** y editable con Inkscape. También existe PNG para el libro. Representa de modo progresivo nueve módulos conceptuales: Entrada A/B, MUX8, registro A/B, ALU359, resultado, banderas y control C28-W.

Incluye **61 trazas visuales de señales** correspondientes a siete segmentos de ocho bits y cinco señales de bandera. El BUS_DATA del mux aparece como dos ramas hacia los dos registros, tal como lo define la RTL `assign BUS_DATA = load_b ? B_IN : A_IN;`. Por tanto, evita el error de mostrar dos vías de captura que omitan el multiplexor compartido.

La figura **no** representa una placa lista para fabricar: los rectángulos son subsistemas y no circuitos integrados de la ALU; no hay disposición verdadera de patillas, pistas del reloj/control, alimentación, huellas, disipación ni conexiones de protoboard comprobadas. La vista hardware no puede afirmar que la ALU ya se ensambló con 359 chips NAND.

## Mapeo de las primeras etapas

| Etapa | Libro | Vista digital futura | Vista física futura | Estado actual |
|---|---|---|---|---|
| E01_NAND2 | Esquema CMOS de cuatro transistores | Tabla de verdad NAND | PMOS/NMOS y sus conexiones reales | Topología conceptual; sin modelo eléctrico |
| E02_ALU359 | Despiece del bit 0 y plano completo | JSON de 359 puertas NAND | Ensamble físico modular | Lógica exhaustivamente verificada; placa pendiente |
| E03_CONTROL_C28W | Ocho líneas de bus y cronología | Visor de flancos | MUX, registros, buses y controlador | Contrato RTL; físicos pendientes |
| E04_MEMORIA_AULA16 | Bancos par/impar de 8 bits | Memoria/lectura futura | Bancos/placas de RAM | Arquitectura candidata |

El futuro aprendizaje incluye también CPU completa, ciclo fetch/decode/execute, I/O, programa y vistas de ensamblador, pero **no se marca ninguna de esas partes como completada**.

## Cómo construir el aplicativo cuando corresponda

Un proyecto JavaFX puede mantener un modelo independiente de interfaz con estados y señales, y dos renderizadores que reciban el **mismo estado**:

1. Renderizador 2D: nodos/cables individualizables, búsqueda por ID, estados lógicos y diagramas vectoriales.
2. Renderizador 3D: escenario `SubScene` con cámara de perspectiva y geometría de módulos/placa mediante `Box`, `Cylinder` y `MeshView` para piezas especializadas, con selección sincronizada por ID.
3. Motor didáctico: etapa actual, nivel de detalle (módulo/compuerta/transistor), `clock step`, deshacer, validaciones explicables.
4. Motor eléctrico opcional: tras definir componentes, patillas y niveles reales; distinto del evaluador booleano actual.

**Decisión pospuesta:** coordenadas definitivas, medidas, iconos, gestos, modo libre de montaje, snap, colisiones, modelos 3D, colores definitivos, temas, condiciones de éxito y eventual simulación analógica. El principio anterior no obliga a ninguna UX concreta.

### Fuentes de inspiración y atribución

- Repositorio de referencia: [djhworld/simple-computer](https://github.com/djhworld/simple-computer) (Go, compuertas/cables, registros, ALU, RAM, control, E/S y ensamblador). Describe una **variante de 16 bits de Scott**, no es la ISA de Aula-8/Aula-16.
- Visual de referencia: [sim4edu — Scott’s 8-bit computer](https://sim4edu.com/sims/26/Scott-8-bit-computer), con esquemático animado, controles de ejecución y RAM.
- Imágenes compartidas por Marcos: circuito de la computadora de Scott, distribución de chips del Commodore 64 y esquemático de su placa. Sirven para identificar tres grados distintos de detalle.

**Derechos:** no se han copiado figuras originales del simulador ni código Go del repositorio. El árbol raíz del repositorio examinado no exponía un archivo `LICENSE`; no debe presumirse autorización para redistribuir su implementación. Las nuevas figuras C28-AC/C28-AD son originales y la referencia se conserva para estudio y atribución.

## Verificación de esta entrega

Ejecuta `python scripts/c28ad_generar_mainboard.py` para regenerar el SVG y PNG (requiere Inkscape); `python scripts/c28ad_verificar_vistas.py` comprueba la correspondencia básica de los recursos, nueve módulos, ocho rutas visuales y 61 líneas. No equivale a una prueba de escena JavaFX ni de una placa física.

**Secuencia acordada:** primero cerrar el libro con todos los circuitos explicados, y después trabajar de forma guiada en GitHub (ramas, commits, PR, IA), debatir UX/UI y construir el editor JavaFX 2D/3D con los recursos técnicos ya generados.
