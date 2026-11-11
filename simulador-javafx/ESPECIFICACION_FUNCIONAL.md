# Especificación funcional del taller guiado

## Motivación del usuario

«Aquí tienes una placa y un kit limitado; completa una celda RAM o una puerta lógica». El estudiante debe sentir que ensambla una máquina concreta, con grados razonables de libertad y ayuda progresiva. Una pantalla llena de millones de transistores sin estructura no cumple el objetivo.

## Modo A: computadora construida

- Elegir Aula-8 o Aula-16.
- Navegar de arquitectura a registros, compuertas, transistores y pinouts.
- Ver buses y señales activos; valores 0, 1, alta impedancia y desconocidos según el motor digital.
- Ejecutar programas paso a paso, por instrucción o microoperación.
- Examinar memoria, registro, flags, terminal y ROM.
- Seleccionar componente para abrir ficha corta: función, pines, modelo, tabla de verdad, prueba y fallos comunes.
- Cambiar entre esquema 2D y representación 3D sin cambiar la identidad del circuito.

## Modo B: hazlo tú mismo

La secuencia será prescrita, por ejemplo:

1. Encender LED con transistor y resistencia.
2. Construir inversor.
3. Completar NAND.
4. Montar latch y comprobar que conserva un bit.
5. Completar un registro/byte.
6. Construir sumador y ALU.
7. Unir buses, reloj, CPU y memoria.
8. Arrancar ROM, terminal y ejecutar programa.
9. En una lección independiente, detener CPU y depositar bytes a RAM desde panel conceptual; observar dirección, datos y propiedad del bus.
10. Entrar al monitor ROM, cargar utilidades a RAM, editar líneas y ejecutar ensamblador **nativo** comprobando su ejecución sobre la CPU Aula.

Cada paso incluirá:

- objetivo expresado como comportamiento;
- piezas autorizadas y cantidad limitada;
- esquema objetivo cuando proceda;
- conexiones y terminales manipulables;
- indicadores visuales de estado;
- comprobación estructural y lógica;
- ayuda graduada: pista conceptual -> zona aproximada -> terminal concreto;
- sello **verificado lógicamente** solo después de aprobar pruebas.

Se podrán agrupar módulos ya completados para no repetir miles de conexiones idénticas. En Aula-8 todo el diseño podrá estar definido estructuralmente a nivel lógico/transistor, pero su representación no instanciará millones de mallas en pantalla. Aula-16 ofrecerá vistas jerárquicas y expansión detallada bajo demanda.

## Biblioteca mínima de piezas

Transistor NPN y MOSFET apropiados, resistencia, condensador, diodo donde corresponda, LED, pulsador, cable, alimentación, reloj, tierra, compuerta/IC seleccionados, SRAM, ROM, terminal fijo y controlador de bloques. Sin catálogos de miles de fabricantes ni tolerancias estadísticas irrelevantes para la enseñanza.

## No objetivos V1

- Diseño totalmente libre de arquitecturas heterogéneas.
- Análisis analógico SPICE, simulación térmica real, certificación contra daño.
- Ray tracing avanzado, modelado 3D fotogramétrico, PCB profesional, motores gráficos externos obligatorios.
- Video VGA, decenas de teclados/pantallas o bibliotecas de dispositivos arbitrarios.
- **Sí queda dentro del contrato lógico (no hardware implementado):** una pantalla educativa fija de texto/bitmap de cuatro colores con VRAM y ROM de caracteres, sin VGA; [contrato detallado](CONTRATO_VIDEO_AULA_V1.md). Esto no introduce una tarjeta GPU ni convierte el taller en diseñador universal.
- Una representación simultánea de cada transistor de 32 KiB de RAM como nodo visual.

## Extensibilidad futura

El formato de componentes y lecciones admitirá variantes y microcomputadoras famosas después de dominar Aula-8 y Aula-16. Esto es capacidad de diseño, no promesa de contenido para R1.

