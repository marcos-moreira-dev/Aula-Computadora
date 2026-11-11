#!/usr/bin/env python3
"""Comprueba el atlas histórico C28-O sin acceso a Internet ni dependencias.

Esta prueba audita archivos, metadatos y estructura del PDF; no prueba
licencias futuras, calidad editorial, lógica HDL ni electrónica física.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "libro" / "ediciones" / "C28_O"
FOTOS = ROOT / "libro" / "figuras_historicas_c28o"
MANIFEST = ATLAS / "ACTIVOS_FOTOGRAFICOS_VERIFICADOS_C28O.json"
PDF = ATLAS / "Aula_Computadora_Atlas_Historico_C28_O.pdf"
MANUSCRITO = ROOT / "libro" / "ATLAS_HISTORICO_C28O.md"


def verify() -> None:
    index = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert index["edicion"] == "C28-O"
    sources = index["fuentes"]
    assert len(sources) == 5, f"Se esperaban cinco fotos, hay {len(sources)}"
    assert len(list(FOTOS.glob("*.jpg"))) == 5, "Fotos extra o incompletas"
    manuscript = MANUSCRITO.read_text(encoding="utf-8")

    for item_id, info in sources.items():
        path = FOTOS / info["archivo"]
        data = path.read_bytes()
        assert data[:3] == b"\xff\xd8\xff", f"JPEG invalido: {item_id}"
        assert len(data) == info["bytes"], f"Tamano incorrecto: {item_id}"
        assert hashlib.sha256(data).hexdigest() == info["sha256"], (
            f"SHA-256 incorrecto: {item_id}")
        assert info["autor"] and info["licencia"].startswith("CC BY")
        assert info["fuente"].startswith("https://commons.wikimedia.org/wiki/File:")
        assert item_id.split("_")[0] in manuscript, f"Falta {item_id} en texto"

    document = PDF.read_bytes()
    assert document.startswith(b"%PDF-"), "Atlas no es un PDF"
    assert len(document) > 500_000, "Atlas demasiado pequeno"
    # El PDF de este paquete lo genera ReportLab con diccionarios Page visibles.
    pages = len(re.findall(rb"/Type\s*/Page\b", document))
    assert pages == 7, f"Atlas con {pages} paginas, se esperaban 7"
    print("C28-O: 5 fotografias JPEG completas, metadatos/licencias presentes")
    print("C28-O: 5 SHA-256 de fotografias correctos")
    print("C28-O: 7 paginas PDF con portada, cinco laminas y creditos")
    print("LIMITES: no comprueba funcionamiento HDL, hardware ni calidad visual")


if __name__ == "__main__":
    verify()
