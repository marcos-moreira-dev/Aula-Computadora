# Arquitectura conceptual — Aula-8 y Aula-16

**Este documento fija invariantes de arquitectura, no equivale todavía a un manual de construcción de circuito certificado.**

## 1. Objetivo de diseño

Una CPU suficientemente pequeña para mostrar cada mecanismo y suficientemente útil para ejecutar un monitor en ROM, programas ensambladores y aplicaciones simples de MiniC-Aula. Contexto microcomputador 1970/1980, diseño original.

| Dimensión | Aula-8 | Aula-16 |
| --- | --- | --- |
| Ancho de registros generales | R0–R3: 8 bits | R0–R3: 16 bits |
| Ancho de ALU | 8 bits | 16 bits |
| PC, SP, X | 16 bits | 16 bits |
| Bus externo de datos | 8 bits | **16 bits** |
| Bus externo de direcciones | 16 bits | 16 bits |
| Capacidad de direccionamiento | 65536 bytes | 65536 bytes |
| Orden de bytes | little-endian en operandos multibyte | little-endian |
| Entrada/salida | mapeada en memoria | mapeada en memoria |

### 1.1. Registros y flags

- R0–R3: operaciones normales; convención de llamadas en simulador-javafx/ISA_Y_COMPILADORES.md.
- PC: contador de programa; tamaño 16 bits.
- SP: puntero de pila descendente.
- X: registro índice de 16 bits para acceso indirecto y arreglos.
- IR y registros temporales de control: internos, descritos al detallar la microarquitectura.
- Z: resultado cero; N: bit más significativo; C: acarreo en suma o préstamo en resta según la operación; V: desbordamiento de aritmética con signo.

Las operaciones lógicas, cargas, shifts, INC y DEC necesitan una tabla definitiva de cuáles flags modifican antes de codificar la ISA.

## 2. Mapa de memoria de 64 KiB

| Inicio | Fin | Bytes | Área |
| --- | --- | ---: | --- |
| 0x0000 | 0x7FFF | 32768 | RAM de programa, datos y pila |
| 0x8000 | 0xBFFF | 16384 | Expansión futura |
| 0xC000 | 0xC0FF | 256 | Dispositivos mapeados |
| 0xC100 | 0xDFFF | 7936 | Reservado |
| 0xE000 | 0xFFFF | 8192 | ROM del sistema |

Total: 65536 bytes. No confundir bus de 16 bits con capacidad de 128 KiB; la dirección referencia un **byte**.

### 2.1. Inicialización

La RAM tras encender no se presume llena de ceros. El firmware inicializa explícitamente pila, búferes y segmentos necesarios. Las comprobaciones no dependerán de un estado de RAM inexistente.

### 2.2. ROM y servicios

- Vector de inicio previsto en **0xFFFC–0xFFFD**; 0xFFFE–0xFFFF reservado.
- Tabla de servicios cerca de **0xFF00**, con ranuras estables de **4 bytes**: FW_PUTC, FW_GETC, FW_PUTS y otras que se confirmen.
- En Aula-8 una entrada puede contener un salto de 3 bytes + relleno; en Aula-16, salto de dos palabras.
- Las ubicaciones se conservarán simbólicamente; el mapa final ROM verificará que las rutinas no colisionen con el vector.
- La ROM del **microcontrol** es interna y no ocupa esta zona del mapa de programas.
- **Propuesta Aula-8 R0.11, no aprobada:** 32 ranuras de 4 bytes en 0xFF00–0xFF7F, cuatro ocupadas, cada una con JMP absoluto little-endian (3 B) y NOP (1 B). Las demás no son entradas invocables. Vector RESET 0xFFFC–0xFFFD permanece separado y la API del firmware **no** usa necesariamente marco MiniC. [Contrato de ROM y monitor](simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.md).

## 3. Bus de Aula-16

Organización tipo dos bancos de 8 bits; no se está clonando el 8086.

| Acceso | Dirección | Banco | Datos |
| --- | --- | --- | --- |
| Byte par | 0x2000 | bajo | D0–D7 |
| Byte impar | 0x2001 | alto | D8–D15 |
| Palabra alineada | 0x2000 | ambos | D0–D15 |
| Palabra desalineada | 0x2001 | error v1 | no se ejecuta |

