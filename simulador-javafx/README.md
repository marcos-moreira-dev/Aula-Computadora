# Simulador JavaFX — taller de Aula-8 y Aula-16

**Estado R0:** solo especificación de un producto futuro. No existe aún aplicación, POM funcional ni ejecutables.

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

