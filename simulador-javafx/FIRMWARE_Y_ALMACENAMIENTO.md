# ROM, terminal, monitor y almacenamiento

## Dos ROM con propósitos diferentes

- **ROM de microcontrol:** memoria del secuenciador de CPU; no aparece en el mapa de direcciones de programas.
- **ROM de firmware:** espacio 0xE000–0xFFFF, contiene arranque, servicios y monitor.

## Arranque previsto

1. RESET.
2. Leer vector de 16 bits en 0xFFFC.
3. Inicializar SP, registro de estado y buffers necesarios de RAM.
4. Inicializar terminal fijo.
5. Mostrar identificación y símbolo de sistema listo.
6. Entrar en bucle de comandos por polling.

La RAM no se presume inicializada. En Aula-16, el monitor respetará alineación de palabra y byte lanes.

## Tabla pública de servicios

| Posición prevista | Nombre simbólico | Propósito |
| --- | --- | --- |
| 0xFF00 | FW_PUTC | emitir carácter |
| 0xFF04 | FW_GETC | recibir carácter |
| 0xFF08 | FW_PUTS | emitir cadena |
| 0xFF0C | FW_STATUS | consultar terminal |
| futuras ranuras de 4 B | FW_READ_BLOCK / FW_WRITE_BLOCK | acceso al almacenamiento |
| 0xFFFC | RESET VECTOR | dirección de inicio |

El acceso a ranuras es por CALL; la implementación interna de cada servicio puede cambiar sin modificar el punto de entrada. Las firmas exactas y preservación de registros siguen pendientes de ABI R1.

**Anexo Aula-8 R0.11, propuesta no aprobada:** [contrato de ROM y monitor hexadecimal](ROM_MONITOR_AULA8_R0_11_BORRADOR.md) y [JSON](ROM_MONITOR_AULA8_R0_11_BORRADOR.json). Las cuatro entradas actuales usan un `JMP` absoluto de 3 B y `NOP` de relleno: FF00→E100, FF04→E140, FF08→E180, FF0C→E1C0, **destinos solo ilustrativos**. Se reservan las 32 ranuras FF00–FF7F (128 B) sin hacer públicas las restantes. RESET FFFC/FFFD admite el ejemplo little-endian `00 E0` para E000; no se ha creado una imagen de ROM. La ABI candidata exige R2/R3/X preservados, R0/R1/FLAGS volátiles y RET que equilibra la pila, **sin imponer el marco MiniC**. La asignación hardware de bits de STATUS y los servicios de bloques siguen pendientes.

## Terminal

Interfaz predeterminada de consola de **caracteres de 8 bits**, con ASCII básico y futura tabla extendida documentada. Registros mapeados en 0xC000 (DATA) y 0xC002 (STATUS), sin modificar la ABI de las cuatro entradas ROM públicas candidatas. Evitar emular toda una pantalla VGA o teclado matricial interno en V1.

**Actualización de diseño lógico V1:** la salida de consola alimentará el buffer de texto de **una única pantalla virtual**, que también puede seleccionar bitmap de cuatro colores. El [controlador de vídeo](CONTRATO_VIDEO_AULA_V1.md) tiene VRAM indirecta mediante `C020–C02F`; cambiar de modo no borra el texto. Esto **no equivale a implementar** la CPU, el firmware, una terminal física serial o un sistema real de salida de vídeo. La terminal física o pantalla comercial concreta se elegirá al diseñar esquemas; el simulador conserva una interfaz fija y no dispositivos arbitrarios.

## Monitor

Comandos nucleares: HELP, MEM, POKE, LOAD, RUN, REG. Pueden añadirse DUMP, DIR, SAVE y TYPE cuando exista formato de sistema de archivos adecuado.

Los programas cargados en RAM se invocarán conforme a ABI; el retorno al monitor debe ser explícito y comprobable.

La ROM mínima no tiene que contener editor, ensamblador, sistema de archivos completo ni compilador. El **editor de líneas y ensamblador nativos de Aula-8** se cargarán en RAM como utilidades desde la imagen de bloques. Debe existir un cargador de bloques crudos antes de presuponer un directorio o `LOAD archivo` por nombre. Ver [programación desde cero](PROGRAMACION_DESDE_CERO.md).

Un presupuesto de ROM 8 KiB y RAM 32 KiB con región *overlay* aparece en [PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md](PRESUPUESTO_ROM_RAM_Y_BOOTSTRAP.md); no hay tamaños de binarios comprobados todavía.

