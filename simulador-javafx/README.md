# Simulador JavaFX — taller de Aula-8 y Aula-16

**Estado 11-nov-2026, R0.8:** existe un corte de código JavaFX para la etapa
NAND2 CMOS de cuatro piezas, con modelo Java independiente, montaje 2D,
**placa 3D conceptual**, interior del chip, redes visibles y tests. **No hay CPU, PCB,
ISA aprobada ni simulador de máquina completa.**

**R0.4:** se corrigió la orientación del texto 3D y se representan tres
contactos metálicos salientes por cada transistor discreto, también en 2D.
No son integrados digitales de 8/14 pines. La forma y orientación de las
patas son didácticas, no una hoja de datos ni un footprint comercial.

**R0.5:** en el Inspector aparecen los conmutadores binarios `A` y `B`.
Una vez montadas las cuatro piezas, la salida `Y` se actualiza al instante
(`0`, `1`, `X` o `Z`), y el interior del chip distingue MOS conductores
de no conductores. El modelo de simulación es único para la prueba en vivo
y la tabla de los cuatro vectores. La acción de GitHub **Java 21 · NAND2**
compila y prueba el código automáticamente en cada cambio del simulador.
No comprueba la apariencia de la interfaz Windows ni el comportamiento
eléctrico o físico real.

**R0.6:** las placas 2D y 3D muestran los valores de A, B e Y del mismo
modelo y actualizan el color de sus trazos al conmutar las entradas. El borde
de las posiciones MOS distingue conducción ideal, sin convertirlo en
animación de corriente real. La red MID conserva color neutro porque el
modelo aún no determina su nivel lógico. El smoke test sin Maven suma
controles automáticos para las rutas 2D/3D y sus colores.

**R0.7:** clic sobre una pista de la placa 2D o 3D abre la **sonda lógica**
en el Inspector. Muestra el nivel digital de A, B, VDD, GND e Y cuando
el modelo lo conoce, distingue `X` de `Z` y deja MID como no calculada.
Los cruces de dos pistas sin nodo no se consideran conexiones; una sonda
2D no elige arbitrariamente una red en el punto exacto del cruce.

**R0.8:** cada una de las tres patitas conceptuales (compuerta, contacto superior e inferior) se puede seleccionar en 2D/3D. El Inspector indica la red desde el mismo `Nand2Lesson.TerminalRef` que usa el circuito; el interior del chip destaca el contacto seleccionado. Los nombres superior/inferior no son un pinout comercial.\n\n**[Ejecutar y probar el primer taller](docs/PRIMER_TALLER_EJECUCION.md)**:
`EJECUTAR_Y_CAPTURAR.cmd` en Windows (prueba + app + F12 + ZIP) o
`mvn test` / `mvn javafx:run` con Maven.

Estructura del corte ejecutable:

- `src/main/java/.../circuitos`: modelo NAND2 y definición de redes.
- `src/main/java/.../interfaz`: vistas 2D/3D, trazos, controles y navegación.
- `src/test`: pruebas del modelo, independientes del dibujo.
- `docs/`: instrucciones y decisiones nuevas de la experiencia ejecutable.
- Archivos `.cmd`/`.ps1` de la raíz: puntos de entrada para Windows.

La documentación de investigación anterior se mantiene por ahora en sus rutas
históricas; se migrará por familias con auditoría de enlaces, sin mezclarla
con clases Java ni eliminar referencias existentes.

## Propósito

Enseñar a construir **una computadora prediseñada y verificable**, desde un transistor hasta el sistema Aula-8 o Aula-16. El software no pretende competir con Proteus ni permitir, de inicio, inventar arquitecturas completamente arbitrarias.

## Dos modos obligatorios

1. **Explorar construida:** la computadora está completa; se puede seleccionar CPU, RAM, ROM, buses y registros; ejecutar un programa y ampliar el circuito hasta el nivel disponible.
2. **Hazlo tú mismo:** el estudiante recibe una placa/kit restringido, piezas y objetivos; coloca, conecta y verifica cada módulo con ayudas graduales.

Escala semántica: transistor -> NAND -> latch -> bit -> byte -> registro -> ALU -> CPU -> microcomputadora. La vista 3D será una representación coherente del **mismo modelo de conexiones** que alimenta al motor lógico y al esquema 2D.

## Índice técnico

- **[CONTRATO_VIDEO_AULA_V1.md](CONTRATO_VIDEO_AULA_V1.md)** y [JSON](VIDEO_AULA_V1_CONTRATO.json): **diseño lógico congelado** de una pantalla texto/bitmap de cuatro colores, consola y VRAM independiente por MMIO `C020–C02F`; **no es hardware ni aplicación implementada**.
- [CUESTIONARIO_MAPA_VIDEO_MMIO.md](CUESTIONARIO_MAPA_VIDEO_MMIO.md) y [PROPUESTA_VIDEO_TEXTO_GRAFICOS_ROM.md](PROPUESTA_VIDEO_TEXTO_GRAFICOS_ROM.md): **antecedentes históricos superados** por el contrato V1.

