#!/usr/bin/env python3
"""Audita el global C28-G + el piloto C28-H y crea feedback recuperable.

No certifica silicio, CPU completa, retardo fisico o eleccion de ISA/PC.
Usa Python 3 estandar; Icarus e Inkscape son opcionales.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED


ROOT = Path(__file__).resolve().parents[1]
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
EVIDENCE = ROOT / ("_PRUEBAS_GLOBAL_C28H_" + STAMP)
EVIDENCE.mkdir(exist_ok=False)
RESULTS = []
PHOTO_REPORT = {"estado": "NO_EJECUTADO", "nota": "La descarga no afecta los controles de circuito"}


def item(name: str, state: str, details: str = "", seconds: float = 0.0) -> None:
    RESULTS.append(dict(nombre=name, estado=state, detalle=details, segundos=round(seconds, 3)))
    print(f"[{state}] {name}: {details}", flush=True)


def environ() -> dict[str, str]:
    env = os.environ.copy()
    extra = []
    if os.name == "nt":
        for key, suffix in (
            ("ProgramFiles", "Inkscape\\bin"),
            ("LOCALAPPDATA", "Programs\\Inkscape\\bin"),
            ("ProgramFiles", "Icarus Verilog\\bin"),
            ("ProgramFiles(x86)", "Icarus Verilog\\bin"),
        ):
            if env.get(key):
                extra.append(str(Path(env[key]) / suffix))
        extra.append("C:\\iverilog\\bin")
    env["PATH"] = os.pathsep.join(extra + [env.get("PATH", "")])
    return env


ENV = environ()


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify_documents() -> None:
    start = time.monotonic()
    base = ROOT / "libro" / "capitulos"
    sets = {ext: {p.stem for p in base.glob("*" + ext)}
            for ext in (".md", ".docx", ".pdf")}
    assert len(sets[".md"]) == 26, f"Fuentes markdown: {len(sets['.md'])}, se esperaban 26"
    assert sets[".md"] == sets[".docx"] == sets[".pdf"], "Fuentes/fasciculos desalineados"
    for stem in sorted(sets[".md"]):
        with ZipFile(base / (stem + ".docx")) as z:
            assert z.testzip() is None, stem
            assert "word/document.xml" in z.namelist(), stem
        assert (base / (stem + ".pdf")).read_bytes()[:5] == b"%PDF-", stem
    masters = ROOT / "libro" / "ediciones" / "C28_G"
    word = masters / "Aula_Computadora_C28_G_MAESTRO.docx"
    pdf = masters / "Aula_Computadora_C28_G_MAESTRO.pdf"
    assert word.stat().st_size > 1_000_000 and pdf.stat().st_size > 1_000_000
    with ZipFile(word) as z:
        assert z.testzip() is None and "word/document.xml" in z.namelist()
    with pdf.open("rb") as f:
        assert f.read(5) == b"%PDF-"
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in (word, pdf)}
    (EVIDENCE / "HASHES_MAESTROS.json").write_text(
        json.dumps(hashes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    item("26 capitulos + Word/PDF maestro", "APROBADO",
         "Integridad de formatos; NO revision semantica de las 26 lecciones",
         time.monotonic() - start)


def execute(name: str, command: list[str], timeout: int = 360) -> None:
    print(f"  Ejecutando: {name}...", flush=True)
    start = time.monotonic()
    try:
        run = subprocess.run(command, cwd=ROOT, env=ENV, text=True,
                             encoding="utf-8", errors="replace",
                             capture_output=True, timeout=timeout, check=False)
        output = (run.stdout or "") + (run.stderr or "")
        (EVIDENCE / (name + ".txt")).write_text(output, encoding="utf-8")
        item(name, "APROBADO" if run.returncode == 0 else "FALLIDO",
             f"codigo={run.returncode}, registro={name}.txt",
             time.monotonic() - start)
    except subprocess.TimeoutExpired as exc:
        (EVIDENCE / (name + ".txt")).write_text(str(exc), encoding="utf-8")
        item(name, "FALLIDO", f"supero {timeout} segundos", time.monotonic() - start)
    except Exception as exc:  # conservar informe de fallo sin abortar todo
        (EVIDENCE / (name + ".txt")).write_text(repr(exc), encoding="utf-8")
        item(name, "FALLIDO", repr(exc), time.monotonic() - start)


def run_python_models() -> None:
    cases = (
        ("LIBRO_C28J_PROGRESION", "c28j_auditar_progresion_libro.py"),
        ("LIBRO_C28L_LOGICA_INICIAL", "c28l_verificar_logica_inicial.py"),
        ("LIBRO_C28M_ALU_MEMORIA_ISA", "c28m_verificar_alu_mapa_y_programa.py"),
        ("LIBRO_C28O_ATLAS_HISTORICO", "c28o_verificar_atlas_historico.py"),
        ("LIBRO_C28P_TRAMO_FINAL", "c28p_auditar_tramo_final.py"),
        ("LIBRO_C28Q_NETLIST_Y_FIGURAS", "c28q_verificar_redes_y_trazabilidad.py"),
        ("LIBRO_C28R_ALU8_NAND_ADD_SUB", "c28r_verificar_alu8_nand.py"),
        ("LIBRO_C28S_EVIDENCIA_PDF_248", "c28s_verificar_evidencia_pdf.py"),
        ("ISA_AULA8_BORRADOR", "verificar_isa_aula8_borrador.py"),
        ("C28_A_REGISTRO8", "c28_verificar_piloto.py"),
        ("C28_D_SELECTOR", "c28d_salto_y_selector_pc.py"),
        ("C28_E_PC16", "c28e_pc16_prueba.py"),
        ("C28_F_PC_MAR", "c28f_incremento_mary_saltos.py"),
        ("C28_G_LECTURA", "c28g_auditar_hdl_y_memoria.py"),
        ("C28_H_LECTURA_SECUENCIAL", "c28h_piloto.py"),
    )
    for name, filename in cases:
        execute(name, [sys.executable, str(ROOT / "scripts" / filename)])
        if name == "C28_G_LECTURA":
            log = EVIDENCE / (name + ".txt")
            output = log.read_text(encoding="utf-8") if log.is_file() else ""
            if RESULTS[-1]["estado"] == "APROBADO" and "RENDER_PNG_APROBADO" in output:
                item("C28_G_RENDER_PNG", "APROBADO",
                     "Inkscape produjo el PNG; contraste de calidad visual por revisar")
            else:
                item("C28_G_RENDER_PNG", "PENDIENTE",
                     "La prueba logica es independiente; revisar log C28_G_LECTURA.txt")
        if name == "C28_H_LECTURA_SECUENCIAL":
            log = EVIDENCE / (name + ".txt")
            output = log.read_text(encoding="utf-8") if log.is_file() else ""
            if RESULTS[-1]["estado"] == "APROBADO" and "RENDER_PNG_APROBADO" in output:
                item("C28_H_RENDER_PNG", "APROBADO",
                     "Se exportaron las dos laminas; inspeccion editorial visual pendiente")
            else:
                item("C28_H_RENDER_PNG", "PENDIENTE",
                     "Los SVG se conservan; ver C28_H_LECTURA_SECUENCIAL.txt")


def run_icarus() -> None:
    iverilog = shutil.which("iverilog", path=ENV["PATH"])
    vvp = shutil.which("vvp", path=ENV["PATH"])
    if not (iverilog and vvp):
        item("Icarus Verilog", "PENDIENTE", "iverilog o vvp no encontrado; no se simulo HDL")
        return
    cases = (
        ("HDL_C28_R_ALU8_NAND_ADD_SUB", "tb_alu8_addsub_134nand", (
            ROOT / "c28_r/rtl/alu8_addsub_134nand.v",
            ROOT / "c28_r/rtl/tb_alu8_addsub_134nand.v")),
        ("HDL_C28_A_REGISTRO8", "tb_registro8", (
            ROOT / "c28_a/piloto_registro8/registro8.v",
            ROOT / "c28_a/piloto_registro8/tb_registro8.v")),
        ("HDL_C28_E_PC16", "tb_pc16_c28e", (
            ROOT / "c28_e/piloto_pc16/pc16_c28e.v",
            ROOT / "c28_e/piloto_pc16/tb_pc16_c28e.v")),
        ("HDL_C28_F_PC_MAR", "tb_pc_mar_c28f", (
            ROOT / "c28_f/piloto_pc_mar/pc_mar_c28f.v",
            ROOT / "c28_f/piloto_pc_mar/tb_pc_mar_c28f.v")),
        ("HDL_C28_H_DOS_POLITICAS", "tb_lectura_c28h", (
            ROOT / "c28_h/rtl/lectura_c28h.v",
            ROOT / "c28_h/rtl/tb_lectura_c28h.v")),
    )
    for name, top, files in cases:
        target = EVIDENCE / (name + ".vvp")
        execute(name + "_COMPILACION", [iverilog, "-g2012", "-s", top,
                                        "-o", str(target), *map(str, files)])
        if RESULTS[-1]["estado"] == "APROBADO":
            execute(name + "_SIMULACION", [vvp, str(target)], timeout=360)
        else:
            item(name + "_SIMULACION", "PENDIENTE", "compilacion incorrecta")
    vcd = ROOT / "c28_h/piloto/c28h_trazas.vcd"
    if vcd.is_file():
        shutil.copy2(vcd, EVIDENCE / vcd.name)


def collect_historical_photos() -> None:
    """Descarga candidatos Wikimedia al feedback sin tocar fuentes del libro."""
    global PHOTO_REPORT
    fotos = EVIDENCE / "FOTOS_HISTORICAS_C28N"
    fotos.mkdir(exist_ok=True)
    command = [sys.executable,
               str(ROOT / "scripts" / "c28n_recolectar_fotos_historicas.py"),
               "--salida", str(fotos)]
    print("\n=== FOTOS HISTORICAS (AUXILIAR, FUERA DE LOS CONTROLES) ===", flush=True)
    try:
        result = subprocess.run(command, cwd=ROOT, env=ENV, text=True,
                                encoding="utf-8", errors="replace", capture_output=True,
                                timeout=160, check=False)
        output = (result.stdout or "") + (result.stderr or "")
        (EVIDENCE / "FOTOS_HISTORICAS_C28N_LOG.txt").write_text(output, encoding="utf-8")
        summary = fotos / "REPORTE_DESCARGA_FOTOS.json"
        if result.returncode == 0 and summary.is_file():
            report = json.loads(summary.read_text(encoding="utf-8"))
            PHOTO_REPORT = dict(estado="EJECUTADO", descargadas=report["descargadas"],
                                total=report["total_catalogadas"],
                                evidencia="FOTOS_HISTORICAS_C28N/REPORTE_DESCARGA_FOTOS.json")
        else:
            PHOTO_REPORT = dict(estado="ERROR_AUXILIAR", codigo=result.returncode,
                                log="FOTOS_HISTORICAS_C28N_LOG.txt")
    except Exception as exc:
        PHOTO_REPORT = dict(estado="ERROR_AUXILIAR", detalle=repr(exc))
        (EVIDENCE / "FOTOS_HISTORICAS_C28N_LOG.txt").write_text(repr(exc), encoding="utf-8")
    print("Fotos historicas:", PHOTO_REPORT, flush=True)


def write_summary() -> Path:
    failures = sum(x["estado"] == "FALLIDO" for x in RESULTS)
    pending = sum(x["estado"] == "PENDIENTE" for x in RESULTS)
    passed = sum(x["estado"] == "APROBADO" for x in RESULTS)
    info = dict(version="C28-S ARITMETICA NAND + AUDITORIA 248 PAGINAS; maestro C28-G conservado",
                controles=RESULTS, aprobados=passed, fallidos=failures,
                pendientes=pending, fotografias_historicas=PHOTO_REPORT,
                limites=["no silicio ni retardos fisicos",
                         "no CPU integrada ni firmware",
                         "PC anticipado y diferido siguen candidatos",
                         "HDL solo validado si las simulaciones figuran APROBADAS"],
                interludio="El suplemento C28-H aun no se inserto en Word/PDF maestro")
    (EVIDENCE / "RESUMEN_GLOBAL_C28H.json").write_text(
        json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# Resultado de pruebas globales C28-H con auditorías C28-R/S", "",
          "| Prueba | Resultado | Detalle |", "| --- | --- | --- |"]
    for r in RESULTS:
        md.append(f"| {r['nombre']} | {r['estado']} | {r['detalle']} |")
    md += ["", f"**Aprobadas:** {passed}. **Fallidas:** {failures}. **Pendientes:** {pending}.",
           "", "**Fotografias historicas (recurso auxiliar):** " + str(PHOTO_REPORT),
           "", "El proyecto completo contiene C28-G y el piloto C28-H,",
           "pero no implica hardware real ni CPU lista."]
    (EVIDENCE / "RESUMEN_GLOBAL_C28H.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    output = ROOT / ("Retroalimentacion_GLOBAL_C28H_" + STAMP + ".zip")
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=7) as z:
        for file in sorted(EVIDENCE.rglob("*")):
            if file.is_file():
                z.write(file, file.relative_to(ROOT))
    print("\n=== ENTREGA DE RETROALIMENTACION ===", flush=True)
    print(output, flush=True)
    print(f"Aprobadas={passed}; fallidas={failures}; pendientes={pending}", flush=True)
    return output


def main() -> int:
    try:
        verify_documents()
    except Exception as exc:
        item("26 capitulos + Word/PDF maestro", "FALLIDO", repr(exc))
    run_python_models()
    run_icarus()
    collect_historical_photos()
    write_summary()
    if any(r["estado"] == "FALLIDO" for r in RESULTS):
        return 1
    return 2 if any(r["estado"] == "PENDIENTE" for r in RESULTS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
