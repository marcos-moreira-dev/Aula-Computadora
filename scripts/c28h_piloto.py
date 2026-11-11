#!/usr/bin/env python3
"""C28-H: referencia independiente, vectores para Icarus y laminas 2D.

No interpreta Verilog, no prueba hardware fisico y no decide la politica de PC.
Usa solo la biblioteca estandar; Inkscape es opcional para PNG.
"""
from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import json
import os
import random
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "c28_h" / "piloto"
RESET_PC = 0x6000
SEED = 0xC28A11
COUNT_RANDOM = 12000


@dataclass
class Ref:
    deferred: bool
    pc: int = RESET_PC
    mar: int = 0
    mdr: int = 0
    rd: int = 0
    busy: int = 0
    valid: int = 0
    accepted: int = 0
    rejected: int = 0
    pending_fetch: int = 0

    def step(self, x: dict[str, int]) -> None:
        if not x["rst_n"]:
            self.pc, self.mar, self.mdr = RESET_PC, 0, 0
            self.rd = self.busy = self.valid = 0
            self.accepted = self.rejected = self.pending_fetch = 0
            return

        self.accepted = self.rejected = 0
        if not self.busy:
            if x["req"] and x["pc_write"]:
                self.rejected = 1
            elif x["pc_write"]:
                self.pc = x["pc_value"]
            elif x["req"]:
                self.mar = self.pc if x["fetch"] else x["data_addr"]
                self.pending_fetch = x["fetch"]
                self.rd = self.busy = 1
                self.valid = 0
                if x["fetch"] and not self.deferred:
                    self.pc = (self.pc + 1) & 0xFFFF
        else:
            if x["req"] or x["pc_write"]:
                self.rejected = 1
            if x["ready"]:
                self.mdr = x["data_in"]
                self.valid = self.accepted = 1
                self.rd = self.busy = 0
                if self.pending_fetch and self.deferred:
                    self.pc = (self.pc + 1) & 0xFFFF

    def output(self) -> tuple[int, ...]:
        return (self.pc, self.mar, self.mdr, self.rd, self.busy,
                self.valid, self.accepted, self.rejected)


INPUT_WIDTHS = (1, 1, 1, 1, 1, 16, 16, 8)
OUTPUT_WIDTHS = (16, 16, 8, 1, 1, 1, 1, 1)


def pack(values: tuple[int, ...], widths: tuple[int, ...]) -> int:
    assert len(values) == len(widths)
    output = 0
    for val, bits in zip(values, widths):
        assert 0 <= val < 2**bits, (val, bits)
        output = (output << bits) | val
    return output


def case(rst_n=1, req=0, fetch=0, pc_write=0, ready=0,
         data_addr=0, pc_value=0, data_in=0) -> dict[str, int]:
    return dict(rst_n=rst_n, req=req, fetch=fetch, pc_write=pc_write,
                ready=ready, data_addr=data_addr, pc_value=pc_value,
                data_in=data_in)


