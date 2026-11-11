#!/usr/bin/env python3
"""Genera la red NAND y el Verilog de una ruta aritmética ADD/SUB de 8 bits.

Su única fuente de topología es el procedimiento declarativo build().
La salida NO es una ALU Aula-8 completa, ISA, reloj ni circuito eléctrico.
--write: regenera las salidas derivadas. --check: comprueba identidad exacta.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NETLIST = ROOT / "c28_r/netlists/alu8_addsub_134nand.json"
RTL = ROOT / "c28_r/rtl/alu8_addsub_134nand.v"


def build() -> dict:
    gates: list[dict] = []
    names = {f"A{i}" for i in range(8)} | {f"B{i}" for i in range(8)} | {"SUB"}

    def nand(name: str, a: str, b: str) -> str:
        assert name not in names, name
        assert a in names and b in names, (name, a, b)
        gates.append({"name": name, "op": "NAND", "inputs": [a, b]})
        names.add(name)
        return name

    carry = "SUB"  # Cin=0 para suma, Cin=1 para resta por complemento a dos.
    for bit in range(8):
        a, b = f"A{bit}", f"B{bit}"

        # XOR(Bi,SUB) en cuatro NAND.
        bx1 = nand(f"bx{bit}_1", b, "SUB")
        bx2 = nand(f"bx{bit}_2", b, bx1)
        bx3 = nand(f"bx{bit}_3", "SUB", bx1)
        bx = nand(f"Bmod{bit}", bx2, bx3)

        # Sumador completo de nueve NAND. La señal an es NAND(A,Bmod).
        an = nand(f"an{bit}", a, bx)
        au = nand(f"au{bit}", a, an)
        av = nand(f"av{bit}", bx, an)
        p = nand(f"P{bit}", au, av)
        cn = nand(f"cn{bit}", p, carry)
        su = nand(f"su{bit}", p, cn)
        sv = nand(f"sv{bit}", carry, cn)
        nand(f"S{bit}", su, sv)
        carry = nand(f"C{bit+1}", an, cn)

    assert carry == "C8"

    # En esta propuesta C=acarreo para ADD; C=préstamo para SUB.
    c1 = nand("cf1", "C8", "SUB")
    c2 = nand("cf2", "C8", c1)
    c3 = nand("cf3", "SUB", c1)
    nand("Cflag", c2, c3)

    # El desbordamiento firmado se obtiene con C7 XOR C8 para ambas rutas.
    v1 = nand("vf1", "C7", "C8")
    v2 = nand("vf2", "C7", v1)
    v3 = nand("vf3", "C8", v1)
    nand("V", v2, v3)

    # Z=AND(NOT S0, ..., NOT S7), usando solo NAND.
    inverted = [nand(f"notS{i}", f"S{i}", f"S{i}") for i in range(8)]
    level = inverted
    step = 0
    while len(level) > 1:
        next_level = []
        for j in range(0, len(level), 2):
            inv = nand(f"z_{step}_{j}_neg", level[j], level[j+1])
            next_level.append(nand(f"z_{step}_{j}", inv, inv))
        level = next_level
        step += 1
    # El último AND ya es Z: crear alias en las salidas, sin puerta extra.
    zero = level[0]

    assert len(gates) == 134, len(gates)
    return {
        "name": "C28R_AULA8_RUTA_ARITMETICA_ADD_SUB_NAND",
        "status": "modelo_combinacional_educativo_no_isa_aprobada_no_hardware",
        "chapters": ["libro/capitulos/10_el_circuito_que_suma.md",
                     "libro/capitulos/11_la_unidad_aritmetico_logica.md"],
        "figures": ["libro/figuras/c10_fig02_sumador_completo.svg",
                    "libro/figuras/c10_fig04_cadena_y_dos_bytes.svg",
                    "libro/figuras/c11_fig01_resta_complemento_dos.svg",
                    "libro/figuras/c11_fig02_alu_selector.svg"],
        "inputs": [f"A{i}" for i in range(8)] + [f"B{i}" for i in range(8)] + ["SUB"],
        "gates": gates,
        "outputs": {
            "S": [f"S{i}" for i in range(8)], "C7": "C7", "Cout": "C8",
            "Cflag": "Cflag", "V": "V", "N": "S7", "Z": zero,
        },
        "limits": ["134 NAND sin retardos ni cargas eléctricas",
                   "solo ADD/SUB, no multiplexor completo de ALU",
                   "no política de flags para AND/OR/XOR/NOT",
                   "no reloj, registros, microcódigo ni CPU"]
    }


def render_verilog(spec: dict) -> str:
    inputs = spec["inputs"]
    gates = spec["gates"]
    lines = [
        "// C28-R: DERIVADO de netlists/alu8_addsub_134nand.json.",
        "// Ruta combinacional ADD/SUB de Aula-8, no chip ni CPU.",
        "// Editar scripts/c28r_generar_alu8_nand.py y regenerar; no editar a mano.",
        "module alu8_addsub_134nand(",
        "    input wire [7:0] A, B,",
        "    input wire SUB,",
        "    output wire [7:0] S,",
        "    output wire Cflag, V, N, Z, Cout",
        ");",
        "  wire " + ", ".join(g["name"] for g in gates
                                if g["name"] not in ("Cflag", "V")) + ";",
    ]
    mapping = {f"A{i}": f"A[{i}]" for i in range(8)}
    mapping.update({f"B{i}": f"B[{i}]" for i in range(8)})
    mapping["SUB"] = "SUB"
    for gate in gates:
        a, b = gate["inputs"]
        lines.append(f"  assign {gate['name']} = ~({mapping.get(a, a)} & {mapping.get(b, b)});")
    for i, name in enumerate(spec["outputs"]["S"]):
        lines.append(f"  assign S[{i}] = {name};")
    for target in ("Cflag", "V", "N", "Z", "Cout"):
        if spec["outputs"][target] != target:
            lines.append(f"  assign {target} = {spec['outputs'][target]};")
    return "\n".join(lines + ["endmodule", ""])


def main() -> None:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="regenerar netlist y RTL")
    mode.add_argument("--check", action="store_true", help="comprobar archivos derivados")
    args = ap.parse_args()
    spec = build()
    files = {
        NETLIST: json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
        RTL: render_verilog(spec),
    }
    if args.write:
        for path, value in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value, encoding="utf-8")
        print("C28-R: 134 NAND, netlist y HDL regenerados")
    else:
        for path, value in files.items():
            assert path.read_text(encoding="utf-8") == value, f"Archivo derivado no coincide: {path}"
        print("C28-R: netlist y HDL identicos a la fuente declarativa")


if __name__ == "__main__":
    main()
