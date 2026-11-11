# Trazabilidad de la construcción de Aula-8 y Aula-16 — C27

Esta tabla distingue lo enseñado de lo ejecutado. Un diagrama correcto no
convierte una arquitectura candidata en una placa construida.

| Tramo | Componente que se añade al recorrido | Figura nueva | Evidencia que sí existe | No demostrado |
| --- | --- | --- | --- | --- |
| C03–C06 | Habilitación, latch de un bit, D y reloj | `c05_fig05_sn74hct00_patillaje` más figuras previas | Tabla de verdad y pinout PDIP-14 contrastado con TI | Latch físico probado, circuito de pulsadores/placa CPU |
| C07 | R0 formado por ocho biestables D | `c07_fig05_registro_aula8` | Registro lógico, captura y conservación del byte | PCB, pines y temporización física |
| C08–C09 | MAR16, MDR8, rutas de lectura/escritura RAM | `c08_fig05_buses_aula8` | Anchos 16/8 y exclusión lógica de conductores | Arbitraje con chips reales |
| C10–C12 | ALU8, R0–R3 y datapath integrado | `c12_fig05_ruta_acumulada_aula8` | Recorrido funcional e instrucciones del manuscrito | CPU cableada o ejecutable |
| C13–C14 | Fetch, opcode, programas y celda de datos | `c14_fig05_ram_contigua_deposito`; `c14_fig06_ram_salto` | Bytes contrastados con `ISA_AULA8_CANDIDATA.json` | Codificación ISA aprobada |
| C15–C16 | PC, JNZ, CALL/RET y pila con SP | `c16_fig05_ram_y_pila_call_ret`; `c16_fig06_ram_bucle_jnz` | Little-endian, celdas consecutivas y retorno explicado | Ejecución de una ROM de control |
| C17–C20 | Arranque, terminal, persistencia, ensamblador | Figuras y tablas preexistentes de capítulos | Contratos y ejemplos documentales | Firmware ROM nativo validado |
| C21–C23B | Aula-16, dos bancos de ocho bits, vídeo V1 | `c22_fig05_dos_bancos_aula16` | 16 datos, 16 direcciones, bytes y palabras en dos carriles | Circuito de vídeo y GPU física |

Los límites anteriores son deliberados: la ISA Aula-8 R0.3, el microcontrol y
la interfaz de vídeo son propuestas didácticas. Las fuentes externas se reúnen
en `FUENTES_CONSULTADAS.txt` y al final del libro; las especificaciones
internas están en los JSON y documentos de arquitectura de este repositorio.
