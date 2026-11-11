#!/usr/bin/env python3
"""Produce entrega global C23 y parche mínimo relativo al ZIP C21-0.3.

Se comparan bytes por hash. Nunca borra ni modifica el ZIP de entrada.
"""
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

BASE = Path(__file__).resolve().parents[1]
WORKSPACE = BASE.parent
PREV = WORKSPACE / 'Aula_Computadora_C21_0_3_GLOBAL.zip'
FULL = WORKSPACE / 'Aula_Computadora_C23_0_1_GLOBAL.zip'
PATCH = WORKSPACE / 'Aula_Computadora_C21_0_3_A_C23_0_1_PATCH.zip'
PREFIX = 'Aula-Computadora/'


def files():
    return sorted(
        p for p in BASE.rglob('*') if p.is_file()
        and not any(s in ('.git', '__pycache__', '.pytest_cache', '.mypy_cache') for s in p.relative_to(BASE).parts)
        and not p.name.endswith(('.pyc', '.pyo'))
    )


def run():
    if not PREV.is_file():
        raise FileNotFoundError(f'No se encontró la base inalterada: {PREV}')
    for output in (FULL, PATCH):
        if output.exists():
            raise FileExistsError(f'La salida ya existe (no sobrescribimos): {output}')
    with ZipFile(PREV) as z:
        previous = {info.filename: sha256(z.read(info)).digest() for info in z.infolist() if not info.is_dir()}
    all_files = files()
    modified = []
    for p in all_files:
        entry = PREFIX + p.relative_to(BASE).as_posix()
        if previous.get(entry) != sha256(p.read_bytes()).digest():
            modified.append(p)
    for destination, batch in ((FULL, all_files), (PATCH, modified)):
        with ZipFile(destination, 'x', compression=ZIP_DEFLATED, compresslevel=6) as zipout:
            for p in batch:
                zipout.write(p, PREFIX + p.relative_to(BASE).as_posix())
        with ZipFile(destination) as zipcheck:
            if zipcheck.testzip() is not None:
                raise AssertionError(f'ZIP corrupto: {destination}')
        print(f'{destination.name}: {len(batch)} archivos, {destination.stat().st_size:,} bytes')
    print('Parche relativo al C21-0.3:')
    for p in modified:
        print(' -', p.relative_to(BASE))


if __name__ == '__main__':
    run()
