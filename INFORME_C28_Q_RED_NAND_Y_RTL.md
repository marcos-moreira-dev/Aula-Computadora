# C28-Q · De la figura lógica a la red de puertas verificable

**Fecha:** 9 de noviembre de 2026 (hora local de Ecuador).
**Producto:** libro Aula-Computadora, con maestro C28-G conservado.

## Resultado real recibido de Marcos

`Retroalimentacion_GLOBAL_C28H_20261109_194334.zip`:

- **19 controles APROBADOS**, cero fallidos y cero pendientes en Windows.
- La auditoría C28-P de 11 lecciones y 50 figuras fue aprobada.
- Las simulaciones existentes C28-F y C28-H volvieron a aprobar Icarus.
- Las cinco fotografías históricas fueron descargadas con su informe auxiliar.
- No hay evidencia nueva de CPU completa, hardware montado o firmware.

## Qué aporta esta etapa

El nuevo archivo `c28_q/netlists/fundamentos_nand.json` contiene dos redes
de lógica digital con **nombres de señales y conexiones explícitas**:

1. XOR de cuatro NAND: N1=NAND(A,B), N2=NAND(A,N1), N3=NAND(B,N1),
   D=NAND(N2,N3). Sus cuatro entradas binarias producen la tabla XOR.
2. Latch SR de dos NAND cruzadas: Q=NAND(S_n,Q_n),
   Q_n=NAND(R_n,Q). Se verifican SET, RESET, HOLD y el estado inválido
   mientras se aplica 00. **No** se simula ni promete la resolución tras
   liberar simultáneamente las dos entradas; depende de física real.

El script `scripts/c28q_verificar_redes_y_trazabilidad.py` comprueba
**desde los archivos JSON serializados**, no únicamente desde generadores
Python en memoria, estas redes y las listas anteriores:

| Fuente lógica | Puertas NAND | Contrastes nuevos | Alcance |
| --- | ---: | ---: | --- |
| XOR capítulo 4 | 4 | 4 vectores | Combinacional, cuatro entradas AB posibles |
| Latch capítulo 5 | 2 | 13 estados/transiciones ideales | Sin retardos ni metastabilidad |
| Selector PC C28-D | 51 | 8.336 combinaciones | Salto condicional y multiplexación de 16 bits |
| Incremento, saltos y MAR C28-F | 177 | 32.768 combinaciones | Incremento de PC16, selección y MAR funcional |

Se compararon también tres rutas de conexión visibles en los SVG del XOR
y latch, y ocho asignaciones del patillaje descritas en el capítulo 5.
Los diagramas fueron inspeccionados visualmente junto con las dos figuras
de la celda y los ocho carriles de registro C28-A. Las líneas del SVG no
son pistas eléctricas verificadas por EDA; los símbolos de MUX, DFF y 3E
son bloques funcionales.

Para contexto de montaje futuro, la hoja de datos de **Texas Instruments,
SN74HCT00 (SCLS062F, revisión de octubre de 2022)** indica cuatro NAND
de dos entradas, encapsulado N de 14 pines y alimentación recomendada
4,5–5,5 V. Referencia:
https://www.ti.com/lit/ds/symlink/sn74hct00.pdf
La comprobación de pines de este hito coteja la tabla del manuscrito con
el propio SVG; no sustituye revisar el dispositivo que se compre, las
entradas flotantes, corrientes, montaje o tiempos.

## Matriz de correspondencia

`libro/MATRIZ_CIRCUITOS_C28Q.md` enumera diez bloques didácticos y para
cada uno registra figura, fuente de comparación y límite de evidencia.
Los fundamentos XOR/SR y las redes C28-D/F disponen ahora de verificación
**desde topología digital declarada**. Sumador, ALU, control, bus Aula-16
y otras 2D siguen necesitando netlists y/o correspondencia exhaustiva.

## Cuatro controles HDL nuevos, todavía no confirmados por Windows

Los testbenches ya existentes ahora entran en el comprobador global como
controles independientes:

- `HDL_C28_A_REGISTRO8_COMPILACION`
- `HDL_C28_A_REGISTRO8_SIMULACION`
- `HDL_C28_E_PC16_COMPILACION`
- `HDL_C28_E_PC16_SIMULACION`

El primero verifica captura al flanco, LOAD, retención y alta impedancia
de un registro de ocho bits. El segundo evalúa el registro PC16, HOLD,
carga en flanco y un borrado **solo de prueba**, no el RESET físico de Aula.
Los testbenches son existentes y no se alteró su lógica, pero **todavía
falta recibir su ejecución efectiva en Icarus bajo Windows**. La nueva
auditoría C28-Q es el quinto control adicional. Objetivo: **24/24**.

## Progreso y límites pendientes

**84 % → 85 % estimado de madurez editorial del libro.** Incremento de
un punto: relación circuito/figura 60→65 % (+0,75) y pruebas digitales
72,5→75 % (+0,25). El desglose está en
`libro/PLAN_CIERRE_EDITORIAL_C28I.md`. No es un porcentaje de hardware.

Queda pendiente especialmente: topología formal de sumador/ALU/control,
selección de la política de PC, integración del suplemento C28-H y atlas
C28-O al Word/PDF, revisión visual integral de páginas y confirmación de
licencias antes de publicación. No se cambió la ISA, ABI, buses, mapa MMIO
ni contrato de vídeo V1, y no se creó ningún repositorio remoto.
