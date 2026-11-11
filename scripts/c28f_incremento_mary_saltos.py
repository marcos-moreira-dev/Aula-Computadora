#!/usr/bin/env python3
"""C28-F: incremento del PC, dos clases de salto y direccion de MAR.

Piloto combinacional reproducible con puertas NAND y registros ideales del
piloto C28-E. No aprueba un incrementador dedicado ni un cronograma de CPU.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import random
import shutil
import subprocess

from c28d_salto_y_selector_pc import BYTES, START
from c28e_pc16_prueba import PC16

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "libro" / "figuras"
PILOT = ROOT / "c28_f" / "piloto_pc_mar"


@dataclass(frozen=True)
class Gate:
    name: str
    kind: str
    inputs: tuple[str, str]


def create_network() -> list[Gate]:
    g: list[Gate] = [Gate("INC0", "NAND", ("PC0", "PC0"))]
    # C_1 = PC_0. Para i>=1, XOR con cuatro NAND y carry con una
    # NAND adicional que invierte T_i. C_16 no hace falta.
    for i in range(1, 16):
        a, b = f"PC{i}", "PC0" if i == 1 else f"C{i}"
        g.extend([
            Gate(f"T{i}", "NAND", (a, b)),
            Gate(f"U{i}", "NAND", (a, f"T{i}")),
            Gate(f"V{i}", "NAND", (b, f"T{i}")),
            Gate(f"INC{i}", "NAND", (f"U{i}", f"V{i}")),
        ])
        if i < 15:
            g.append(Gate(f"C{i+1}", "NAND", (f"T{i}", f"T{i}")))
    g.extend([
        Gate("ZN", "NAND", ("Z", "Z")),
        Gate("JNZ_N", "NAND", ("JNZ", "ZN")),
        Gate("JMP_N", "NAND", ("JMP", "JMP")),
        Gate("TAKE", "NAND", ("JNZ_N", "JMP_N")),
        Gate("TAKE_N", "NAND", ("TAKE", "TAKE")),
    ])
    for i in range(16):
        g.extend([
            Gate(f"SA{i}", "NAND", (f"INC{i}", "TAKE_N")),
            Gate(f"SB{i}", "NAND", (f"TARGET{i}", "TAKE")),
            Gate(f"PC_D{i}", "NAND", (f"SA{i}", f"SB{i}")),
        ])
    g.append(Gate("FETCH_N", "NAND", ("FETCH", "FETCH")))
    for i in range(16):
        g.extend([
            Gate(f"MA{i}", "NAND", (f"PC{i}", "FETCH")),
            Gate(f"MB{i}", "NAND", (f"DATA_ADDR{i}", "FETCH_N")),
            Gate(f"MAR_D{i}", "NAND", (f"MA{i}", f"MB{i}")),
        ])
    return g


GATES = create_network()
INC_GATES, SELECT_GATES, MAR_GATES = 75, 53, 49


def evaluate(pc: int, target: int, data_addr: int, z: int,
             jmp: int, jnz: int, fetch: int) -> dict:
    assert 0 <= pc <= 0xFFFF and 0 <= target <= 0xFFFF
    assert 0 <= data_addr <= 0xFFFF
    assert z in (0, 1) and jmp in (0, 1) and jnz in (0, 1) and fetch in (0, 1)
    if jmp and jnz:
        raise ValueError("Control inválido: JMP y JNZ simultáneos")
    wires = {"Z": z, "JMP": jmp, "JNZ": jnz, "FETCH": fetch}
    for i in range(16):
        wires[f"PC{i}"] = (pc >> i) & 1
        wires[f"TARGET{i}"] = (target >> i) & 1
        wires[f"DATA_ADDR{i}"] = (data_addr >> i) & 1
    for gate in GATES:
        a, b = (wires[name] for name in gate.inputs)
        wires[gate.name] = 1 - (a & b)
    word = lambda prefix: sum(wires[f"{prefix}{i}"] << i for i in range(16))
    return {
        "pc_inc": word("INC"),
        "take": wires["TAKE"],
        "pc_d": word("PC_D"),
        "mar_d": word("MAR_D"),
    }


def expected(pc: int, target: int, data_addr: int, z: int,
             jmp: int, jnz: int, fetch: int) -> dict:
    take = int(bool(jmp or (jnz and not z)))
    inc = (pc + 1) & 0xFFFF
    return {
        "pc_inc": inc,
        "take": take,
        "pc_d": target if take else inc,
        "mar_d": pc if fetch else data_addr,
    }


@dataclass
class IdealBus:
    pc: PC16
    mar: PC16
    events: list[dict]

    @classmethod
    def create(cls, entry: int):
        pc, mar = PC16(), PC16()
        pc.drive(1, 1, 0, entry)
        return cls(pc, mar, [])

    def step(self, label: str, pc_load: int = 1, mar_load: int = 1,
             fetch: int = 1, data_addr: int = 0, target: int = 0,
             jmp: int = 0, jnz: int = 0, z: int = 0) -> dict:
        before_pc, before_mar = self.pc.q, self.mar.q
        assert isinstance(before_pc, int)
        # Una sola instantánea de PC_Q alimenta ambas entradas D ANTES del
        # flanco. Las dos capturas ideales suceden en el mismo instante.
        c = evaluate(before_pc, target, data_addr, z, jmp, jnz, fetch)
        self.pc.drive(0, 0, 0, 0)
        self.mar.drive(0, 0, 0, 0)
        after_mar = self.mar.drive(1, mar_load, 0, c["mar_d"])
        after_pc = self.pc.drive(1, pc_load, 0, c["pc_d"])
        assert after_pc == (c["pc_d"] if pc_load else before_pc)
        assert after_mar == (c["mar_d"] if mar_load else before_mar)
        row = {
            "accion": label, "pc_antes": before_pc, "mar_antes": before_mar,
            "pc_d": c["pc_d"], "mar_d": c["mar_d"], "pc_despues": after_pc,
            "mar_despues": after_mar, "fetch": fetch, "pc_load": pc_load,
            "mar_load": mar_load, "jmp": jmp, "jnz": jnz, "z": z,
            "target": target, "data_addr": data_addr,
        }
        self.events.append(row)
        return row


def program_route(z: int) -> dict:
    """Solo direcciones y bytes seleccionados; decodificación de anfitrión."""
    assert z in (0, 1)
    ram = {START + i: value for i, value in enumerate(BYTES)}
    bus = IdealBus.create(START)
    fetched: list[dict] = []

    def fetch_n(count: int):
        for _ in range(count):
            row = bus.step("FETCH", fetch=1)
            addr = row["mar_despues"]
            assert addr == row["pc_antes"] and addr in ram
            fetched.append({"direccion": addr, "byte": ram[addr],
                            "pc_despues": row["pc_despues"],
                            "mar_despues": addr})

    fetch_n(3)  # JNZ opcode + los dos bytes de destino.
    assert [x["direccion"] for x in fetched] == [0x6000, 0x6001, 0x6002]
    assert ram[0x6000] == 0x32
    assert ram[0x6001] | (ram[0x6002] << 8) == 0x6009
    # Si Z=1 NO se toma JNZ: PC ya apunta a 6003 tras los operandos.
    # Por ello control desactiva PC_LOAD. Capturar el INC en este punto
    # saltaría accidentalmente el opcode siguiente.
    bus.step("JNZ (tras operandos)", pc_load=1-z, mar_load=0,
             fetch=1, target=0x6009, jnz=1, z=z)
    if z == 0:
        assert bus.pc.q == 0x6009
        fetch_n(3)  # LDI R1,9.
    else:
        assert bus.pc.q == 0x6003
        fetch_n(3)  # LDI R1,7.
        fetch_n(3)  # JMP 0x600C.
        assert ram[0x6006] == 0x30
        bus.step("JMP (tras operandos)", 1, 0, 1, target=0x600C, jmp=1)
    fetch_n(1)  # HALT.
    assert fetched[-1]["direccion"] == 0x600C
    assert bus.pc.q == 0x600D and bus.mar.q == 0x600C
    assert {START + i: value for i, value in enumerate(BYTES)} == ram
    return {"z": z, "eventos": bus.events, "lecturas": fetched,
            "pc_final": bus.pc.q, "mar_final": bus.mar.q}


def verify() -> int:
    assert len(GATES) == INC_GATES + SELECT_GATES + MAR_GATES == 177
    assert len({g.name for g in GATES}) == len(GATES)
    rng = random.Random(0xC28F)
    checked = 0
    # Barrido exhaustivo del sumador de incremento, incluso el wrap 0xFFFF.
    for pc in range(0x10000):
        result = evaluate(pc, 0, 0, 0, 0, 0, 1)
        assert result["pc_inc"] == (pc + 1) & 0xFFFF
        checked += 1
    controls = [(0, 0, 0), (0, 0, 1), (0, 1, 0),
                (0, 1, 1), (1, 0, 0), (1, 0, 1)]
    for _ in range(8_000):
        pc, target, data_addr = (rng.randrange(0x10000) for _ in range(3))
        for jmp, jnz, z in controls:
            for fetch in (0, 1):
                out = evaluate(pc, target, data_addr, z, jmp, jnz, fetch)
                assert out == expected(pc, target, data_addr, z, jmp, jnz, fetch)
                checked += 1
    try:
        evaluate(0, 0, 0, 0, 1, 1, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("JMP+JNZ debe ser rechazado")
    for z in (0, 1):
        program_route(z)
    # Cuando MAR recibe datos, PC puede permanecer apuntando al código.
    bus = IdealBus.create(0x6007)
    step = bus.step("MAR para ST", pc_load=0, mar_load=1,
                    fetch=0, data_addr=0x6F00)
    assert (step["pc_despues"], step["mar_despues"]) == (0x6007, 0x6F00)
    checked += 1
    print(f"C28-F: {checked:,} comparaciones de redes NAND correctas")
    print("Dos recorridos de 13 bytes: MAR usa PC anterior; PC avanza o salta.")
    print("177 NAND combinacionales candidatas; no hay HDL ejecutado ni CPU real.")
    return checked


def text(x: int, y: int, content: str, size: int = 30, bold: bool = False,
         color: str = "#173b4d", anchor: str = "start") -> str:
    import html
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-family="DejaVu Sans" font-weight="{"bold" if bold else "normal"}" '
            f'text-anchor="{anchor}">{html.escape(content)}</text>')


def rect(x: int, y: int, w: int, h: int, bg: str) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{bg}"/>'


def art(content: list[str], w: int = 1760, h: int = 1060) -> str:
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fdfdfb"/>', *content, "</svg>"
    ])


def incremental_svg() -> str:
    """Diagrama compacto: una celda XOR NAND y el acarreo de 16 bits."""
    assert [g.name for g in GATES[:5]] == ["INC0", "T1", "U1", "V1", "INC1"]
    c = [
        text(72, 80, "Incrementar el PC es una suma binaria de uno", 41, True),
        text(72, 132, "El acarreo se propaga entre bits; la salida no modifica FLAGS.", 26, color="#58727d"),
        rect(72, 176, 1616, 302, "#edf4f8"),
        text(110, 219, "Cadena de 16 bits: el acarreo avanza desde el bit 0", 30, True),
    ]
    for i, x in enumerate((132, 454, 776, 1098, 1420)):
        label = ("bit 0", "bit 1", "bit 2", "…", "bit 15")[i]
        c.append(rect(x, 277, 220, 125, "#dff1e8" if i < 3 else "#e6edf7"))
        c.append(text(x+110, 315, label, 29, True, anchor="middle"))
        c.append(text(x+110, 358, "XOR + carry" if i not in (0, 3) else
                      ("NOT PC0" if i == 0 else "propaga"), 22, anchor="middle"))
        if i < 4:
            c.append(f'<path d="M{x+220} 337 H{x+320}" stroke="#287489" stroke-width="5"/>')
    c.append(text(108, 449, "C1=PC0   ·   C2=PC1·C1   ·   ...   ·   INC[i]=PC[i] XOR C[i]", 26))
    c.extend([
        rect(72, 515, 1616, 446, "#f4f8f5"),
        text(112, 563, "Un bit i>0: XOR realizado con NAND, y acarreo siguiente", 28, True),
    ])
    # Estas ecuaciones corresponden literalmente a los nombres de GATES.
    rows = [
        ("T_i", "NAND(PC[i], C_i)", "Negación del AND"),
        ("U_i", "NAND(PC[i], T_i)", "Rama del XOR"),
        ("V_i", "NAND(C_i, T_i)", "Segunda rama del XOR"),
        ("INC[i]", "NAND(U_i, V_i)", "Bit incrementado"),
        ("C_(i+1)", "NAND(T_i, T_i)", "Acarreo para el bit siguiente"),
    ]
    for i, (label, formula, meaning) in enumerate(rows):
        y = 625 + 62*i
        c.append(rect(104, y-35, 1532, 55, "#e7eff4" if i%2==0 else "#fbfcfd"))
        c.append(text(142, y, label, 27, True))
        c.append(text(420, y, formula, 27))
        c.append(text(1070, y, meaning, 25, color="#486577"))
    c.extend([
        text(108, 945, "Bit 0: INC0 = NOT PC0, C1 = PC0. En bit 15 ya no hace falta C16.", 25),
        text(108, 1016, "75 NAND para PC+1; el desbordamiento FFFF→0000 se prueba sin tocar C visible.", 26, True),
    ])
    return art(c, 1760, 1080)


def route_svg(route0: dict, route1: dict) -> str:
    c = [
        text(72, 82, "MAR mira la dirección anterior; PC puede avanzar", 40, True),
        text(72, 131, "Dos registros ideales capturan a la vez; lo siguiente no equivale a ciclos de CPU.", 25, color="#59717c"),
        rect(70, 179, 1620, 780, "#edf4f8"),
    ]
    xcols = (105, 310, 560, 860, 1190)
    for x, name in zip(xcols, ("Evento", "PC antes", "MAR después", "PC después", "Lectura o decisión")):
        c.append(text(x, 239, name, 27, True))
    samples: list[tuple[str,dict]] = []
    for z, route in ((0,route0), (1,route1)):
        taken = route["eventos"]
        samples.append((f"Z={z} · FETCH", taken[0]))
        samples.append((f"Z={z} · FETCH", taken[1]))
        samples.append((f"Z={z} · FETCH", taken[2]))
        samples.append((f"Z={z} · JNZ", taken[3]))
        if z == 1:
            samples.append(("Z=1 · JMP", next(x for x in taken if x["accion"].startswith("JMP"))))
    for i, (label,row) in enumerate(samples):
        y=268+i*74
        c.append(rect(91,y,1575,65, "#dff2e9" if row["accion"]=="FETCH" else "#fff2de"))
        c.append(text(115,y+42,label,24,True))
        c.append(text(327,y+42,f"0x{row['pc_antes']:04X}",26))
        mar = "HOLD" if not row["mar_load"] else f"0x{row['mar_despues']:04X}"
        c.append(text(576,y+42,mar,26))
        c.append(text(867,y+42,f"0x{row['pc_despues']:04X}",26,True))
        c.append(text(1190,y+42,"leer byte" if row["accion"]=="FETCH" else
                      ("JNZ según Z" if label.endswith("JNZ") else "JMP absoluto"),24))
    c.append(text(101,1012,"FETCH: MAR ← PC_Q anterior; PC_Q ← PC_Q+1, en un mismo flanco ideal.",27,True))
    return art(c,1760,1080)


def verilog_from_gates() -> str:
    """Genera el bloque combinacional HDL desde exactamente GATES."""
    pins = {"Z": "z", "JMP": "jmp", "JNZ": "jnz", "FETCH": "fetch"}

    def signal(name: str) -> str:
        if name in pins:
            return pins[name]
        for prefix, port in (
            ("PC", "pc_q"), ("TARGET", "target"),
            ("DATA_ADDR", "data_addr"),
        ):
            tail = name[len(prefix):] if name.startswith(prefix) else ""
            if tail.isdigit():
                return f"{port}[{int(tail)}]"
        return name.lower()

    lines = [
        "// Generado desde las 177 NAND de c28f_incremento_mary_saltos.py.",
        "// COMBINACIONAL: no representa flancos, memoria ni CPU completa.",
        "module pc_mar_c28f(",
        "    input wire [15:0] pc_q, target, data_addr,",
        "    input wire z, jmp, jnz, fetch,",
        "    output wire [15:0] pc_inc, pc_d, mar_d,",
        "    output wire take",
        ");",
    ]
    lines.extend(f"  wire {gate.name.lower()};" for gate in GATES)
    for gate in GATES:
        a, b = (signal(n) for n in gate.inputs)
        lines.append(f"  assign {gate.name.lower()} = ~({a} & {b});")
    for prefix, port in (("INC", "pc_inc"), ("PC_D", "pc_d"), ("MAR_D", "mar_d")):
        for i in range(16):
            lines.append(f"  assign {port}[{i}] = {prefix.lower()}{i};")
    lines.extend(["  assign take = take;",
                  "endmodule"])
    # Evitar asignación circular: la señal TAKE calculada por NAND es el
    # puerto de salida del mismo nombre. No se redeclara como wire interno.
    lines = [line for line in lines if line not in ("  wire take;", "  assign take = take;")]
    return "\n".join(lines) + "\n"


def testbench_verilog() -> str:
    """Pruebas deterministas y pseudoaleatorias del bloque combinacional."""
    return """// Ejecutar con Icarus Verilog. No verificado en esta edición.
