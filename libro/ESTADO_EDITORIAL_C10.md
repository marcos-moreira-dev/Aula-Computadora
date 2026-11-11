# Estado editorial después de C10-0.1

**Fecha de corte:** 7 de noviembre de 2026 (Ecuador). El libro tiene **10 de 24 capítulos numerados** con Word/PDF, más el interludio P07B. Permanecen **14 capítulos numerados** (11–24), además de la integración y revisión del volumen maestro. El simulador y la CPU Aula siguen sin implementarse.

## Trabajo del capítulo 10

- **«El circuito que suma»**: necesidad de operar con bytes; aritmética de base dos; medio sumador como XOR/AND y su tabla completa de cuatro estados; sumador completo con dos medios sumadores más OR y su tabla completa de ocho estados.
- **Propagación de acarreo en ocho bits**, diferenciando orden visual de los bits y orden de suma de derecha a izquierda. Prueba completa de **13 + 9 = 22**, con tabla de las ocho posiciones, suma y acarreos. Se explicita el acarreo que produce `S1=1` aunque los dos bits de los operandos allí sean cero.
- **Salida de ocho bits y banderas:** suma sin signo truncada módulo 256, acarreo final `C`; overflow con signo `V` como diferencia de acarreos C7/C8; `Z` y `N`. Casos `250+10`, `127+1`, `FF+01`; `C` y `V` no son sinónimos.
- **Dos pasadas para suma de dieciséis bits** con un sumador de ocho: `01FF+0001=0200`. No se afirma que el diseño definitivo de Aula-8 o Aula-16 ya use estos chips o conexiones.
- **Cuatro figuras propias** SVG/PNG, **8 páginas** Word/PDF, **17 ecuaciones editables OMML**, **12 ejercicios con soluciones** y cuatro tablas útiles para comparar estados/columnas.
- Referencias primarias: Texas Instruments **CD74HC283**, sumador completo de 4 bits con acarreo, y **SN74HC86**, cuatro compuertas XOR. Se contrasta la función lógica con dispositivos reales sin asignarles retardos ni alimentación no medidos.
- El verificador `scripts/verificar_capitulo_10.py` contrastó exhaustivamente **131072** operaciones de suma `A+B+Cin` de ocho bits, comprobando resultado, acarreo, overflow, Z/N, invariantes bit a bit y archivos; **786541 controles matemáticos/documentales**. Incluido en CI.

## Limitaciones explícitas

Los esquemas son **funcionales**, no netlists o esquemas de conexión eléctrica. La propagación en papel no fija nanosegundos, frecuencia máxima, compatibilidad de niveles, pinout, disipación o desacoplo. Ninguna ALU, CPU, micro-ROM, memoria Aula ni prototipo físico se han ensayado. Las banderas referidas al Aula-8 candidato aún deben consolidarse en el diseño final junto con las operaciones de resta, que se estudiarán en el capítulo 11.

## Estado acumulado

| Indicador | C10-0.1 |
|---|---|
| Capítulos numerados previstos | **24** |
| Capítulos numerados redactados Word/PDF | **10** |
| Interludios redactados | **1** (P07B) |
| Capítulos numerados restantes | **14** (11–24) |
| Páginas de capítulos e interludio | **95** (87 + 8) |
| Figuras SVG/PNG originales | **42** |
| Ejercicios resueltos | **132** |
| Ecuaciones Word OMML | **130** |
| Controles del capítulo 10 | **786541** |
| Word/PDF maestro e índice general | **Pendientes** |
| CPU, firmware, chips conectados y aplicación | **No implementados** |

## Qué falta para concluir

1. Redactar los capítulos **11–24**, empezando por **«La unidad aritmético-lógica»** con resta, comparación, funciones lógicas y banderas.
2. Revisar las **95 páginas** en conjunto: continuidad, notación binaria/hexadecimal, citas de fabricantes, correspondencia entre gráficos y texto, ejercicios e integridad de solucionarios.
3. Consolidar las decisiones candidatas de hardware de Aula-8 y Aula-16 **antes** de prometer ejecución física, compatibilidad de programas, tiempos o mapa definitivo.
4. Componer **Word y PDF maestros** con portada, navegación, glosario, créditos, bibliografía, accesibilidad y paginación global.
5. Realizar en una etapa separada la revisión eléctrica/temporal y el desarrollo de software; ninguna verificación matemática actual equivale a lo anterior.

## Reproducción

```bash
python3 scripts/generar_figuras_capitulo_10.py
python3 scripts/generar_capitulo_10.py
# Exportar el Word a PDF y validar su maquetación visual.
python3 scripts/verificar_capitulo_10.py
```
