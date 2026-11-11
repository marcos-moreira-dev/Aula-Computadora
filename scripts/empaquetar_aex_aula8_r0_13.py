#!/usr/bin/env python3
"""Utilidad ANFITRIÓN para crear o inspeccionar contenedores AEX1 Aula-8."""

from __future__ import annotations

import argparse
from pathlib import Path

from modelo_ejecutable_aula8_r0_13 import (
    AexError, KIND_PRACTICE, KIND_TOOL, decode_aex, pack_aex,
)


def hex16(value: str) -> int:
    if len(value) != 4 or any(c not in "0123456789abcdefABCDEF" for c in value):
        raise argparse.ArgumentTypeError("Utiliza 4 dígitos hexadecimales, por ejemplo 6000")
    return int(value, 16)


def main() -> int:
    parser = argparse.ArgumentParser(description="AEX1 propuesto: SOLO anfitrión, no cargador de CPU")
    sub = parser.add_subparsers(dest="action", required=True)
    create = sub.add_parser("crear", help="binario plano a bloques AEX1")
    create.add_argument("--bin", required=True, type=Path)
    create.add_argument("--out", required=True, type=Path)
    create.add_argument("--origen", required=True, type=hex16)
    create.add_argument("--entrada", required=True, type=hex16)
    create.add_argument("--tipo", required=True, choices=("practica", "herramienta"))
    inspect = sub.add_parser("inspeccionar", help="verificar archivo AEX1 autónomo")
    inspect.add_argument("--archivo", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.action == "crear":
            data = args.bin.read_bytes()
            kind = KIND_PRACTICE if args.tipo == "practica" else KIND_TOOL
            blob = pack_aex(data, kind=kind, origin=args.origen, entry=args.entrada)
            with args.out.open("xb") as sink:  # No sobrescribir trabajo previo.
                sink.write(blob)
            print(f"AEX1 creado: {args.out} ({len(blob) // 256} bloques, {len(data)} B útiles)")
        else:
            decoded = decode_aex(args.archivo.read_bytes())
            tipo = "practica" if decoded.kind == KIND_PRACTICE else "herramienta"
            print(f"AEX1 válido: Aula-8, {tipo}, origen={decoded.origin:04X}, "
                  f"entrada={decoded.entry:04X}, código={len(decoded.payload)} B, "
                  f"bloques={decoded.total_blocks}, CRC16={decoded.payload_crc16:04X}")
        return 0
    except (AexError, OSError) as exc:
        parser.exit(2, f"ERROR AEX1: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
