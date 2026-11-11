#!/usr/bin/env python3
"""C28-R: interpreta la topología NAND serializada de ADD/SUB, no hardware."""

from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET

import c28r_generar_alu8_nand as generator


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "c28_r/netlists/alu8_addsub_134nand.json"
RESULT = ROOT / "c28_r/auditoria/C28_R_RESULTADOS.json"


def signed8(value: int) -> int:
    return value if value < 128 else value - 256


def verify_documents(spec: dict) -> dict:
    c10, c11 = ((ROOT / p).read_text(encoding="utf-8") for p in spec["chapters"])
    for formula in ("S = P ⊕ Cin", "Cout = G ∨ (P ∧ Cin)", "V = C7 ⊕ C8"):
        assert formula in c10, formula
    for formula in ("A − B ≡ A + (¬B) + 1", "B' = B ⊕", "C en SUB = préstamo"):
        assert formula in c11, formula
    checks = {
        "c10_sumador_completo": (spec["figures"][0], ("Medio sumador 1", "Medio sumador 2", "Cout")),
        "c10_cadena": (spec["figures"][1], ("C0", "C8")),
        "c11_add_sub": (spec["figures"][2], ("SUB=0", "SUB=1", "Cin=SUB", "Cout interno")),
        "c11_selector": (spec["figures"][3], ("ADD / SUB", "AND OR XOR NOT", "MUX")),
    }
    for name, (file, labels) in checks.items():
        svg = ET.parse(ROOT / file).getroot()
        assert svg.tag.endswith("svg"), name
        text = " ".join(t.strip() for t in svg.itertext())
        for label in labels:
            assert label in text, (name, label)
    tb = (ROOT / "c28_r/rtl/tb_alu8_addsub_134nand.v").read_text(encoding="utf-8")
    assert "131072 vectores" in tb and "$fatal(1," in tb
    return {"figuras_funcionales_cotejadas_por_rotulos": len(checks),
            "capitulos_con_ecuaciones_cotejadas": 2}


def compile_serialized_netlist(spec: dict) -> tuple[list[tuple[int, int]], dict[str, int]]:
    assert spec["status"] == "modelo_combinacional_educativo_no_isa_aprobada_no_hardware"
    assert spec["inputs"] == [f"A{i}" for i in range(8)] + [f"B{i}" for i in range(8)] + ["SUB"]
    indices = {name: i for i, name in enumerate(spec["inputs"])}
    network = []
    for gate in spec["gates"]:
        assert gate["op"] == "NAND"
        assert gate["name"] not in indices
        assert len(gate["inputs"]) == 2
        a, b = gate["inputs"]
        assert a in indices and b in indices, gate
        network.append((indices[a], indices[b]))
        indices[gate["name"]] = len(indices)
    assert len(network) == 134, len(network)
    assert all(name in indices for name in spec["outputs"]["S"])
    assert all(name in indices for name in (spec["outputs"][k]
               for k in ("C7", "Cout", "Cflag", "V", "N", "Z")))
    return network, indices


def verify() -> dict:
    # Esta igualdad falla ante una modificación accidental del Verilog o JSON,
    # pero la referencia de cálculo inferior NO ejecuta el generador.
    spec = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert spec == generator.build(), "Netlist almacenado difiere de la fuente declarativa"
    assert (ROOT / "c28_r/rtl/alu8_addsub_134nand.v").read_text(encoding="utf-8") == generator.render_verilog(spec)
    documents = verify_documents(spec)
    gates, indices = compile_serialized_netlist(spec)
    offset = len(spec["inputs"])
    values = [0] * (offset + len(gates))
    outs = spec["outputs"]
    sum_ids = [indices[name] for name in outs["S"]]
    flag_ids = {name: indices[outs[name]] for name in ("C7", "Cout", "Cflag", "V", "N", "Z")}
    examples = {}
    flag_counts = {"ADD_C": 0, "SUB_prestamo": 0, "ADD_V": 0, "SUB_V": 0}

    # 131.072 pares: cada resultado se calcula recorriendo LAS 134 NAND de
    # la lista guardada. No se utiliza la fórmula del generador como árbitro.
    for sub in (0, 1):
        for a in range(256):
            for b in range(256):
                for bit in range(8):
                    values[bit] = (a >> bit) & 1
                    values[8 + bit] = (b >> bit) & 1
                values[16] = sub
                for j, (u, v) in enumerate(gates):
                    values[offset + j] = 1 - (values[u] & values[v])
                s = sum(values[ix] << bit for bit, ix in enumerate(sum_ids))
                c7 = values[flag_ids["C7"]]
                cout = values[flag_ids["Cout"]]
                cflag = values[flag_ids["Cflag"]]
                ov = values[flag_ids["V"]]
                n, z = values[flag_ids["N"]], values[flag_ids["Z"]]
                modified_b = b ^ (255 if sub else 0)
                total = a + modified_b + sub
                expected_s = total & 255
                expected_cout = total >> 8
                expected_c7 = ((a & 127) + (modified_b & 127) + sub) >> 7
                signed_total = signed8(a) + (-signed8(b) if sub else signed8(b))
                expected_v = int(not (-128 <= signed_total <= 127))
                expected_c = expected_cout ^ sub
                assert (s, c7, cout, cflag, ov, n, z) == (
                    expected_s, expected_c7, expected_cout, expected_c,
                    expected_v, expected_s >> 7, int(expected_s == 0)), (sub, a, b)
                if cflag:
                    flag_counts["SUB_prestamo" if sub else "ADD_C"] += 1
                if ov:
                    flag_counts["SUB_V" if sub else "ADD_V"] += 1
                if (a, b) in ((13, 9), (9, 13), (127, 1), (128, 1), (250, 10)):
                    examples[f"{'SUB' if sub else 'ADD'}_{a}_{b}"] = {
                        "resultado": f"{s:02X}", "C": cflag, "V": ov,
                        "Z": z, "N": n,
                    }

    assert examples["ADD_13_9"] == {"resultado": "16", "C": 0, "V": 0, "Z": 0, "N": 0}
    assert examples["SUB_13_9"] == {"resultado": "04", "C": 0, "V": 0, "Z": 0, "N": 0}
    assert examples["SUB_9_13"] == {"resultado": "FC", "C": 1, "V": 0, "Z": 0, "N": 1}
    assert examples["SUB_128_1"] == {"resultado": "7F", "C": 0, "V": 1, "Z": 0, "N": 0}
    assert examples["ADD_127_1"] == {"resultado": "80", "C": 0, "V": 1, "Z": 0, "N": 1}
    return {
        "etapa": "C28-R / 8 bits ADD-SUB desde netlist NAND serializado",
        "gates_NAND": len(gates), "vectores_ADD": 65536, "vectores_SUB": 65536,
        "resultados": examples, "cuentas_flags_activadas": flag_counts,
        "cotejo_editorial": documents,
        "hdl_icarus": "PENDIENTE_WINDOWS",
        "limites": spec["limits"] + ["SVG cotejados solo a nivel de rotulos, no rutas electricas"],
    }


def main() -> None:
    result = verify()
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("C28-R: 134 NAND serializadas, 131.072 vectores ADD/SUB correctos")
    print("C28-R: C7/Cout, C préstamo-acarreo, V, Z y N cotejadas")
    print("RESULTADO_C28R_MODELO_APROBADO; HDL_PENDIENTE_WINDOWS")


if __name__ == "__main__":
    main()
