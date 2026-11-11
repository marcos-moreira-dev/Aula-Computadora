# Estado editorial C27-0.1 — la computadora aparece mientras se aprende

**Fecha:** 8 de noviembre de 2026. **Tipo de entrega:** edición maestra y
fascículos didácticos, no prototipo físico ni CPU ejecutable.

## Resultado medido

- **26 capítulos**: 24 troncales y dos capítulos puente 7B y 23B.
- **236 páginas** en el libro PDF maestro; Word maestro editable y PDF con
  índice medido en el documento final.
- **115 figuras** originales en los capítulos: nueve incorporadas en C27;
  hay **332 ecuaciones OfficeMath** en el Word maestro.
- **110 ejercicios esenciales con solución** en el libro de lectura, según
  relevancia de capítulo, no seis obligatorios por capítulo. Las **312**
  actividades originales con solución siguen en los 26 fascículos y Markdown.
- **20 secciones causales** de construcción seleccionadas: desde señales y
  registro R0 hasta buses, ALU, programa, salto, pila, arranque y Aula-16.
- **9 imágenes técnicas SVG y PNG adicionales**, generadas por un script con
  validación de integridad, incluidos mapas contiguos de RAM y un patillaje
  SN74HCT00N PDIP-14 contrastado con la hoja de datos TI.
- **Portada conceptual nueva**: composición original de taller electrónico
  histórico con máquina ficticia. No es una fotografía de la CPU construida.

## Problemas editoriales atendidos

1. El relato de Aula-8 ya comienza a construirse por piezas antes de la
   presentación arquitectónica del capítulo 12.
2. Las instrucciones concretas se ven en **direcciones consecutivas reales**.
   Flechas externas representan movimiento de PC y cambios por JMP/JNZ/CALL/RET,
   nunca líneas eléctricas inexistentes; se marcan regiones omitidas.
3. Aula-8 muestra por separado 8 líneas de datos y 16 de dirección; Aula-16
   representa banco bajo y alto, con flechas de lectura desde RAM hacia CPU.
4. Se conserva el arreglo visual de la corriente convencional del capítulo 1,
   el control del capítulo 13 y las potencias de base 16 en OfficeMath.
5. Las referencias quedan agrupadas al final y en `FUENTES_CONSULTADAS.txt`.
   Se mantiene cita técnica puntual cuando importa verificar una patilla.

## Verificación realizada

- `scripts/verificar_libro_maestro_c27.py`: 26 capítulos, 115 figuras,
  332 fórmulas, 110 ejercicios esenciales y 236 páginas, sin páginas vacías.
- `scripts/verificar_capitulos_c27.py`: comprueba Word/PDF de 26 fascículos,
  las figuras y todas las ecuaciones contra sus 26 fuentes Markdown.
- `scripts/auditar_revision_c27.py`: confirma nueve figuras derivadas, las
  señales Aula, los bytes de ejemplos candidatos y la presencia de hitos.
- Quince verificadores de contratos y modelos anteriores se ejecutaron
  correctamente. Corroboran modelos matemáticos/documentales, no hardware.
- Se renderizaron **las 236 páginas** en baja resolución para revisar la
  composición general y se ampliaron páginas de alto riesgo (LED, exponente
  hexadecimal, despacho, datapath, programas en RAM, CALL/RET, Aula-16).
- La exportación comprueba que cada PNG es íntegro, evitando incluir imágenes
  truncadas que aparentan ser válidas por nombre/tamaño.

## Límites y pendientes explícitos

- Falta una **lectura humana profesional de principio a fin** para detectar
  matices de estilo y redundancias que las pruebas estructurales no captan.
- Falta el **esquema eléctrico completo**, elección de chips/cables por unidad,
  temporización de la CPU, protoboard certificable, ensayos de alimentación y
  simulación/medición física. El nuevo patillaje no demuestra que el latch esté
  montado.
- La ISA Aula-8 R0.3 y el microcontrol no son definitivos ni ejecutables;
  Aula-16 carece de ensamblado binario definitivo. Falta construir el taller
  guiado y el firmware real.
- Las imágenes históricas documentales (fotografías de equipos reales) siguen
  pendientes de selección, licencia y atribución. La portada conceptual sí
  está terminada, pero no autoriza reproducir otras fotografías.
- La edición queda identificada **C27 candidata de estudio**, no libro
  certificado de publicación ni esquema seguro para fabricar hardware.

Las decisiones de buses, memoria, vídeo V1, RAM/ROM y ABI de los documentos de
arquitectura y contratos anteriores **no se modificaron**.
