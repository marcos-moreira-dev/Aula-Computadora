#!/usr/bin/env python3
"""Ensamblador de REFERENCIA para una subcolección de la ISA Aula-8 R0.3.

Ejecuta en la PC anfitriona; NO es el ensamblador nativo ni ejecuta la CPU.
Acepta una sola sección .ORG en 6000..6EFF y etiquetas absolutas.
El producto sirve para auditar bytes, longitudes y referencias adelantadas.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


OPCODES = {
    'HALT': (0x01, 'none', 1), 'RET': (0x02, 'none', 1),
    'LDI': (0x11, 'reg_imm8', 3), 'ST': (0x13, 'st_abs', 4),
    'ADD': (0x20, 'regpair', 2), 'SUB': (0x22, 'regpair', 2),
    'CMP': (0x24, 'regpair', 2), 'DEC': (0x2A, 'reg', 2),
    'JMP': (0x30, 'imm16', 3), 'JZ': (0x31, 'imm16', 3),
    'JNZ': (0x32, 'imm16', 3), 'JNC': (0x34, 'imm16', 3),
    'CALL': (0x35, 'imm16', 3),
}
LABEL = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
ST_ARGS = re.compile(r'^\[(0x[0-9a-fA-F]+|\d+)\]\s*,\s*(R[0-3])$', re.I)


@dataclass(frozen=True)
class Assembly:
    origin: int
    data: bytes
    symbols: dict[str, int]
    listing: tuple[tuple[int, bytes, str], ...]


def number(token: str, limit: int, symbols: dict[str, int] | None = None) -> int:
    token = token.strip()
    if symbols is not None and token.upper() in symbols:
        val = symbols[token.upper()]
    else:
        try:
            val = int(token, 0) if token.lower().startswith('0x') else int(token, 10)
        except ValueError as exc:
            raise ValueError(f'Número o etiqueta no resuelta: {token}') from exc
    if not 0 <= val <= limit:
        raise ValueError(f'Fuera de rango 0..{limit}: {token}')
    return val


def reg(text: str) -> int:
    value = text.strip().upper()
    if not re.fullmatch(r'R[0-3]', value):
        raise ValueError(f'Se esperaba R0..R3: {text}')
    return int(value[1])


def assemble(source: str) -> Assembly:
    """Dos pasadas: direcciones/etiquetas, después emisión de bytes.

    Restringe deliberadamente el alcance: no comprueba semántica de CPU,
    temporización, profundidad de pila ni ROM real.
    """
    symbols: dict[str, int] = {}
    instructions: list[tuple[int, str, str, str]] = []
    cursor: int | None = None
    origin: int | None = None
    for line_no, raw in enumerate(source.splitlines(), 1):
        line = raw.split(';', 1)[0].strip()
        if not line:
            continue
        if ':' in line:
            candidate, line = line.split(':', 1)
            candidate = candidate.strip().upper()
            if not LABEL.fullmatch(candidate):
                raise ValueError(f'Línea {line_no}: etiqueta inválida')
            if cursor is None:
                raise ValueError(f'Línea {line_no}: .ORG debe preceder etiquetas')
            if candidate in symbols:
                raise ValueError(f'Línea {line_no}: etiqueta duplicada {candidate}')
            symbols[candidate] = cursor
            line = line.strip()
            if not line:
                continue
        parts = line.split(None, 1)
        op, args = parts[0].upper(), (parts[1].strip() if len(parts) == 2 else '')
        if op == '.ORG':
            if origin is not None or not args:
                raise ValueError(f'Línea {line_no}: solo una directiva .ORG con dirección')
            origin = cursor = number(args, 0xFFFF)
            if not 0x6000 <= cursor < 0x6F00:
                raise ValueError('El área educativa de código es 6000..6EFF')
            continue
        if op not in OPCODES:
            raise ValueError(f'Línea {line_no}: operación no admitida {op}')
        if cursor is None:
            raise ValueError(f'Línea {line_no}: falta .ORG')
        size = OPCODES[op][2]
        if cursor + size > 0x6F00:
            raise ValueError(f'Línea {line_no}: el programa invade la zona 6F00')
        instructions.append((cursor, op, args, raw.strip()))
        cursor += size
    if origin is None or not instructions:
        raise ValueError('Se requiere .ORG y al menos una instrucción')

    assembled = bytearray()
    listing: list[tuple[int, bytes, str]] = []
    for pc, op, args, raw in instructions:
        opcode, form, _ = OPCODES[op]
        data = [opcode]
        if form == 'none':
            if args:
                raise ValueError(f'{op} no acepta operandos')
        elif form == 'reg':
            data.append(reg(args))
        elif form == 'reg_imm8':
            fields = [x.strip() for x in args.split(',')]
            if len(fields) != 2:
                raise ValueError('LDI requiere registro e inmediato')
            data += [reg(fields[0]), number(fields[1], 0xFF)]
        elif form == 'regpair':
            fields = [x.strip() for x in args.split(',')]
            if len(fields) != 2:
                raise ValueError(f'{op} requiere dos registros')
            data.append((reg(fields[0]) << 2) | reg(fields[1]))
        elif form == 'st_abs':
            match = ST_ARGS.fullmatch(args)
            if not match:
                raise ValueError('ST admite [dirección_absoluta], R0..R3')
            addr = number(match[1], 0xFFFF)
            if not 0x6000 <= addr <= 0x7FFF:
                raise ValueError('ST educativo solo admite RAM 6000..7FFF')
            data += [reg(match[2]), addr & 0xFF, addr >> 8]
        elif form == 'imm16':
            addr = number(args, 0xFFFF, symbols)
            if op != 'CALL' and not 0x6000 <= addr < 0x6F00:
                raise ValueError('Saltos de práctica deben permanecer en 6000..6EFF')
            if op == 'CALL' and not (0x6000 <= addr < 0x6F00 or addr in (0xFF00,0xFF04,0xFF08,0xFF0C)):
                raise ValueError('CALL fuera de programa o API ROM pública de ejemplo')
            data += [addr & 0xFF, addr >> 8]
        payload = bytes(data)
        if len(payload) != OPCODES[op][2]:
            raise AssertionError(f'Longitud incoherente de {op}')
        assembled.extend(payload)
        listing.append((pc, payload, raw))
    return Assembly(origin, bytes(assembled), symbols, tuple(listing))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('fuente', type=Path, help='Archivo .asm en sintaxis educativa')
    args = parser.parse_args()
    result = assemble(args.fuente.read_text(encoding='utf-8'))
    print(f'Ensamblado teórico Aula-8 R0.3 (SOLO ANFITRIÓN): {len(result.data)} bytes')
    for pc, data, source in result.listing:
        print(f'{pc:04X}: {data.hex(" ").upper():<13}  {source}')
    print('ETIQUETAS:', ', '.join(f'{k}={v:04X}' for k, v in result.symbols.items()))
    print('IMAGEN:', result.data.hex(' ').upper())


if __name__ == '__main__':
    main()
