# Calidad, verificación y criterios de certificación

## Estados de evidencia

1. **Documentado:** el objeto tiene ficha, límites, entradas, salidas y esquema.
2. **Verificado lógicamente:** tablas de verdad y pruebas digitales correctas.
3. **Integrado:** se demostró operación en el sistema Aula-8/Aula-16 simulado.
4. **Validado físicamente:** se aportó montaje, instrumento, mediciones y condiciones de la prueba.

Estos estados **no son equivalentes**. ERC, una tabla de verdad o un renderizado 3D no prueban por sí mismos seguridad o funcionamiento analógico real.

## Requisitos de cada módulo

- Identificador estable y descripción funcional.
- Circuito esquemático con pines y alimentación.
- Explicación del mecanismo y límites del modelo didáctico.
- Datos verificables: voltaje, corriente, consumo, timing y tolerancias, cuando corresponda.
- Pruebas positivas, negativas y de borde.
- Errores deliberados para el taller guiado.
- Enlaces a hojas de datos si usa componente comercial.

## Verificación digital planeada

- NAND: cuatro combinaciones.
- Full adder: ocho combinaciones A/B/Cin.
- ALU Aula-8: parejas exhaustivas cuando sean razonables, por ejemplo 256 × 256 sumas.
- ALU Aula-16: límites de bandera y casos aleatorizados con semillas reproducibles.
- RAM/ROM: lectura, escritura, triestado, selección y direccionamiento de bordes.
- Aula-16: byte par/impar, palabra par y rechazo de palabra impar.
- CPU: comparar intérprete de referencia independiente con secuencia de control por netlist.
- ISA candidata: controles de opcodes y decodificación documental **no son** ejecución de instrucciones; solo afirmar test funcional de CPU cuando exista un motor independiente.
- Microtrazas candidatas: validar que los eventos esperados no activan simultáneamente RD/WR y que corresponden a bytes propuestos; no confundir eso con prueba de transitorios, frecuencia, firmware o una CPU ejecutada.
- Unidad de control candidata R0.5: el verificador de JSON solo comprueba **secuencias descritas y dependencias**: retención de operandos de dirección, preparación de dato, rutas y recuento de transacciones. No es simulador de microcódigo, estimador de ciclos ni prueba de señales reales.
- Flujo y pila candidata R0.6: comparar orden de lectura/escritura, convenio de retorno little-endian, SP y decisiones de salto como **consistencia documental**. No concluir que CALL/RET/branches ejecutan realmente, que el hardware protege la pila ni que el microcontrol cabe en ROM.
- Pila y banderas candidatas R0.7: contrastar fórmulas aritméticas de 8 bits con enteros matemáticos para Z/N/C/V, verificar rutas declaradas PUSH/POP/INC/DEC y una traza documental; no considerar ese contraste como validación de ALU o CPU real.
- Direccionamiento indexado candidato R0.8: comparar extensión de signo y dos pasadas ALU8 con aritmética modular de 16 bits, selectores X/SP, traza y regiones de RAM/ROM; el contraste documental **no** simula transistores, micro-ROM, CPU ni seguridad física de accesos.
- Ajustes X/SP y marcos candidatos R0.9: contrastar ALU8 en dos pasadas con sumas modulares de 16 bits para LEAX/ADJSP/ADDXW, bytes de opcodes de R0.3, preservación de FLAGS, equilibrio SP y traza CALL/RET. No equivale a ejecutar CPU, certificar seguridad de pila o medir ciclos.
- ABI candidata MiniC-Aula8 R0.10: comprobar orden de PUSH alto/bajo y argumentos derecha/izquierda, offsets de X tras PUSHX/PUSH R2/PUSH R3, registros preservados, CALL/RET, limpieza caller, u16 ADD/ADC y recursividad matemática. La prueba de escritorio no sustituye compilador, intérprete ISA completo ni hardware.
- ROM/monitor candidatos Aula-8 R0.11: contrastar saltos JMP/NOP con opcodes provisionales, tabla FF00–FF7F, vector RESET FFFC/FFFD, presupuesto ROM, protección de MEM/POKE/RUN y transiciones CALL/RET frente a HALT. Las 40 comprobaciones del parser propuesto **no** equivalen a ejecutar el monitor o probar EEPROM, terminal, controlador de bloques, trap ni protección de memoria.
- Controlador de bloques R0.12: comprobar unicidad de ocho registros pares C010–C01E, little-endian del número de bloque y contador, 256 transferencias exactas, abortos de escritura incompleta, errores y reapertura de imagen; plan futuro LOAD con destinos alineados y ventanas protegidas. Las **20 pruebas ejecutan un modelo Python en anfitrión**, no firmware en CPU Aula, controlador físico, persistencia segura tras corte eléctrico ni sistema de archivos.
- AEX1 R0.13: contrastar cabecera 32 B, CRC-16/CCITT-FALSE (vector 123456789→29B1), longitud, tipo de RAM, CPU ID, relleno, bloques y entrada válida; rechazar truncamientos y corrupción antes de **simular** copia RAM en el anfitrión. **42 pruebas de Python**, sin ensamblador, carga de CPU, verificación criptográfica ni garantía de staging nativo; el búfer provisional de 3584 B no sostiene un paquete máximo de herramienta.
- LOADX R0.14: CRC-16 incremental y dos pasadas de bloques de 256 B, primera prevalidación sin escribir RAM y segunda copia de payload. **30 pruebas solo en Python anfitrión** cubren errores tardíos y muestran posible RAM **parcial** sin autorizar la entrada. No fingir ejecución de CPU, enforcement nativo de RUN, atomicidad, recuperación tras corte o memoria temporal medida de firmware.
- Firmware: arranque, servicios públicos y comandos del monitor.
- Programación nativa: verificar que editor y ensamblador corren como **binarios de Aula**; cotejar resultados del ensamblador nativo y cruzado, probar símbolos hacia delante, errores y agotamiento de RAM.
- Panel: CPU detenida, propiedad exclusiva del bus y protección de ROM durante depósito.
- Memoria de software: comprobar ROM, RAM, pila y regiones *overlay* con **mapas de enlace y pruebas reales**; una suma de presupuesto en Markdown solo prueba consistencia aritmética, no cabida de software ejecutable.
- MiniC: compilar, ensamblar, cargar y ejecutar vectores de programas.
- Persistencia: guardar, apagar/reiniciar simulación y recuperar.

## Verificación editorial planeada

- Leer contenido pertinente completo y distinguir hecho, simplificación e hipótesis.
- Explicación continua y causal; no catálogo ni narración de un proceso de IA.
- Imagen precedida por orientación, seguida por identificación de sus elementos y cierre.
- Esquema exacto: los cables, etiquetas, polaridades y estados del texto coinciden con la figura.
- Word principal con estilos, figuras PNG incrustadas y descripción alternativa; sin SVG incrustado.
- Renderizar Word y verificar páginas; exportar PDF y examinarlo **por separado**, incluyendo texto seleccionable.
- Ejercicios y soluciones separados; las pruebas de DocuPodcast solo se declaran efectuadas cuando se puedan ejecutar realmente.

## GitHub y entregas

- Los documentos base deben permitir reanudar el proyecto sin chats previos.
- Cuando exista Java/Maven: pruebas unitarias, smoke tests y CI. No declarar «CI aprobado» en R0 porque no hay software construido.
- Registrar resultados y artefactos reproducibles, con retroalimentación de Windows cuando corresponda.
- Proteger trabajo del usuario y no sustituir archivos por borradores incompletos.