- La palabra 0x1234 almacenada desde 0x2000 ocupa **0x34** en 0x2000 y **0x12** en 0x2001.
- Una carga de byte a registro de 16 bits pondrá el byte en los 8 bits inferiores y limpiará los 8 superiores, salvo modificación posterior documentada.
- Se necesita **steering bidireccional** de carril para que una lectura/escritura de byte impar funcione desde el procesador.
- Los dos bancos requieren selección/decodificación, señales de escritura/lectura, control de triestado y temporización compatible con el dispositivo concreto.
- Usar dos memorias de 32 KiB × 8 cuando solo se necesitan dos mitades de 16 KiB desperdiciaría capacidad; el circuito/BOM final debe decidir si se tolera esa simplicidad o se eligen chips de tamaño exacto.

## 4. Acceso a E/S

Rango de registro general: **0xC000–0xC0FF**.

Asignación preliminar compatible con ambos:

| Dirección | Dispositivo | Función |
| --- | --- | --- |
| 0xC000 | Terminal DATA | Leer entrada / escribir salida |
| 0xC002 | Terminal STATUS | Estado: dato disponible / salida lista |
| 0xC010–0xC01F | Almacenamiento | Comando, estado, dirección de bloque y datos |
| **0xC020–0xC02F** | **Controlador de vídeo lógico V1** | **Seis registros pares** para texto, bitmap, bancos separados y VRAM indirecta; impares no alias |

Los registros expuestos a software serán preferentemente de 8 bits en direcciones pares; no se permite emitir accesos de palabra sin soporte del dispositivo. El [borrador R0.12](simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md) propone en **Aula-8** COMMAND=C010, STATUS=C012, BLOCK_LO=C014, BLOCK_HI=C016, DATA=C018, ERROR=C01A, COUNT_LO=C01C y COUNT_HI=C01E: codificación candidata, sin electrónica o firmware ejecutados. Aula-16 sigue con su bus externo **de 16 bits**.

### 4.1. Contrato lógico de vídeo V1 (congelado; hardware pendiente)

Por delegación explícita del usuario se ha adoptado **una única pantalla virtual** con consola y dos modos excluyentes: texto **32×16, ROM de 256 glifos ×8 = 2 KiB**, y bitmap **256×128 a 2 bpp / cuatro colores**, sin GPU ni VGA. El buffer de texto **512 B** y la VRAM gráfica **8192 B** son dos bancos **independientes del mapa de 64 KiB de la CPU**, que conservan contenido al cambiar de modo. `C000/C002` continúan atendiendo entrada/salida de consola; un `C000` de salida alimentará el banco de texto aunque los gráficos estén visibles. Se reserva `C020–C02F`, con registros **de 8 bits en direcciones pares**. El acceso a bancos es indirecto y requiere `ADDR_LO/HI` más `DATA`. El mismo dispositivo podrá atender posteriormente Aula-16 con operaciones de byte y carril adecuado. **No se añaden instrucciones gráficas ni entradas ROM públicas.**

La codificación exacta de registros, índices de color, RESET, errores y límites está en el [contrato de vídeo Aula V1](simulador-javafx/CONTRATO_VIDEO_AULA_V1.md) y [su JSON](simulador-javafx/VIDEO_AULA_V1_CONTRATO.json). Congelar **el mapa lógico** no aprueba netlist, vídeo físico, sincronización, ISA definitiva o ROM ensamblada. La propuesta previa queda [archivada como antecedente](simulador-javafx/PROPUESTA_VIDEO_TEXTO_GRAFICOS_ROM.md).

## 5. ISA y control

La semántica será común: MOV, LDI, LD/ST, acceso por X, aritmética ADD/ADC/SUB/SBC/CMP, lógica AND/OR/XOR/NOT/SHL/SHR, saltos, CALL/RET, PUSH/POP, NOP, HALT. Faltan opcodes binarios oficiales.

