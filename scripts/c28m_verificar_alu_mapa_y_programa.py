#!/usr/bin/env python3
"""Auditoría matemática del hilo C08-C14 (NO CPU ni placa construidas).

Se comprueban tablas y ejemplos del manuscrito, 16 bits de direcciones,
sumador/ALU ideales y el flujo documental LDI/ST/HALT del borrador ISA.
"""

from __future__ import annotations

from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "libro" / "capitulos"
OUT = ROOT / "c28_m" / "auditoria" / "C28_M_RESULTADOS.json"


def signed8(byte: int) -> int:
    return byte - 256 if byte & 0x80 else byte


def ripple8(a: int, b: int, carry_in: int = 0) -> tuple[int, int, int]:
    """Ocho sumadores completos, de bit 0 a bit 7."""
    carry = carry_in
    output = 0
    into_sign = 0
    for bit in range(8):
        if bit == 7:
            into_sign = carry
        av, bv = (a >> bit) & 1, (b >> bit) & 1
        digit = av ^ bv ^ carry
        carry = (av & bv) | (av & carry) | (bv & carry)
        output |= digit << bit
    return output, carry, into_sign


def chapter(number: int, title: str) -> str:
    return (CHAPTERS / f"{number:02d}_{title}.md").read_text(encoding="utf-8")


def assert_rows(content: str, rows: list[str]) -> None:
    for row in rows:
        assert row in content, f"Fila del manuscrito no encontrada: {row}"


