# Capítulo 6. Memorizar en el tiempo

*Parte II · Memoria digital elemental · Aula-Computadora*

En el capítulo 5 construimos una memoria capaz de conservar un bit. Las órdenes SET y RESET nos permitían decidir si Q debía valer 1 o 0. Pero el latch SR elemental tenía un inconveniente práctico: necesitábamos organizar **dos señales de control** y evitar una combinación prohibida. Al conectar muchas memorias dentro de una computadora, queremos una regla más simple: presentar el dato por un lado y decidir **cuándo** se permite guardarlo por otro.

El lector de este capítulo terminará pudiendo distinguir un latch D de un flip-flop D, leer una secuencia de reloj sin confundir nivel con flanco y explicar por qué el reset y los tiempos de preparación de datos importan. Seguiremos hablando de **estados lógicos ideales**; no hemos construido ni medido estos circuitos.

## 1. Una entrada para el dato y otra para el permiso

Imagina un cartel electrónico que puede mostrar 0 o 1. Un cable trae la propuesta de valor y otro indica si aceptamos cambios. La primera señal se llama **D**, de *data*. La segunda se llama **LE**, de *latch enable*, o habilitación del latch.

Definiremos el permiso como **activo en alto**: LE = 1 significa «seguir D» y LE = 0 significa «conservar lo que ya estaba guardado». Observa que no estoy diciendo que 1 sea siempre «activar» en electrónica: recuerda el capítulo 5, donde SET y RESET se activaban con 0. La polaridad forma parte de la **semántica lógica** de cada señal.

Con LE = 1, si D vale 0, Q termina valiendo 0; si D vale 1, Q termina valiendo 1. Con LE = 0, un cambio en D no debe modificar el estado estable de Q. A este comportamiento lo llamamos **latch D sensible a nivel**.

[[EQ:Q_siguiente = D   si   LE = 1]]

[[EQ:Q_siguiente = Q_anterior   si   LE = 0]]

No interpretes «siguiente» como «en el próximo pulso»: aquí significa **después de asentarse las señales**, según el modo que esté activo. El latch D no necesita que ocurra un flanco de reloj para dejar pasar datos.

## 2. Del latch SR al latch D

Podemos explicar su funcionamiento a partir del latch NAND que ya conocemos. Recordemos que el latch SR del capítulo anterior tiene controles `S_n` y `R_n` **activos en bajo**. Si usamos una NAND para cada control y añadimos una inversión de D, obtenemos:

[[EQ:S_n = NAND(D, LE)]]

[[EQ:R_n = NAND(NOT D, LE)]]

Cuando LE = 0, ambas NAND producen 1. El latch SR recibe entonces `S_n R_n = 11` y **mantiene** su valor anterior. Cuando LE = 1 y D = 1, resulta `S_n R_n = 01`: orden SET. Cuando LE = 1 y D = 0, resulta `S_n R_n = 10`: orden RESET. Con valores binarios ideales y esta red correcta, **no se pide simultáneamente SET y RESET**, porque D y NOT D son complementarios.

La figura 1 muestra las conexiones por bloques funcionales. La NAND superior crea `S_n`; la inferior recibe el dato invertido para crear `R_n`. Ambas señales gobiernan el latch SR NAND del capítulo 5. El diagrama es una **descomposición lógica didáctica**; los retardos reales y cambios simultáneos requieren análisis temporal al construir hardware.

[[FIG:c06_fig01_desde_sr_hasta_d|Figura 1. Un dato D y una habilitación LE producen los dos controles del latch SR NAND.|La entrada D va a una NAND de SET y, a través de un inversor, a una NAND de RESET; LE llega a ambas y sus salidas S_n y R_n alimentan el latch SR.]]

Este paso es importante para la construcción de nuestra computadora: aprendemos a **encapsular conexiones**. El usuario de un bloque D necesita conocer su contrato de entradas y salidas, aunque el bloque pueda estar hecho internamente con varias compuertas.

## 3. La palabra transparente tiene un sentido técnico

Cuando LE = 1 decimos que el latch está **transparente**. No significa que desaparezca la memoria, ni que Q cambie instantáneamente sin retardo. Significa que, tras el tiempo de propagación, Q sigue los cambios de D mientras la habilitación permanezca activa.

