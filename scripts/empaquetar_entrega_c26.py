#!/usr/bin/env python3
"""Construye la entrega C26 y un parche sobre C25, sin borrar archivos."""
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT.parent
BASE = DIST / 'Aula_Computadora_C25_0_1_GLOBAL.zip'
FULL = DIST / 'Aula_Computadora_C26_0_1_GLOBAL.zip'
PATCH = DIST / 'Aula_Computadora_C25_0_1_A_C26_0_1_PATCH.zip'
PREFIX = 'Aula-Computadora/'


def inventory():
    return sorted(
        path for path in ROOT.rglob('*') if path.is_file()
        and not any(part in {'.git', '__pycache__', '.pytest_cache', '.mypy_cache'}
                    for part in path.relative_to(ROOT).parts)
        and not path.name.endswith(('.pyc', '.pyo'))
    )


def archive_name(path):
    return PREFIX + path.relative_to(ROOT).as_posix()


def main():
    if not BASE.is_file():
        raise FileNotFoundError(f'Base C25 ausente: {BASE}')
    for output in (FULL, PATCH):
        if output.exists():
            raise FileExistsError(f'Conservar versiones: no sobrescribir {output}')

    with ZipFile(BASE) as arc:
        assert arc.testzip() is None
        old = {entry.filename: sha256(arc.read(entry)).digest()
               for entry in arc.infolist() if not entry.is_dir()}

    files = inventory()
    current = {archive_name(path): sha256(path.read_bytes()).digest()
               for path in files}
    deleted = sorted(set(old) - set(current))
    if deleted:
        raise ValueError(f'El parche por superposición no debe borrar: {deleted[:8]}')

    changed = [path for path in files if current[archive_name(path)] != old.get(archive_name(path))]
    for destination, selected in ((FULL, files), (PATCH, changed)):
        with ZipFile(destination, 'x', ZIP_DEFLATED, compresslevel=6) as arc:
            for path in selected:
                arc.write(path, archive_name(path))
        with ZipFile(destination) as arc:
            assert arc.testzip() is None
        print(f'{destination}: {len(selected)} entradas, {destination.stat().st_size:,} bytes')

    with ZipFile(PATCH) as arc:
        reconstructed = {**old, **{entry.filename: sha256(arc.read(entry)).digest()
                                  for entry in arc.infolist() if not entry.is_dir()}}
    assert reconstructed == current, 'Los bytes reconstruidos no son idénticos a C26'
    print(f'FUSIÓN C25 + C26 CORRECTA: {len(current)} archivos, {len(changed)} incorporados/modificados')


if __name__ == '__main__':
    main()
