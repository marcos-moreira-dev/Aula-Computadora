# Aula-Computadora | Estado de comprobación y ruta anterior a JavaFX

**Corte de evidencia: piloto C28-H.** Esta matriz distingue tres artefactos que
no son intercambiables: una explicación en el libro, una verificación digital
y un plano que un estudiante pueda construir. No se confunde un diagrama de
bloques SVG con un esquema de puertas eléctricamente conectado.

## Qué se sabe y qué falta

| Bloque del aprendizaje | Uso progresivo en nuestra computadora | Evidencia disponible | Comprobación todavía pendiente |
| --- | --- | --- | --- |
| Transistor, niveles lógicos y NAND | De estados físicos idealizados a la primera puerta | Explicación conceptual y reglas booleanas; piloto de NAND referido en C28-A | Modelo eléctrico con polarización, márgenes de ruido, fan-out y tiempos de propagación |
| NOT, AND, OR, XOR, decodificadores | Componer funciones con NAND y seleccionar líneas | Tablas de verdad conceptuales y subpruebas lógicas de los pilotos anteriores | Prueba automatizada por puerta y esquema verificable de cada composición |
| Latch, flip-flop D y reloj | Pasar del cálculo instantáneo al estado almacenado | Pruebas de flancos y retención reportadas en C28-A | HDL separado del almacenamiento elemental; montaje y tiempos setup/hold |
| Registro de 8 bits | Mantener datos y habilitar LOAD/HOLD/Z | **509.268 comparaciones correctas** reportadas por Marcos para C28-A | Ejecutar testbench HDL del registro completo y generar netlist de puertas |
| Sumador/ALU y banderas | Crear resultados aritméticos y decisiones | Modelos de referencia de la línea C28; no consta aquí certificación HDL integral de la ALU | Vectores exhaustivos por operación y verificación RTL/puertas |
| PC y MAR | Seleccionar la dirección de instrucción o de datos | C28-F: **73.536 casos HDL** reportados por Marcos; rutas y protocolo modelados en C28-G | Concordancia entre implementación secuencial, modelo y política final de PC |
| MAR, RD, READY y MDR | Pedir un byte, esperar y conservarlo | C28-G: 8.360 casos de subconjunto Verilog comparados con referencia; C28-H: **24.248** verificaciones de modelo Python | Correr **Icarus Verilog** para el RTL secuencial C28-H en Windows; READY aún es estímulo ideal |
| RAM/ROM, escritura, buses | Convertir lecturas individuales en memoria utilizable | Protocolo de lectura docente, sin temporización física | WR, arbitraje, triestado si aplica, mapa coherente y dispositivo concreto |
| Secuenciador, ISA y CPU integrada | Unir ALU, registro, contador, memoria e instrucciones | Diseño pedagógico en evolución | Integración extremo a extremo: FETCH/DECODE/EXECUTE, ramas, interrupciones y programas de prueba |
| Programa de simulación JavaFX | Permitir observar y manipular todos los estados | **Pendiente de debate UX/UI** por decisión de Marcos | Especificar vistas, controles, trazas y contratos después de consolidar arquitectura digital |

**Precisión sobre la evidencia:** los resultados históricos C28-A/C28-F/C28-G
son salidas previamente compartidas por Marcos; este ZIP no reproduce por sí
solo esos proyectos completos. Los únicos vectores incluidos y reproducibles
aquí son los del piloto C28-H. Un resultado de modelo Python no se convierte
automáticamente en una simulación de circuito Verilog.

## Secuencia editorial obligatoria por cada bloque

1. **Problema concreto:** qué necesita hacer nuestra computadora a continuación.
2. **Concepto nuevo:** qué es y por qué el bloque anterior no basta.
3. **Tabla de verdad o tabla de transición:** todas las entradas relevantes;
   distinguir circuitos combinacionales de secuenciales.
4. **Construcción de menor a mayor:** puerta → componente → registro → bus
   → bloque de CPU; numerar señales, anchos y conexiones.
5. **Ejemplo trabajado con valores:** recorrer una entrada real, un flanco o
   una lectura y mostrar dónde aparece el resultado.
6. **Comprobación digital reproducible:** oráculo, vectores y prueba HDL,
   con reporte de aprobado/fallido y limitaciones explícitas.
7. **Imagen 2D trazable:** esquema funcional primero; luego netlist de puertas
   si se sintetiza; esquema físico con pines solo después de elegir chips.
8. **Enlace al capítulo siguiente:** qué nueva capacidad permite integrar.

Si alguno de los pasos 4, 6 o 7 está incompleto, marcarlo como **pendiente**;
no disimularlo con una figura decorativa ni introducirlo como si ya fuera un
producto funcional.

## Próximos hitos antes del diálogo UX/UI de JavaFX

1. Ejecutar el archivo `PROBAR_C28H.cmd` en Windows. Recoger el ZIP de
   retroalimentación; registrar la salida explícita de Icarus.
2. Comparar trazas PC anticipado/diferido y decidir una **política del
   contador de programa** con Marcos antes de integrar el controlador.
3. Auditar puertas y elementos secuenciales del libro con tablas de verdad,
   referencias y testbenches individuales; las ilustraciones de cada bloque
   tendrán el mismo nombre de señal que los módulos HDL.
4. Extender el piloto a **escritura y RAM de prueba** con lectura/escritura,
   reset, selección de dirección y colisiones; no simular tiempos físicos.
5. Conectar el camino de datos de CPU con una ISA educativa acordada y
   ejecutar al menos dos programas pequeños sobre el modelo y el HDL.
6. Exportar diagramas 2D reproducibles: funcional, RTL y puertas sintetizadas
   (por ejemplo Yosys + Graphviz si se instalan). Guardar versión y evidencia.
7. Volcar estos resultados al libro maestro y hacer auditoría didáctica:
   problema→concepto→construcción→prueba→siguiente componente.
8. Recién entonces debatir con Marcos el simulador JavaFX, su UX/UI y los
   niveles de detalle según el estudiante: vista general, interna y temporal.

## Política de no sobreatribución

- La **verificación digital funcional** prueba correspondencia con un contrato
  idealizado: no prueba circuitos integrados reales, electricidad o velocidad.
- El **diagrama SVG de C28-H** es funcional: visualiza conexiones abstractas,
  no es todavía un netlist puerta a puerta fabricable.
- La **simulación HDL** del nuevo piloto se considera pendiente hasta recibir
  la salida real de Icarus en Windows y revisar los datos de retroalimentación.
- Elegir PC anticipado o diferido es una decisión de arquitectura del autor,
  no un resultado que el testbench pueda imponer.