Cuando LE pasa a 0, el latch deja de seguir D y conserva el **último valor válido que alcanzó** en el intervalo habilitado, respetando las condiciones temporales del circuito real. La tabla resume el modelo lógico:

| LE | D | Q después de asentarse | Conducta |
|---|---|---|---|
| 0 | 0 o 1 | Q anterior | Conserva |
| 1 | 0 | 0 | Transparente; pasa un 0 |
| 1 | 1 | 1 | Transparente; pasa un 1 |

La figura 2 destaca que el primer renglón no se puede resolver únicamente con D: necesitamos saber qué había guardado el latch antes de deshabilitarlo.

[[FIG:c06_fig02_tabla_latch_d|Figura 2. El latch D deja pasar los datos con LE = 1 y los conserva con LE = 0.|Tabla de tres situaciones que distingue retención, paso de cero y paso de uno para un latch D activo en alto.]]

Vamos a seguir cinco observaciones estables. Partimos de Q = 0 conocido porque antes se habilitó el latch con D = 0, y **no** porque hayamos supuesto un valor al encender:

| Momento | LE D | Q estable | Explicación |
|---|---|---|---|
| t0 | 0 0 | 0 | Estado inicial conocido |
| t1 | 0 1 | 0 | D cambia, pero LE = 0 conserva |
| t2 | 1 1 | 1 | LE = 1 deja pasar el 1 |
| t3 | 1 0 | 0 | Sigue transparente: pasa el 0 |
| t4 | 0 1 | 0 | LE = 0: D vuelve a 1, Q no cambia |

En t1 y t4 D vale 1, pero Q permanece en 0: el permiso está cerrado. En t2, en cambio, Q llega a 1 porque LE permanece abierto. Si una señal D tuviera pequeñas oscilaciones durante LE = 1, también podrían reflejarse en Q; por eso el latch transparente **no es todavía la solución universal** para coordinar una CPU.

## 4. ¿Por qué hace falta un reloj?

Imagina cuatro registros que deben actualizarse como parte de un mismo paso de cálculo. Si el resultado de una etapa vuelve a entrar en otra que sigue transparente, los cambios podrían propagarse por varias etapas durante el mismo intervalo de habilitación. El problema ya no consiste solamente en guardar un 1: hay que decidir **en qué momento se acepta el siguiente dato**.

Una señal periódica llamada **reloj**, o CLK, aporta instantes de referencia. En nuestro modelo sencillo alterna entre nivel bajo y alto. Llamamos **flanco ascendente** a su transición de 0 a 1, y **flanco descendente** a la transición de 1 a 0. Ninguno de esos flancos dura mágicamente «cero tiempo» en un circuito real; las curvas de tensión atraviesan regiones de transición. En las tablas lógicas dibujaremos eventos ideales para aprender el mecanismo.

El período T mide cuánto tarda un ciclo completo. Si un reloj ideal tiene un período de 1 milisegundo, completa mil ciclos por segundo:

[[EQ:f = 1 / T]]

[[EQ:T = 1 ms = 0,001 s   entonces   f = 1000 Hz]]

Es un **ejemplo aritmético**, no la frecuencia recomendada o medida de ningún circuito del libro. Más adelante veremos que la frecuencia real admisible depende de retardos, caminos de datos, alimentación y márgenes temporales.

## 5. Un flip-flop D de flanco ascendente

Un **flip-flop D** activado por flanco ascendente conserva Q durante casi todo el ciclo; toma el D válido presente alrededor de una transición **0 → 1 de CLK**. Una vez ocurrido ese evento y transcurrido su retardo de salida, Q mantiene el valor capturado hasta otro flanco pertinente o una orden asíncrona, como el reset.

[[EQ:Q_siguiente = D_muestreado   en   flanco_ascendente(CLK)]]

[[EQ:Q_siguiente = Q_anterior   sin   flanco   ni   reset]]

La diferencia con el latch D es visible cuando CLK o LE permanece alto. El latch transparente sigue los cambios de D mientras LE = 1; un flip-flop de flanco ascendente **no vuelve a copiar D por el mero hecho de que CLK permanezca en 1**. Necesita otro flanco ascendente válido.

