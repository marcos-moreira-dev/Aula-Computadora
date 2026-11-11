# Catálogo mínimo de componentes

**Candidatos; no lista de compra.** Cada ficha deberá verificarse contra la hoja de datos de su fabricante y el encapsulado seleccionado.

| Tipo | Referencia candidata | Papel |
| --- | --- | --- |
| Transistor BJT | 2N3904, NPN | interruptor didáctico, lógica discreta |
| MOSFET | n/p complementarios por seleccionar | lógica CMOS y celda SRAM conceptual |
| NAND de cuatro puertas | SN74HCT00 | prácticas digitales y escalado |
| Flip-flops de cuatro bits | CD74HCT173 | construir registros paralelos |
| SRAM 8 bits | AS6C62256, 32K×8 | RAM comercial de máquina |
| EEPROM 8 bits | AT28C64B, 8K×8 | ROM de firmware |
| Pasivos/indicadores | resistencias, condensadores, LED, pulsadores | alimentación, reloj y diagnóstico |
| Periféricos | terminal y controlador de bloque fijo | E/S sin diseñar teclado/pantalla internamente |

Referencias: ../REFERENCIAS.md.

## Compatibilidad eléctrica

La propuesta se basa en baja tensión regulada de unos **5 V**, nunca en alimentar directamente desde 110/220 V. Compartir VCC no garantiza compatibilidad: verificar tensión de HIGH y LOW, corriente de salida, fan-out, temporización, pinout y protección.

La lógica **HCT** es una opción particularmente razonable en las interfaces con SRAM/EEPROM de niveles TTL-compatibles. No sustituir por HC sin analizar VIH/VOH y cargas.

## Fichas obligatorias antes de certificar un componente

- Nombres, modelo completo y fabricante.
- Encapsulado físico, dimensiones y pines.
- Símbolo y esquemático de ejemplo.
- Límites absolutos versus condiciones recomendadas.
- Entradas/salidas y verdad/temporización.
- Riesgos y casos límite.
- Tabla de pruebas y evidencia.
- Modelo geométrico 3D opcional: fiel a terminales y encapsulado, sin variabilidad dimensional innecesaria.

## Memoria y escala

- Aula-8 puede aprovechar una SRAM 32K×8 y una EEPROM 8K×8.
- Aula-16 requiere dos bancos de 8; los chips definitivos se seleccionarán para cubrir solo los bytes necesarios o justificar capacidad no usada.
- El circuito de selección par/impar requiere control adicional y steering bidireccional para bytes.
- Una 6T SRAM discreta es **demostración de principios**, no promesa de facilidad en protoboard.

## Reloj y energía

Empezar con pulso manual antirrebote y reloj lento medible; la frecuencia máxima física se determinará tras diagramas temporales y prototipos. Incluir desacoplamiento, estado de reset definido y medición de consumo en cada etapa.

