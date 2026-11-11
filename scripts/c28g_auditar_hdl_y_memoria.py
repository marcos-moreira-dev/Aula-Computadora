#!/usr/bin/env python3
"""C28-G: lee el HDL emitido y pilota MAR/MDR/RD con esperas abstractas.

NO es Icarus Verilog: interpreta solo las asignaciones NAND y de salida de
nuestro modulo combinacional. La lectura de memoria tiene flancos ideales,
sin describir latencia fisica, pin READY o micro-ROM ejecutable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import random
import re
import shutil
import subprocess

from c28d_salto_y_selector_pc import BYTES, START
from c28f_incremento_mary_saltos import IdealBus, PILOT as F_PILOT, expected, art, rect, text

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "c28_g" / "piloto_lectura"
FIG = ROOT / "libro" / "figuras"
HDL = F_PILOT / "pc_mar_c28f.v"

NAND_RE = re.compile(r"assign\s+(\w+)\s*=\s*~\(\s*([\w\[\]]+)\s*&\s*([\w\[\]]+)\s*\)\s*;")
ALIAS_RE = re.compile(r"assign\s+((?:pc_inc|pc_d|mar_d)\[\d+\])\s*=\s*(\w+)\s*;")
INPUT_RE = re.compile(r"^(pc_q|target|data_addr)\[(\d+)\]$")


def read_hdl_assignments() -> tuple[list[tuple[str, str, str]], dict[str, str]]:
    """Analiza una gramatica limitada; aborta si el archivo cambia de forma."""
    source = HDL.read_text(encoding="utf-8")
    assert "module pc_mar_c28f(" in source and source.rstrip().endswith("endmodule")
    gates = NAND_RE.findall(source)
    aliases = dict(ALIAS_RE.findall(source))
    assert len(gates) == 177, f"Se esperaban 177 NAND, llegaron {len(gates)}"
    assert len({g[0] for g in gates}) == len(gates)
    assert len(aliases) == 48
    assert set(aliases) == {
        f"{prefix}[{i}]" for prefix in ("pc_inc", "pc_d", "mar_d")
        for i in range(16)
    }
    assert re.search(r"assign\s+take\s*=\s*~\(", source)
    assert source.count("assign ") == 177 + 48
    return gates, aliases


def interpret_hdl(gates: list[tuple[str, str, str]], aliases: dict[str, str],
                  pc: int, target: int, data_addr: int,
                  z: int, jmp: int, jnz: int, fetch: int) -> dict:
    """Interprete independiente de las asignaciones Verilog de este subconjunto."""
    values = {"z": z, "jmp": jmp, "jnz": jnz, "fetch": fetch}
    for prefix, number in (("pc_q", pc), ("target", target), ("data_addr", data_addr)):
        for i in range(16):
            values[f"{prefix}[{i}]"] = (number >> i) & 1
    for output, a, b in gates:
        assert output not in values and a in values and b in values
        values[output] = 1 ^ (values[a] & values[b])
    def word(prefix: str) -> int:
        return sum(values[aliases[f"{prefix}[{i}]"]] << i for i in range(16))
    return {"pc_inc": word("pc_inc"), "take": values["take"],
            "pc_d": word("pc_d"), "mar_d": word("mar_d")}


@dataclass
class Reader:
    memory: dict[int, int]
    bus: IdealBus
    phase: str = "IDLE"
    rd: int = 0
    pending_fetch: bool = False
    mdr: int | None = None
    mdr_valid: bool = False
    trace: list[dict] = field(default_factory=list)

    @classmethod
    def at(cls, pc: int, memory: dict[int, int]) -> "Reader":
        return cls(memory=memory, bus=IdealBus.create(pc))

    def _record(self, action: str, signals: dict, ready: int | None,
                previous_mdr: int | None) -> None:
        self.trace.append({
            "accion": action, "fase_despues": self.phase, "ready": ready,
            "rd_despues": self.rd, "pc_antes": signals["pc_antes"],
            "pc_despues": signals["pc_despues"],
            "mar_antes": signals["mar_antes"],
            "mar_despues": signals["mar_despues"],
            "pc_load": signals["pc_load"], "mar_load": signals["mar_load"],
            "mdr_load": int(action == "ACEPTAR"),
            "mdr_antes": previous_mdr, "mdr_despues": self.mdr,
            "mdr_valid": self.mdr_valid,
        })

    def prepare(self, *, fetch: bool, data_addr: int = 0) -> None:
        if self.phase != "IDLE":
            raise RuntimeError("No iniciar otra lectura mientras RD está ocupado")
        if not 0 <= data_addr <= 0xFFFF:
            raise ValueError("La dirección efectiva debe tener 16 bits")
        signal = self.bus.step("PREPARAR", pc_load=0, mar_load=1,
                               fetch=int(fetch), data_addr=data_addr)
        assert signal["pc_despues"] == signal["pc_antes"]
        assert signal["mar_despues"] == (
            signal["pc_antes"] if fetch else data_addr)
        self.phase, self.rd = "WAIT", 1
        self.pending_fetch = fetch
        self.mdr_valid = False
        self._record("PREPARAR", signal, None, self.mdr)

    def edge(self, ready: bool) -> int | None:
        if self.phase != "WAIT" or self.rd != 1:
            raise RuntimeError("READY sin una lectura pendiente")
        old_pc, old_mar, old_mdr = self.bus.pc.q, self.bus.mar.q, self.mdr
        if not ready:
            signal = self.bus.step("ESPERAR", pc_load=0, mar_load=0,
                                   fetch=int(self.pending_fetch))
            assert (self.bus.pc.q, self.bus.mar.q, self.mdr) == (
                old_pc, old_mar, old_mdr)
            self._record("ESPERAR", signal, 0, old_mdr)
            return None
        if old_mar not in self.memory:
            raise KeyError(f"No hay memoria de prueba en 0x{old_mar:04X}")
        # PRECONDICION: el modelo externo declara el dato estable antes
        # del flanco. Los tiempos reales de acceso NO se representan.
        value = self.memory[old_mar]
        signal = self.bus.step("ACEPTAR", pc_load=int(self.pending_fetch),
                               mar_load=0, fetch=int(self.pending_fetch))
        self.mdr, self.mdr_valid = value, True
        self.phase, self.rd = "IDLE", 0
        assert self.bus.mar.q == old_mar
        assert self.bus.pc.q == ((old_pc + 1) & 0xFFFF
                                if self.pending_fetch else old_pc)
        self._record("ACEPTAR", signal, 1, old_mdr)
        return value

    def read(self, *, fetch: bool, data_addr: int = 0, stalls: int = 0) -> int:
        if stalls < 0:
            raise ValueError("Las esperas no pueden ser negativas")
        self.prepare(fetch=fetch, data_addr=data_addr)
        for _ in range(stalls):
            assert self.edge(False) is None and not self.mdr_valid
        result = self.edge(True)
        assert result is not None and self.mdr_valid
        return result


def program_route(z: int, delays: dict[int, int]) -> dict:
    assert z in (0, 1)
    memory = {START + i: x for i, x in enumerate(BYTES)}
    reader = Reader.at(START, memory)
    fetched: list[dict] = []
    def fetch_n(n: int):
        for _ in range(n):
            old = reader.bus.pc.q
            value = reader.read(fetch=True, stalls=delays.get(old, 0))
            assert reader.bus.mar.q == old and value == memory[old]
            fetched.append({"direccion": old, "byte": value})
    fetch_n(3)  # JNZ, destino bajo, destino alto
    assert [e["byte"] for e in fetched] == [0x32, 0x09, 0x60]
    assert reader.rd == 0 and reader.bus.pc.q == 0x6003
    reader.bus.step("DECIDIR JNZ", pc_load=1-z, mar_load=0,
                    fetch=1, target=0x6009, jnz=1, z=z)
    if z == 0:
        assert reader.bus.pc.q == 0x6009
        fetch_n(3)  # LDI R1, 9
    else:
        assert reader.bus.pc.q == 0x6003
        fetch_n(3)  # LDI R1, 7
        fetch_n(3)  # JMP 0x600C
        assert fetched[-3]["byte"] == 0x30
        reader.bus.step("DECIDIR JMP", pc_load=1, mar_load=0,
                        fetch=1, target=0x600C, jmp=1)
    fetch_n(1)  # HALT
    assert (reader.bus.pc.q, reader.bus.mar.q) == (0x600D, 0x600C)
    assert reader.memory == memory
    assert len(fetched) == (7 if z == 0 else 10)
    assert len(reader.trace) == (2 * len(fetched)
                                + sum(delays.get(x["direccion"], 0) for x in fetched))
    return {"z": z, "pc_final": reader.bus.pc.q, "mar_final": reader.bus.mar.q,
            "lecturas": fetched, "traza": reader.trace}


def verify() -> dict:
    gates, aliases = read_hdl_assignments()
    rng = random.Random(0xC28A)
    cases = [
        (pc, target, data_addr, z, jmp, jnz, fetch)
        for pc in (0, 1, 0x60FF, 0x7FFF, 0xFFFF)
        for target in (0, 0x6009, 0xFFFF)
        for data_addr in (0, 0x6F00)
        for z, jmp, jnz in ((0,0,0), (1,0,0), (0,0,1), (1,0,1), (0,1,0), (1,1,0))
        for fetch in (0,1)
    ]
    cases += [
        (rng.randrange(0x10000), rng.randrange(0x10000),
         rng.randrange(0x10000), rng.randrange(2), *rng.choice(((0,0),(1,0),(0,1))),
         rng.randrange(2))
        for _ in range(8000)
    ]
    for pc, target, data_addr, z, jmp, jnz, fetch in cases:
        got = interpret_hdl(gates, aliases, pc, target, data_addr,
                            z, jmp, jnz, fetch)
        want = expected(pc, target, data_addr, z, jmp, jnz, fetch)
        assert got == want, (pc, target, data_addr, z, jmp, jnz, fetch, got, want)
    memories = {i: ((i * 13) ^ (i >> 3) ^ 0xA5) & 0xFF for i in range(0x100)}
    for pc, stalls in ((0,0), (0x7F,3), (0xFE,9), (0xFF,20)):
        mem = {pc: memories[pc]}
        reader = Reader.at(pc, mem)
        value = reader.read(fetch=True, stalls=stalls)
        assert value == mem[pc] and reader.bus.pc.q == pc + 1
        assert reader.bus.mar.q == pc and reader.rd == 0
    for pc in (0x60FF, 0xFFFF):
        reader = Reader.at(pc, {pc:0xA5})
        assert reader.read(fetch=True, stalls=5) == 0xA5
        assert reader.bus.pc.q == (pc+1)&0xFFFF
    reader = Reader.at(0x6007, {0x6F00:0x2A})
    reader.prepare(fetch=False, data_addr=0x6F00)
    try:
        reader.prepare(fetch=True)
    except RuntimeError:
        pass
    else:
        raise AssertionError("No se puede iniciar dos lecturas")
    for _ in range(100):
        reader.edge(False)
    assert reader.edge(True) == 0x2A and reader.bus.pc.q == 0x6007
    try:
        reader.edge(True)
    except RuntimeError:
        pass
    else:
        raise AssertionError("READY sin solicitud debe rechazarse")
    delays = {0x6000:2, 0x6001:0, 0x6002:3, 0x6006:4, 0x600C:1}
    routes = {str(z):program_route(z,delays) for z in (0,1)}
    print(f"C28-G: {len(cases):,} vectores del subconjunto Verilog contra referencia correctos")
    print("C28-G: protocolo PREPARAR/ESPERAR/ACEPTAR y dos rutas coherentes")
    print("Icarus Verilog: NO EJECUTADO; READY es una abstracción, no un pin probado")
    return {
        "verilog_subset": "assign NAND / assign salida, no simulador HDL completo",
        "hdl_iverilog_executed": False,
        "hdl_vectors": len(cases),
        "nand_parsed": len(gates),
        "control_contract": {
            "PREPARAR": {"MAR_LOAD":1, "PC_LOAD":0, "MDR_LOAD":0, "RD_after":1},
            "ESPERAR_READY_0": {"MAR_LOAD":0, "PC_LOAD":0, "MDR_LOAD":0, "RD_after":1},
            "ACEPTAR_FETCH_READY_1": {"MAR_LOAD":0, "PC_LOAD":1, "MDR_LOAD":1, "RD_after":0},
            "ACEPTAR_DATO_READY_1": {"MAR_LOAD":0, "PC_LOAD":0, "MDR_LOAD":1, "RD_after":0},
        },
        "delays": {f"{k:04X}":v for k,v in delays.items()},
        "routes":routes,
    }


def figure(trace: list[dict]) -> str:
    """Tabla visual generada directamente de eventos sometidos a prueba."""
    events = trace[:6]
    assert [e["accion"] for e in events] == [
        "PREPARAR", "ESPERAR", "ESPERAR", "ACEPTAR", "PREPARAR", "ACEPTAR"]
    c = [
        text(72, 82, "Una lectura ocupa varios momentos, no un instante mágico", 37, True),
        text(72, 134, "Contrato temporal del piloto, sin tiempos eléctricos ni pin READY obligatorio", 25,
             color="#4d697c"),
        rect(69, 179, 1622, 760, "#edf4f8"),
    ]
    columns = ((98, "Momento"), (380, "PC después"), (620, "MAR después"),
               (912, "RD"), (1085, "MDR válido"), (1380, "Dato"))
    for x,label in columns:
        c.append(text(x,237,label,26,True))
    for idx,e in enumerate(events):
        y = 275 + idx*96
        c.append(rect(90,y,1580,82,("#dcefe7" if e["accion"]=="ACEPTAR" else
                                     "#fff0d8" if e["accion"]=="ESPERAR" else "#e3ebf7")))
        c.extend([
            text(112,y+52,e["accion"],26,True),
            text(390,y+52,f"{e['pc_despues']:04X}",28),
            text(625,y+52,f"{e['mar_despues']:04X}",28),
            text(926,y+52,str(e["rd_despues"]),28,True),
            text(1118,y+52, "sí" if e["mdr_valid"] else "no",28),
            text(1385,y+52,f"{e['mdr_despues']:02X}" if e["mdr_valid"] else "—",28,True),
        ])
    c.extend([
        text(94, 1003, "PC y MAR se mantienen durante READY=0; el PC avanza solo al aceptar el byte.",25,True),
        text(94, 1052, "Dato de ejemplo: MEM[6000]=32, MEM[6001]=09; sólo modelo de anfitrión.",23,
             color="#526b78"),
    ])
    return art(c,1760,1115)


def save(data: dict) -> None:
    OUT.mkdir(parents=True,exist_ok=True)
    FIG.mkdir(parents=True,exist_ok=True)
    (OUT/"auditoria_y_trazas.json").write_text(
        json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    svg = FIG/"c28g_lectura_con_espera.svg"
    svg.write_text(figure(data["routes"]["0"]["traza"]),encoding="utf-8")
    # La validez logica del HDL NO depende de poder renderizar una figura.
    # Windows puede tener Inkscape instalado sin exponerlo en PATH.
    inkscape = shutil.which("inkscape")
    if not inkscape and os.name == "nt":
        paths = (
            ("ProgramFiles", "Inkscape/bin/inkscape.exe"),
            ("ProgramFiles(x86)", "Inkscape/bin/inkscape.exe"),
            ("LOCALAPPDATA", "Programs/Inkscape/bin/inkscape.exe"),
        )
        inkscape = next((str(candidate)
                         for variable, suffix in paths
                         if os.environ.get(variable)
                         for candidate in [Path(os.environ[variable]) / suffix]
                         if candidate.is_file()), None)
    if not inkscape:
        print("C28-G: RENDER_PNG_PENDIENTE; Inkscape no encontrado. "
              "SVG y resultados logicos guardados; no se genero PNG nuevo.")
        return
    try:
        subprocess.run([inkscape, str(svg),
                        f"--export-filename={FIG/'c28g_lectura_con_espera.png'}",
                        "--export-width=1800"], check=True, capture_output=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"C28-G: RENDER_PNG_PENDIENTE; fallo exportacion: {exc}. "
              "SVG y resultados logicos guardados.")
    else:
        print("C28-G: RENDER_PNG_APROBADO; figura PNG regenerada.")


if __name__=="__main__":
    save(verify())
