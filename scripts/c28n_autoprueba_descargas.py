#!/usr/bin/env python3
"""Autoprueba offline del recolector C28-N: NO hace solicitudes a Internet."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import c28n_recolectar_fotos_historicas as collector


class PruebasDescargaC28N(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(collector.CATALOG.read_text(encoding="utf-8"))
        self.licenses = {d["titulo_commons"]: d["licencia_esperada"]
                         for d in self.manifest["fotografias"]}

    def fake_info(self, name: str, width: int) -> dict:
        self.assertEqual(width, 1800)
        return {"thumburl": "https://upload.wikimedia.org/mock.jpg",
                "extmetadata": {
                    "LicenseShortName": {"value": self.licenses[name]},
                    "LicenseUrl": {"value": "https://creativecommons.org/licenses/mock/"},
                    "Artist": {"value": "<a>Autor documentado</a>"}}}

    def test_lote_completo_sin_internet(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(collector, "imageinfo", side_effect=self.fake_info), \
                 patch.object(collector, "read_url", return_value=b"\xff\xd8\xff" + b"x" * 1300):
                result = collector.collect(Path(folder))
            self.assertEqual(result["descargadas"], 5)
            self.assertEqual(result["no_descargadas"], 0)
            self.assertEqual(len(list(Path(folder).glob("H*.jpg"))), 5)
            self.assertTrue((Path(folder) / "CREDITOS_Y_PROCEDENCIA.md").is_file())
            self.assertTrue((Path(folder) / "REPORTE_DESCARGA_FOTOS.json").is_file())

    def test_licencia_cambiada_bloquea_descarga(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            modified_info = self.fake_info("File:MITS Altair 8800 Front Panel.jpg", 1800)
            modified_info["extmetadata"]["LicenseShortName"]["value"] = "All Rights Reserved"
            with patch.object(collector, "imageinfo", return_value=modified_info), \
                 patch.object(collector, "read_url") as network:
                rec = collector.download_one(self.manifest["fotografias"][0], Path(folder),
                                             1800, collector.MAX_BYTES_TOTAL)
            self.assertEqual(rec["estado"], "NO_DESCARGADA")
            self.assertIn("LICENCIA DISTINTA", rec["incidencia"])
            network.assert_not_called()

    def test_url_ajena_rechazada(self) -> None:
        with self.assertRaisesRegex(ValueError, "lista segura"):
            collector.read_url("https://example.net/imagen.jpg", 2000, {"upload.wikimedia.org"})

    def test_catalogo_con_cinco_fuentes_distintas(self) -> None:
        photos = self.manifest["fotografias"]
        self.assertEqual(len(photos), 5)
        self.assertEqual(len({p["archivo"] for p in photos}), 5)
        self.assertEqual(len({p["pagina_fuente"] for p in photos}), 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