Existen flip-flops de flanco descendente y dispositivos con otras funciones. En este capítulo elegimos el **flanco ascendente** como convención para que las secuencias sean inequívocas. La figura 3 presenta un ejemplo con dos instantes de captura, sin atribuir duraciones físicas a las líneas dibujadas.

[[FIG:c06_fig03_flancos_y_capturas|Figura 3. El flip-flop D copia el dato en los flancos ascendentes y lo conserva entre ellos.|Ondas digitales idealizadas de CLK, D y Q: en el primer flanco ascendente se captura D igual a 1 y en el segundo se captura D igual a 0; entre los flancos Q se mantiene.]]

## 6. Leamos siete momentos de un flip-flop

Partimos otra vez de un valor Q = 0 **previamente establecido**. No suponemos que un chip apagado recuerde un bit o arranque necesariamente en 0. Seguimos esta secuencia de instantes; siempre consideramos Q **después del retardo de propagación** cuando ha ocurrido un flanco.

| Instante | CLK D | Q estable | Evento |
|---|---|---|---|
| t0 | 0 0 | 0 | Estado conocido |
| t1 | 0 1 | 0 | D cambia; sin flanco |
| t2 | 1 1 | 1 | Flanco ascendente |
| t3 | 1 0 | 1 | D cambia con CLK alto |
| t4 | 0 0 | 1 | Flanco descendente |
| t5 | 1 0 | 0 | Segundo flanco ascendente |
| t6 | 1 1 | 0 | D cambia sin nuevo flanco |

Aquí hay dos comprobaciones decisivas. En **t3**, D ya bajó a 0, pero Q continúa en 1: CLK sigue alto, aunque no ha ocurrido otro flanco ascendente. En **t6**, D vuelve a 1 y Q sigue en 0 por la misma razón. Un latch D transparente con LE alto **sí** habría seguido D en esas situaciones.

La figura 4 reúne ambos contratos: a la izquierda, una ventana de transparencia del latch; a la derecha, dos capturas puntuales del flip-flop. La imagen enseña cuándo se acepta un nuevo valor, sin intentar representar una curva eléctrica real.

[[FIG:c06_fig04_latch_versus_flipflop|Figura 4. Latch D por nivel y flip-flop D por flanco tienen reglas distintas para actualizar Q.|Comparación conceptual de un latch D habilitado durante un intervalo y un flip-flop D que solo muestrea datos en flancos ascendentes.]]

## 7. Reset y preset: controlar el estado inicial

Un procesador debe arrancar desde una situación definida. No basta mirar un diagrama de flip-flop y escribir «Q comienza en 0». Antes del primer dato conocido, el estado puede ser desconocido. Una señal de **reset**, también llamada **clear**, sirve para llevar una memoria al estado requerido.

El **SN74HC74** de Texas Instruments incorpora dos flip-flops D de flanco ascendente. Cada uno dispone de entradas asíncronas de **preset** y **clear**, activas en bajo. Para estudiar el mecanismo llamaremos `PRE_n` y `CLR_n` a esas señales. Si `CLR_n = 0` y `PRE_n = 1`, se solicita Q = 0 **sin esperar flanco de reloj**; si `PRE_n = 0` y `CLR_n = 1`, se solicita Q = 1. En operación normal, ambas se mantienen en 1 para dejar que los flancos de CLK gobiernen el almacenamiento.

| PRE_n | CLR_n | CLK | Resultado lógico |
|---|---|---|---|
| 1 | 0 | Cualquiera | Clear asíncrono: Q = 0 |
| 0 | 1 | Cualquiera | Preset asíncrono: Q = 1 |
| 1 | 1 | Flanco 0 → 1 | Q copia D válido |
| 1 | 1 | Sin flanco 0 → 1 | Q conserva el estado |
| 0 | 0 | Cualquiera | Combinación simultánea no admitida para uso normal |

La última fila **no** se debe usar como método de inicialización. Tampoco estamos afirmando aquí que todos los dispositivos comerciales compartan el mismo comportamiento: esta explicación se basa en el **SN74HC74** y su hoja de datos. Reset y preset asíncronos son útiles, pero deben retirarse cumpliendo los requisitos temporales especificados por el fabricante.

## 8. Preparar D antes del flanco y mantenerlo después

