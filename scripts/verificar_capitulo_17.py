#!/usr/bin/env python3
"""Verifica el mapa ROM/RESET/monitor de C17 sobre contratos candidatos."""

import json
from verificar_capitulos_16_17_comun import ROOT, verificar_documentos
from verificar_rom_monitor_aula8_r0_11_borrador import parse_monitor, check_rom, check_abi_and_return


def main():
    spec = json.loads((ROOT / 'simulador-javafx/ROM_MONITOR_AULA8_R0_11_BORRADOR.json')
                      .read_text(encoding='utf-8'))
    isa = json.loads((ROOT / 'simulador-javafx/ISA_AULA8_CANDIDATA.json')
                     .read_text(encoding='utf-8'))
    state = json.loads((ROOT / 'ESTADO_PORTABLE.json').read_text(encoding='utf-8'))
    assert spec['status'] == 'propuesta_no_aprobada'
    assert not spec['firmware_implemented'] and not spec['cpu_executed']
    assert not spec['rom_image_built'] and not spec['electrical_validation']
    checks = 4 + check_rom(spec, isa, state) + check_abi_and_return(spec, isa)

    monitor = spec['monitor_candidate']
    for case in spec['example_monitor_vectors']:
        result, info = parse_monitor(case['line'], monitor)
        assert result == case['result'], (case, result)
        if 'count' in case:
            assert info['count'] == case['count'], case
        if 'error' in case:
            assert info['error'] == case['error'], case
        checks += 1

    # Ejercicios de contorno de lectura, escritura y ejecución: 65536 direcciones.
    for address in range(0x10000):
        hexaddr = f'{address:04X}'
        poke, _ = parse_monitor(f'POKE {hexaddr} 2A', monitor)
        run, _ = parse_monitor(f'RUN {hexaddr}', monitor)
        mem, _ = parse_monitor(f'MEM {hexaddr} 01', monitor)
        assert (poke == 'POKE') == (0x6000 <= address <= 0x6FFF)
        assert (run == 'RUN') == (0x6000 <= address <= 0x6FFF)
        assert (mem == 'MEM') == (address <= 0x7FFF or address >= 0xE000)
        checks += 3

    checks += verificar_documentos('17', 'encender_una_computadora', (
        'c17_fig01_vector_reset', 'c17_fig02_mapa_memoria',
        'c17_fig03_ranuras_rom', 'c17_fig04_run_dos_ret',
    ), 8, ('FFFC', 'FFFD', 'E000', '8192', 'FW_PUTC', 'FW_GETC',
           'MEM 6000 10', 'POKE 6000 2A', 'RUN 6000', 'HALT', 'RET', 'capítulo 18'))
    print(f'Capítulo 17: {checks} comprobaciones lógicas/documentales correctas; ROM y CPU no ejecutadas.')


if __name__ == '__main__':
    main()
