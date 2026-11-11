# Diagramas, esquemas y mini enciclopedia de componentes

## Capas de representación

| Vista | Pregunta que resuelve | Ejemplo |
| --- | --- | --- |
| Física | ¿Qué pieza o terminal se conecta? | protoboard, pinout de NPN, SRAM en DIP |
| Eléctrica | ¿Cómo se comporta el circuito? | VCC/GND, resistencias, CE#/OE#/WE# |
| Lógica | ¿Qué función ejecuta? | NAND, latch, full-adder |
| Temporal | ¿Cuándo cambia su salida? | reloj, setup/hold, read/write |
| Arquitectónica | ¿Cómo colabora con otras unidades? | registros, ALU, buses, RAM/ROM |
| Software | ¿Qué estado produce una instrucción? | PC/IR/R0/flags por micro-paso |

La portada o ilustraciones históricas pueden ser artísticas; **nunca reemplazarán** un esquema técnico exacto.

## Convenciones

- Preferir símbolos normativos reconocibles y una leyenda cuando se use una variante IEC/ANSI.
- Nombrar redes y polos sin ambigüedad: VCC, GND, A0, D0, CLOCK, CE#, OE#, WE#.
- Diferenciar cruce de cables de unión eléctrica mediante puntos y rutas legibles.
- Documentar dirección y ancho de cada bus; no representar 16 líneas como una señal de 1 bit.
- Contar bytes por direcciones, no inferir memoria total solo a partir del ancho del bus.
- Dibujar físicamente el selector de carril par/impar de Aula-16 cuando se llegue a memoria de 16 bits.

## Mini ficha de cada componente

1. Nombre lógico y modelo comercial preciso.
2. Función dentro de la computadora.
3. Símbolo, terminales y numeración de pines.
4. Alimentación y corriente admitidas; limitaciones.
5. Tabla o ecuación de funcionamiento.
6. Esquema y circuito mínimo de uso.
7. Forma de comprobarlo.
8. Fallas típicas: pinout invertido, entradas flotantes, bus en conflicto.
9. Hoja de datos y estado de validación.

## Principio de escala

Una celda SRAM de seis transistores explica cómo funciona un bit. Una matriz de 32 KiB necesita modelado jerárquico. El libro puede documentar «expandir hasta transistor» pero no debe fingir que cablear más de un millón de MOSFET individuales sea una tarea doméstica trivial.

