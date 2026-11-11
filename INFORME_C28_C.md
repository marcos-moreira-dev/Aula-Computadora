# Aula-Computadora — informe de avance C28-C

**Fecha de trabajo:** 8 de noviembre de 2026. **Estado:** edición de trabajo, todavía no es el libro final.

## Qué avanzó

1. El capítulo 7 presenta ahora una **celda completa de R0**: MUX de entrada con realimentación, flip-flop D, reloj de flanco ascendente y salida triestado con `OE_n`. Se explica que `LOAD` controla la captura y `OE_n` controla la conducción al bus; no son operaciones equivalentes.
2. El mismo capítulo despliega las **ocho posiciones de R0**, de `IN7` a `IN0`, con carriles independientes hasta `BUS7` a `BUS0`. Se conservan las dos tablas de verdad introducidas en C28-B, así como los casos de retención, carga y estado `Z`.
3. El capítulo 22 incluye un **bus Aula-16 de dieciséis conductores**, visibles uno por uno, repartidos entre banco alto (`D15…D8`) y banco bajo (`D7…D0`). El gráfico distingue conductor, banco y dirección: `A14…A1` selecciona fila, `A15` región y `A0` carril de byte en la RAM del ejemplo.
4. La figura del bus se genera por código SVG de forma reproducible. El generador verifica que existan exactamente 16 vías y que cada una corresponda a su banco. Se entrega también la representación PNG para la edición Word/PDF.
5. Se regeneraron las fuentes de los capítulos y los maestros en `libro/ediciones/C28_C`, preservando intactos C27 y C28-B.

## Verificaciones y límites

- **509.268 comparaciones** del modelo lógico Python de C28-A siguen siendo la prueba disponible de NAND, flancos, carga, retención, triestado y estado inicial desconocido. La ejecución se repitió en C28-C.
- **16 vías de datos distintas** y asignaciones a los bancos correspondientes: verificadas automáticamente en el SVG.
- El Word maestro contiene **121 imágenes**: las 118 de C28-B y tres láminas de circuito adicionales. El PDF de trabajo pasó a **239 páginas A4**.
- La paginación y el índice fueron reconstruidos a partir del PDF de esta edición.
- Se realizó una revisión visual de las láminas nuevas en páginas representativas del PDF. Esa revisión no equivale a inspeccionar individualmente cada una de las 115 figuras heredadas.
- Los dibujos son **modelos digitales funcionales**. No se declara verificado ningún circuito eléctrico con patillas de integrados, alimentación, retardos reales, simulación de Verilog o montaje físico.

## Qué continúa

1. Completar la auditoría visual por figura y página, con atención a cables cruzados, rótulos y ecuaciones; corregir las incidencias confirmadas sin alterar esquemas correctos.
2. Derivar los esquemas críticos de una **descripción única del circuito** (conectividad/netlist o HDL), ejecutar pruebas digitales reproducibles, y generar dibujos a partir de conexiones verificadas. Una lámina conceptual no sustituye un esquema lógico verificable ni un plano de montaje.
3. Continuar **Aula-8** como construcción progresiva: registro, bus, ALU, control, memoria, contador de programa, y programas cortos. Mostrar la RAM como direcciones contiguas y dibujar flechas en las instrucciones de salto, con estados antes/después.
4. Mantener Aula-16 como evolución gradual de Aula-8. Aún están por fijarse el mapa final de regiones, contrato de instrucciones y detalles de microarquitectura.
5. Implementar el motor y las pruebas de **JavaFX** cuando la semántica de la computadora sea suficientemente estable. El debate concreto de **UX/UI** queda reservado para esa fase con Marcos; no se adelantan pantallas como si fueran decisiones tomadas.
6. Integrar posteriormente capturas comprobadas del simulador y las ilustraciones históricas en el libro. El arte de portada aprobado es decorativo y no se usará para demostrar una conexión eléctrica.

## Reproducibilidad

La edición C28-C se puede regenerar sobre C27 + el parche C28-B + el parche C28-C con `scripts/generar_c28c_bus16_carriles.py` y `scripts/generar_libro_maestro_c28c.py`. El guion específico para Windows está en `LEEME_PARCHE_C28_C.txt`.