def verify() -> dict:
    c08 = chapter(8, "direcciones_y_buses")
    c09 = chapter(9, "ram_y_rom_reales")
    c10 = chapter(10, "el_circuito_que_suma")
    c11 = chapter(11, "la_unidad_aritmetico_logica")
    c12 = chapter(12, "arquitectura_aula_8")
    c13 = chapter(13, "la_unidad_de_control")
    c14 = chapter(14, "de_numeros_a_instrucciones")

    # Comprobación de la progresión causal, no solo de la presencia de capítulos.
    steps = [
        (c08, "conectar el registro con un lugar de memoria"),
        (c09, "un registro ya puede intercambiar bytes con RAM"),
        (c10, "una operación que cambia el estado"),
        (c11, "elegir la operación antes de escribir"),
        (c12, "lo acumulado ya tiene una arquitectura"),
        (c13, "una instrucción es una serie de autorizaciones"),
        (c14, "leer la RAM como si estuviéramos frente al panel"),
    ]
    for text, expected in steps:
        assert expected in text

    assert_rows(c08, [
        "| 0 | 0 | `SEL0` |", "| 0 | 1 | `SEL1` |",
        "| 1 | 0 | `SEL2` |", "| 1 | 1 | `SEL3` |",
    ])
    assert "0x1200" in c08 and "4608" in c08
    assert "0x1234" in c08 and "0x34" in c08 and "0x12" in c08

    # Dos decodificadores independientes deben evitar solapamientos; la
    # región no asignada debe seguir siendo de 24 KiB en este EJEMPLO.
    widths = {"sram": 0, "rom": 0, "sin_asignar": 0}
    for addr in range(65536):
        sram = (addr & 0x8000) == 0
        rom = (addr & 0xE000) == 0xE000
        assert not (sram and rom)
        if sram:
            assert (addr & 0x7FFF) == addr
            widths["sram"] += 1
        elif rom:
            assert (addr & 0x1FFF) == addr - 0xE000
            widths["rom"] += 1
        else:
            assert 0x8000 <= addr <= 0xDFFF
            widths["sin_asignar"] += 1
    assert widths == {"sram": 32768, "rom": 8192, "sin_asignar": 24576}
    assert_rows(c09, [
        "| `0x0000–0x7FFF` | 32 KiB | SRAM 32K × 8 |",
        "| `0x8000–0xDFFF` | 24 KiB | Sin asignación aquí; futura E/S u otros |",
        "| `0xE000–0xFFFF` | 8 KiB | EEPROM 8K × 8 usada como ROM |",
    ])
    assert 0xE123 - 0xE000 == 0x0123 == 291
    assert "0xE123 − 0xE000 = 0x0123" in c09

    # Tablas independientes del código que calcula los acarreos.
    half_rows = [
        "| 0 | 0 | 0 | 0 |", "| 0 | 1 | 1 | 0 |",
        "| 1 | 0 | 1 | 0 |", "| 1 | 1 | 0 | 1 |",
    ]
    full_rows = [
        "| 0 | 0 | 0 | 0 | 0 |", "| 0 | 0 | 1 | 1 | 0 |",
        "| 0 | 1 | 0 | 1 | 0 |", "| 0 | 1 | 1 | 0 | 1 |",
        "| 1 | 0 | 0 | 1 | 0 |", "| 1 | 0 | 1 | 0 | 1 |",
        "| 1 | 1 | 0 | 0 | 1 |", "| 1 | 1 | 1 | 1 | 1 |",
    ]
    assert_rows(c10, half_rows + full_rows)
    for a, b in product((0, 1), repeat=2):
        assert ((a ^ b), (a & b)) == ((a + b) % 2, (a + b) // 2)
    for a, b, cin in product((0, 1), repeat=3):
        total = a + b + cin
        assert ((a ^ b ^ cin), ((a & b) | (a & cin) | (b & cin))) == (total % 2, total // 2)

    for a, b in product(range(256), repeat=2):
        result, carry, c7 = ripple8(a, b)
        exact = a + b
        assert result == (exact & 255)
        assert carry == int(exact >= 256)
        add_overflow = not (-128 <= signed8(a) + signed8(b) <= 127)
        assert (c7 ^ carry) == int(add_overflow)

        neg_b = b ^ 255
        sub, cout, _ = ripple8(a, neg_b, 1)
        borrow = 1 - cout
        sub_overflow = bool(((a ^ b) & (a ^ sub) & 0x80) != 0)
        expected_sign_overflow = not (-128 <= signed8(a) - signed8(b) <= 127)
        negative = (sub >> 7) & 1
        zero = int(sub == 0)
        assert sub == ((a - b) & 255)
        assert borrow == int(a < b)
        assert sub_overflow == expected_sign_overflow
        assert (negative ^ int(sub_overflow)) == int(signed8(a) < signed8(b))
        assert ((not borrow) and (not zero)) == (a > b)
        assert (zero == 1) == (a == b)

    assert_rows(c10, [
        "| `13 + 9` | `0x16` (22) | 0 | 0 | 0 | 0 |",
        "| `250 + 10` | `0x04` (4) | 1 | 0 | 0 | 0 |",
        "| `127 + 1` | `0x80` (−128 con signo) | 0 | 1 | 0 | 1 |",
        "| `0xFF + 0x01` | `0x00` (0) | 1 | 0 | 1 | 0 |",
    ])
    assert_rows(c11, [
        "| `13 − 9` | `0x04` | 0 | 0 | 0 | 0 |",
        "| `9 − 13` | `0xFC` | 1 | 0 | 0 | 1 |",
        "| `0x80 − 0x01` | `0x7F` | 0 | 1 | 0 | 0 |",
        "| `0x2A − 0x2A` | `0x00` | 0 | 0 | 1 | 0 |",
    ])
    assert "C en SUB = préstamo = 1 − Cout interno" in c11
    assert "N ⊕ V" in c11
    assert "0x5A" in c11 and "0x3C" in c11
    assert (0x5A & 0x3C, 0x5A | 0x3C, 0x5A ^ 0x3C, 0x5A ^ 255) == (0x18, 0x7E, 0x66, 0xA5)

    # C12/13: la máquina diferencia control de cálculo y respeta un bus
    # exclusivo; este chequeo documental NO prueba un microsecuenciador.
    assert "MAR" in c12 and "MDR" in c12 and "PC" in c12
    assert "LDI_SELECTOR" in c13 and "ST_STAGE_DATA" in c13
    assert "MDR para WR = R0 = 0x2A" in c13
    assert "ocho lecturas de memoria de programa y una escritura" in c13

    spec = json.loads((ROOT / "simulador-javafx" / "ISA_AULA8_CANDIDATA.json").read_text(encoding="utf-8"))
    assert spec["status"] == "propuesta_no_aprobada"
    opcodes = {item["mnemonic"]: int(item["opcode"], 16) for item in spec["instructions"]}
    assert (opcodes["LDI"], opcodes["ST"], opcodes["HALT"]) == (0x11, 0x13, 0x01)
    example = next(e for e in spec["examples"] if e["name"] == "depositar_42")
    program = bytes.fromhex(example["bytes_hex"])
    assert program == bytes((0x11, 0, 0x2A, 0x13, 0, 0, 0x6F, 0x01))
    assert example["origin"] == 0x6000
    assert "11 00 2A" in c14 and "13 00 00 6F" in c14
    assert "PC final = 0x6008" in c14

    # Interpretador de TRES operaciones del ejemplo, nunca CPU/microcódigo.
    ram = {example["origin"] + i: byte for i, byte in enumerate(program)}
    reg = [0, 0, 0, 0]
    pc = example["origin"]
    reads, writes, instructions = 0, 0, []

    def fetch() -> int:
        nonlocal pc, reads
        value = ram[pc]
        pc += 1
        reads += 1
        return value

    for _ in range(3):
        op = fetch()
        if op == opcodes["LDI"]:
            selector, immediate = fetch(), fetch()
            assert 0 <= selector <= 3
            reg[selector] = immediate
            instructions.append("LDI")
        elif op == opcodes["ST"]:
            selector, lo, hi = fetch(), fetch(), fetch()
            assert selector <= 3
            addr = lo | (hi << 8)
            assert 0 <= addr < 0x8000 and addr not in range(0x6000, 0x6008)
            ram[addr] = reg[selector]
            writes += 1
            instructions.append("ST")
        elif op == opcodes["HALT"]:
            instructions.append("HALT")
            break
        else:
            raise AssertionError(f"Opcode fuera del ejemplo: {op:02X}")
    assert instructions == ["LDI", "ST", "HALT"]
    assert pc == 0x6008 and reads == 8 and writes == 1
    assert reg[0] == ram[0x6F00] == 0x2A
    assert ram[0x6002] == 0x2A  # la escritura no pisa el programa

    return {
        "etapa": "C28-M: memoria, aritmética, banderas e ISA de papel",
        "vectores_exhaustivos": {
            "decodificacion_memoria": 65536,
            "sumador8": 65536,
            "restador8_y_comparaciones": 65536,
            "medio_sumador": 4,
            "sumador_completo": 8,
        },
        "total_vectores": 196620,
        "programa_documental": {
            "instrucciones": instructions,
            "lecturas": reads,
            "escrituras": writes,
            "pc_final": hex(pc),
            "registro_r0": hex(reg[0]),
            "ram_6f00": hex(ram[0x6F00]),
        },
        "limitaciones": [
            "No ensaya SRAM/EEPROM físicas ni las señales eléctricas de CE/OE/WE",
            "ALU ideal; no calcula retardos reales ni implementa un HDL de ocho bits",
            "La interpretación LDI/ST/HALT es una referencia de tres instrucciones, NO una CPU",
            "ISA, mapa y microsecuencias siguen propuestas sin aprobación física",
            "Presencia de ecuaciones/tablas no equivale a transcribir todos los cables de imágenes",
        ],
    }


def main() -> None:
    result = verify()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"C28-M: {result['total_vectores']:,} vectores de referencia aprobados")
    for name, count in result["vectores_exhaustivos"].items():
        print(f"  {name}: {count:,}")
    print("Programa de papel: 3 instrucciones; 8 lecturas; 1 escritura; PC=6008")
    print("Límite: NO CPU, hardware, ni tiempos físicos certificados")


if __name__ == "__main__":
    main()
