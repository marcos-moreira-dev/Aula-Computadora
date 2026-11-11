# Matriz C28-P de figuras en capítulos 15–24

**Cobertura:** 11 lecciones, contando 23B, y 50 referencias a
figuras PNG/SVG. El control comprueba archivos, dimensiones, etiquetas
y contratos matemáticos relacionados; **no** deduce netlists ni
integridad eléctrica a partir de un dibujo.

| Cap. | Identificador | Propósito de la figura | Evidencia y límite |
| --- | --- | --- | --- |
| 15 | `c15_fig01_camino_fetch` | Figura 1. PC selecciona la dirección, MAR la presenta a RAM, MDR recibe el byte e IR conserva el opcode para el despacho. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 15 | `c15_fig02_direccion_st` | Figura 2. La dirección de ST se construye con dos bytes retenidos mientras MAR se usa para leer el programa. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 15 | `c15_fig03_preparar_escritura` | Figura 3. ST debe sustituir en MDR el byte de dirección 6F por el dato 2A de R0 antes de habilitar una escritura. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 15 | `c15_fig04_transacciones` | Figura 4. La traza tiene ocho lecturas y una escritura; el último opcode se lee después de almacenar el dato. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 16 | `c16_fig01_pila_retorno` | Figura 1. CALL reserva dos bytes al descender SP y conserva allí el retorno 0x6003 en orden little-endian. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 16 | `c16_fig02_llamar_regresar` | Figura 2. CALL llega a la subrutina y RET recupera exactamente la continuación del llamador. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 16 | `c16_fig03_llamadas_anidadas` | Figura 3. Dos CALL anidados apilan dos direcciones de retorno diferentes y RET recupera la última primero. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 16 | `c16_fig04_bucle_jnz` | Figura 4. JNZ vuelve al decremento dos veces y continúa hacia HALT cuando el contador llega a cero. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 16 | `c16_fig05_ram_y_pila_call_ret` | Figura 5. CALL y RET conectan dos tramos de RAM de programa con las dos celdas contiguas donde se guarda el retorno. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 16 | `c16_fig06_ram_bucle_jnz` | Figura 6. El bucle de tres decrementos vuelve a 0x6003 mientras JNZ se toma y avanza a HALT cuando Z vale 1. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 17 | `c17_fig01_vector_reset` | Figura 1. Reset lee dos bytes de ROM y carga la dirección inicial del firmware. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 17 | `c17_fig02_mapa_memoria` | Figura 2. Espacio de 64 KiB con RAM inicial, registros de periféricos y ROM de firmware, sin rellenar artificialmente los huecos. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 17 | `c17_fig03_ranuras_rom` | Figura 3. Una ranura de ROM fija enlaza mediante JMP con una rutina que terminaría en RET. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 17 | `c17_fig04_run_dos_ret` | Figura 4. RUN crea un retorno al monitor y CALL PUTC crea otro retorno dentro del programa. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 18 | `c18_fig01_terminal_y_mmio` | Figura 1. Un terminal intercambia bytes con Aula-8 a través de los puertos DATA y STATUS candidatos. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 18 | `c18_fig02_llamada_publica_rom` | Figura 2. CALL llega a una ranura pública, JMP salta a la implementación y RET vuelve al programa. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 18 | `c18_fig03_eco_con_variable` | Figura 3. GETC entrega un byte, ST lo guarda en RAM y PUTC lo envía. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 18 | `c18_fig04_cadena_terminada` | Figura 4. FW_PUTS recorre cuatro caracteres ASCII y se detiene ante el terminador 00. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 19 | `c19_fig01_bloques_y_offsets` | Figura 1. Una imagen persistente se divide en bloques de 256 bytes y cada número determina un offset exacto. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 19 | `c19_fig02_registros_controlador` | Figura 2. Ocho registros MMIO controlan bloques persistentes, y el DATA de C018 transfiere un byte por acceso. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 19 | `c19_fig03_estados_transferencia` | Figura 3. El controlador pasa de reposo a transferencia y termina en DONE o ERROR según los 256 accesos. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 19 | `c19_fig04_carga_cruda_y_aex1` | Figura 4. LOAD crudo copia bloques completos, mientras LOADX candidato separa cabecera AEX1 y copia solo código validado. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 20 | `c20_fig01_herramientas_y_capas` | Figura 1. Editor, ensamblador, almacenamiento, cargador, monitor y CPU desempeñan funciones diferentes. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 20 | `c20_fig02_dos_pasadas_y_etiquetas` | Figura 2. Las dos pasadas separan el cálculo de direcciones de la emisión de bytes y resuelven saltos hacia etiquetas posteriores. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 20 | `c20_fig03_euclides_estados` | Figura 3. El algoritmo de Euclides avanza por restas entre dos registros positivos hasta obtener 6. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 20 | `c20_fig04_mini_sistema_y_pruebas` | Figura 4. El sistema propuesto distingue monitor ROM, herramientas RAM, programa de usuario y soporte persistente. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 21 | `c21_fig01_palabra_y_direcciones` | Figura 1. Dos computadoras con igual espacio de direcciones pueden tener registros y ALU de anchuras diferentes. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 21 | `c21_fig02_acarreo_16_bits` | Figura 2. Dos grupos de ocho bits transmiten un acarreo intermedio en un sumador de dieciséis bits. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 21 | `c21_fig03_suma_dos_anchos` | Figura 3. La misma suma se expresa en dos operaciones aritméticas de byte o una de palabra según la ALU. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 21 | `c21_fig04_registro_a_ram` | Figura 4. Un registro de dieciséis bits se almacena en dos direcciones consecutivas de bytes. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 22 | `c22_fig01_bancos_y_carriles` | Figura 1. Dos bancos de ocho bits comparten fila, pero tienen líneas de datos distintas. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 22 | `c22_fig02_palabra_y_little_endian` | Figura 2. Una palabra de registro llega a dos direcciones de byte y se reconstruye sin pérdida. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 22 | `c22_fig03_matriz_operaciones` | Figura 3. La matriz de operaciones deja claro qué carril trabaja en cada acceso. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 22 | `c22_fig04_casos_fallo_bus` | Figura 4. Cuatro síntomas diferentes permiten ubicar el defecto antes de construir el circuito. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 22 | `c22_fig05_dos_bancos_aula16` | Figura 5. Aula-16 conecta un bus de datos externo de 16 bits a dos bancos de ocho bits y distingue direcciones pares e impares. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 23 | `c23_fig01_niveles_de_programa` | Figura 1. Un problema pasa por fuente, ensamblador, binario y CPU cuando todas esas piezas existan. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 23 | `c23_fig02_sumar_arreglo` | Figura 2. Tres palabras consecutivas se recorren avanzando dos direcciones de byte por elemento. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 23 | `c23_fig03_euclides_dos_maquinas` | Figura 3. El mismo algoritmo y sus pruebas sirven para Aula-8 y Aula-16, aunque cambie la representación en instrucciones. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 23 | `c23_fig04_compilacion_y_pruebas` | Figura 4. La compilación cruzada necesita ISA, ABI, ensamblador y cargador antes de producir programas Aula-16 ejecutables. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 23B | `p23v_fig01_codigo_glifo` | Figura 1. El código 41 hexadecimal selecciona una A formada por ocho filas binarias. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 23B | `p23v_fig02_mapa_texto_32x16` | Figura 2. HOLA ocupa las cuatro primeras celdas de un mapa de texto de 32 por 16. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 23B | `p23v_fig03_pixeles_y_offsets` | Figura 3. Las coordenadas se convierten en offsets distintos en 1 bpp y 2 bpp. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 23B | `p23v_fig04_rom_controlador` | Figura 4. La ROM del programa, la ROM de glifos y el controlador realizan tareas distintas. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 23B | `p23v_fig05_tres_direcciones` | Figura 5. El procesador accede a registros MMIO y estos resuelven un offset de VRAM. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 23B | `p23v_fig06_profundidad_color` | Figura 6. Duplicar los bits por píxel aumenta la memoria necesaria. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 23B | `p23v_fig07_tipografia_y_contornos` | Figura 7. Una letra puede almacenarse como filas de bits o describirse con contornos geométricos. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 24 | `c24_fig01_alcances_y_evidencias` | Figura 1. Entender el diseño, comprobar un modelo y construir hardware son logros diferentes. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 24 | `c24_fig02_mapa_final` | Figura 2. Mapa global de memoria de Aula con RAM, regiones reservadas, MMIO y firmware ROM. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 24 | `c24_fig03_dos_arquitecturas_un_metodo` | Figura 3. Aula-8 y Aula-16 conservan los algoritmos de estudio, pero no comparten código máquina. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |
| 24 | `c24_fig04_escalera_verificacion` | Figura 4. El paso desde un modelo a un prototipo añade validaciones distintas. | PNG y SVG correctos; correspondencia de pines/RTL pendiente |

La simulación RTL C28-H corresponde a las **dos políticas
candidatas de lectura secuencial**, no a una validación HDL
automática de estas 50 ilustraciones. No hay placa física.
