# Estado editorial después de C07-0.1

**Fecha de corte:** 6 de noviembre de 2026. **Alcance:** siete capítulos numerados del libro con manuscrito, ilustraciones, Word y PDF. Los modelos técnicos R0.14 siguen siendo candidatos; no hay CPU, firmware ni protoboard funcional verificados.

## Entrega del capítulo 7

- **«Del bit al registro»**: ocho flip-flops D conservan un byte, b7…b0, y el texto explica cómo se leen sus pesos de potencias de dos sin suponer todavía una interpretación de software.
- Conversión íntegra `10110110₂ = 182₁₀ = 0xB6`, con todos los términos, incluidos los que aportan cero.
- **LOAD** independiente del reloj: un multiplexor permite elegir la entrada nueva o el estado anterior; en el flanco ascendente todos los bits capturan o retienen según la habilitación.
- **OE_n y alta impedancia Z**: un búfer decide si el valor guardado se conduce al bus; deshabilitarlo no borra el registro, Z no es otro bit y un bus sin conductor no debe presumirse cero.
- Transferencia demostrada entre dos registros A y B: A = `0x3C`, B = `0xA5`; B captura `0x3C`, A conserva `0x3C`. El control prohíbe que dos salidas conduzcan simultáneamente.
- Referencias a **Texas Instruments SN74HC377** (ocho flip-flops de flanco ascendente con habilitación de carga; **sin** salida triestado) y **SN74HC245** (transceptor bidireccional de bus con OE_n; **sin** memoria interna), sin confundirlos con el modelo didáctico compuesto.
- **Cuatro figuras originales SVG/PNG**, Word editable y PDF de **ocho páginas**, nueve ecuaciones OMML y **12 ejercicios resueltos**.
- Verificador independiente: **198502 controles** de lógica de carga/retención, conversión de los 256 bytes, conducción exclusiva y consistencia de manuscrito, ecuaciones, dibujos y PDF. Incluido en CI.

**Límites:** la simulación ideal hecha en Python no verifica integración de componentes, niveles de tensión, transitorios, disipación por contención, tiempos de setup/hold, retardo de buses, inicialización física ni firmware. Las hojas de datos son referencias, no certificación de un circuito construido.

## Estado acumulado

| Indicador | C07-0.1 |
| --- | --- |
| Capítulos previstos | **24** |
| Capítulos redactados con Word y PDF | **7** (1–7) |
| Capítulos numerados pendientes | **17** (8–24) |
| Páginas acumuladas | **62** (9 + 10 + 10 + 9 + 8 + 8 + 8) |
| Figuras originales | **26 SVG + 26 PNG** |
| Ejercicios con solucionario | **84** |
| Ecuaciones OMML | **82** |
| Comprobaciones específicas C07 | **198502** |
| Puente sobre semántica y significado | Propuesto sin redactar ni renumerar |
| Portada, índice y Word/PDF maestro | Pendientes |
| CPU, firmware y aplicación educativa | No implementados |

## Qué falta para terminar el libro aparte de la portada

1. **Redactar los 17 capítulos 8–24** con diagramas exactos, ejemplos comprobados y ejercicios resueltos. Los próximos cuatro desarrollan direcciones/buses, RAM/ROM, sumadores y ALU.
2. Desarrollar el **puente «Del bit al significado»**, previsto entre los capítulos 7 y 8. Falta decidir si queda como interludio sin numerar o se incorpora como capítulo numerado (lo que elevaría el currículo a 25). El concepto está aceptado; **la numeración nueva no lo está**.
3. Antes de los capítulos que enseñan instrucciones y programas, **cerrar y verificar los contratos de Aula-8 y Aula-16** (ISA, datapath, señales de control, ROM/monitor, memoria, puertos, temporización, ensamblador, compilación y casos de arranque). Hoy son propuestas documentales, no código ejecutable.
4. Hacer una **auditoría pedagógica transversal** de los capítulos 1–7: vocabulario acumulativo, índices de bits, supuestos de electrónica, correlación imagen/texto, problemas y respuestas. Lo que sea ejercicio teórico debe identificarse como tal; cualquier práctica física exige su propia validación.
5. Componer el **Word maestro y PDF maestro**, con índice navegable, glosario de términos, abreviaturas, bibliografía, créditos, referencias cruzadas, paginación continua y versiones de lectura e impresión.
6. Ejecutar controles finales de **ortografía, accesibilidad, consistencia visual, derechos de texto/figuras y formatos de exportación**. No declarar DocuPodcast, montajes reales ni publicación GitHub como terminados si todavía no se prueban.

## Reproducir esta entrega

Con Python 3, `python-docx`, Inkscape, LibreOffice y Poppler:

```bash
python3 scripts/generar_figuras_capitulo_07.py
python3 scripts/generar_capitulo_07.py
# Exportar el Word a libro/capitulos/07_del_bit_al_registro.pdf
python3 scripts/verificar_capitulo_07.py
```

**Siguiente hito editorial sugerido:** redactar el puente entre bits y significado como interludio independiente sin alterar el total de 24, y después continuar con el capítulo 8 «Direcciones y buses». La decisión sobre convertirlo en capítulo numerado requiere aprobación de Marcos.
