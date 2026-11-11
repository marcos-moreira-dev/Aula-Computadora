# Arquitectura de software prevista

**Nota 11-nov-2026:** la estructura R0 descrita abajo fue inicialmente
prospectiva. Ahora existe un `pom.xml` real y el corte acotado
`circuitos/Nand2Lesson.java` + `interfaz/` + `src/test/`, exclusivamente
para la etapa NAND2. El resto de paquetes continúa siendo una meta futura.

## Stack

- Java **21**.
- JavaFX (UI 2D/3D, escenas, mallas, materiales).
- Maven.
- JUnit y pruebas ejecutables en CI.
- Aplicación local inicialmente sin servidor, base de datos ni conexión permanente a Internet.

## Estructura inicial recomendada

**Un solo proyecto Maven modular por paquetes**, antes de dividir en numerosos artefactos independientes.

~~~text
simulador-javafx/
  pom.xml                 # creado para el primer taller
  src/main/java/.../
    dominio/
    circuitos/
    logica/
    memoria/
    cpu/
    ensamblador/
    minic/
    firmware/
    lecciones/
    interfaz/
  src/main/resources/
    componentes/
    circuitos/
    programas/
  src/test/java/.../
~~~

El listado completo sigue siendo la arquitectura futura: **no se han
creado los paquetes de CPU, firmware, ensamblador o MiniC**, y el POM
actual solo incorpora las dependencias del primer taller JavaFX.

## Capas

1. **Dominio:** Component, Pin, Net, Circuit, CpuSpec, Instruction, MemoryRegion.
2. **Motor lógico:** electrónica digital, reloj, memoria, buses, microsecuenciador y tests.
3. **Herramientas de desarrollo:** ensamblador Aula-8, Aula-16 y compilador MiniC-Aula.
4. **Lecciones:** kits, pasos, ayudas, validación de construcción.
5. **Presentación:** vistas 2D/3D, biblioteca limitada, visualización de señales, consola.

La UI **no decide el resultado lógico**. El motor debe poder ejecutar tests de CPU y programas binarios en modo sin pantalla.

### Origen y ejecución de herramientas: distinguir anfitrión de Aula

- El ensamblador y compilador **cruzados** son código Java y pueden ejecutar en el anfitrión.
- El **editor de líneas y ensamblador nativos** se suministran como binarios de Aula-8 y deben correr instrucción a instrucción sobre el modelo de CPU Aula.
- El terminal visible es solo entrada/salida. No debe interceptar `ASM` y resolverlo en Java sin indicarlo claramente como función **externa**.
- Para pruebas, comparar la salida nativa con la del ensamblador Java cruzado, sin sustituir la primera por la segunda.
- El panel manual debe comprobar que se detuvo la CPU y que existe un único controlador del bus antes de realizar depósitos en RAM.

Este contrato de autenticidad tiene detalle y casos de prueba en [PROGRAMACION_DESDE_CERO.md](PROGRAMACION_DESDE_CERO.md).

## Arquitectura de referencia y diseño real

Mantener dos caminos de pruebas:

- intérprete independiente de la ISA, que ejecuta por semántica;
- CPU digital derivada de la microarquitectura, que ejecuta por microestados y netlist.

Sus estados deben coincidir al final de cada instrucción. Las salidas del motor se observan en la UI sin modificar la semántica.

## Desarrollo y distribución

- Maven debe compilar, probar y empaquetar desde instrucciones de README.
- Evitar pruebas de UI cuando basta una prueba de dominio.
- Cuando exista un ejecutable, incluir script/PowerShell para pruebas y ZIP de retroalimentación en Windows.
- Documentar compatibilidad con la laptop del usuario, rendimiento de la vista 3D y carga de memorias.

