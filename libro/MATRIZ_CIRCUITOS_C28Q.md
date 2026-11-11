# C28-Q · Matriz entre circuitos, figuras y evidencia

**Uso:** localizar la prueba y la fuente concreta de cada modulo. El
estado de un modelo, un netlist digital, un RTL y una ilustracion
no son intercambiables. Las figuras son funcionales salvo que una
fuente indique expresamente otro nivel.

| Cap. | Circuito o bloque | Figura 2D | Evidencia existente | Límite |
| --- | --- | --- | --- | --- |
| 03–04 | NAND/NOT/AND/OR/XOR | `c04_fig03_xor_cuatro_nand` | C28-Q red de 4 NAND + tablas | Cuatro puertas; sin pinout fisico |
| 05 | Latch SR | `c05_fig02_latch_nand_cruzado` | C28-Q feedback NAND + tabla | Estado invalido y metastabilidad sin resolver |
| 06 | Latch D/flip-flop | `c06_fig03_flancos_y_capturas` | C28-L modelo por flancos | Sin RTL de célula ni setup/hold |
| 07 | Registro de ocho bits | `c07_fig05_registro_aula8` | C28-A RTL + nuevo testbench Icarus | Sin pines/silicona; figura funcional |
| 10 | Sumador de 8 bits | `c10_fig02_sumador_completo`, `c10_fig04_cadena_y_dos_bytes` y **C28-T figura 1** (`c28_t/figuras/c28t_fig01_sumador_completo_nueve_nand.svg`) | C28-R ruta NAND de 134 puertas compartida para ADD/SUB; 65.536 vectores de ADD; C28-T explica el recorrido N1…N9 | Esquema digital funcional; sin temporizacion fisica ni placa |
| 11 | ALU, ruta aritmética ADD/SUB | `c11_fig01_resta_complemento_dos`, `c11_fig02_alu_selector` y **C28-T figura 2** (`c28_t/figuras/c28t_fig02_ruta_aritmetica_8_bits_134_nand.svg`) | C28-R 65.536 vectores SUB y flags C/V/N/Z; C28-T documenta el conteo 32+72+4+4+22 y banderas | **Solo ruta ADD/SUB**; HDL nuevo pendiente de Windows, MUX/AND/OR/XOR/NOT y política de flags lógicos aún sin netlist |
| 12–13 | Selector PC/MAR | `c28f_pc_mar_dos_rutas` | C28-Q 177 NAND JSON + HDL C28-F previo | No CPU integrada ni rutas de control |
| 14–16 | Selección salto | `c28d_selector_pc_nand` | C28-Q 51 NAND JSON + C28-D previo | No microsecuencia CALL/RET |
| 13–15 | Lectura secuencial | `c28g_lectura_con_espera` | C28-H HDL de dos politicas, Windows aprobado | PC no elegido; no SRAM real |
| 22 | Carriles de Aula-16 | `c22_fig05_dos_bancos_aula16` | C28-P mapa y alineacion | Sin arbitraje de bus 16 bits implementado |

**Niveles de evidencia actuales:** las redes de 4/2 NAND, 51 NAND
y 177 NAND se compararon con sus tablas o formulas desde listas de
conexiones; el RTL de registro8 y PC16 solo tiene **pruebas nuevas
aprobadas en Windows, según la retroalimentación de C28-Q con 24/24 controles**.
El HDL nuevo C28-R de 134 NAND requiere verificación de Icarus en Windows.
Los HDL C28-F/H también pasaron. Ninguna verificación
certifica continuidad de cables, retardo, voltajes, seleccion de chips,
firmware ni una CPU completa.

**Nota C28-T:** las nuevas figuras y el suplemento son una representación
didáctica de las conexiones digitales existentes. Se prepararon sin nuevas
pruebas y no se integraron al Word/PDF maestro; consultar
`libro/PLAN_INSERCION_C28T_SIN_REEDITAR_MAESTRO.md`.
