#!/usr/bin/env python3
"""C28-Q: evalúa netlists NAND serializadas y localiza sus dibujos/RTL.

Audita conexiones lógicas escritas y ciertos trazos SVG identificados, no
continuidad eléctrica real ni funcionamiento físico de un procesador.
"""

from __future__ import annotations

import json
from pathlib import Path
import random
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "c28_q" / "auditoria" / "C28_Q_RESULTADOS.json"
MATRIX = ROOT / "libro" / "MATRIZ_CIRCUITOS_C28Q.md"


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def read_md(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def ordered_gates(gates: list[dict], primary_inputs: set[str],
                  name_field: str, op_field: str,
                  allow_feedback: bool = False) -> None:
    """Comprueba nombres, operaciones, referencias y DAG si corresponde."""
    names = [gate[name_field] for gate in gates]
    assert len(names) == len(set(names)), "Nombre de NAND duplicado"
    assert all(gate[op_field] == "NAND" for gate in gates)
    assert all(len(gate["inputs"]) == 2 for gate in gates)
    allowed = primary_inputs | (set(names) if allow_feedback else set())
    for gate in gates:
        assert gate[name_field] not in primary_inputs
        assert all(name in allowed for name in gate["inputs"]), gate
        allowed.add(gate[name_field])


def combinational(gates: list[dict], inputs: dict[str, int],
                  name_field: str) -> dict[str, int]:
    values = dict(inputs)
    for gate in gates:
        a, b = (values[name] for name in gate["inputs"])
        assert a in (0, 1) and b in (0, 1)
        values[gate[name_field]] = 1 - (a & b)
    return values


def svg_components(path: str) -> tuple[str, list[str]]:
    root = ET.parse(ROOT / path).getroot()
    assert root.tag.endswith("svg")
    strings = " ".join(x.strip() for x in root.itertext() if x.strip())
    routes = [el.attrib["d"] for el in root.iter()
              if el.tag.endswith("path") and "d" in el.attrib]
    return strings, routes


def verify_foundations() -> dict:
    doc = read_json("c28_q/netlists/fundamentos_nand.json")
    assert doc["status"] == "contratos_para_auditoria_no_hardware_fabricado"
    xor, latch = doc["circuits"]
    assert xor["id"] == "C04_XOR_4NAND" and latch["id"] == "C05_SR_LATCH_2NAND"
    ordered_gates(xor["gates"], {"A", "B"}, "name", "operation")
    ordered_gates(latch["gates"], {"S_n", "R_n"}, "name", "operation",
                  allow_feedback=True)
    assert [g["name"] for g in xor["gates"]] == ["N1", "N2", "N3", "D"]
    assert [g["name"] for g in latch["gates"]] == ["Q", "Q_n"]
    chapter4 = read_md(xor["source_chapter"])
    chapter5 = read_md(latch["source_chapter"])
    for formula in ("N1 = NAND(A, B)", "N2 = NAND(A, N1)",
                    "N3 = NAND(B, N1)", "D = NAND(N2, N3)"):
        assert formula in chapter4
    xor_table = {
        (0, 0): (1, 1, 1, 0),
        (0, 1): (1, 1, 0, 1),
        (1, 0): (1, 0, 1, 1),
        (1, 1): (0, 1, 1, 0),
    }
    for (a, b), expected in xor_table.items():
        wires = combinational(xor["gates"], {"A": a, "B": b}, "name")
        assert tuple(wires[x] for x in ("N1", "N2", "N3", "D")) == expected
        assert wires["D"] == (a ^ b)
    assert "| 00 | 1 | 1, 1 | 0 |" in chapter4
    assert "| 11 | 0 | 1, 1 | 0 |" in chapter4

    # Latch SR: las dos entradas cruzadas son referencias de estado; en
    # el caso 00 solo modelamos el estado prohibido. NO prometemos la
    # resolución física al liberar ambas órdenes de manera simultánea.
    def settle(q: int, qn: int, sn: int, rn: int) -> tuple[int, int]:
        for _ in range(12):
            following = (1 - (sn & qn), 1 - (rn & q))
            if following == (q, qn):
                return following
            q, qn = following
        raise AssertionError("Transición no alcanza estado fijo")

    sr_checks = 0
    for initial in ((1, 0), (0, 1)):
        for sn, rn, expected in (
            (1, 1, initial), (0, 1, (1, 0)),
            (1, 0, (0, 1)), (0, 0, (1, 1))
        ):
            assert settle(*initial, sn, rn) == expected
            sr_checks += 1
    q, qn = 0, 1
    for sn, rn, result in ((1, 1, 0), (0, 1, 1), (1, 1, 1),
                           (1, 0, 0), (1, 1, 0)):
        q, qn = settle(q, qn, sn, rn)
        assert (q, qn) == (result, 1 - result)
        sr_checks += 1
    assert "entrada prohibida" in chapter5.lower()

    # Los trazos SVG identificados son recorridos revisados a escala.
    # Son indicios de conectividad gráfica, NO extracción de una netlist
    # mediante un EDA ni continuidad eléctrica medida.
    xor_labels, xor_paths = svg_components(xor["figure"])
    sr_labels, sr_paths = svg_components(latch["figure"])
    assert all(name in xor_labels for name in ("N1", "N2", "N3", "N4", "D"))
    assert all(name in sr_labels for name in ("S_n", "R_n", "Q_n", "NAND 1", "NAND 2"))
    assert any("M337,230 H423 V196 H530 M423,230 V307 H530" in d
               for d in xor_paths), "No aparece ramificación N1 hacia N2/N3"
    assert any("M506,205 H617 V316 H670" in d for d in sr_paths), "Falta retorno Q a NAND2"
    assert any("M903,329 V456 H234 V230 H330" in d for d in sr_paths), "Falta retorno Q_n a NAND1"
    # Cotejo de la asignacion interna de pines descrita en la leccion.
    # No valida montaje, encapsulado comprado ni pistas de una placa.
    for pin, signal in (("1 (1A)", "S_n"), ("2 (1B)", "Q_n"),
                        ("3 (1Y)", "Q"), ("4 (2A)", "R_n"),
                        ("5 (2B)", "Q"), ("6 (2Y)", "Q_n"),
                        ("7", "GND"), ("14", "VCC")):
        assert f"| {signal} | {pin} |" in chapter5
    pin_labels, _ = svg_components("libro/figuras/c05_fig05_sn74hct00_patillaje.svg")
    assert all(label in pin_labels for label in
               ("1A", "1B", "1Y", "2A", "2B", "2Y", "GND", "VCC"))
    return {"xor_vectores": 4, "latch_estados_ideales": sr_checks,
            "rutas_svg_identificadas": 3, "pines_latch_cotejados": 8,
            "netlists_basicas": 2}


def verify_selector_d() -> dict:
    doc = read_json("c28_d/piloto_pc/netlist_selector_pc_nand.json")
    gates = doc["gates"]
    inputs = {"Z", "JNZ"} | {f"{prefix}{bit}" for prefix in ("SEQ", "TARGET")
                            for bit in range(16)}
    ordered_gates(gates, inputs, "ident", "operation")
    assert len(gates) == 51 and [g["ident"] for g in gates[:3]] == [
        "NZ", "TAKE_N", "TAKE"]
    assert all(f"D{i}" in {g["ident"] for g in gates} for i in range(16))
    rng = random.Random(0xC28D)
    samples = [(a, b) for a in (0, 1, 0x7FFF, 0x8000, 0xFFFF, 0x5555)
               for b in (0, 1, 0x7FFF, 0x8000, 0xFFFF, 0x5555)]
    samples += [(rng.randrange(65536), rng.randrange(65536)) for _ in range(2048)]
    checks = 0
    for seq, target in samples:
        for z in (0, 1):
            for jnz in (0, 1):
                signals = {"Z": z, "JNZ": jnz}
                for i in range(16):
                    signals[f"SEQ{i}"] = (seq >> i) & 1
                    signals[f"TARGET{i}"] = (target >> i) & 1
                result = combinational(gates, signals, "ident")
                output = sum(result[f"D{i}"] << i for i in range(16))
                taken = int(bool(jnz and not z))
                assert result["TAKE"] == taken
                assert output == (target if taken else seq)
                checks += 1
    assert (ROOT / "libro/figuras/c28d_selector_pc_nand.svg").is_file()
    return {"NAND": 51, "comparaciones": checks, "tipo": "combinacional"}


def verify_pc_mar_f() -> dict:
    doc = read_json("c28_f/piloto_pc_mar/netlist_pc_mar.json")
    gates = doc["gates"]
    primary = {"Z", "JMP", "JNZ", "FETCH"}
    primary.update(f"{kind}{bit}" for kind in ("PC", "TARGET", "DATA_ADDR")
                   for bit in range(16))
    ordered_gates(gates, primary, "name", "kind")
    assert (len(gates), doc["gate_count"], doc["increment_nand"],
            doc["branch_nand"], doc["mar_nand"]) == (177, 177, 75, 53, 49)

    def evaluate(pc: int, target: int, data: int, z: int,
                 jmp: int, jnz: int, fetch: int) -> dict:
        wires = {"Z": z, "JMP": jmp, "JNZ": jnz, "FETCH": fetch}
        for i in range(16):
            wires[f"PC{i}"] = (pc >> i) & 1
            wires[f"TARGET{i}"] = (target >> i) & 1
            wires[f"DATA_ADDR{i}"] = (data >> i) & 1
        out = combinational(gates, wires, "name")
        word = lambda name: sum(out[f"{name}{i}"] << i for i in range(16))
        return {"inc": word("INC"), "take": out["TAKE"],
                "pc_d": word("PC_D"), "mar_d": word("MAR_D")}

    count = 0
    for pc in list(range(4096)) + list(range(61440, 65536)):
        actual = evaluate(pc, 0, 0, 0, 0, 0, 1)
        assert actual == {"inc": (pc + 1) & 0xFFFF, "take": 0,
                          "pc_d": (pc + 1) & 0xFFFF, "mar_d": pc}
        count += 1
    rng = random.Random(0xC28F)
    controls = ((0, 0, 0), (0, 0, 1), (0, 1, 0),
                (0, 1, 1), (1, 0, 0), (1, 0, 1))
    for _ in range(2048):
        pc, target, data = (rng.randrange(65536) for _ in range(3))
        for jmp, jnz, z in controls:
            take = int(bool(jmp or (jnz and not z)))
            for fetch in (0, 1):
                actual = evaluate(pc, target, data, z, jmp, jnz, fetch)
                assert actual == {
                    "inc": (pc + 1) & 0xFFFF,
                    "take": take,
                    "pc_d": target if take else (pc + 1) & 0xFFFF,
                    "mar_d": pc if fetch else data,
                }
                count += 1
    assert all((ROOT / f"libro/figuras/{name}.svg").is_file()
               for name in ("c28f_incremento_pc", "c28f_pc_mar_dos_rutas"))
    return {"NAND": 177, "comparaciones": count,
            "tipo": "combinacional; no controla el reloj ni el bus fisico"}


def verify_register_and_hdl_sources() -> dict:
    contract = read_json("c28_a/piloto_registro8/registro8_contrato.json")
    assert contract["anchura_bits"] == contract["celdas"] == 8
    assert contract["sin_reset_implicitamente"] is True
    rtl = read_md("c28_a/piloto_registro8/registro8.v")
    assert "always @(posedge CLK)" in rtl
    assert "if (LOAD)" in rtl and "q <= IN;" in rtl
    assert "8'bzzzzzzzz" in rtl
    tb = read_md("c28_a/piloto_registro8/tb_registro8.v")
    assert "module tb_registro8;" in tb and "$fatal(1)" in tb
    pc_rtl = read_md("c28_e/piloto_pc16/pc16_c28e.v")
    pc_tb = read_md("c28_e/piloto_pc16/tb_pc16_c28e.v")
    assert "module pc16_c28e(" in pc_rtl
    assert "output reg [15:0] q" in pc_rtl
    assert "always @(posedge clk)" in pc_rtl
    assert "module tb_pc16_c28e;" in pc_tb and "$fatal(1," in pc_tb
    return {"registro8_estructura": "coherente_con_contrato",
            "pc16_fuentes": "presentes",
            "simulacion_icarus": "PENDIENTE_EN_WINDOWS_NUEVA_SUITE"}


def write_matrix() -> None:
    rows = [
        ("03–04", "NAND/NOT/AND/OR/XOR", "c04_fig03_xor_cuatro_nand",
         "C28-Q red de 4 NAND + tablas", "Cuatro puertas; sin pinout fisico"),
        ("05", "Latch SR", "c05_fig02_latch_nand_cruzado",
         "C28-Q feedback NAND + tabla", "Estado invalido y metastabilidad sin resolver"),
        ("06", "Latch D/flip-flop", "c06_fig03_flancos_y_capturas",
         "C28-L modelo por flancos", "Sin RTL de célula ni setup/hold"),
        ("07", "Registro de ocho bits", "c07_fig05_registro_aula8",
         "C28-A RTL + nuevo testbench Icarus", "Sin pines/silicona; figura funcional"),
        ("10", "Sumador de 8 bits", "c10_fig03_suma_trece_mas_nueve",
         "C28-M sumador por acarreo propagado", "Sin netlist HDL del sumador"),
        ("11", "ALU ADD/SUB", "c11_fig02_alu_selector",
         "C28-M operaciones y flags", "MUX/ALU fisicos sin verificar"),
        ("12–13", "Selector PC/MAR", "c28f_pc_mar_dos_rutas",
         "C28-Q 177 NAND JSON + HDL C28-F previo", "No CPU integrada ni rutas de control"),
        ("14–16", "Selección salto", "c28d_selector_pc_nand",
         "C28-Q 51 NAND JSON + C28-D previo", "No microsecuencia CALL/RET"),
        ("13–15", "Lectura secuencial", "c28g_lectura_con_espera",
         "C28-H HDL de dos politicas, Windows aprobado", "PC no elegido; no SRAM real"),
        ("22", "Carriles de Aula-16", "c22_fig05_dos_bancos_aula16",
         "C28-P mapa y alineacion", "Sin arbitraje de bus 16 bits implementado"),
    ]
    lines = [
        "# C28-Q · Matriz entre circuitos, figuras y evidencia",
        "",
        "**Uso:** localizar la prueba y la fuente concreta de cada modulo. El",
        "estado de un modelo, un netlist digital, un RTL y una ilustracion",
        "no son intercambiables. Las figuras son funcionales salvo que una",
        "fuente indique expresamente otro nivel.",
        "",
        "| Cap. | Circuito o bloque | Figura 2D | Evidencia existente | Límite |",
        "| --- | --- | --- | --- | --- |",
    ]
    for cap, block, fig, evidence, limit in rows:
        assert (ROOT / f"libro/figuras/{fig}.svg").is_file()
        lines.append(f"| {cap} | {block} | `{fig}` | {evidence} | {limit} |")
    lines += [
        "",
        "**Niveles de evidencia actuales:** las redes de 4/2 NAND, 51 NAND",
        "y 177 NAND se compararon con sus tablas o formulas desde listas de",
        "conexiones; el RTL de registro8 y PC16 solo tiene **pruebas nuevas",
        "pendientes en Windows** hasta recibir la proxima retroalimentacion.",
        "Los HDL C28-F/H ya pasaron en la ronda anterior. Ninguna verificacion",
        "certifica continuidad de cables, retardo, voltajes, seleccion de chips,",
        "firmware ni una CPU completa.",
    ]
    MATRIX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    foundational = verify_foundations()
    selector = verify_selector_d()
    pc_mar = verify_pc_mar_f()
    sources = verify_register_and_hdl_sources()
    write_matrix()
    report = {
        "etapa": "C28-Q / auditoria de netlists serializados y trazabilidad",
        "fundamentos": foundational, "selector_C28D": selector,
        "pc_mar_C28F": pc_mar, "fuentes_hdl": sources,
        "controles_nuevos_previstos": [
            "LIBRO_C28Q_NETLIST_Y_FIGURAS",
            "HDL_C28_A_REGISTRO8_COMPILACION", "HDL_C28_A_REGISTRO8_SIMULACION",
            "HDL_C28_E_PC16_COMPILACION", "HDL_C28_E_PC16_SIMULACION"
        ],
        "limitaciones": [
            "Un netlist digital correcto no equivale a un esquema electrico fabricable",
            "Las rutas SVG comprobadas son recorridos identificados, no EDA",
            "El latch invalido no tiene estado final garantizado al liberar entradas",
            "RTL de registro8/PC16 aun debe pasar nuevas pruebas en Windows",
            "No se ha implementado CPU, firmware ni arbitraje fisico del bus",
            "El maestro Word/PDF continua siendo C28-G",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f'C28-Q: XOR {foundational["xor_vectores"]} vectores, latch '
          f'{foundational["latch_estados_ideales"]} estados ideales.')
    print(f'C28-D JSON: {selector["NAND"]} NAND, '
          f'{selector["comparaciones"]:,} combinaciones.')
    print(f'C28-F JSON: {pc_mar["NAND"]} NAND, '
          f'{pc_mar["comparaciones"]:,} combinaciones.')
    print("RESULTADO_C28Q_APROBADO_MODELOS; HDL_A_E_PENDIENTE_WINDOWS")


if __name__ == "__main__":
    main()