R0.11 concreta **solo como interfaz candidata** la sintaxis `MEM 6000 10`, `POKE 6000 2A` y `RUN 6000`: los comandos POKE y RUN usan inicialmente la ventana 6000–6FFF; `MEM` solo recorre RAM o ROM, nunca E/S mapeada ni rangos desbordados. RUN crea una llamada al programa, y solo `RET` con pila equilibrada permite recuperar el prompt. `REG` y `LOAD` responden NO DISPONIBLE hasta diseñar el respaldo de registros y el controlador de bloques. No existe monitor programado.

`HALT` significa detener la ejecución; **no** se asumirá que equivale automáticamente a `RET` o que recrea el prompt. Falta especificar el mecanismo correcto de salida de un programa. Igual ocurre con el comando `REG`, cuya captura/restauración de registros depende de un contrato de depuración o trap todavía pendiente.

## Almacenamiento persistente

- Dispositivo digital de bloques fijos de **256 bytes**, respaldado por archivo imagen.
- Puerto de comandos, estado, dirección de bloque y transferencia de datos.
- El contenido debe sobrevivir al cierre y reapertura del simulador cuando se guarde.
- **No** simular físicamente cabezales de disco duro, casetes o platos.
- Modelo exacto de registros, endian de número de bloque, errores, checksum y directorio de archivos: pendiente de hito R1/R5.
- **R0.12: propuesta revisable** de [ocho registros MMIO y protocolo READ/WRITE](CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.md), con [JSON](CONTROLADOR_BLOQUES_AULA8_R0_12_BORRADOR.json). Se concretan como candidatos COMMAND/STATUS/BLOCK_LO/BLOCK_HI/DATA/ERROR/COUNT_LO/COUNT_HI en C010–C01E, todos de 8 bits en direcciones pares. El checksum, directorio y controlador físico siguen pendientes.
- Un micro sistema de archivos sencillo se desarrollará solo después de demostrar operaciones de bloques correctas.
- Al ampliar a archivos: comprobar que cada ejecutable declara correctamente CPU destino (Aula-8/Aula-16), rangos de RAM, punto de entrada y tamaño. No cargar accidentalmente binarios incompatibles en el bus de la otra arquitectura.

El futuro comando `LOAD bloque destino cantidad` se restringiría a bloques enteros y destinos alineados dentro de 1000–2FFF (herramientas) o 6000–6FFF (programas). **Continúa NO DISPONIBLE** en el monitor de R0.11. El modelo de referencia Python verifica la lógica de bloque y la reapertura de un archivo temporal **en el anfitrión**, no demuestra que firmware Aula ni un circuito real pueda hacerlo.

# R0.13: paquetes de programas AEX1 (NO aprobados)

Un contenedor Aula-8 **AEX1** cabe en sectores crudos R0.12 de 256 B: cabecera
de 32 B (CPU 08, tipo, origen/entrada/longitud, CRC16 de cabecera y payload)
y programa útil. El `LOAD` crudo R0.12 sigue independiente del hipotético
`LOADX bloque_hex4` con validación previa. **Ambos comandos continúan sin
firmware nativo**. Un paquete para overlay no puede ejecutarse mediante el
`RUN` de práctica de R0.11.

El [contrato detallado](EJECUTABLE_AEX1_AULA8_R0_13_BORRADOR.md) identifica
un bloqueo importante: los 3584 B del búfer provisional de ROM son menores
que el máximo de 8160 B del payload de herramienta. La referencia anfitriona
sí retiene el archivo completo, pero **no demuestra** que eso sea viable en
RAM de Aula-8 con las regiones presupuestadas. Queda pendiente resolver
staging/rollback y dimensionar ROM; ningún servicio nuevo de la tabla FF00
se considera asignado.

## R0.14: validación en dos pasadas (solo Python)

El [contrato LOADX R0.14](LOADX_DOS_PASADAS_AULA8_R0_14_BORRADOR.md)
propone **primero** verificar el AEX1 entero con CRC16 incremental
y un temporal de 256 B, **después** releer para copiar únicamente
los bytes útiles. Esto evita necesitar un staging completo de 8160 B
en RAM. **Sigue sin haber firmware LOADX** ni enforcement de RUN:
si la segunda pasada falla puede haber RAM parcial, nunca se debe
invocar el código. La lectura estable, atomicidad y recuperación
ante corte eléctrico siguen sin garantía.

