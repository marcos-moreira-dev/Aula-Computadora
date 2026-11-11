#!/usr/bin/env python3
"""Comprueba únicamente la codificación documental propuesta, NO ejecuta una CPU."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "simulador-javafx" / "ISA_AULA8_CANDIDATA.json"
FORMATS = {"none", "reg", "regpair", "reg_imm8", "imm16", "disp8", "memory"}
FLAG_GROUPS = {
    "preserva", "aritmetica_suma", "aritmetica_resta", "logica",
    "incremento", "decremento", "shift",
}


def instruction_size(form: str, data: bytes, index: int) -> int:
    """Valida descriptor y calcula longitud; no reproduce semántica de CPU."""
    if form == "none":
        return 1
    if index + 1 >= len(data):
        raise ValueError("falta byte de operando")

    selector = data[index + 1]
    if form == "reg":
        if selector > 3:
            raise ValueError(f"selector de registro inválido: {selector:02X}")
        return 2
    if form == "regpair":
        if selector > 15:
            raise ValueError(f"selector de par inválido: {selector:02X}")
        return 2
    if form == "reg_imm8":
        if selector > 3:
            raise ValueError(f"registro inválido en inmediato: {selector:02X}")
        return 3
    if form == "imm16":
        return 3
    if form == "disp8":
        return 2
    if form == "memory":
        if selector > 11:
            raise ValueError(f"modo/registro de memoria inválido: {selector:02X}")
        return 4 if selector >> 2 == 0 else 3
    raise ValueError(f"formato desconocido: {form}")


def main() -> int:
    errors: list[str] = []
    try:
        spec = json.loads(SPEC.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: no se puede leer la especificación: {exc}", file=sys.stderr)
        return 1

    if spec.get("status") != "propuesta_no_aprobada":
        errors.append("El contrato aún es BORRADOR, no ISA aprobada")
    if spec.get("architecture") != "Aula-8":
        errors.append("La especificación debe ser exclusiva de Aula-8")
    enc = spec.get("encoding", {})
    if enc.get("external_data_bus_bits") != 8 or enc.get("address_bits") != 16:
        errors.append("No se pueden cambiar los buses de Aula-8")

    by_opcode: dict[int, dict] = {}
    by_mnemonic: set[str] = set()
    for item in spec.get("instructions", []):
        mnemonic = item.get("mnemonic", "")
        hex_opcode = item.get("opcode", "")
        fmt = item.get("format", "")
        if not re.fullmatch(r"[0-9A-F]{2}", hex_opcode):
            errors.append(f"Opcode no hex de 2 dígitos: {mnemonic}={hex_opcode!r}")
            continue
        opcode = int(hex_opcode, 16)
        if opcode in by_opcode:
            errors.append(f"Colisión de opcode {hex_opcode}: {mnemonic}")
        by_opcode[opcode] = item
        if mnemonic in by_mnemonic or not mnemonic:
            errors.append(f"Mnemónico duplicado o vacío: {mnemonic!r}")
        by_mnemonic.add(mnemonic)
        if fmt not in FORMATS:
            errors.append(f"Formato no admitido para {mnemonic}: {fmt}")
        if item.get("flags") not in FLAG_GROUPS:
            errors.append(f"Reglas de flags no reconocidas para {mnemonic}")

    if len(by_opcode) != 36:
        errors.append(f"Esperados 36 opcodes candidatos; encontrados {len(by_opcode)}")

    instruction_count = 0
    examples = spec.get("examples", [])
    if len(examples) != 3:
        errors.append("Se esperan tres lecciones en bytes")

    for example in examples:
        name = example.get("name", "sin_nombre")
        try:
            origin = example["origin"]
            data = bytes.fromhex(example["bytes_hex"])
            if origin < 0 or origin + len(data) > 0x8000:
                raise ValueError("ejemplo no cabe íntegramente en RAM")
            expected = example["expected_decode"]
            decoded: list[dict] = []
            pos = 0
            while pos < len(data):
                opcode = data[pos]
                if opcode not in by_opcode:
                    raise ValueError(f"opcode no definido en {origin + pos:04X}: {opcode:02X}")
                inst = by_opcode[opcode]
                size = instruction_size(inst["format"], data, pos)
                if pos + size > len(data):
                    raise ValueError(f"instrucción truncada en {origin + pos:04X}")
                decoded.append({"pc": origin + pos, "mnemonic": inst["mnemonic"], "size": size})
                pos += size
            if decoded != expected:
                raise ValueError(f"mapa de decodificación inconsistente: {decoded!r}")
            if decoded[-1]["mnemonic"] != "HALT":
                raise ValueError("el ejemplo no termina en HALT")

            boundaries = {item["pc"] for item in decoded}
            stored_absolute_addresses: set[int] = set()
            for item in decoded:
                start = item["pc"] - origin
                mnemonic = item["mnemonic"]
                if mnemonic in {"JMP", "JZ", "JNZ", "JC", "JNC", "CALL"}:
                    target = data[start + 1] | (data[start + 2] << 8)
                    if origin <= target < origin + len(data) and target not in boundaries:
                        raise ValueError(f"salto cae dentro de una instrucción en {target:04X}")
                if mnemonic == "ST" and data[start + 1] >> 2 == 0:
                    stored_absolute_addresses.add(data[start + 2] | (data[start + 3] << 8))

            if "expected_ram_write" in example:
                address = example["expected_ram_write"]["address"]
                value = example["expected_ram_write"]["value"]
                if not (0 <= address < 0x8000 and 0 <= value <= 255):
                    raise ValueError("destino o dato esperado fuera de RAM/byte")
                if origin <= address < origin + len(data):
                    raise ValueError("resultado sobrescribiría bytes del propio programa")
                if address not in stored_absolute_addresses:
                    raise ValueError("dirección declarada no coincide con ningún ST absoluto")
            instruction_count += len(decoded)
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f"Ejemplo {name}: {exc}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"ISA Aula-8 BORRADOR: {len(by_opcode)} opcodes sin colisión")
    print(f"Ejemplos: {len(examples)} programas, {instruction_count} instrucciones decodificadas")
    print("CODIFICACIÓN DOCUMENTAL: APROBADA (NO es una simulación de CPU)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
