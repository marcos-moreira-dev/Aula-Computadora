#!/usr/bin/env python3
"""Empaquetar C25 global y parche acumulativo sobre C24 sin borrar archivos."""
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT.parent
BASE=FOLDER/'Aula_Computadora_C24_0_1_GLOBAL.zip'
FULL=FOLDER/'Aula_Computadora_C25_0_1_GLOBAL.zip'
PATCH=FOLDER/'Aula_Computadora_C24_0_1_A_C25_0_1_PATCH.zip'
PREFIX='Aula-Computadora/'


def inventory():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and not any(part in {'.git','__pycache__','.pytest_cache','.mypy_cache'}
                              for part in p.relative_to(ROOT).parts)
                  and not p.name.endswith(('.pyc','.pyo')))


def name(path):
    return PREFIX+path.relative_to(ROOT).as_posix()


def main():
    if not BASE.is_file():
        raise FileNotFoundError(BASE)
    for out in (FULL,PATCH):
        if out.exists():
            raise FileExistsError(f'Para no sobrescribir, mueve o versiona primero: {out}')
    with ZipFile(BASE) as arc:
        assert arc.testzip() is None
        old={r.filename:sha256(arc.read(r)).digest() for r in arc.infolist() if not r.is_dir()}
    batch=inventory()
    now={name(p):sha256(p.read_bytes()).digest() for p in batch}
    deleted=sorted(set(old)-set(now))
    if deleted:
        raise ValueError(f'Una fusión por superposición no puede borrar {deleted[:8]}')
    changes=[p for p in batch if now[name(p)] != old.get(name(p))]
    for dest,items in ((FULL,batch),(PATCH,changes)):
        with ZipFile(dest,'x',ZIP_DEFLATED,compresslevel=6) as arc:
            for item in items: arc.write(item,name(item))
        with ZipFile(dest) as arc:
            assert arc.testzip() is None
        print(f'{dest.name}: {len(items)} entradas; {dest.stat().st_size:,} bytes')
    with ZipFile(PATCH) as arc:
        merged={**old,**{r.filename:sha256(arc.read(r)).digest()
                         for r in arc.infolist() if not r.is_dir()}}
    assert merged==now,'El parche no recompone el contenido exacto del global'
    print(f'FUSIÓN VALIDADA POR SHA-256: {len(now)} archivos, {len(changes)} modificados/nuevos')


if __name__=='__main__':
    main()
