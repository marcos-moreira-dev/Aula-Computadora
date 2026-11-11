# Aula-8 — direccionamiento por X y SP (R0.8)

**Estado: PROPUESTA NO APROBADA.** Se deriva de la [ISA Aula-8 candidata](ISA_AULA8_CANDIDATA.md), el [datapath R0.4](MICROARQUITECTURA_AULA8_BORRADOR.md) y las [microacciones R0.5](UNIDAD_CONTROL_AULA8_BORRADOR.md). No hay micro-ROM binaria, simulador de CPU ni esquemas eléctricos validados.

## 1. Del número inmediato a una dirección calculada

Hasta ahora, `ST [0x6F00], R0` llevaba la dirección completa de memoria dentro de sus bytes de instrucción. Los programas reales también necesitan recorrer arreglos y consultar parámetros sin escribir una dirección nueva para cada elemento.

Aula-8 propone dos registros de dirección de **16 bits**: `X` como índice y `SP` como base de pila. Las instrucciones de memoria pueden añadir a cualquiera de ellos un desplazamiento **con signo de 8 bits** (`−128` a `+127`). El bus de datos exterior sigue teniendo **8 bits**; únicamente el bus de direcciones tiene 16.

| Expresión | Base de 16 bits | Desplazamiento | Resultado de 16 bits |
| --- | --- | --- | --- |
| `[X+2]` | X=`0x12FF` | `+2` (`02`) | `0x1301` |
| `[X−1]` | X=`0x1200` | `−1` (`FF`) | `0x11FF` |
| `[SP+0]` | SP=`0x7FEE` | `0` (`00`) | `0x7FEE` |
| `[X−128]` | X=`0x0000` | `−128` (`80`) | `0xFF80` (módulo 65536) |
| `[X+1]` | X=`0xFFFF` | `+1` (`01`) | `0x0000` (desbordamiento modular) |

La aritmética de direcciones se propone **módulo 65536**, sin cambiar los flags `Z/N/C/V` del programa. No confundir el acarreo temporal del cálculo con la bandera C visible que puede utilizar `JNC` tras una comparación.

## 2. Codificación de tres bytes

Los mismos opcodes `LD=12` y `ST=13` se reutilizan; el byte selector distingue el modo:

| Modo | Selector para R0 | Selector para R1 | Selector para R2 | Selector para R3 | Tamaño |
| --- | --- | --- | --- | --- | --- |
| Absoluto (0) | `00` | `01` | `02` | `03` | 4 bytes (`OP selector lo hi`) |
| `X+disp8` (1) | `04` | `05` | `06` | `07` | 3 bytes (`OP selector disp`) |
| `SP+disp8` (2) | `08` | `09` | `0A` | `0B` | 3 bytes (`OP selector disp`) |

Todos los bits superiores deben ser cero; el modo `3` y los selectores `0x0C–0xFF` permanecen inválidos o reservados **en la propuesta actual**. No inventar un opcode distinto para `LDX`/`STX`: podrán ser alias del ensamblador para el modo X.

Por ejemplo:

~~~text
12 05 FF   ; LD R1,[X-1]  (modo 1, registro 1, desplazamiento -1)
13 0A 00   ; ST [SP+0],R2 (modo 2, registro 2, desplazamiento 0)
~~~

El opcode selecciona `LD`/`ST`, el selector elige **modo y registro**, y el byte final es un entero firmado, **no una dirección absoluta de 8 bits**.

## 3. Sumar una dirección de 16 bits con una ALU de 8

¿Cómo realizar `X + 2` si la ALU solo es de ocho bits? Propuesta de dos pasadas:

1. Capturar `disp8` completo, por ejemplo `02` o `FF`.
2. Extender el signo: `02 → 0x0002`, `FF → 0xFFFF`, `80 → 0xFF80`.
3. Sumar **bytes bajos**: `base_low + disp8`; guardar resultado bajo en `ADDR_LO` y el acarreo en `ADDR_CARRY` privado.
4. Sumar **bytes altos**: `base_high + (FF si disp negativo; 00 si no) + ADDR_CARRY`; guardar `ADDR_HI`.
5. Formar `MAR ← ADDR_HI:ADDR_LO`, sin modificar el registro base ni las banderas visibles.

### Ejemplo con acarreo

Para `X=0x12FF` y `d=+2`:

- Bajo: `FF + 02 = 0x101` → `ADDR_LO=01`, `ADDR_CARRY=1`.
- Alto: `12 + 00 + 1 = 13` → `ADDR_HI=13`.
- Dirección final `0x1301`.

### Ejemplo con desplazamiento negativo

Para `X=0x1200` y `d=−1` (`FF`):

- Bajo: `00 + FF = FF` → `ADDR_LO=FF`, `ADDR_CARRY=0`.
- Alto: `12 + FF + 0 = 0x111` → `ADDR_HI=11`.
- Dirección final `0x11FF`.

El acarreo final fuera del bit 15 se descarta para la aritmética modular, pero no significa que el acceso a memoria sea permitido. Una dirección calculada en ROM, E/S o una región vacía se somete al **decodificador de memoria**, no a la intuición del programador.

## 4. Ruta lógica de LD/ST con índice

El **fetch compartido** de R0.5 captura opcode y avanza PC. El detalle siguiente corresponde a instrucciones `LD/ST` en modo X o SP y conserva las rutas `LD/ST` absolutas de tandas anteriores.