def scenarios() -> list[dict[str, int]]:
    cases = [case(rst_n=0), case(rst_n=0), case(ready=1)]
    # FETCH en 6000, dos esperas, captura 32.
    cases += [case(req=1, fetch=1), case(ready=0, data_in=0xEF),
              case(ready=0, data_in=0xAB), case(ready=1, data_in=0x32),
              case(ready=1)]
    # Dato comun: PC debe quedar igual; READY=1 durante la solicitud no
    # acepta el dato antes de que el controlador pase por Esperando.
    cases += [case(req=1, data_addr=0x6F00, ready=1),
              case(ready=1, data_in=0x2A), case()]
    # Cruce de FFFF a 0000 y orden incompatible en reposo.
    cases += [case(pc_write=1, pc_value=0xFFFF),
              case(req=1, pc_write=1, fetch=1, pc_value=0x1234),
              case(req=1, fetch=1), case(ready=0),
              case(ready=1, data_in=0x99)]
    # Orden en curso: se rechaza la segunda sin interrumpir la primera.
    cases += [case(req=1, data_addr=0x6F00),
              case(req=1, fetch=1, ready=0),
              case(pc_write=1, pc_value=0x7777, ready=1, data_in=0xA5)]
    # RESET durante una lectura aborta la operacion sin aceptar un dato.
    cases += [case(req=1, fetch=1), case(rst_n=0, ready=1), case()]
    # Cien esperas consecutivas: MAR y RD estables.
    cases += [case(req=1, fetch=1)]
    cases += [case(ready=0, data_in=i) for i in range(100)]
    cases += [case(ready=1, data_in=0x5A)]
    rng = random.Random(SEED)
    for _ in range(COUNT_RANDOM):
        cases.append(case(
            rst_n=int(rng.randrange(499) != 0),
            req=int(rng.random() < .29),
            fetch=rng.randrange(2),
            pc_write=int(rng.random() < .08),
            ready=int(rng.random() < .62),
            data_addr=rng.randrange(65536),
            pc_value=rng.randrange(65536),
            data_in=rng.randrange(256),
        ))
    return cases


def check_transition(before: tuple[int, ...], after: tuple[int, ...],
                     x: dict[str, int], deferred: bool) -> None:
    pc0, mar0, mdr0, rd0, busy0, valid0, _, _ = before
    pc, mar, mdr, rd, busy, valid, accepted, rejected = after
    assert rd == busy, "RD y BUSY deben coincidir en este contrato"
    if not x["rst_n"]:
        assert after == (RESET_PC, 0, 0, 0, 0, 0, 0, 0)
        return
    assert accepted == int(bool(busy0 and x["ready"]))
    assert rejected == int(bool(
        (busy0 and (x["req"] or x["pc_write"])) or
        (not busy0 and x["req"] and x["pc_write"])))
    if busy0 and not x["ready"]:
        assert mar == mar0 and mdr == mdr0 and rd == rd0 and busy == busy0
        assert pc == pc0 and valid == valid0
    if busy0 and x["ready"]:
        assert mdr == x["data_in"] and valid == 1 and not rd and not busy
        if deferred and not accepted:
            raise AssertionError("PC diferido sin aceptación")
    if not busy0 and not x["req"] and not x["pc_write"]:
        assert (pc, mar, mdr) == (pc0, mar0, mdr0)