- [ESPECIFICACION_FUNCIONAL.md](ESPECIFICACION_FUNCIONAL.md): modos, lecciones y comportamiento.
- [MODELO_CIRCUITOS.md](MODELO_CIRCUITOS.md): entidades electrónicas, netlist, simulación y verificación.
- [ARQUITECTURA_SOFTWARE.md](ARQUITECTURA_SOFTWARE.md): estructura Java 21/JavaFX/Maven.
- [CATALOGO_COMPONENTES.md](CATALOGO_COMPONENTES.md): kit mínimo y candidatos comerciales.
- [ISA_Y_COMPILADORES.md](ISA_Y_COMPILADORES.md): ensamblador, ABI, MiniC y relación con CPU.
- [FIRMWARE_Y_ALMACENAMIENTO.md](FIRMWARE_Y_ALMACENAMIENTO.md): ROM, terminal, monitor y bloques.
- [PROGRAMACION_DESDE_CERO.md](PROGRAMACION_DESDE_CERO.md): depósito manual, bootstrap, herramientas nativas y plan de aceptación.
- [PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md](PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md): presupuesto candidato de 8192 B ROM/32768 B RAM y herramientas alternadas.
- [ISA_AULA8_CANDIDATA.md](ISA_AULA8_CANDIDATA.md) y [JSON](ISA_AULA8_CANDIDATA.json): 36 opcodes y tres programas **propuestos, sin aprobación**.
- [MICROARQUITECTURA_AULA8_BORRADOR.md](MICROARQUITECTURA_AULA8_BORRADOR.md) y [microtraza JSON](MICROTRAZA_AULA8_BORRADOR.json): datapath y nueve transacciones **esperadas, no ejecutadas**.
- [UNIDAD_CONTROL_AULA8_BORRADOR.md](UNIDAD_CONTROL_AULA8_BORRADOR.md) y [microsecuencias JSON](MICROSECUENCIAS_AULA8_BORRADOR.json): fetch, despacho y rutas LDI/ST/HALT como **acciones lógicas, no ciclos físicos**.
- [CONTROL_FLUJO_PILA_AULA8_BORRADOR.md](CONTROL_FLUJO_PILA_AULA8_BORRADOR.md) y [microflujo JSON](MICROFLUJO_AULA8_R0_6_BORRADOR.json): CALL/RET, pila y saltos como **acciones lógicas y trazas esperadas**.
- [PILA_Y_BANDERAS_AULA8_BORRADOR.md](PILA_Y_BANDERAS_AULA8_BORRADOR.md) y [microdatos JSON](MICRODATOS_PILA_FLAGS_AULA8_R0_7_BORRADOR.json): PUSH/POP/PUSHX/POPX, INC/DEC y banderas **todavía sin ejecución**.
- [DIRECCIONAMIENTO_INDEXADO_AULA8_BORRADOR.md](DIRECCIONAMIENTO_INDEXADO_AULA8_BORRADOR.md) y [microíndices JSON](MICROINDICES_AULA8_R0_8_BORRADOR.json): LD/ST por X/SP, desplazamiento firmado, dos pasadas ALU8 y ejemplo teórico **sin CPU ejecutada**.
- [AJUSTES_X_SP_Y_MARCOS_AULA8_BORRADOR.md](AJUSTES_X_SP_Y_MARCOS_AULA8_BORRADOR.md) y [microajustes JSON](MICROAJUSTES_AULA8_R0_9_BORRADOR.json): LEAX/ADJSP/ADDXW/SETSP/XFROMSP y función con variable local, **solo lógica documentada**.
- [ABI_MINIC_AULA8_R0_10_BORRADOR.md](ABI_MINIC_AULA8_R0_10_BORRADOR.md) y [contrato JSON](ABI_MINIC_AULA8_R0_10_BORRADOR.json): parámetros u8/u16, prólogo/epílogo fijo, registros, retorno y recursividad **solo en modelo de escritorio**.
- [ROM_MONITOR_AULA8_R0_11_BORRADOR.md](ROM_MONITOR_AULA8_R0_11_BORRADOR.md) y [contrato JSON](ROM_MONITOR_AULA8_R0_11_BORRADOR.json): tabla estable de ROM, bytes JMP/NOP y vector RESET, ABI de firmware independiente, monitor hexadecimal y RET frente a HALT, **sin EEPROM ni CPU**.
- [CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md](CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md) y [contrato JSON](CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.json): ocho registros MMIO, imagen cruda de bloques 256 B, READ/WRITE, errores, LOAD futuro y **modelo de persistencia únicamente en anfitrión**.
- [EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md](EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md) y [contrato JSON](EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.json): contenedor binario AEX1 de 32 B más payload, CRC16, ventanas de RAM y futura carga LOADX, **verificado solo en anfitrión; sin CPU ni loader nativo**.
- [LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.md](LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.md) y [JSON](LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.json): CRC incremental AEX1 de dos pasadas y copia por bloques, **sin staging de programa completo; no garantiza RAM atómica ni ejecución Aula**.
- [PLAN_PRUEBAS.md](PLAN_PRUEBAS.md): criterios verificables.

## Restricción cardinal

**Aula-16 utiliza un bus externo de datos de 16 bits**. La CPU de 8 bits no es una simple opción de apariencia.

## Secuencia

La implementación de este producto va **después** de la elaboración y validación prioritaria del libro. En R0 no crear interfaz falsa sin núcleo lógico.