| Acción | `LD Rd,[BASE+d]` | `ST [BASE+d],Rs` |
| --- | --- | --- |
| Leer selector | Sí; modo 1 o 2 + registro | Sí; modo 1 o 2 + registro |
| Validarlo | Rechazar selector reservado antes de modificar destino | Rechazar selector reservado antes de escribir RAM |
| Leer desplazamiento | Un byte firmado; PC avanza | Un byte firmado; PC avanza |
| Calcular dirección | ALU8 en dos pasadas; `ADDR_CARRY` privado | Igual |
| Construir MAR | `MAR ← dirección efectiva` | Igual |
| Transferir dato | Leer `[MAR]` en MDR; cargar registro | `MDR ← Rs`; escribir `[MAR]` |
| Flags y base | `Z/N/C/V`, X/SP intactos | `Z/N/C/V`, X/SP intactos |

Un `ST` **no** puede utilizar directamente el último byte leído como dato de escritura: ese byte era el desplazamiento. Debe copiar `Rs` a `MDR` después de construir la dirección, como ya ocurrió en R0.5 con `ST` absoluto. Una lectura `LD` captura el dato y luego habilita la escritura del registro destino sin modificar flags.

El [JSON R0.8](MICROINDICES_AULA8_R0_8_BORRADOR.json) describe estas rutas como **macros lógicas**, no microestados de un reloj. Incluye también la carga de `X` por `SETX` para ilustrar un programa autocontenido; quedan sin microcontrol detallado `LEAX`, `ADJSP`, `ADDXW` y otros ajustes de 16 bits.

## 5. Programa de prueba: escribir y leer un elemento indexado

~~~asm
.ORG 0x6000
    SETX 0x6F00
    LDI R0, 0x2A
    ST [X+1], R0
    LD R1, [X+1]
    HALT
~~~

| Dirección | Bytes | Interpretación |
| --- | --- | --- |
| `6000` | `14 00 6F` | X = 0x6F00 |
| `6003` | `11 00 2A` | R0 = 42 |
| `6006` | `13 04 01` | RAM[0x6F01] = R0 |
| `6009` | `12 05 01` | R1 = RAM[0x6F01] |
| `600C` | `01` | HALT |

Resultado esperado: `X=0x6F00`, `R0=R1=0x2A`, `RAM[0x6F01]=0x2A`, `PC=0x600D`; flags anteriores intactos. Son **13 lecturas de bytes de instrucción + una escritura + una lectura de RAM**, es decir **14 lecturas y 1 escritura** externas esperadas. No se infiere frecuencia ni tiempo eléctrico.

## 6. Variables locales y parámetros relativos a SP

El segundo modo es útil para MiniC. Supongamos `SP=0x7FF0` y una función que reserve **dos bytes** mediante la instrucción candidata `ADJSP −2`: ahora `SP=0x7FEE`.

~~~asm
; R2 contiene 0x35 antes del ejemplo.
ADJSP -2           ; reserva dos bytes; microcontrol aún por diseñar
ST [SP+0], R2      ; 13 0A 00: escribe en 0x7FEE
LD R3, [SP+0]      ; 12 0B 00: R3 recupera 0x35
ADJSP +2           ; libera dos bytes; no borra RAM
~~~

Al terminar `SP=0x7FF0` y `R3=0x35`, si las direcciones son RAM válidas y se conserva ese marco de pila durante la secuencia. Esta es una **proyección semántica**, ya que todavía no se ha detallado el microcontrol de `ADJSP` ni una ABI congelada para funciones.

Conviene distinguir:

- `[SP+0]` después de reservar espacio: posición local que la función administra.
- `[SP+2]` en una función: su significado **depende** de cuánto haya reservado la función y de la posición de la dirección de retorno; podría alcanzar retorno o parámetros según el marco. No asignar offsets sin especificar la ABI.
- `[SP−2]` sin reservar: escribiría debajo del SP actual y podría pisar datos en una futura expansión de pila. No enseñarlo como variable local segura.

El libro presentará la relación entre **dirección lógica**, **memoria asignada** y **convención de llamadas** con diagramas precisos. El simulador posterior utilizará el mismo modelo lógico para sus vistas.

## 7. Validación y límites

- El verificador compara una suma de bytes bajos/altos con `(base + signed_disp) & 0xFFFF` en casos de borde, incluidos desbordamientos y desplazamientos negativos.
- Verifica selectores de X/SP, longitud y orden de bytes de un programa de ejemplo y traza de bus **declarada**.
- Las operaciones de direcciones conservan banderas visibles, y los `ST` requieren dueño único del bus de datos.
- La diferencia entre memoria RAM, ROM, E/S y regiones reservadas permanece explícita; `ST` hacia ROM no es escritura de RAM válida.
- El cálculo de dirección **no** cambia `X` o `SP`; `LEAX`/`ADJSP` sí los cambiarían, pero se especificarán aparte.
- No se han determinado circuitos exactos de sumador, latches compartidos, ciclos, señales físicas, protecciones de memoria, control de excepción ni costos de transistores.

**Resultado R0.8:** se dispone de un recorrido causal para `LD/ST` indexado que ya puede servir para planificar el capítulo de arreglos y variables locales. **No** es un procesador ejecutable ni un esquema electrónico listo para fabricar.

**Continuación R0.9:** las microacciones candidatas de `LEAX`, `ADJSP`, `ADDXW`, `SETSP` y `XFROMSP`, y un ejemplo integrado de marco, constan en [ajustes y marcos de Aula-8](AJUSTES_X_SP_Y_MARCOS_AULA8_BORRADOR.md). Esta continuación **no congela la ABI ni ejecuta una CPU**.
