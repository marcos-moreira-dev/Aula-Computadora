# Modelo común de circuitos y simulación

## La fuente de verdad

La vista esquemática 2D, la representación 3D, la ejecución lógica y la verificación estructural leen **el mismo netlist jerárquico**. No se mantiene un dibujo independiente con conexiones distintas de las simuladas.

## Entidades conceptuales

| Concepto | Responsabilidad |
| --- | --- |
| ComponentDefinition | tipo, modelo, referencia comercial, pines, límites y símbolo |
| ComponentInstance | una pieza concreta con ID estable y posición opcional |
| Pin | nombre, dirección eléctrica, polaridad y capacidad |
| Net | conjunto real de terminales conectados eléctricamente |
| Circuit | subcircuito y su interfaz de entradas/salidas |
| Module | unidad semántica reutilizable (NAND, registro, RAM) |
| Board | espacio de trabajo y regiones habilitadas de montaje |
| Lesson | objetivo, kit, conexiones permitidas, pistas, pruebas |
| CpuState | PC, SP, X, R0–R3, IR, flags, microestado |
| MemoryMap | mapeo RAM, ROM y E/S con ancho/política de acceso |
| SignalValue | 0, 1, Z (sin conducción), X (desconocido/conflicto) |

Cada red/instancia tiene un ID y una ruta jerárquica. Los módulos pueden contraerse o expandirse sin perder la correspondencia entre señal digital y representación visual.

## Motor digital

1. Calcular cambios de las entradas.
2. Propagar eventos o evaluar módulos de forma determinista.
3. Resolver drivers y detectar bus en conflicto.
4. Actualizar biestables/registros con reglas de reloj.
5. Emitir instantánea para 2D, 3D, registros y paneles de diagnóstico.

Debe declararse la simplificación temporal (lógica síncrona y latencias elegidas) y distinguirla de un análisis analógico. La frecuencia real y la estabilidad física exigen otras pruebas.

## Verificador de ensamblaje

- Verificar cantidad y tipo de piezas.
- Comprobar pines conectados a redes esperadas o equivalentes, teniendo en cuenta terminales simétricos cuando la función lo permite.
- Detectar salidas conectadas entre sí, entradas flotantes y ausencia de alimentación.
- Ejecutar tablas de verdad, conservación de estado y vectores de prueba.
- Mostrar error educativo: qué síntoma se detectó y cómo investigarlo, sin revelar toda la solución inmediatamente.
- Las alertas eléctricas son limitadas; no se promete detectar todas las maneras de dañar un montaje.

## Capas visuales

- Nivel arquitectura: CPU, RAM, ROM, E/S, buses.
- Nivel módulo: ALU, registros, decodificadores, control.
- Nivel puerta/latch: cables y señales individuales.
- Nivel componente: transistores, pines, resistencias y LED.
- Nivel físico: encapsulado 3D y placa o protoboard cuando aporte comprensión.

El 3D usa geometrías reutilizables, materiales simples y color/luminosidad para estados 0/1. Debe incluir etiquetas y patrones para no depender solo del color. LOD e instanciación bajo demanda evitan saturar escena.