def run() -> tuple[list[dict], dict]:
    models = (Ref(False), Ref(True))
    traces: list[dict] = []
    line_data: list[str] = []
    checks = 0
    for index, inputs in enumerate(scenarios()):
        previous = [model.output() for model in models]
        for model in models:
            model.step(inputs)
        new = [model.output() for model in models]
        for old, current, model in zip(previous, new, models):
            check_transition(old, current, inputs, model.deferred)
            checks += 1
        input_fields = tuple(inputs[k] for k in (
            "rst_n", "req", "fetch", "pc_write", "ready",
            "data_addr", "pc_value", "data_in"))
        word = pack(input_fields, INPUT_WIDTHS)
        word = (word << 45) | pack(new[0], OUTPUT_WIDTHS)
        word = (word << 45) | pack(new[1], OUTPUT_WIDTHS)
        assert word < (1 << 135)
        line_data.append(f"{word:034x}")
        if index < 23:
            traces.append({"ciclo": index, "entrada": inputs,
                           "pc_anticipado": f"{new[0][0]:04X}",
                           "pc_diferido": f"{new[1][0]:04X}",
                           "mar": f"{new[1][1]:04X}",
                           "mdr": f"{new[1][2]:02X}",
                           "rd": new[1][3], "valid": new[1][5],
                           "aceptado": new[1][6], "rechazado": new[1][7]})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "vectores_c28h.mem").write_text("\n".join(line_data) + "\n", encoding="ascii")
    result = {"estado": "MODELO_PYTHON_APROBADO",
              "nota": "El HDL todavia requiere ejecucion independiente con Icarus",
              "vectores_por_alternativa": len(line_data),
              "comparaciones_referencia": checks,
              "semilla": SEED, "random": COUNT_RANDOM,
              "politica_pc": ["anticipado C28-F", "diferido C28-G"],
              "restricciones": ["READY abstracto", "reset fijo de prueba",
                                "sin timings fisicos", "sin bus de escritura"]}
    (OUT / "resultado_python.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "traza_breve.json").write_text(
        json.dumps(traces, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return traces, result


def figure_functional() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="780" viewBox="0 0 1500 780">
<defs><marker id="arrow" markerWidth="12" markerHeight="10" refX="10" refY="5" orient="auto"><path d="M0,0 L12,5 L0,10 Z" fill="#315774"/></marker></defs>
<rect width="1500" height="780" fill="#f8fbfe"/>
<text x="70" y="87" font-family="DejaVu Sans" font-size="38" font-weight="bold" fill="#153952">C28-H · Cómo se conserva una lectura</text>
<text x="70" y="130" font-family="DejaVu Sans" font-size="23" fill="#526c80">Diagrama funcional del piloto, no esquema de cables ni netlist eléctrico.</text>
<g stroke="#315774" stroke-width="3" fill="none" marker-end="url(#arrow)"><path d="M337 335 H440"/><path d="M680 335 H790"/><path d="M1038 335 H1140"/><path d="M555 235 V280"/><path d="M920 230 V280"/></g>
<g stroke="#24465c" stroke-width="3">
<rect x="70" y="281" width="267" height="110" rx="14" fill="#e5eff6"/>
<rect x="440" y="281" width="240" height="110" rx="14" fill="#e6ecff"/>
<rect x="790" y="281" width="248" height="110" rx="14" fill="#fff0dc"/>
<rect x="1140" y="281" width="265" height="110" rx="14" fill="#dcf2e7"/>
<rect x="416" y="151" width="280" height="79" rx="14" fill="#dceaf5"/>
<rect x="790" y="151" width="248" height="79" rx="14" fill="#f1e7fc"/>
</g>
<g font-family="DejaVu Sans" fill="#183b53" text-anchor="middle">
<text x="204" y="326" font-size="25" font-weight="bold">Solicitud</text><text x="204" y="360" font-size="21">FETCH / DATO</text>
<text x="560" y="326" font-size="27" font-weight="bold">MAR (16)</text><text x="560" y="360" font-size="20">retiene dirección</text>
<text x="914" y="326" font-size="26" font-weight="bold">Memoria</text><text x="914" y="360" font-size="20">respuesta ideal</text>
<text x="1272" y="326" font-size="26" font-weight="bold">MDR (8)</text><text x="1272" y="360" font-size="20">captura byte</text>
<text x="555" y="184" font-size="25" font-weight="bold">PC (16)</text><text x="555" y="211" font-size="18">dirección de instrucción</text>
<text x="914" y="184" font-size="25" font-weight="bold">RD / READY</text><text x="914" y="211" font-size="18">esperar o aceptar</text>
</g>
<rect x="70" y="455" width="1335" height="225" rx="15" fill="#eaf2f7"/>
<g font-family="DejaVu Sans" fill="#173c55"><text x="100" y="500" font-size="26" font-weight="bold">¿Cuándo cambia el PC?</text>
<text x="105" y="551" font-size="23">Alternativa A (C28-F): al solicitar FETCH, con MAR conservando la dirección anterior.</text>
<text x="105" y="600" font-size="23">Alternativa B (C28-G): al aceptar FETCH tras READY=1.</text>
<text x="105" y="645" font-size="20" fill="#6f4350">Ambas están a prueba; ninguna es arquitectura definitiva.</text></g>
<text x="70" y="744" font-family="DejaVu Sans" font-size="20" fill="#556d7d">Fuente: contrato C28-H y vectores del modelo de referencia. RESET=6000 solo para el piloto.</text>
</svg>'''


def figure_table(traces: list[dict]) -> str:
    chosen = [t for t in traces if 3 <= t["ciclo"] <= 10]
    cols = (("Paso", 70), ("req", 230), ("READY", 360), ("RD", 510),
            ("PC A", 645), ("PC B", 830), ("MAR", 1020), ("MDR", 1210))
    rows = []
    for index, item in enumerate(chosen):
        y = 225 + index * 66
        fill = "#dcf1e7" if item["aceptado"] else "#fff0d8" if item["rd"] else "#e5edf5"
        rows.append(f'<rect x="58" y="{y}" width="1340" height="60" rx="7" fill="{fill}"/>')
        fields = (str(item["ciclo"]), str(item["entrada"]["req"]),
                  str(item["entrada"]["ready"]), str(item["rd"]),
                  item["pc_anticipado"], item["pc_diferido"], item["mar"], item["mdr"])
        for (_, x), val in zip(cols, fields):
            rows.append(f'<text x="{x}" y="{y+39}" font-size="24">{escape(val)}</text>')
    headers = ''.join(f'<text x="{x}" y="199" font-size="24" font-weight="bold">{escape(label)}</text>'
                      for label, x in cols)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="880" viewBox="0 0 1500 880">
<rect width="1500" height="880" fill="#f8fbfe"/>
<g font-family="DejaVu Sans" fill="#173c55"><text x="60" y="85" font-size="36" font-weight="bold">C28-H · Dos maneras de avanzar PC</text>
<text x="60" y="130" font-size="22">Valores extraídos de una misma secuencia de prueba, con idénticas entradas.</text>
{headers}{''.join(rows)}
<text x="65" y="795" font-size="22">A: PC avanza al pedir FETCH. B: PC avanza al aceptar el byte.</text>
<text x="65" y="832" font-size="20" fill="#6a4b55">La tabla es lógica de flancos ideales, no una medición temporal física.</text></g></svg>'''


def illustrations(traces: list[dict]) -> None:
    paths = (("c28h_esquema_funcional", figure_functional()),
             ("c28h_comparacion_pc", figure_table(traces)))
    renderer = shutil.which("inkscape")
    if not renderer and os.name == "nt":
        locations = (
            ("ProgramFiles", "Inkscape/bin/inkscape.exe"),
            ("ProgramFiles(x86)", "Inkscape/bin/inkscape.exe"),
            ("LOCALAPPDATA", "Programs/Inkscape/bin/inkscape.exe"),
        )
        renderer = next((str(candidate)
                         for variable, suffix in locations
                         if os.environ.get(variable)
                         for candidate in [Path(os.environ[variable]) / suffix]
                         if candidate.is_file()), None)
    rendered = 0
    for base, payload in paths:
        svg = OUT / (base + ".svg")
        svg.write_text(payload, encoding="utf-8")
        if renderer:
            try:
                subprocess.run([renderer, str(svg),
                                f"--export-filename={OUT / (base + '.png')}",
                                "--export-width=1800"], check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if (OUT / (base + ".png")).read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
                    raise ValueError("la salida no es un archivo PNG valido")
                rendered += 1
            except (OSError, subprocess.CalledProcessError) as error:
                print(f"AVISO: no se produjo {base}.png: {error}")
            except ValueError as error:
                print(f"AVISO: no se valido {base}.png: {error}")
        else:
            print(f"AVISO: Inkscape ausente; se conserva {base}.svg")
    if rendered == len(paths):
        print("C28-H: RENDER_PNG_APROBADO; dos laminas PNG regeneradas.")
    else:
        print(f"C28-H: RENDER_PNG_PENDIENTE; {rendered}/{len(paths)} laminas exportadas; SVG conservados.")


if __name__ == "__main__":
    t, evidence = run()
    illustrations(t)
    print(f"C28-H modelo Python: {evidence['comparaciones_referencia']:,} comprobaciones correctas")
    print(f"C28-H: {evidence['vectores_por_alternativa']:,} vectores para cada alternativa HDL")
    print("C28-H: este modelo Python no ejecuta HDL; la auditoria global registra Icarus por separado.")
