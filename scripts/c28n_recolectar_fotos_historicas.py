#!/usr/bin/env python3
"""Recolecta fotos historicas candidatas de Wikimedia Commons en evidencia.

No modifica el libro, no instala software y no declara licencias aprobadas.
Cada imagen se consulta primero en MediaWiki para comprobar licencia y fuente.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "libro" / "FOTOGRAFIAS_HISTORICAS_C28N_MANIFIESTO.json"
MAX_BYTES_PER_FILE = 10 * 1024 * 1024
MAX_BYTES_TOTAL = 35 * 1024 * 1024
AGENT = "AulaComputadora-lector-historico/1.0 (investigacion personal; Wikimedia Commons)"
HEADERS = {"User-Agent": AGENT, "Accept": "application/json,image/jpeg,image/png,*/*"}


def read_url(url: str, limit: int, expected_hosts: set[str], timeout: int = 12) -> bytes:
    host = urlsplit(url).hostname
    if urlsplit(url).scheme != "https" or host not in expected_hosts:
        raise ValueError("URL externa fuera de la lista segura")
    with urlopen(Request(url, headers=HEADERS), timeout=timeout) as resp:
        final = urlsplit(resp.geturl())
        if final.scheme != "https" or final.hostname not in expected_hosts:
            raise ValueError("Redireccion no autorizada")
        if resp.headers.get("Content-Length"):
            if int(resp.headers["Content-Length"]) > limit:
                raise ValueError("Archivo remoto mas grande que el limite")
        chunks = bytearray()
        while True:
            block = resp.read(min(65536, limit + 1 - len(chunks)))
            if not block:
                break
            chunks.extend(block)
            if len(chunks) > limit:
                raise ValueError("Descarga supera el limite")
        return bytes(chunks)


def plain_html(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", value or "")).strip()[:1200]


def common_license(name: str) -> str:
    return " ".join(name.upper().replace("CREATIVE COMMONS", "CC").split())


def imageinfo(name: str, max_width: int) -> dict:
    api = "https://commons.wikimedia.org/w/api.php?" + urlencode({
        "action": "query", "format": "json", "prop": "imageinfo",
        "iiprop": "url|size|extmetadata", "iiurlwidth": str(max_width),
        "titles": name,
    })
    raw = read_url(api, 2 * 1024 * 1024, {"commons.wikimedia.org"})
    pages = json.loads(raw)["query"]["pages"]
    if len(pages) != 1:
        raise ValueError("Resultado ambiguo en Commons")
    page = next(iter(pages.values()))
    if page.get("missing") is not None or not page.get("imageinfo"):
        raise ValueError("Imagen inexistente o sin metadatos")
    return page["imageinfo"][0]


def download_one(item: dict, dest: Path, max_width: int, free_bytes: int) -> dict:
    record = {"id": item["id"], "archivo": item["archivo"],
              "pagina_fuente": item["pagina_fuente"],
              "autor_catalogo": item["autor_documentado"],
              "licencia_esperada": item["licencia_esperada"],
              "licencia_url_catalogo": item["url_licencia"],
              "capitulos_propuestos": item["uso_propuesto"],
              "estado": "PENDIENTE", "uso_editorial": "REQUIERE_REVISION"}
    try:
        filename = item["archivo"]
        if not re.fullmatch(r"[A-Za-z0-9_\-]+\.(jpg|jpeg|png)", filename):
            raise ValueError("Nombre de archivo no seguro")
        info = imageinfo(item["titulo_commons"], max_width)
        meta = info.get("extmetadata", {})
        lic = plain_html(meta.get("LicenseShortName", {}).get("value", ""))
        licurl = plain_html(meta.get("LicenseUrl", {}).get("value", ""))
        autor = plain_html(meta.get("Artist", {}).get("value", ""))
        record.update(licencia_commons=lic, url_licencia_commons=licurl,
                      autor_commons=autor, fecha_consulta_utc=datetime.now(timezone.utc).isoformat())
        if common_license(lic) != common_license(item["licencia_esperada"]):
            raise ValueError("LICENCIA DISTINTA: descarga detenida; requiere revision")
        image_url = info.get("thumburl") or info.get("url")
        if not image_url:
            raise ValueError("Commons no devolvio URL para imagen")
        max_allowed = min(MAX_BYTES_PER_FILE, free_bytes)
        if max_allowed < 1024:
            raise ValueError("Limite total de descargas alcanzado")
        data = read_url(image_url, max_allowed,
                        {"upload.wikimedia.org", "thumb.wikimedia.org"}, timeout=20)
        if filename.lower().endswith((".jpg", ".jpeg")) and not data.startswith(b"\xff\xd8\xff"):
            raise ValueError("Contenido descargado no es JPEG")
        if filename.lower().endswith(".png") and not data.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Contenido descargado no es PNG")
        if len(data) < 1024:
            raise ValueError("Imagen inesperadamente pequena")
        target = dest / filename
        if target.exists():
            raise ValueError("Archivo de destino ya existe; no se sobrescribe")
        with target.open("xb") as fd:
            fd.write(data)
        record.update(estado="DESCARGADA", bytes=len(data),
                      sha256=hashlib.sha256(data).hexdigest(),
                      url_archivo=image_url, ruta_evidencia=target.name)
    except Exception as exc:
        record.update(estado="NO_DESCARGADA", incidencia=str(exc)[:500])
    return record


def collect(out: Path, manifest_path: Path = CATALOG) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = []
    total_bytes = 0
    for index, item in enumerate(manifest["fotografias"], 1):
        print(f"  [{index}/{len(manifest['fotografias'])}] {item['id']}...", flush=True)
        result = download_one(item, out, manifest["ancho_maximo_px"], MAX_BYTES_TOTAL - total_bytes)
        records.append(result)
        if result["estado"] == "DESCARGADA":
            total_bytes += result["bytes"]
        print(f"      {result['estado']}: {result.get('incidencia', result.get('bytes', ''))}", flush=True)
    success = sum(r["estado"] == "DESCARGADA" for r in records)
    report = {"version": manifest["version"], "total_catalogadas": len(records),
              "descargadas": success, "no_descargadas": len(records) - success,
              "bytes_total": total_bytes, "fotografias": records,
              "nota": "No incorporar al libro sin inspeccion visual y atribucion correcta de licencias CC."}
    (out / "REPORTE_DESCARGA_FOTOS.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    credits = ["# Fotografias historicas candidatas para Aula-Computadora", "",
               "**No publicar todavia.** Revisar cada foto, su licencia, autor y posible recorte.", ""]
    for entry in records:
        credits.extend([f"## {entry['id']} — {entry['estado']}", "",
                        f"- Fuente: {entry['pagina_fuente']}",
                        f"- Autor catalogado: {entry['autor_catalogo']}",
                        f"- Autor/metadatos de Commons: {entry.get('autor_commons', 'No disponible')}",
                        f"- Licencia: {entry.get('licencia_commons', 'No comprobada')}",
                        f"- Texto de licencia: {entry.get('url_licencia_commons') or entry['licencia_url_catalogo']}",
                        f"- Uso propuesto: {entry['capitulos_propuestos']}",
                        f"- SHA-256: {entry.get('sha256', 'No descargada')}", ""])
    (out / "CREDITOS_Y_PROCEDENCIA.md").write_text("\n".join(credits), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = collect(args.salida)
        print(f"FOTOS C28-N: {report['descargadas']}/{report['total_catalogadas']} descargadas")
        return 0  # descargarlas es auxiliar, no invalida controles logicos
    except Exception as exc:
        args.salida.mkdir(parents=True, exist_ok=True)
        (args.salida / "ERROR_RECOLECTOR.txt").write_text(repr(exc), encoding="utf-8")
        print(f"RECOLECTOR C28-N: error auxiliar: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
