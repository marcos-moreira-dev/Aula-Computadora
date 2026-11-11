# Informe C28-T · Avance documental sin pruebas nuevas

**Fecha local:** 9 de noviembre de 2026. **Alcance:** material de lectura
y dos nuevas ilustraciones originales. El usuario ha pedido continuar
sin ejecutar ni solicitar pruebas en Windows durante esta ronda.

## Trabajo incorporado

| Entregable | Ruta en el repositorio | Qué aporta |
| --- | --- | --- |
| Despiece del sumador | `c28_t/figuras/c28t_fig01_sumador_completo_nueve_nand.svg` y `.png` | Identifica N1…N9, sus dos entradas y las señales intermedias del sumador completo |
| Ruta ADD/SUB de 8 bits | `c28_t/figuras/c28t_fig02_ruta_aritmetica_8_bits_134_nand.svg` y `.png` | Relaciona ocho XOR condicionales, ocho sumadores, cadena C0…C8 y banderas C/V/N/Z |
| Suplemento didáctico | `libro/SUPLEMENTO_C28T_DEL_BIT_A_134_NAND.md` | Enseña NAND, acarreos, restas y banderas con tablas, ejemplos y referencias a figuras |
| Propuesta de integración | `libro/PLAN_INSERCION_C28T_SIN_REEDITAR_MAESTRO.md` | Describe los lugares previstos de C4, C10 y C11 sin editar el maestro vigente |
| Matriz de correspondencia | `libro/MATRIZ_CIRCUITOS_C28Q.md` | Agrega referencias cruzadas a los nuevos esquemas y explicita sus límites |

Las figuras corresponden a la **topología digital** previamente
serializada por C28-R. La primera dibuja la estructura clásica de un
sumador completo con nueve NAND de dos entradas; la segunda representa
el presupuesto de 134 puertas: 32 para transformar B con `SUB`, 72 para
ocho sumadores, 4 para C, 4 para V y 22 para detectar cero. La bandera
N sale del bit más significativo del resultado.

## Estado y alcance de la evidencia

- La última retroalimentación recibida de Marcos confirma **24/24
  controles Windows aprobados** en C28-Q y cinco fotos históricas.
- C28-R ya contaba con 131.072 casos digitales de ADD/SUB contrastados
  en Python. **No se repitieron ni ampliaron esas pruebas en C28-T**.
- Los cuatro controles adicionales previstos para C28-R/S siguen sin
  evidencia Windows. Por tanto, **no se afirma 28/28**.
- La nueva red es combinacional: no equivale a un circuito eléctricamente
  montado, a 134 chips, ni a un recuento de transistores de fabricación.
- El selector de operaciones lógicas, las banderas de AND/OR/XOR/NOT,
  la ISA definitiva, la CPU integrada, el firmware y la placa siguen
  pendientes. Las políticas de PC anticipado/diferido continúan abiertas.
- **El Word y el PDF maestro C28-G de 248 páginas no se alteraron**.
  La revisión editorial del volumen y la integración C28-H/C28-O
  permanecen como tareas futuras.

## Interpretación del progreso

La estimación razonada del **libro** pasa de **87,3 a 88,5 %**. El
incremento de +1,2 puntos se justifica por el hilo didáctico (+0,15)
y la correspondencia de circuitos y figuras (+1,05), tal como desglosa
`libro/PLAN_CIERRE_EDITORIAL_C28I.md`. **No representa una medición
automática ni el progreso de fabricación de la computadora.**

## Cómo retomar después

Se puede continuar insertando el suplemento en una futura edición
maestra controlada, cotejar circuitos a escala de página y decidir
la política de PC cuando Marcos esté disponible. El paquete global
C28-T conserva todos los materiales previos; el parche C28-T reúne
solo las piezas nuevas y los documentos de continuidad modificados
desde C28-S. Ninguna de esas acciones obliga a Marcos a efectuar
pruebas ahora.