- Aula-8: instrucciones de 1 o más bytes; constantes/direcciones de 16 bits en little-endian.
- Aula-16: palabra de instrucción inicial de 16 bits, seguida de palabras adicionales; dirección de instrucción alineada.
- Se reservan modos indirectos e indexados, y relativos a SP, para que MiniC-Aula pueda implementar arreglos y locales.
- La **unidad de control microprogramada** es la propuesta inicial: secuencia de estados y señales observables por instrucción. No confundir un micro-paso con un ciclo completo de instrucción o con una instrucción de máquina.
- En la primera versión: polling, sin dependencia del sistema de interrupciones.

**Anexo de revisión R0.3:** existe una [primera codificación de Aula-8 candidata](simulador-javafx/ISA_AULA8_CANDIDATA.md) con 36 opcodes y ejemplos en bytes; **no ha sido aprobada** ni demuestra que exista microcódigo/circuito. El contrato de Aula-16 sigue siendo independiente y pendiente de su propia codificación.

**Anexo de revisión R0.4:** la [microarquitectura candidata de Aula-8](simulador-javafx/MICROARQUITECTURA_AULA8_BORRADOR.md) plantea datapath8, registros internos, acceso a bus y fetch común; es un diseño documental, **no** un circuito eléctrico final. El incremento PC, el control de pila, la frecuencia y las señales exactas de microcódigo permanecen abiertos.

**Anexo de revisión R0.5:** la [unidad de control candidata](simulador-javafx/UNIDAD_CONTROL_AULA8_BORRADOR.md) divide fetch, despacho y rutas LDI/ST/HALT en **acciones lógicas** documentadas. `ST` absoluto requiere retener dos bytes de dirección y preparar `MDR` antes de escribir; se proponen `ADDR_LO/ADDR_HI`, sin fijar su implementación. La [especificación JSON](simulador-javafx/MICROSECUENCIAS_AULA8_BORRADOR.json) no es microcódigo ejecutable, ROM dimensionada ni tabla de ciclos.

**Anexo de revisión R0.6:** [control de flujo y pila candidato](simulador-javafx/CONTROL_FLUJO_PILA_AULA8_BORRADOR.md), con CALL/RET y salto absoluto/condicional. `SP` desciende de `0x8000` a `0x7FFE` en la llamada de muestra; allí se guardan bytes `03 60` del retorno little-endian. El [microflujo JSON](simulador-javafx/MICROFLUJO_AULA8_R0_6_BORRADOR.json) y su verificador documentan 10 lecturas y 2 escrituras esperadas, no CPU ejecutada ni pila eléctrica certificada.

**Anexo de revisión R0.7:** [pila de datos e indicadores candidatos](simulador-javafx/PILA_Y_BANDERAS_AULA8_BORRADOR.md). `PUSH/POP` mueven SP un byte, `PUSHX/POPX` lo mueven dos y conservan orden little-endian. `INC/DEC` modifican Z/N/V pero preservan `C`; las sumas usan carry y las restas borrow. El [JSON R0.7](simulador-javafx/MICRODATOS_PILA_FLAGS_AULA8_R0_7_BORRADOR.json) describe acciones lógicas y ejemplos, **no una implementación de ALU o RAM**.

**Anexo de revisión R0.8:** [direccionamiento indexado por X/SP](simulador-javafx/DIRECCIONAMIENTO_INDEXADO_AULA8_BORRADOR.md) con desplazamiento de 8 bits firmado y acumulación de dirección de 16 bits usando **dos pasadas de ALU8** y `ADDR_CARRY` privado. Los selectores de `LD/ST` de 3 bytes, [JSON de rutas](simulador-javafx/MICROINDICES_AULA8_R0_8_BORRADOR.json) y el ejemplo con 14 lecturas y una escritura representan **expectativas documentales**, no ejecución de CPU ni autorización eléctrica de la dirección.

**Anexo de revisión R0.9:** [ajustes de X/SP y marco de una función](simulador-javafx/AJUSTES_X_SP_Y_MARCOS_AULA8_BORRADOR.md). `LEAX/ADJSP` suman desplazamientos con signo; `ADDXW` agrega `R1:R0` a X por dos pasadas; `SETSP` y `XFROMSP` transfieren palabras de 16 bits sin modificar flags. El [JSON R0.9](simulador-javafx/MICROAJUSTES_AULA8_R0_9_BORRADOR.json) y el test de 1572864 casos documentan una función CALL/PUSHX/ADJSP/POPX/RET con 29 lecturas y 5 escrituras **esperadas**, no CPU, ABI definitiva ni circuito protegido.

