#!/usr/bin/env python3
"""C28-E: banco PC16 educativo con CLEAR sincronico, LOAD y HOLD.

La red de 82 NAND calcula entradas D. Dieciseis DFF ideales capturan en
flanco ascendente. CLEAR_TEST no equivale al RESET de la CPU desde ROM.
No hay retardo fisico, setup/hold, buses electricos ni CPU implementada.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import random
import subprocess
import shutil

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "libro" / "figuras"
PILOT = ROOT / "c28_e" / "piloto_pc16"


@dataclass(frozen=True)
class Gate:
    name: str
    kind: str
    inputs: tuple[str, str]


def make_gates() -> list[Gate]:
    # Dos inversores de control compartidos + cinco NAND por cada bit.
    gates = [
        Gate("LOAD_N", "NAND", ("LOAD", "LOAD")),
        Gate("CLR_N", "NAND", ("CLR_TEST", "CLR_TEST")),
    ]
    for i in range(16):
        gates.extend([
            Gate(f"A{i}", "NAND", (f"Q{i}", "LOAD_N")),
            Gate(f"B{i}", "NAND", (f"NEXT{i}", "LOAD")),
            Gate(f"M{i}", "NAND", (f"A{i}", f"B{i}")),
            Gate(f"N{i}", "NAND", (f"M{i}", "CLR_N")),
            Gate(f"D{i}", "NAND", (f"N{i}", f"N{i}")),
        ])
    return gates


GATES = make_gates()


def nand3(a: int | None, b: int | None) -> int | None:
    """NAND 0/1/X ideal: un 0 conocido domina; None significa X."""
    if a == 0 or b == 0:
        return 1
    if a == b == 1:
        return 0
    return None


def network_d(q: int | None, next_pc: int, load: int, clear: int) -> int | None:
    assert q is None or 0 <= q <= 0xFFFF
    assert 0 <= next_pc <= 0xFFFF and load in (0, 1) and clear in (0, 1)
    wires: dict[str, int | None] = {"LOAD": load, "CLR_TEST": clear}
    for i in range(16):
        wires[f"Q{i}"] = None if q is None else (q >> i) & 1
        wires[f"NEXT{i}"] = (next_pc >> i) & 1
    for gate in GATES:
        wires[gate.name] = nand3(wires[gate.inputs[0]], wires[gate.inputs[1]])
    bits = [wires[f"D{i}"] for i in range(16)]
    return None if any(bit is None for bit in bits) else sum(bit << i for i, bit in enumerate(bits))


def oracle_d(q: int | None, next_pc: int, load: int, clear: int) -> int | None:
    """Especificacion independiente de la estructura NAND."""
    if clear:
        return 0
    if load:
        return next_pc
    return q


@dataclass
class PC16:
    q: int | None = None
    old_clk: int = 0

    def drive(self, clk: int, load: int, clear: int, next_pc: int) -> int | None:
        assert clk in (0, 1)
        if self.old_clk == 0 and clk == 1:
            self.q = network_d(self.q, next_pc, load, clear)
        self.old_clk = clk
        return self.q


SCHEDULE = (
    (0, 0, 0, 0x1111, "Encender: Q desconocido"),
    (1, 0, 0, 0x1111, "HOLD en flanco: sigue X"),
    (1, 1, 0, 0x6000, "LOAD sin nuevo flanco: sigue X"),
    (0, 1, 0, 0x6000, "CLK baja: sigue X"),
    (1, 1, 0, 0x6000, "Flanco: cargar 6000"),
    (0, 0, 0, 0x6003, "Dato cambia; Q no"),
    (1, 0, 0, 0x6003, "HOLD en flanco"),
    (0, 1, 0, 0x6009, "Preparar destino JNZ"),
    (1, 1, 0, 0x6009, "Flanco: cargar 6009"),
    (1, 1, 1, 0x7777, "CLEAR con CLK alto; esperar"),
    (0, 1, 1, 0x7777, "CLK baja: Q no cambia"),
    (1, 1, 1, 0x7777, "CLEAR gana ante LOAD"),
)


def timeline() -> list[dict]:
    unit = PC16()
    out = []
    for i, (clk, load, clear, data, meaning) in enumerate(SCHEDULE):
        prevclk, prevq = unit.old_clk, unit.q
        now = unit.drive(clk, load, clear, data)
        out.append({"step": i, "clk": clk, "edge": "↑" if prevclk == 0 and clk == 1
                    else "↓" if prevclk == 1 and clk == 0 else "—",
                    "load": load, "clear_test": clear, "next": data, "q": now,
                    "meaning": meaning, "previous_q": prevq})
    assert [x["q"] for x in out] == [
        None, None, None, None, 0x6000, 0x6000, 0x6000,
        0x6000, 0x6009, 0x6009, 0x6009, 0,
    ]
    return out


def verify() -> int:
    assert len(GATES) == 82 and len({g.name for g in GATES}) == 82
    tests = 0
    corners = (0, 1, 0xFFFF, 0x8000, 0x5555, 0xAAAA)
    rng = random.Random(0xC28E)
    inputs = [(a, b) for a in corners for b in corners]
    inputs.extend((rng.randrange(65536), rng.randrange(65536)) for _ in range(20_000))
    for q, next_pc in inputs:
        for load in (0, 1):
            for clear in (0, 1):
                assert network_d(q, next_pc, load, clear) == oracle_d(q, next_pc, load, clear)
                tests += 1
    for load in (0, 1):
        for clear in (0, 1):
            for next_pc in corners:
                assert network_d(None, next_pc, load, clear) == oracle_d(None, next_pc, load, clear)
                tests += 1
    # Cada secuencia verifica flancos, ausencia de flancos, retencion y
    # prioridad con una maquina-oraculo independiente de la netlist.
    for _ in range(2_000):
        unit = PC16()
        expected: int | None = None
        old_clk = 0
        for _ in range(15):
            clk, load, clear = (rng.randrange(2) for _ in range(3))
            next_pc = rng.randrange(65536)
            if old_clk == 0 and clk == 1:
                expected = oracle_d(expected, next_pc, load, clear)
            old_clk = clk
            assert unit.drive(clk, load, clear, next_pc) == expected
            tests += 1
    timeline()
    # La salida de C28-D se convierte en ENTRADA del PC: la red no escribe
    # Q hasta que LOAD y un flanco ascendente coinciden.
    from c28d_salto_y_selector_pc import netlist_eval
    for z, target in ((0, 0x6009), (1, 0x6003)):
        value, take = netlist_eval(z, 1, 0x6003, 0x6009)
        assert (value, take) == (target, int(z == 0))
        unit = PC16()
        assert unit.drive(1, 1, 0, 0x6000) == 0x6000
        assert unit.drive(1, 1, 0, value) == 0x6000  # CLK sigue alto.
        assert unit.drive(0, 1, 0, value) == 0x6000
        assert unit.drive(1, 1, 0, value) == target
        tests += 4
    print(f"PC16 C28-E: {tests:,} comparaciones lógicas y de flanco correctas")
    print("Red de 82 NAND + 16 DFF ideales, con estado inicial X.")
    print("CLR_TEST síncrono de laboratorio; NO es el RESET de Aula-8.")
    return tests


def txt(x: int, y: int, s: str, n: int = 26, color: str = "#153a4e",
        bold: bool = False, anchor: str = "start") -> str:
    import html
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{n}" '
            f'font-family="DejaVu Sans" font-weight="{"bold" if bold else "normal"}" '
            f'text-anchor="{anchor}">{html.escape(s)}</text>')


def box(x: int, y: int, w: int, h: int, fill: str, radius: int = 15) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"/>'


def svg(w: int, h: int, content: list[str]) -> str:
    return "\n".join([f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" '
                      f'height="{h}" viewBox="0 0 {w} {h}">',
                      '<rect width="100%" height="100%" fill="#fdfdfc"/>',
                      *content, "</svg>"])


def nand_symbol(x: int, y: int, name: str, in1: str, in2: str,
                w: int = 155, h: int = 98) -> list[str]:
    items = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
        'fill="#fff8e8" stroke="#ae803f" stroke-width="3"/>',
        txt(x + w // 2, y + 66, "&", 49, "#684f27", True, "middle"),
        f'<circle cx="{x+w+10}" cy="{y+h//2}" r="10" '
        'fill="#fdfdfc" stroke="#ae803f" stroke-width="3"/>',
        txt(x + w // 2, y - 13, name, 25, bold=True, anchor="middle"),
    ]
    for i, signal in enumerate((in1, in2)):
        iy = y + (31 if i == 0 else 70)
        items.extend([
            f'<path d="M{x-54} {iy} H{x}" stroke="#2d687d" stroke-width="4"/>',
            txt(x-62, iy-9, signal, 20, "#2d687d", anchor="end"),
        ])
    return items


def architecture_svg() -> str:
    assert [g.name for g in GATES[:2]] == ["LOAD_N", "CLR_N"]
    c = [
        txt(80, 91, "El PC guarda una dirección; no cambia cuando cambia su entrada", 39, bold=True),
        txt(80, 147, "PC16 · banco de 16 DFF de flanco ascendente · circuito candidato de laboratorio", 25, "#587080"),
        box(76, 182, 1740, 388, "#edf4f8"),
        txt(117, 232, "Vista de los dieciséis bits", 29, bold=True),
        box(480, 284, 540, 178, "#e3f0ec"),
        txt(750, 341, "RED COMBINACIONAL", 31, bold=True, anchor="middle"),
        txt(750, 387, "82 NAND · LOAD / CLR_TEST", 27, anchor="middle"),
        txt(750, 430, "D = ¬CLR_TEST · MUX(LOAD, Q, NEXT)", 23, anchor="middle"),
        box(1190, 284, 348, 178, "#dfe8f6"),
        txt(1364, 345, "16 × DFF", 35, bold=True, anchor="middle"),
        txt(1364, 394, "capturan solo en CLK ↑", 23, anchor="middle"),
        '<path d="M116 315 H470" stroke="#247d91" stroke-width="6"/>',
        txt(116, 284, "PC_NEXT[15:0]", 27, bold=True),
        '<path d="M1020 363 H1180" stroke="#247d91" stroke-width="6"/>',
        txt(1098, 335, "D[15:0]", 23, anchor="middle"),
        '<path d="M1538 363 H1762" stroke="#247d91" stroke-width="6"/>',
        txt(1556, 330, "PC_Q[15:0]", 26, bold=True),
        '<path d="M1658 363 V510 H360 V437 H470" fill="none" stroke="#1b8b79" stroke-width="5"/>',
        txt(490, 537, "Realimentación Q hacia la función HOLD", 23, "#1b806f"),
        '<path d="M736 475 V462" stroke="#b78a3e" stroke-width="5"/>',
        txt(736, 501, "LOAD · CLR_TEST", 22, anchor="middle"),
        '<path d="M1364 514 V465" stroke="#b78a3e" stroke-width="5"/>',
        txt(1364, 542, "CLK ↑", 24, anchor="middle"),
        box(76, 602, 1740, 660, "#f4f8f5"),
        txt(116, 649, "Detalle de una celda i (las etiquetas de red conectan señales iguales)", 27, bold=True),
    ]
    # La topología de esta celda procede de GATES; no hay una segunda
    # representación con puertas o entradas definidas a mano.
    lookup = {g.name: g for g in GATES}
    specs = (("A0", 306, 743), ("B0", 306, 931),
             ("M0", 734, 830), ("N0", 1172, 830), ("D0", 1530, 830))
    for name, x, y in specs:
        gate = lookup[name]
        names = []
        for signal in gate.inputs:
            if signal in ("Q0", "NEXT0"):
                names.append(signal[:-1] + "[i]")
            elif signal.endswith("0"):
                names.append(signal[:-1] + "_i")
            else:
                names.append(signal)
        c.extend(nand_symbol(x, y, name.replace("0", "_i"), names[0], names[1]))
    c.extend([
        '<path d="M471 792 H620 V861 H680" stroke="#35768a" stroke-width="4" fill="none"/>',
        '<path d="M471 980 H645 V900 H680" stroke="#35768a" stroke-width="4" fill="none"/>',
        txt(518, 778, "A_i", 21), txt(526, 967, "B_i", 21),
        '<path d="M899 879 H1028 V861 H1118" stroke="#35768a" stroke-width="4" fill="none"/>',
        '<path d="M1337 879 H1410 V861 H1476 M1410 879 V900 H1476" '
        'stroke="#35768a" stroke-width="4" fill="none"/>',
        '<circle cx="1410" cy="879" r="6" fill="#35768a"/>',
        '<path d="M1695 879 H1780" stroke="#35768a" stroke-width="5"/>',
        txt(1778, 851, "D[i]", 23, bold=True, anchor="end"),
        txt(120, 1128, "LOAD_N = NAND(LOAD, LOAD)   ·   CLR_N = NAND(CLR_TEST, CLR_TEST)", 27),
        txt(120, 1179, "Se repiten cinco NAND por bit: 2 compartidas + 5 × 16 = 82 NAND.", 27, bold=True),
        txt(120, 1228, "No dibuja el interior de los DFF, ni RESET físico, retardos o bus externo.", 23, "#596f7d"),
    ])
    return svg(1900, 1310, c)


def event_svg(events: list[dict]) -> str:
    c = [
        txt(80, 85, "Un flanco cambia el PC; las otras variaciones no", 39, bold=True),
        txt(80, 135, "Secuencia comprobada · CLR_TEST se captura en el mismo flanco que LOAD", 25, "#566f80"),
        box(74, 180, 1750, 864, "#f1f5f8"),
    ]
    headers = [(112, "Paso"), (265, "CLK"), (415, "Flanco"),
               (580, "LOAD"), (760, "CLR_TEST"), (1020, "PC_NEXT"),
               (1270, "PC_Q"), (1480, "Qué sucede")]
    for x, h in headers:
        c.append(txt(x, 239, h, 24, bold=True))
    for i, row in enumerate(events):
        y = 260 + i * 63
        fill = "#dff2e9" if row["edge"] == "↑" else ("#fff4de" if row["clear_test"] else
               ("#e9eef3" if i % 2 == 0 else "#f9fafb"))
        c.append(box(92, y, 1710, 57, fill, 6))
        vals = [
            (120, str(row["step"])),
            (278, str(row["clk"])),
            (445, row["edge"]),
            (612, str(row["load"])),
            (800, str(row["clear_test"])),
            (1050, f"0x{row['next']:04X}"),
            (1290, "X" if row["q"] is None else f"0x{row['q']:04X}"),
        ]
        for x, value in vals:
            c.append(txt(x, y + 37, value, 23, bold=(x==1290)))
        c.append(txt(1494, y + 37, row["meaning"], 19))
    c.extend([
        txt(92, 1102, "Las filas verdes contienen un flanco ascendente: solo ahí se captura D.", 27),
        txt(92, 1150, "Aunque CLR_TEST suba en un reloj ya alto, Q no cambia hasta el siguiente ↑.", 25),
        txt(92, 1200, "El cero final es una limpieza de prueba; el RESET real debe buscar el vector de ROM.", 24, "#526c7d"),
    ])
    return svg(1900, 1260, c)


def verilog_from_gates() -> str:
    """Emite el módulo HDL desde exactamente GATES, sin redefinir la red."""
    def signal(name: str) -> str:
        if name == "LOAD":
            return "load"
        if name == "CLR_TEST":
            return "clr_test"
        if name.startswith("NEXT") and name[4:].isdigit():
            return f"next_pc[{int(name[4:])}]"
        if name.startswith("Q") and name[1:].isdigit():
            return f"q[{int(name[1:])}]"
        return name.lower()

    lines = [
        "// Generado por scripts/c28e_pc16_prueba.py, NO verificado con Icarus.",
        "// CLR_TEST es un borrado sincrono para el piloto, NO reset CPU.",
        "module pc16_c28e(",
        "    input wire clk, load, clr_test,",
        "    input wire [15:0] next_pc,",
        "    output reg [15:0] q",
        ");",
    ]
    lines.extend(f"  wire {gate.name.lower()};" for gate in GATES)
    for gate in GATES:
        a, b = (signal(name) for name in gate.inputs)
        lines.append(f"  assign {gate.name.lower()} = ~({a} & {b});")
    d_bus = ", ".join(f"d{i}" for i in reversed(range(16)))
    lines.extend([f"  wire [15:0] d = {{{d_bus}}};",
                  "  always @(posedge clk) begin",
                  "    q <= d;",
                  "  end",
                  "endmodule"])
    return "\n".join(lines) + "\n"


def testbench_from_events(events: list[dict]) -> str:
    lines = [
        "// Tabla de flancos generada desde el mismo calendario Python.",
        "module tb_pc16_c28e;",
        "  reg clk, load, clr_test;",
        "  reg [15:0] next_pc;",
        "  wire [15:0] q;",
        "  pc16_c28e dut (.clk(clk), .load(load), .clr_test(clr_test),",
        "                  .next_pc(next_pc), .q(q));",
        "  initial begin",
        "    clk=0; load=0; clr_test=0; next_pc=16'h1111;",
        "    #1;",
    ]
    for event in events:
        want = "xxxx" if event["q"] is None else f"{event['q']:04x}"
        lines.extend([
            f"    // Paso {event['step']}: {event['meaning']}",
            f"    load=1'b{event['load']}; clr_test=1'b{event['clear_test']}; "
            f"next_pc=16'h{event['next']:04x};",
            "    #4;",
            f"    clk=1'b{event['clk']}; #1;",
            f"    if (q !== 16'h{want}) $fatal(1, \"Fallo paso {event['step']}\");",
        ])
    lines.extend(["    $display(\"PC16 C28-E: trazas HDL correctas\");",
                  "    $finish;",
                  "  end",
                  "endmodule"])
    return "\n".join(lines) + "\n"


def save_artifacts() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    PILOT.mkdir(parents=True, exist_ok=True)
    events = timeline()
    (PILOT / "pc16_contrato_y_netlist.json").write_text(
        json.dumps({
            "name": "PC16_C28E", "data_bits": 16, "initial": "X",
            "clock_edge": "rising", "clear_test": "synchronous, active-high, priority",
            "load": "synchronous, active-high", "otherwise": "HOLD",
            "cpu_reset_vector": "NOT IMPLEMENTED; distinct from CLR_TEST",
            "gates": [asdict(g) for g in GATES], "flipflops": 16,
            "formula": "D_i = (!CLR_TEST) & ((LOAD & NEXT_i) | (!LOAD & Q_i))",
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (PILOT / "pc16_eventos.json").write_text(
        json.dumps(events, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (PILOT / "pc16_c28e.v").write_text(verilog_from_gates(), encoding="utf-8")
    (PILOT / "tb_pc16_c28e.v").write_text(testbench_from_events(events), encoding="utf-8")
    artwork = {
        "c28e_pc16_red_y_dff": architecture_svg(),
        "c28e_pc16_flancos": event_svg(events),
    }
    for name, data in artwork.items():
        (FIG / f"{name}.svg").write_text(data, encoding="utf-8")
        if shutil.which("inkscape"):
            subprocess.run(["inkscape", str(FIG / f"{name}.svg"),
                            f"--export-filename={FIG / (name + '.png')}",
                            "--export-width=1800"], check=True, capture_output=True)
        elif not (FIG / f"{name}.png").exists():
            raise RuntimeError("Falta Inkscape para generar PNG nuevos")
    print("C28-E: dos láminas SVG/PNG y contrato/netlist JSON generados.")


if __name__ == "__main__":
    verify()
    save_artifacts()
