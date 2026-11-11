# Atlas historico de cinco piezas reales

**Aula Computadora · Complemento editorial C28-O · 9 de noviembre de 2026**

El libro desarrolla una computadora educativa por etapas. Estas fotografias
permiten comparar los modelos que aprendemos con dispositivos que si
existieron, sin presentar las imagenes como pruebas de nuestros circuitos.
Todas las fotografias se obtuvieron con la retroalimentacion C28-N de Windows,
se inspeccionaron visualmente y conservaron su fuente, autor y licencia.

## 1. MITS Altair 8800: hacer visible un byte

![Panel frontal Altair 8800](figuras_historicas_c28o/H01_altair_8800_panel.jpg)

La foto presenta luces de estado, indicadores de direccion y de datos,
interruptores numerados y controles como `EXAMINE`, `DEPOSIT` y `SINGLE STEP`.
Su panel permite entender que el usuario podia preparar una direccion,
depositar un byte y observar un estado mediante controles manuales.

**Conectamos con Aula:** el capitulo 14 usa `LDI R0,42` como los bytes
`11 00 2A`, propuestos para depositarlos en `0x6000`, `0x6001`, `0x6002`.
La fotografia inspira la interfaz pero no define nuestro arbitraje de bus,
temporizacion ni circuiteria de lectura.

**Comprueba:** convierte `0x2A` a ocho bits y explica por que pulsar DEPOSIT
no equivale a ejecutar el programa.

## 2. Apple II: el mapa de bloques se vuelve placa

![Placa madre Apple II](figuras_historicas_c28o/H02_apple_ii_placa.jpg)

La placa deja ver el integrado principal `6502`, zonas rotuladas ROM y RAM,
ranuras de expansion y pistas que comunican circuitos. Algunos chips
pertenecen a logica auxiliar; no se deduce su funcion completa solo de la
forma del encapsulado.

**Conectamos con Aula:** el capitulo 9 distingue direccion interna del chip
(`A0…A14`, por ejemplo) y seleccion de la ventana de memoria; el capitulo 12
integra memoria, CPU y buses. Una fotografia proporciona escala fisica,
pero para diseñar un cableado hace falta un esquema electrico y hojas de datos.

**Comprueba:** localiza en la foto el 6502 y dos filas de memorias. Explica
por que un chip de RAM y un registro de CPU no son intercambiables.

## 3. DEC VT100: texto visible no significa CPU en la pantalla

![Terminal DEC VT100](figuras_historicas_c28o/H03_dec_vt100_terminal.jpg)

El DEC VT100 dispone de teclado y pantalla y puede comunicarse con un
ordenador anfitrion. La foto muestra texto en columnas, no los bytes que
viajaron ni el circuito exacto que activó cada punto luminoso.

**Conectamos con Aula:** los capitulos 18 y 23B distinguen valor de byte,
codigo de caracter y representacion visible. La terminal historica no
valida el controlador de video educativo que hemos propuesto.

**Comprueba:** explica la diferencia entre almacenar el byte numerico
`0x41` y representar en pantalla la letra `A` bajo la codificacion ASCII.

## 4. Intel 8086: el aspecto del chip no revela su arquitectura

![Microprocesador Intel 8086](figuras_historicas_c28o/H04_intel_8086_chip.jpg)

El encapsulado tiene patillas metalicas e identificacion de modelo.
El Intel 8086 fue un microprocesador comercial con bus externo de datos de
16 bits. La cantidad de pines o la etiqueta no indican por si solas las
microoperaciones internas ni el control real de una memoria.

**Conectamos con Aula:** el capitulo 22 contrasta accesos por bytes y
palabras. Aula-16 sigue siendo un diseño educativo candidato; fotografiar
un 8086 no demuestra que hayamos implementado una CPU Aula-16.

**Comprueba:** si una palabra tiene 16 bits y un byte ocho, ¿por que el
ancho del bus y la organizacion de memoria son dos decisiones distintas?

## 5. IBM PC 5150: una computadora es un sistema de sistemas

![IBM PC 5150](figuras_historicas_c28o/H05_ibm_pc_5150.jpg)

Se aprecia una unidad central, monitor y teclado; la fotografia presenta
un ordenador completo de una generacion historica. Su modelo original
empleaba un procesador **Intel 8088**, con bus externo de datos de ocho
bits. No debe confundirse con el 8086 de la imagen anterior.

**Conectamos con Aula:** los capitulos 22–24 reúnen arquitectura,
perifericos, firmware y experiencias de usuario. Ese conjunto explica
por qué una CPU aislada no equivale a una computadora utilizable.

**Comprueba:** enumera tres componentes que hacen falta, ademas de una ALU,
para pasar de operaciones binarias a una computadora con teclado y pantalla.

## Licencias y publicacion

| Foto | Autor | Licencia |
| --- | --- | --- |
| Altair | Cromemco | CC BY-SA 4.0 |
| Apple II | Steve Jurvetson | CC BY 2.0 |
| DEC VT100 | Jason Scott | CC BY 2.0 |
| Intel 8086 | Thomas Nguyen | CC BY-SA 4.0 |
| IBM PC 5150 | Ruben de Rijcke | CC BY-SA 3.0 |

Las fichas de procedencia completas figuran en
`FOTOGRAFIAS_HISTORICAS_C28N_MANIFIESTO.json`; cada fotografia tiene una
pagina individual de Wikimedia Commons, un enlace a la licencia y SHA-256.
En este atlas se han escalado para maquetacion; si se recortan o editan de
otro modo, se documentaran esos cambios. Las licencias no convierten los
componentes historicos en disenos de propiedad de Aula.

**Estado editorial:** esta es una separata de revision. Cuando se aprueben
las ubicaciones, se podran integrar en los capitulos indicados. La edicion
maestra C28-G permanece intacta mientras se revisan los 26 capitulos.