module tb_pc_mar_c28f;
  reg [15:0] pc_q, target, data_addr;
  reg z, jmp, jnz, fetch;
  wire [15:0] pc_inc, pc_d, mar_d;
  wire take;
  integer k;
  reg expected_take;
  pc_mar_c28f dut(
    .pc_q(pc_q), .target(target), .data_addr(data_addr),
    .z(z), .jmp(jmp), .jnz(jnz), .fetch(fetch),
    .pc_inc(pc_inc), .pc_d(pc_d), .mar_d(mar_d), .take(take)
  );
  task check;
    begin
      expected_take = jmp | (jnz & ~z);
      #1;
      if (pc_inc !== ((pc_q + 16'd1) & 16'hffff))
        $fatal(1, "Incremento incorrecto PC=%h", pc_q);
      if (take !== expected_take)
        $fatal(1, "Selector TAKE incorrecto");
      if (pc_d !== (expected_take ? target : (pc_q + 16'd1)))
        $fatal(1, "PC_D incorrecto");
      if (mar_d !== (fetch ? pc_q : data_addr))
        $fatal(1, "MAR_D incorrecto");
    end
  endtask
  initial begin
    pc_q=0; target=0; data_addr=0; z=0; jmp=0; jnz=0; fetch=1;
    for (k=0; k<65536; k=k+1) begin
      pc_q=k; check();
    end
    pc_q=16'h60ff; target=16'h6009; data_addr=16'h6f00;
    for (k=0; k<8000; k=k+1) begin
      pc_q=$random; target=$random; data_addr=$random;
      z=k%2; jmp=(k/2)%2; jnz=(k/4)%2;
      if (jmp && jnz) jnz=0;
      fetch=(k/8)%2;
      check();
    end
    $display("C28-F HDL combinacional: comprobaciones correctas");
    $finish;
  end
endmodule
"""


def save() -> None:
    FIG.mkdir(parents=True,exist_ok=True)
    PILOT.mkdir(parents=True,exist_ok=True)
    routes = {str(z): program_route(z) for z in (0,1)}
    (PILOT/"netlist_pc_mar.json").write_text(json.dumps({
        "candidate":True, "gate_count":len(GATES),
        "increment_nand":INC_GATES, "branch_nand":SELECT_GATES,
        "mar_nand":MAR_GATES, "no_flags_side_effect":True,
        "control_constraint":"JMP and JNZ may not both be asserted",
        "gates":[asdict(g) for g in GATES],
    },indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (PILOT/"trazas_pc_mar.json").write_text(
        json.dumps(routes,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (PILOT/"pc_mar_c28f.v").write_text(verilog_from_gates(),encoding="utf-8")
    (PILOT/"tb_pc_mar_c28f.v").write_text(testbench_verilog(),encoding="utf-8")
    drawings = {
        "c28f_incremento_pc":incremental_svg(),
        "c28f_pc_mar_dos_rutas":route_svg(routes["0"],routes["1"]),
    }
    for name,s in drawings.items():
        (FIG/f"{name}.svg").write_text(s,encoding="utf-8")
        if shutil.which("inkscape"):
            subprocess.run(["inkscape",str(FIG/f"{name}.svg"),
                            f"--export-filename={FIG/(name+'.png')}",
                            "--export-width=1800"],check=True,capture_output=True)
        elif not (FIG/f"{name}.png").exists():
            raise RuntimeError("Falta Inkscape para generar PNG nuevos")
    print("C28-F: dos láminas SVG/PNG y netlist/trazas JSON generados.")


if __name__=="__main__":
    verify()
    save()
