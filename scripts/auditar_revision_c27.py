#!/usr/bin/env python3
"""Auditoría de contrato para los añadidos didácticos de C27.

No certifica la electrónica: comprueba integridad, referencias y que los ejemplos
binarios derivan de los contratos candidatos conservados en este repositorio.
"""

from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image
import generar_figuras_construccion_c27 as diagramas
import generar_libro_maestro as maestro


def main():
    raiz = Path(__file__).resolve().parents[1]
    figuras = raiz / 'libro' / 'figuras'
    nuevo = {
        'c05_fig05_sn74hct00_patillaje': '05_la_realimentacion_conserva_informacion.md',
        'c07_fig05_registro_aula8': '07_del_bit_al_registro.md',
        'c08_fig05_buses_aula8': '08_direcciones_y_buses.md',
        'c12_fig05_ruta_acumulada_aula8': '12_arquitectura_aula_8.md',
        'c14_fig05_ram_contigua_deposito': '14_de_numeros_a_instrucciones.md',
        'c14_fig06_ram_salto': '14_de_numeros_a_instrucciones.md',
        'c16_fig05_ram_y_pila_call_ret': '16_subrutinas_y_pila.md',
        'c16_fig06_ram_bucle_jnz': '16_subrutinas_y_pila.md',
        'c22_fig05_dos_bancos_aula16': '22_un_bus_externo_de_16_bits.md',
    }
    opcodes, programita, bucle = diagramas.validate_isa()
    assert programita['bytes_hex'].split() == ['11','00','2A','13','00','00','6F','01']
    assert bucle['bytes_hex'].split() == ['11','00','03','2A','00','32','03','60','01']
    assert opcodes['JMP'] == 0x30 and opcodes['CALL'] == 0x35
    assert opcodes['RET'] == 0x02 and opcodes['JNZ'] == 0x32
    for nombre,capitulo in nuevo.items():
        md = (raiz / 'libro' / 'capitulos' / capitulo).read_text(encoding='utf-8')
        assert f'[[FIG:{nombre}|' in md, (nombre, capitulo)
        svg, png = figuras / f'{nombre}.svg', figuras / f'{nombre}.png'
        ET.parse(svg)
        with Image.open(png) as foto:
            assert foto.width >= 1600
            foto.verify()
    secciones = 0
    for capitulo in maestro.ORDER:
        contenido = capitulo.read_text(encoding='utf-8')
        assert 'JavaFX' not in contenido and 'javafx' not in contenido
        secciones += contenido.count('## Construimos Aula-')
    assert secciones >= 18, secciones
    contenido_pdf = (raiz / 'libro' / 'Aula_Computadora_C27_0_1_MAESTRO.pdf')
    assert contenido_pdf.exists(), 'Todavía falta generar el PDF de la edición C27.'
    print(f'CONTRATOS C27 CORRECTOS: {len(nuevo)} figuras nuevas, '
          f'{secciones} hitos narrativos, ISA R0.3 candidata.')


if __name__ == '__main__':
    main()
