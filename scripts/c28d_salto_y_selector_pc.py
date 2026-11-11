#!/usr/bin/env python3
"""Piloto C28-D: programa contiguo, dos rutas y selector PC de compuertas NAND.

El código de operación pertenece a la ISA *candidata* Aula-8. Las pruebas
simulan solo estas instrucciones en un modelo anfitrión, no una CPU/ROM real.
La lámina del selector se deriva de la misma lista de puertas comprobada.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import random
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "libro" / "figuras"
PILOT = ROOT / "c28_d" / "piloto_pc"
START = 0x6000
BYTES = (0x32, 0x09, 0x60, 0x11, 0x01, 0x07, 0x30, 0x0C, 0x60,
         0x11, 0x01, 0x09, 0x01)
ROLES = (
    "JNZ · opcode", "destino bajo", "destino alto",
    "LDI R1,7 · opcode", "registro R1", "inmediato 7",
    "JMP · opcode", "destino bajo", "destino alto",
    "LDI R1,9 · opcode", "registro R1", "inmediato 9",
    "HALT · opcode",
)


@dataclass(frozen=True)
class Gate:
    ident: str
    operation: str
    inputs: tuple[str, str]


def make_gates() -> list[Gate]:
    # Control y 16 celdas binarias. Toda puerta es NAND de dos entradas.
    gates = [
        Gate("NZ", "NAND", ("Z", "Z")),
        Gate("TAKE_N", "NAND", ("JNZ", "NZ")),
        Gate("TAKE", "NAND", ("TAKE_N", "TAKE_N")),
    ]
    for i in range(16):
        gates += [
            Gate(f"A{i}", "NAND", (f"SEQ{i}", "TAKE_N")),
            Gate(f"B{i}", "NAND", (f"TARGET{i}", "TAKE")),
            Gate(f"D{i}", "NAND", (f"A{i}", f"B{i}")),
        ]
    return gates


GATES = make_gates()


def netlist_eval(z: int, jnz: int, seq: int, target: int) -> tuple[int, int]:
    assert z in (0, 1) and jnz in (0, 1)
    assert 0 <= seq <= 0xFFFF and 0 <= target <= 0xFFFF
    values = {"Z": z, "JNZ": jnz}
    values.update({f"SEQ{i}": (seq >> i) & 1 for i in range(16)})
    values.update({f"TARGET{i}": (target >> i) & 1 for i in range(16)})
    for gate in GATES:
        a, b = (values[s] for s in gate.inputs)
        values[gate.ident] = 1 - (a & b)
    out = sum(values[f"D{i}"] << i for i in range(16))
    return out, values["TAKE"]


def run_program(z: int) -> dict:
    """Solo JNZ, JMP, LDI R1 y HALT; precondición explícita de Z conocida."""
    assert z in (0, 1)
    memory = {START + i: byte for i, byte in enumerate(BYTES)}
    pc, r1, trace, visited = START, None, [], set()
    for _ in range(8):
        assert pc not in visited, "Bucle inesperado en programa ilustrativo"
        visited.add(pc)
        opcode = memory[pc]
        if opcode in (0x32, 0x30):
            low, high = memory[pc + 1], memory[pc + 2]
            dest = low | (high << 8)
            pcseq = pc + 3
            is_jnz = opcode == 0x32
            next_pc, take = netlist_eval(z, int(is_jnz), pcseq, dest)
            if opcode == 0x30:  # JMP no pasa por el selector condicional JNZ.
                next_pc, take = dest, 1
            trace.append({"pc": pc, "opcode": opcode, "len": 3,
                          "next": next_pc, "taken": bool(take)})
            pc = next_pc
        elif opcode == 0x11:
            assert memory[pc + 1] == 0x01, "El ejemplo solo usa R1"
            r1 = memory[pc + 2]
            trace.append({"pc": pc, "opcode": opcode, "len": 3,
                          "next": pc + 3, "r1": r1})
            pc += 3
        elif opcode == 0x01:
            trace.append({"pc": pc, "opcode": opcode, "len": 1,
                          "next": pc + 1, "halt": True})
            pc += 1
            break
        else:
            raise AssertionError(f"Opcode inesperado 0x{opcode:02X} en {pc:04X}")
    assert trace[-1].get("halt") is True
    assert memory == {START + i: byte for i, byte in enumerate(BYTES)}
    return {"z": z, "r1": r1, "pc_final": pc, "trace": trace,
            "memory": memory}


def verify() -> None:
    assert len(GATES) == 51 and len({g.ident for g in GATES}) == 51
    # Verificación completa de los casos de UN carril de datos.
    for z in (0, 1):
        for jnz in (0, 1):
            for a in (0, 1):
                for b in (0, 1):
                    out, take = netlist_eval(z, jnz, a, b)
                    assert take == (jnz and not z)
                    assert out == (b if take else a)
    rng = random.Random(0xC28D)
    # Verificación multicarril con extremos, vectores y entradas aleatorias.
    samples = [(a, b) for a in (0, 1, 0xFFFF, 0x8000, 0x5555, 0xAAAA)
               for b in (0, 1, 0xFFFF, 0x8000, 0x5555, 0xAAAA)]
    samples += [(rng.randrange(0x10000), rng.randrange(0x10000))
                for _ in range(40_000)]
    checks = 0
    for a, b in samples:
        for z in (0, 1):
            for jnz in (0, 1):
                result, take = netlist_eval(z, jnz, a, b)
                assert result == (b if (jnz and not z) else a)
                assert take == int(jnz and not z)
                checks += 1
    z0, z1 = run_program(0), run_program(1)
    assert [x["pc"] for x in z0["trace"]] == [0x6000, 0x6009, 0x600C]
    assert [x["pc"] for x in z1["trace"]] == [0x6000, 0x6003, 0x6006, 0x600C]
    assert (z0["r1"], z1["r1"]) == (0x09, 0x07)
    assert z0["pc_final"] == z1["pc_final"] == 0x600D
    print(f"C28-D: {checks:,} comparaciones de selector NAND correctas")
    print("C28-D: 2 rutas del programa y 13 bytes contiguos correctos")


def esc(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def svg_text(x: int, y: int, value: str, size: int = 29,
             color: str = "#18344a", weight: str = "normal",
             anchor: str = "start") -> str:
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-family="DejaVu Sans" font-weight="{weight}" '
            f'text-anchor="{anchor}">{esc(value)}</text>')


def svg_base(width: int, height: int, content: list[str]) -> str:
    prefix = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
              f'height="{height}" viewBox="0 0 {width} {height}">')
    return "\n".join([prefix, '<rect width="100%" height="100%" fill="#fcfdfd"/>',
                      *content, "</svg>"])


def memory_map_svg(z: int) -> str:
    assert z in (0, 1)
    result = run_program(z)
    starts = [step["pc"] for step in result["trace"]]
    used = set()
    for step in result["trace"]:
        used.update(range(step["pc"], step["pc"] + step["len"]))
    c: list[str] = [
        svg_text(80, 78, f"La RAM es la misma; el PC elige otro camino · Z={z}", 42, weight="bold"),
        svg_text(80, 134, "13 direcciones de byte consecutivas · ISA Aula-8 candidata", 26, "#4d6373"),
        '<rect x="75" y="185" width="1335" height="960" rx="22" fill="#f2f6f8"/>',
        svg_text(122, 234, "Dirección", 25, weight="bold"),
        svg_text(395, 234, "Byte", 25, weight="bold"),
        svg_text(555, 234, "Función de ese byte", 25, weight="bold"),
        svg_text(1110, 234, "Recorrido del PC", 25, weight="bold"),
    ]
    y0, step_h = 262, 66
    for idx, byte in enumerate(BYTES):
        address = START + idx
        y = y0 + idx * step_h
        active = address in used
        back = "#dff2eb" if active else ("#e6eaf0" if idx % 2 else "#f9fafb")
        c.append(f'<rect x="102" y="{y}" width="906" height="{step_h - 4}" rx="7" fill="{back}"/>')
        if address in starts:
            c.append(f'<rect x="96" y="{y}" width="7" height="{step_h - 4}" fill="#15846b"/>')
        c.append(svg_text(130, y + 43, f"0x{address:04X}", 28, "#1d455c", "bold"))
        c.append(svg_text(398, y + 43, f"{byte:02X}", 30, "#18344a", "bold"))
        c.append(svg_text(548, y + 43, ROLES[idx], 25, "#273e4c" if active else "#71818d"))
        if address in starts:
            c.append(f'<circle cx="1037" cy="{y+30}" r="10" fill="#16836a"/>')
    for step in result["trace"][:-1]:
        fr, to = step["pc"] - START, step["next"] - START
        ay, by = y0 + fr * step_h + 30, y0 + to * step_h + 30
        # Las flechas son flujo del PC. No son conexiones eléctricas.
        c.append(f'<path d="M1047 {ay} H1150 V{by} H1049" fill="none" '
                 'stroke="#136d85" stroke-width="5" stroke-linecap="round"/>')
        c.append(f'<path d="M1051 {by-9} L1034 {by} L1051 {by+9} Z" fill="#136d85"/>')
        if fr == 0:
            caption = "JNZ sí" if z == 0 else "JNZ no"
        elif step["opcode"] == 0x30:
            caption = "JMP"
        else:
            caption = "siguiente"
        c.append(svg_text(1184, (ay + by) // 2 + 9, caption, 24, "#136d85", "bold"))
    c.append('<rect x="80" y="1167" width="1320" height="152" rx="13" fill="#e5eef3"/>')
    c.append(svg_text(115, 1215, f"Resultado hipotético: R1=0x{result['r1']:02X}; PC al leer HALT termina en 0x600D.", 29, weight="bold"))
    c.append(svg_text(115, 1263, "Las filas grises siguen almacenadas: saltar NO borra ni mueve bytes.", 25))
    c.append(svg_text(115, 1300, "Flecha = cambio de PC; los conductores eléctricos se representan aparte.", 21, "#536778"))
    return svg_base(1480, 1350, c)


def gate_svg(ident: str, x: int, y: int, inputs: tuple[str, str]) -> list[str]:
    # Símbolo IEC pedagógico: rectángulo '&' con burbuja de inversión a la salida.
    out = [f'<rect x="{x}" y="{y}" width="182" height="124" rx="11" '
           'fill="#fff9e9" stroke="#ba8744" stroke-width="3"/>',
           svg_text(x + 91, y + 79, "&", 51, "#5f4a28", "bold", "middle"),
           f'<circle cx="{x+193}" cy="{y+62}" r="11" fill="#fcfdfd" '
           'stroke="#ba8744" stroke-width="3"/>',
           svg_text(x + 88, y - 16, ident, 24, weight="bold", anchor="middle")]
    for i, sig in enumerate(inputs):
        iy = y + (40 if i == 0 else 88)
        out.append(f'<line x1="{x-72}" y1="{iy}" x2="{x}" y2="{iy}" '
                   'stroke="#426179" stroke-width="4"/>')
        out.append(svg_text(x - 78, iy - 10, sig, 21, "#426179", anchor="end"))
    return out


def circuit_svg() -> str:
    assert {g.ident for g in GATES}.issuperset({"NZ", "TAKE_N", "TAKE", "A0", "B0", "D0"})
    lookup = {g.ident: g for g in GATES}
    c = [svg_text(65, 78, "Decidir el próximo PC mediante puertas NAND", 42, weight="bold"),
         svg_text(65, 128, "Selector de salto JNZ · una de las 16 celdas de datos", 27, "#4c6373"),
         '<rect x="65" y="175" width="1630" height="310" rx="18" fill="#eaf3f8"/>',
         svg_text(100, 222, "Control compartido por los 16 bits", 27, weight="bold")]
    for ident, x in (("NZ", 280), ("TAKE_N", 800), ("TAKE", 1320)):
        c.extend(gate_svg(ident, x, 284, lookup[ident].inputs))
    c.append(svg_text(120, 463, "Z=0 y JNZ=1 → TAKE=1; cualquier otro caso → TAKE=0", 26))
    c.append('<rect x="65" y="512" width="1630" height="455" rx="18" fill="#f2f8f4"/>')
    c.append(svg_text(100, 557, "Una celda de selección, repetida 16 veces (i = 0…15)", 27, weight="bold"))
    for ident, x, y in (("A0", 300, 627), ("B0", 300, 797), ("D0", 1180, 713)):
        c.extend(gate_svg(ident.replace("0", "i"), x, y,
                          tuple(s.replace("0", "[i]") if s in ("SEQ0", "TARGET0") else
                                s.replace("0", "_i") if s in ("A0", "B0") else s
                                for s in lookup[ident].inputs)))
    c.append('<path d="M504 689 H930 V753 H1108" fill="none" stroke="#326f85" stroke-width="4"/>')
    c.append('<path d="M504 859 H984 V801 H1108" fill="none" stroke="#326f85" stroke-width="4"/>')
    c.append(svg_text(598, 674, "A_i", 22, "#326f85"))
    c.append(svg_text(598, 843, "B_i", 22, "#326f85"))
    c.append('<path d="M1384 775 H1580" stroke="#326f85" stroke-width="5"/>')
    c.append(svg_text(1604, 768, "D[i]", 23, "#326f85", "bold", "end"))
    c.append(svg_text(82, 1036, "Las etiquetas TAKE y TAKE_N conectan redes con el mismo nombre.", 26))
    c.append(svg_text(82, 1080, "La burbuja en cada salida indica inversión: todas las puertas son NAND.", 26))
    c.append(svg_text(82, 1132, "D[i] es la entrada candidata del PC; todavía falta el registro, LOAD y el reloj.", 25, "#516677"))
    return svg_base(1760, 1180, c)


def write_assets() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PILOT.mkdir(parents=True, exist_ok=True)
    names = {
        "c28d_ram_jnz_z0": memory_map_svg(0),
        "c28d_ram_jnz_z1": memory_map_svg(1),
        "c28d_selector_pc_nand": circuit_svg(),
    }
    for stem, content in names.items():
        (OUT / f"{stem}.svg").write_text(content, encoding="utf-8")
    (PILOT / "netlist_selector_pc_nand.json").write_text(
        json.dumps({"status": "piloto combinacional; no PC completo",
                    "ports": ["Z", "JNZ", "SEQ[15:0]", "TARGET[15:0]"],
                    "outputs": ["TAKE", "D[15:0]"],
                    "gates": [asdict(g) for g in GATES]}, indent=2), encoding="utf-8")
    (PILOT / "trazas_salto.json").write_text(
        json.dumps({"status": "trazas en anfitrión, ISA candidata",
                    "code_start": "0x6000", "bytes_hex": [f"{b:02X}" for b in BYTES],
                    "z0": run_program(0), "z1": run_program(1)}, indent=2), encoding="utf-8")
    inkscape = shutil.which("inkscape")
    if inkscape:
        for stem in names:
            subprocess.run([inkscape, str(OUT / f"{stem}.svg"),
                            f"--export-filename={OUT / (stem + '.png')}"],
                           check=True, capture_output=True)
    else:
        print("Inkscape no presente: SVG generados; PNG preexistentes se conservan.")
    print("Tres láminas C28-D generadas desde los datos comprobados")


if __name__ == "__main__":
    verify()
    write_assets()