Es tentador imaginar el flanco como una fotografía exacta tomada en un solo instante. El dispositivo físico necesita una pequeña ventana de estabilidad a su alrededor. El dato debe estar establecido **antes** del flanco durante un tiempo mínimo llamado **setup**, y debe mantenerse **después** durante un tiempo mínimo llamado **hold**.

Llamaremos `t_setup` y `t_hold` a esos intervalos. Su valor numérico depende del chip y de las condiciones de su hoja de datos. No dibujamos ni calculamos nanosegundos inventados.

[[EQ:Datos estables desde t_flanco - t_setup hasta t_flanco + t_hold]]

También existe el retardo **clock-to-Q**: incluso después de un flanco válido, Q no cambia instantáneamente. Si una nueva entrada llega demasiado tarde, el sistema podría capturar el valor anterior; si viola las condiciones temporales, **no se garantiza un resultado lógico correcto** y puede aparecer un estado transitorio difícil de resolver, llamado *metastabilidad*.

La palabra *metastabilidad* no significa que un bit almacenado sea siempre aleatorio ni que todo flanco produzca problemas. Significa que los biestables físicos tienen límites; una tabla ideal no basta para demostrar que una señal arbitraria, especialmente si procede de un pulsador o de otro dominio de reloj, será segura para muestrear. En sistemas reales se diseñan sincronizadores apropiados, pero aquí no dimensionaremos uno.

## 9. Dos ejemplos de integrados reales

Para el **latch sensible a nivel**, Texas Instruments ofrece la familia **SN74HC373**, que contiene ocho latches D transparentes. Cuando la habilitación `LE` está alta, sus salidas siguen a D; cuando LE baja, conservan el estado. El integrado tiene además una señal distinta `OE_n` para activar o desconectar **las salidas** mediante alta impedancia: esto **no borra el dato almacenado**. Esa separación nos será útil al hablar de buses en los capítulos 7 y 8.

Para el **flip-flop sensible a flanco**, la familia **SN74HC74** contiene dos biestables D de flanco ascendente, con entradas independientes de preset y clear asíncronos. La documentación del fabricante indica límites de alimentación y temporización que deberán consultarse para un encapsulado y condiciones concretas antes de cualquier práctica.

En ambos casos, conocer el principio lógico no equivale a verificar el montaje: faltan esquemas eléctricos completos, niveles de alimentación, desacoplo, conexiones no utilizadas, márgenes de corriente y medidas reales. No hemos conectado una protoboard ni registrado señales con un osciloscopio. **No construiremos una CPU basándonos únicamente en dibujos conceptuales.**

## 10. Cómo prepara este capítulo los registros

Ya contamos con una memoria elemental que acepta un dato D y una regla temporal de actualización. En el capítulo 7 colocaremos **varios elementos de memoria uno al lado del otro**, con entradas de varios bits y señales de carga comunes. Aprenderemos a leer y almacenar un byte completo, y a distinguir lo que sucede dentro de un registro de lo que viaja por un bus.

Esta transición también ayuda a separar niveles de significado. En el hardware, un flanco «autoriza una captura» porque **así se definió el contrato lógico** del circuito. Si el bit guardado significa una cifra, una letra o una bandera de programa, esa interpretación llegará mediante otras reglas. El futuro capítulo puente «Del bit al significado», propuesto tras el capítulo 7, desarrollará esa distinción antes de estudiar buses y direcciones.

## Construimos Aula-8: de conservar a decidir cuándo cargar

Nuestro objetivo inmediato ya no es recordar una orden arbitraria de SET o RESET, sino capturar **el valor que llegue por la entrada D** cuando corresponda. Imagina que R0 de Aula-8 recibe un byte desde un bus interno. Antes del flanco activo, sus ocho entradas deben estar estables; en el flanco, los elementos elegidos capturan el dato; después, Q conserva ese resultado hasta una nueva carga o reinicio conforme al diseño.

La señal `LOAD` no cambia por sí sola el significado de flanco: se necesitará un registro con habilitación o lógica de selección que elija entre el dato nuevo y el previamente conservado. Tampoco podemos asumir que todos los circuitos D poseen el mismo RESET o los mismos tiempos. La figura acumulativa del capítulo 7 representará ese **contrato lógico**; las patillas y tiempos físicos dependerán del dispositivo que finalmente se seleccione.

