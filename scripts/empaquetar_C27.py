#!/usr/bin/env python3
"""Entrega C27 reproducible: ZIP global, parche relativo a C26 y 12 trozos.

No elimina la base C26. Las copias binarias históricas C25/C26 no se incluyen
en el ZIP global para no multiplicar descargas de una edición reemplazada.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / 'Aula-Computadora'
OUT = ROOT.parent
GLOBAL = OUT / 'Aula_Computadora_C27_GLOBAL.zip'
PATCH = OUT / 'Aula_Computadora_C27_PATCH_DESDE_C26.zip'
MANIFEST = OUT / 'MANIFIESTO_ENTREGA_C27.json'
PREFIX = 'Aula-Computadora/'
PARTS = 12


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def keep(rel):
    if any(piece in {'__pycache__', '.git', 'node_modules'} for piece in rel.parts):
        return False
    if rel.name in {
        'Aula_Computadora_C25_0_1_MAESTRO.docx',
        'Aula_Computadora_C25_0_1_MAESTRO.pdf',
        'Aula_Computadora_C26_0_1_MAESTRO.docx',
        'Aula_Computadora_C26_0_1_MAESTRO.pdf',
    }:
        return False
    return True


def buildzip(path, files):
    with ZipFile(path, 'w', compression=ZIP_DEFLATED, compresslevel=6,
                 allowZip64=True) as z:
        for src in files:
            relative = src.relative_to(ROOT)
            z.write(src, PREFIX + relative.as_posix())
    with ZipFile(path) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(files)


def splitzip(path):
    byte_count = path.stat().st_size
    chunk = math.ceil(byte_count / PARTS)
    result = []
    with path.open('rb') as read:
        for i in range(1, PARTS + 1):
            dest = OUT / f'{path.name}.part{i:02d}'
            with dest.open('wb') as write:
                remaining = chunk
                while remaining > 0:
                    data = read.read(min(1024 * 1024, remaining))
                    if not data:
                        break
                    write.write(data)
                    remaining -= len(data)
            assert dest.stat().st_size > 0
            result.append({'archivo': dest.name, 'bytes': dest.stat().st_size,
                           'sha256': digest(dest)})
        assert read.read(1) == b''
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', type=Path, default=BASE)
    args = ap.parse_args()
    base = args.base.resolve()
    assert base.is_dir(), f'Base C26 ausente para calcular el parche: {base}'
    must = [ROOT / 'libro' / ('Aula_Computadora_C27_0_1_MAESTRO.' + e)
            for e in ('pdf', 'docx')]
    assert all(f.is_file() and f.stat().st_size > 1_000_000 for f in must)
    files = sorted((f for f in ROOT.rglob('*') if f.is_file()
                    and keep(f.relative_to(ROOT))), key=lambda p: p.as_posix())
    updated = []
    for path in files:
        old = base / path.relative_to(ROOT)
        if not old.exists() or digest(old) != digest(path):
            updated.append(path)
    buildzip(GLOBAL, files)
    buildzip(PATCH, updated)
    parts = splitzip(GLOBAL)
    manifest = {
        'revision': 'C27-0.1',
        'base': 'C26-0.1 (preservada)',
        'repositorio_archivos': len(files),
        'parche_archivos': len(updated),
        'global': {'archivo': GLOBAL.name, 'bytes': GLOBAL.stat().st_size,
                   'sha256': digest(GLOBAL)},
        'parche': {'archivo': PATCH.name, 'bytes': PATCH.stat().st_size,
                   'sha256': digest(PATCH)},
        'partes_global': parts,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
                        encoding='utf-8')
    print(f'GLOBAL: {GLOBAL.name}, {len(files)} archivos, {GLOBAL.stat().st_size:,} bytes')
    print(f'PARCHE: {PATCH.name}, {len(updated)} archivos, {PATCH.stat().st_size:,} bytes')
    print(f'TROZOS: {len(parts)}; MANIFIESTO: {MANIFEST.name}')


if __name__ == '__main__':
    main()
