# Estado editorial del libro Aula-Computadora después de R0.14

**Fecha de corte: 5 de noviembre de 2026.** Documento de seguimiento,
no es el contenido del libro ni un certificado de edición terminada.
Este informe excluye deliberadamente el diseño de la **portada**,
que Marcos ha pedido evaluar por separado.

## 1. Veredicto honesto

El **currículo y contrato editorial están definidos**. Los **24 capítulos**
siguen **sin redactarse como manuscrito terminado**. El libro **no tiene aún**
un Word maestro ni PDF editorial completo. Hay documentación técnica
revisable, modelos matemáticos y verificadores en Python; no existe todavía
una CPU Aula ejecutable ni circuitos físicos medidos. No confundir
**12 verificadores de preproducción** con 24 capítulos revisados o con
una validación física.

Se puede **empezar a escribir ya**, especialmente los capítulos 1–11
de electricidad, lógica, memoria y aritmética, siempre que las fórmulas
y ejemplos se verifiquen y que la electrónica se apoye en hojas de datos.
No hace falta que todo el simulador esté construido para redactar.
Los capítulos 12–24 necesitarán además cerrar ciertos contratos técnicos
de Aula-8/Aula-16 antes de afirmar que las instrucciones funcionan.

## 2. Estado de las seis partes

| Parte | Capítulos | Manuscrito | Bloqueo principal |
| --- | ---: | --- | --- |
| I: electricidad y transistores | 1–3 | **No redactado** | ejemplos medidos/seguros, esquemas y datasheets |
| II: lógica y registros | 4–7 | **No redactado** | circuitos reproducibles, capturas exactas, tablas de verdad |
| III: buses, memoria y ALU | 8–11 | **No redactado** | esquemas y pruebas de sumadores, memoria y señales |
| IV: CPU Aula-8 | 12–16 | **No redactado** | ISA y microcontrol aún **propuestos**, sin CPU ejecutada |
| V: firmware y programación | 17–20 | **No redactado** | ROM real, cargador, editor y ensamblador nativos inexistentes |
| VI: CPU Aula-16 y cierre | 21–24 | **No redactado** | ISA/ABI y datapath Aula-16 por especificar, bus externo confirmado de 16 bits |

## 3. Trabajo necesario, aparte de la portada

1. **Escribir los 24 capítulos originales.** Cada uno necesita objetivo,
   prerrequisitos, explicación paso a paso, cálculo o circuito, ejemplo
   completo, fallos habituales, ejercicios y cierre. Evitar el formato
   «catálogo de componentes» y no mencionar JavaFX dentro del libro.
2. **Diseñar figuras técnicas originales.** Transistor con polaridad,
   compuertas, latch, registro, sumador, ALU, buses, datapath, pila,
   ciclos de instrucciones, mapa de memoria, ROM, MMIO, bloques y
   bancos pares/impares de Aula-16. Cada flecha, pin y conexión debe
   representar el mecanismo exacto que explica el texto. Se requiere
   una secuencia visual, no ilustraciones decorativas aisladas.
3. **Obtener evidencia técnica reproducible.** Hojas de datos verificadas,
   dimensiones eléctricas, niveles lógicos y temporización; tablas de verdad
   y pruebas digitales. Separar «calculado», «simulado» y «medido
   físicamente». No hacen falta millones de transistores discretos:
   la CPU final puede estudiar memorias comerciales.
4. **Completar el contrato R1 para capítulos de máquina.** Confirmar ISA
   Aula-8, microcontrol, vectores de reset, ABI, ROM de firmware, monitor,
   entrada desde panel y control de permisos del cargador. Describir la
   carga de dos pasadas R0.14 con sus límites; desarrollar y probar
   de verdad al menos los ejemplos de programa que se publiquen como
   «ejecutables». Para Aula-16, definir ISA y datapath específicos
   sin reducir el bus externo de datos de **16 bits**.
5. **Desarrollar los ejemplos de programación.** Depósito manual,
   ROM PUTC/GETC/PUTS, CALL/RET, editor de líneas y ensamblador
   **nativos** en Aula-8, binarios cargables, persistencia y MiniC
   cruzado. Si una utilidad no está implementada, marcar el fragmento
   como diseño ilustrativo y no venderlo como práctica comprobada.
6. **Crear ejercicios, solucionario y anexos.** Problemas de cada
   bloque de prerrequisitos, guía de diagnóstico, glosario, tabla
   de símbolos electrónicos, ISA, referencias, comandos y
   definiciones de unidades/bytes.
7. **Revisar originalidad, derechos y fuentes.** El manuscrito anterior
   y las obras históricas son referentes, nunca material para copiar.
   Revisar derechos de coautoría, fotos, gráficos, citas y datasheets.
   Corregir afirmaciones inestables o dependientes de componentes
   concretos con evidencia primaria.
8. **Maquetar y certificar dos formatos.** Word DOCX editable con estilos,
   ecuaciones genuinas o editables, PNG de figuras con texto alternativo,
   índice/capitulado/referencias. Después exportar PDF con texto
   seleccionable y verificar ambas versiones página por página:
   desbordes, márgenes, ecuaciones, tablas, pies y legibilidad.
   La compatibilidad con DocuPodcast se indica como **no verificada**
   hasta poder probarla de verdad.

## 4. Qué ya tenemos listo

- [Currículo de 24 capítulos](CURRICULO.md) y seis partes.
- [Contrato editorial](CONTRATO_EDITORIAL.md), plantilla, bibliografía,
  reglas de originalidad y validación.
- Arquitecturas conceptuales Aula-8 y Aula-16, mapa de memoria y
  pila; **bus externo Aula-16 de 16 bits confirmado**.
- ISA, registros, saltos, ABI MiniC, ROM/monitor, bloques y AEX1 como
  propuestas con pruebas documentales y de anfitrión.
- Propuesta de **LOADX con dos pasadas R0.14** y límite claro de carga
  no atómica.

## 5. Orden recomendado desde este punto

1. **Comenzar Capítulo 1 ya**, con ejemplos eléctricos sencillos,
   esquemas originales y ejercicios corregibles. Preparar primero
   una muestra Word+PDF de 8–12 páginas como control editorial
   (extensión orientativa, no cuota obligatoria).
2. Continuar en orden de prerrequisitos por los capítulos 2–11,
   mientras R1 se cierra sin condicionar el inicio de la obra.
3. Antes de los capítulos 12–20, poner a prueba la ISA/CPU/ROM
   de forma independiente y seleccionar ejemplos realmente
   ejecutables; registrar apartados todavía hipotéticos.
4. Definir y verificar Aula-16 con su propia ISA antes de redactar
   capítulos 21–23; reservar integración, errores y proyectos para 24.
5. Integrar el Word maestro y el PDF final únicamente después de
   corregir texto, figuras, referencias y pruebas por capítulo.

**Punto de control:** no hacen falta más versiones R0 de cabeceras o
metadatos para **empezar el libro**. El mayor trabajo pendiente no es
la portada ni otro ZIP de planificación: es **escribir, ilustrar,
probar y maquetar los capítulos**.
