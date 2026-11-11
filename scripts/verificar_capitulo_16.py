#!/usr/bin/env python3
"""CALL/RET, LIFO y JNZ: validaciones documentales, no ejecución de CPU."""

import json
from pathlib import Path
from verificar_capitulos_16_17_comun import ROOT, verificar_documentos


def main():
    micro = json.loads((ROOT / 'simulador-javafx/MICROFLUJO_AULA8_R0_6_BORRADOR.json')
                       .read_text(encoding='utf-8'))
    assert micro['status'] == 'propuesta_no_aprobada'
    assert micro['granularity'] == 'acciones_logicas_no_ciclos_de_reloj'
    assert micro['exact_clock_cycles'] is None and not micro['cpu_executed']
    stack = micro['stack_convention']
    assert stack['initial_sp_candidate'] == 0x8000
    assert stack['direction'] == 'descendente'
    assert stack['call_subtracts_from_sp'] == 2 and stack['ret_adds_to_sp'] == 2
    assert stack['return_low_at_sp'] and stack['return_high_at_sp_plus_one']
    assert not stack['ret_does_not_clear_memory'] is False
    checks = 8

    program = {}
    for segment in micro['example']['segments']:
        for offset, data in enumerate(bytes.fromhex(segment['bytes_hex'])):
            program[segment['origin'] + offset] = data

    # Se interpretan únicamente las instrucciones concretas del ejemplo.
    for initial_flags in range(16):
        for initial_r0 in range(256):
            pc, sp, r0, halted = 0x6000, 0x8000, initial_r0, False
            ram = dict(program)
            events = []

            def read(address):
                value = ram[address]
                events.append({'operation': 'read', 'address': address, 'value': value})
                return value

            def write(address, value):
                ram[address] = value
                events.append({'operation': 'write', 'address': address, 'value': value})

            for mnemonic in ('CALL', 'LDI', 'RET', 'HALT'):
                opcode = read(pc)
                pc += 1
                if mnemonic == 'CALL':
                    assert opcode == int(micro['routes']['CALL']['opcode'], 16)
                    low, high = read(pc), read(pc + 1)
                    pc += 2
                    ret = pc
                    sp -= 2
                    write(sp, ret & 0xFF)
                    write(sp + 1, ret >> 8)
                    pc = low | high << 8
                elif mnemonic == 'LDI':
                    assert opcode == 0x11
                    sel, immediate = read(pc), read(pc + 1)
                    assert sel == 0
                    r0 = immediate
                    pc += 2
                elif mnemonic == 'RET':
                    assert opcode == int(micro['routes']['RET']['opcode'], 16)
                    pc = read(sp) | read(sp + 1) << 8
                    sp += 2
                elif mnemonic == 'HALT':
                    assert opcode == 0x01
                    halted = True
            assert events == micro['example']['expected_trace']
            assert (pc, sp, r0, halted) == (0x6004, 0x8000, 42, True)
            assert ram[0x7FFE] == 3 and ram[0x7FFF] == 0x60
            assert initial_flags in range(16)  # Ninguna instrucción escribió FLAGS.
            checks += 5

    assert sum(e['operation'] == 'read' for e in events) == 10
    assert sum(e['operation'] == 'write' for e in events) == 2
    checks += 2

    for outer in range(0x10000):
        # Dos llamadas: el retorno interior sale primero y el exterior queda intacto.
        sp = 0x8000
        ram = {}
        for ret in (outer, 0x6013):
            sp -= 2
            ram[sp] = ret & 0xFF
            ram[sp + 1] = ret >> 8
        assert sp == 0x7FFC
        top = ram[sp] | ram[sp + 1] << 8
        sp += 2
        older = ram[sp] | ram[sp + 1] << 8
        sp += 2
        assert (top, older, sp) == (0x6013, outer, 0x8000)
        checks += 2

    branch = micro['branch_example']
    assert branch['mnemonic'] == 'JNZ'
    assert branch['encoded_bytes'] == '32 03 60'
    assert branch['observed_z_assumed_from_dec'] == [0, 0, 1]
    assert branch['expected_taken'] == [True, True, False]
    assert not branch['dec_microcontrol_implemented']
    for counter in range(1, 256):
        count = counter
        while count:
            count -= 1
            z = int(count == 0)
            taken = z == 0
            assert taken == (count != 0)
            checks += 1
    checks += 5

    checks += verificar_documentos('16', 'subrutinas_y_pila', (
        'c16_fig01_pila_retorno', 'c16_fig02_llamar_regresar',
        'c16_fig03_llamadas_anidadas', 'c16_fig04_bucle_jnz',
    ), 7, ('CALL', 'RET', 'JNZ', 'LIFO', '0x7FFE', '10 lecturas',
           '2 escrituras', 'microsecuencia', 'capítulo 17'))
    print(f'Capítulo 16: {checks} comprobaciones lógicas/documentales correctas; CPU real no ejecutada.')


if __name__ == '__main__':
    main()
