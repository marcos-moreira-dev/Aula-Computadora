# Fotografias historicas propuestas para Aula-Computadora · C28-N

**Estado C28-O: cinco fotos descargadas y verificadas; atlas histórico creado,
integración definitiva en Word/PDF maestro pendiente.**
Se verificaron paginas individuales de Wikimedia Commons el 9 de noviembre de 2026.
El ZIP de retroalimentación de Marcos confirmó cinco descargas correctas;
se revisaron visualmente, se cotejaron los SHA-256 y se conservaron
en `libro/figuras_historicas_c28o/`. Sus explicaciones y créditos figuran
en `libro/ATLAS_HISTORICO_C28O.md` y en el PDF de `libro/ediciones/C28_O/`.
No se ha insertado nada en la edición maestra C28-G.

| ID | Fotografia | Credito/licencia | Enseñanza y posible lugar |
| --- | --- | --- | --- |
| H01 | [Panel de MITS Altair 8800](https://commons.wikimedia.org/wiki/File:MITS_Altair_8800_Front_Panel.jpg) | Cromemco; CC BY-SA 4.0 | Interruptores y LED: capitulos 14–17 |
| H02 | [Placa de Apple II](https://commons.wikimedia.org/wiki/File:Apple_II_motherboard_(53171103722).jpg) | Steve Jurvetson; CC BY 2.0 | Interconexion de circuitos, memorias y buses: capitulos 9–12 |
| H03 | [Terminal DEC VT100](https://commons.wikimedia.org/wiki/File:DEC_VT100_terminal.jpg) | Jason Scott; CC BY 2.0 | Terminal, codigos y video: capitulos 18 y 23B |
| H04 | [Procesador Intel P8086](https://commons.wikimedia.org/wiki/File:Intel_P8086.jpg) | Thomas Nguyen; CC BY-SA 4.0 | Diferencia entre CPU educativa y microprocesador comercial: capitulo 22 |
| H05 | [IBM PC 5150](https://commons.wikimedia.org/wiki/File:Ibm_pc_5150.jpg) | Ruben de Rijcke; CC BY-SA 3.0 | Computadora personal integrada: capitulos 22–24 |

## Rigor historico y tecnico

- El Altair 8800 aparecio en el entorno de microcomputadoras de 1975; la foto
  es contemporanea **del aparato conservado**, no una fotografia fechada en 1975.
- La placa del Apple II no identifica por si sola todos los circuitos;
  las etiquetas de CPU/RAM/ROM requeriran un esquema complementario propio.
- El terminal VT100 sirve para explicar interfaz de caracteres, **no** para
  validar el contrato de video ni los circuitos de Aula.
- El 8086 real no demuestra nada sobre una CPU Aula-16 que aun no esta integrada.
- El IBM PC original de modelo 5150 usaba **Intel 8088** (bus externo de 8 bits).
  No confundirlo con el Intel 8086 de la foto H04.

## Recogida automatica y protecciones

La ejecucion `PROBAR_TODO_GLOBAL_C28H.cmd` llama ahora al recolector
`scripts/c28n_recolectar_fotos_historicas.py` al terminar las pruebas.
**Solo necesita el mismo Python 3 (`py`) de las pruebas previas**.
Consulta primero la API de Wikimedia Commons, compara la licencia y descarga
una version de hasta 1800 pixeles, sin copiarla al manuscrito.
Todos los resultados llegan dentro de `_PRUEBAS_GLOBAL_C28H_.../FOTOS_HISTORICAS_C28N/`
del ZIP de retroalimentacion, con SHA-256, fuente, autor, licencia e incidencias.
Cada recurso tiene limite de 10 MiB; total del lote 35 MiB. La falta de
conexion o un cambio de permiso queda registrada sin alterar el 17/17 de
la auditoria de logica/HDL.

**Siguiente paso editorial:** revisar el atlas junto al hilo completo de
los 26 capítulos, decidir emplazamiento de las figuras en Word/PDF,
conservar las atribuciones y avisos de modificación/recorte pertinentes,
regenerar el PDF maestro y revisar todas las páginas. Ninguna foto demuestra
el funcionamiento lógico o físico de un circuito.
