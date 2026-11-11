# C28-L · Lectura didáctica y auditoría lógica de los fundamentos

**Fecha:** 9 de noviembre de 2026. **Ámbito:** capítulos 1 a 7B de
*Aula-Computadora*, edición fuente C28-G. Esta es una auditoría **parcial**:
no supone que se haya leído y validado todavía la edición completa.

## Qué encontró la lectura

| Tramo | Relación concepto → uso en nuestra computadora | Observación |
| --- | --- | --- |
| 1: corriente | Fuente, resistencia y LED; diferencia entre recorrido de corriente y medida | La práctica usa baja tensión y advierte cómo no cortocircuitar con el amperímetro. |
| 2: transistor | Interruptor controlado por señal que prepara el concepto de decisión lógica | La identificación física del 2N3904 es específica del fabricante/encapsulado y así se advierte. |
| 3: puertas | De tabla de verdad a NAND comercial y a sus combinaciones NOT, AND y OR | El capítulo distingue función ideal de requisitos eléctricos reales. |
| 4: funciones | XOR de cuatro NAND que permite combinar condiciones en una red | La lámina `c04_fig03_xor_cuatro_nand.png` representa visualmente las cuatro fórmulas y sus ramales; no es una netlist certificada. |
| 5: realimentación | Latch SR NAND: SET, RESET, HOLD y entrada prohibida | Los estados válidos y el estado 00 se comprueban en el modelo; la salida después de liberar 00 no se predice. |
| 6: tiempo | Diferenciar latch sensible a nivel de flip-flop D sensible a flanco | El modelo no pretende medir tiempos de preparación, mantenimiento ni metastabilidad. |
| 7: registro | Ocho flip-flops con selección LOAD/retenido; primer bloque de almacenamiento Aula-8 | Se comprueban exhaustivamente los 256 valores anteriores × 256 valores de entrada × 2 valores LOAD. |
| 7B: significado | Del estado eléctrico al valor codificado; evita tratar un byte como instrucción sin ISA | Es un puente conceptual, no un componente hardware nuevo ni una ISA definitiva. |

Se observó una progresión real de la explicación a **piezas reutilizables**.
El encabezado exacto «Construimos...» no es la única forma de hacerlo;
por ejemplo, los capítulos 1, 2 y 7B hacen el puente con otros títulos.

## Prueba reproducible C28-L

Ejecutar desde la carpeta `Aula-Computadora`:

```powershell
py .\scripts\c28l_verificar_logica_inicial.py
```

| Familia / comprobación | Comparaciones superadas |
| --- | ---: |
| NAND y XOR construido con cuatro NAND | 8 |
| NOT, AND y OR fabricadas matemáticamente con NAND; presencia de fórmulas C03 | 15 |
| Presencia de cuatro fórmulas y referencia a diagrama XOR C04 | 5 |
| Latch SR NAND y cinco pasos narrativos | 13 |
| Latch D y flip-flop D ideales, estados y ejemplo temporal | 31 |
| Registro Aula-8 de ocho bits, selección LOAD y retención | 131.072 |
| **Total de comparaciones** | **131.144** |

El resultado se guarda en `c28_l/auditoria/C28_L_RESULTADOS.json` y el
script forma parte también de la prueba global de Windows.

**Interpretación correcta de las cifras:** contar 131.144 comparaciones no
equivale a disponer de 131.144 circuitos independientes ni de ensayos físicos.
La mayoría proviene del espacio exhaustivo de entradas de **un registro de
ocho bits**. Los cálculos cotejan modelos digitales con tablas/contratos y
la presencia de ciertas expresiones del manuscrito; **no certifican que
cada trazo de cada PNG esté bien cableado**.

## Distinciones y comprobaciones todavía pendientes

1. **Consistencia de dibujo:** transcribir las conexiones de esquemas
   prioritarios a netlists y cotejar punto por punto los nodos y terminales.
2. **Simulación de hardware digital:** preparar o cotejar testbenches HDL
   de esos mismos esquemas. Los pilotos C28-F/H sí tienen sus pruebas Verilog,
   pero no representan todos los circuitos del libro.
3. **Comportamiento físico:** confirmar hojas de datos, polaridades, alimentación,
   tolerancia, retardos y corrientes antes de presentar una lámina como plano
   construible. Simular lógica abstracta no demuestra estabilidad eléctrica.
4. **Edición publicada:** el Word/PDF maestro sigue siendo C28-G. Este
   diagnóstico y el piloto C28-H todavía no están integrados en sus páginas.
5. **Lectura editorial:** completar el examen de capítulos 8–24 y después
   inspeccionar la exportación final del libro página por página.

Fuentes de contraste para componentes citados:

- Texas Instruments, [SN74HCT00: cuatro puertas NAND de dos entradas](https://www.ti.com/product/SN74HCT00).
- Texas Instruments, [SN74HC74: dos flip-flops D de flanco ascendente](https://www.ti.com/product/SN74HC74).

La presente prueba no altera las alternativas de política del contador de
programa (PC anticipado o diferido), ni instala software ni crea repositorios.