**Anexo de revisión R0.10:** [convenio binario propuesto para funciones MiniC-Aula8](simulador-javafx/ABI_MINIC_AULA8_R0_10_BORRADOR.md). La pila usa argumentos de 2 bytes, orden derecho a izquierdo, PUSH de alto antes de bajo; el prólogo fijo conserva X/R2/R3 y forma offsets constantes desde X. La [especificación JSON R0.10](simulador-javafx/ABI_MINIC_AULA8_R0_10_BORRADOR.json) describe una suma u16 con CALL/RET y 73 lecturas+10 escrituras externas **previstas**. Los flags son volátiles entre funciones; **no** se ha congelado la ABI, código MiniC ni un circuito físico.

**Anexo de revisión R0.11:** [ROM pública y monitor Aula-8 candidatos](simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.md). Un CALL a FF00 entra por JMP E100 **ilustrativo** y el RET de la rutina retorna al llamador. La tabla reserva 128 B (32 ranuras) sin invadir el vector de reset. Se proponen MEM/POKE/RUN restringidos y se mantienen REG/LOAD pendientes de hardware. RUN hace CALL y admite retorno explícito por RET; HALT detiene, no trae de vuelta el prompt. El [JSON](simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.json) y su prueba verifican interfaz y límites, **sin firmware ejecutable ni CPU**.

**Anexo de revisión R0.12:** [controlador de bloques propuesto](simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md) y [JSON](simulador-javafx/CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.json). Se formalizan ocho registros MMIO, número de bloque little-endian, READ/WRITE en transferencias de 256 B, STATUS/ERROR, conteo y buffer. Una referencia Python en anfitrión prueba persistencia y cancelación de escritura incompleta, pero **no** controlador electrónico, ROM, CPU ni LOAD nativo. El futuro LOAD crudo solo admitiría RAM 1000–2FFF o 6000–6FFF alineada a 256 B; en fallo parcial no se ejecuta el programa.

**Anexo de revisión R0.13:** [paquete AEX1 propuesto](simulador-javafx/EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md) y [JSON](simulador-javafx/EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.json). Cabecera de 32 B en sector 256 B con origen, entrada, tamaño y CRC de programa y cabecera; carga `LOADX` futura y separada de `LOAD` crudo R0.12. El modelo Python compara errores antes de producir una **copia de RAM de anfitrión**, nunca ejecuta Aula. El búfer del monitor es demasiado pequeño para la herramienta máxima y requiere rediseño de staging. Aula-16 preserva bus externo de **16 bits** y necesita formato/ISA propios.

**Anexo de revisión R0.14:** [LOADX de dos pasadas candidato](simulador-javafx/LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.md): verificación CRC incremental completa en la primera lectura y **copia de hasta 256 B temporales** por bloque en la segunda. Esto elimina la necesidad de staging completo de herramienta, pero **no la carga parcial ante fallo de segunda pasada**. La autorización de ejecución en ROM real está por definir; el modelo Python solo devuelve un punto de entrada candidato si todo pasa. **Aula-16 conserva bus externo de 16 bits**.

## 6. Pila y llamadas

- Dirección de retorno: **16 bits** en ambas CPU.
- Pila descendente desde zona superior de RAM, con inicio provisional en dirección par.
- Aula-16: accesos de palabra alineados.
- ABI compilada: se prevén ranuras de parámetro de 2 bytes, también para u8, para conservar alineación.
- Implementación y desplazamientos finales de parámetros/locales se especificarán antes del compilador.

## 7. Lo que se debe mostrar en diagramas

Vista arquitectónica -> buses y bloques -> registros y selectores -> puertas -> transistores. Los estados eléctricos se explicarán con niveles y limitaciones, no con colores arbitrarios presentados como medidas reales. Las vistas pueden contraerse por niveles semánticos.

