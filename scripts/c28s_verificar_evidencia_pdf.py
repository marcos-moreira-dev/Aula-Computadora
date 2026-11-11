#!/usr/bin/env python3
"""C28-S: comprueba la integridad del análisis PDF sin requerir PyMuPDF.

Este control Windows coteja las evidencias YA renderizadas en el entorno
editorial; no repite el análisis de bounding boxes ni la lectura humana.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "libro/ediciones/C28_G/Aula_Computadora_C28_G_MAESTRO.pdf"
REPORT = ROOT / "c28_s/revision_pdf/C28_S_REPORTE_PAGINAS.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    assert data["paginas"] == 248
    assert data["fragmentos_texto"] > 17000
    assert data["bloques_imagen"] >= 120
    assert data["caracteres_reemplazo"] == 0
    assert data["entradas_indice_verificadas"] == 26
    assert data["pies_de_pagina_con_numero"] == 247
    assert data["indice_coincide_con_capitulos"] is True
    assert len(data["indice"]) == 26
    assert not data["alertas_cajas_o_paginas"]
    assert len(data["paginas_detalle"]) == 248
    for number, page in enumerate(data["paginas_detalle"], start=1):
        assert page["numero"] == number
        assert page["cajas_fuera_de_pagina"] == 0
        assert page["caracteres_reemplazo"] == 0
    assert digest(PDF) == data["sha256_maestro"], "Maestro cambió; regenerar evidencia"
    assert len(data["hojas_contacto"]) == 8
    for idx, relative in enumerate(data["hojas_contacto"], start=1):
        img = REPORT.parent / relative
        assert img.name == f"C28_S_CONTACTO_{idx:02d}.jpg"
        assert img.stat().st_size > 100_000
        with img.open("rb") as file:
            assert file.read(2) == b"\xff\xd8", img.name
    print("C28-S: 248 páginas, 26 entradas de índice y 247 folios concordantes")
    print("C28-S: 8 hojas de contacto íntegras")
    print("C28-S: SHA-256 del PDF maestro idéntico al auditado")
    print("EVIDENCIA_C28S_APROBADA; REVISION_HUMANA_FINAL_PENDIENTE")


if __name__ == "__main__":
    main()