## 11. Ejercicios para comprobar la memoria temporal

**Ejercicio 1 — Señales.** Explica para qué sirven D, LE y Q en un latch D transparente activo en alto.

**Ejercicio 2 — Construcción.** Con `S_n = NAND(D,LE)` y `R_n = NAND(NOT D,LE)`, calcula los controles del latch SR para LE = 0 y D = 1.

**Ejercicio 3 — SET.** Calcula `S_n R_n` y el Q estable cuando LE = 1 y D = 1.

**Ejercicio 4 — RESET.** Calcula `S_n R_n` y el Q estable cuando LE = 1 y D = 0.

**Ejercicio 5 — Retención.** Con Q inicial conocido 1, ¿qué sucede si LE = 0 y D cambia de 1 a 0 y después vuelve a 1?

**Ejercicio 6 — Transparencia.** Un latch D tiene LE = 1. D cambia 0 → 1 → 0. ¿Qué secuencia de valores estables sigue Q?

**Ejercicio 7 — Período.** Calcula la frecuencia de un reloj ideal cuyo período es 2 milisegundos. Muestra la conversión a segundos.

**Ejercicio 8 — Flanco.** Un flip-flop de flanco ascendente guarda Q = 0. D vale 1, y CLK cambia de 0 a 1: ¿qué Q resulta después del retardo?

**Ejercicio 9 — Reloj alto.** Después del ejercicio 8, CLK permanece en 1 y D baja a 0. ¿Cambia Q? Compáralo con un latch transparente con LE = 1.

**Ejercicio 10 — Secuencia.** Para el flip-flop de la tabla t0–t6, escribe la sucesión completa de Q estable.

**Ejercicio 11 — Reset.** En el SN74HC74, con `CLR_n = 0`, `PRE_n = 1`, D = 1 y ningún flanco, ¿qué estado se solicita y por qué?

**Ejercicio 12 — Tiempos.** Explica qué deben cumplir setup y hold, y por qué una tabla de verdad no basta para probar que un circuito real siempre captura correctamente.

## Solucionario del capítulo 6

Las respuestas describen **comportamientos lógicos ideales o requisitos documentados**. No certifican un dispositivo físico.

**1.** D presenta el valor candidato; LE = 1 permite que Q siga D después del retardo; LE = 0 ordena conservar el último valor válido.

**2.** Como LE = 0, `S_n = NAND(1,0) = 1` y `R_n = NAND(0,0) = 1`. Los controles 11 conservan el estado anterior.

**3.** `S_n = NAND(1,1) = 0`; `R_n = NAND(0,1) = 1`. El par 01 solicita SET y Q queda en 1.

**4.** `S_n = NAND(0,1) = 1`; `R_n = NAND(1,1) = 0`. El par 10 solicita RESET y Q queda en 0.

**5.** Q permanece en 1 porque el latch está deshabilitado; D no puede cambiar el estado mientras LE = 0.

**6.** Tras asentarse cada cambio, Q sigue **0 → 1 → 0** mientras LE permanezca en 1. No se requiere flanco.

**7.** `T = 2 ms = 0,002 s`; `f = 1 / 0,002 = 500 Hz`. No es una velocidad medida del SN74HC74.

**8.** El flanco ascendente captura el D válido igual a 1; Q resulta 1 después de su retardo de propagación.

**9.** El flip-flop conserva Q = 1 porque CLK sigue alto y no hubo otro flanco ascendente. Un latch D con LE = 1 dejaría pasar el nuevo D = 0.

**10.** Q en t0–t6: **0, 0, 1, 1, 1, 0, 0**. Solo t2 y t5 tienen flanco ascendente.

**11.** `CLR_n = 0` solicita Q = 0 de modo asíncrono: no necesita esperar un flanco. Debe mantenerse `PRE_n = 1` para evitar la combinación simultánea no admitida.

**12.** D debe estar estable cierto tiempo antes (setup) y después (hold) del flanco; además se espera el retardo de CLK a Q. Si se violan estos límites, la lógica ideal no garantiza qué valor se capturará ni el tiempo de resolución.

