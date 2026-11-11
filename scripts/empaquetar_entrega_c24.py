#!/usr/bin/env python3
"""C24 global y parche exacto contra C23 global, sin sobrescribir entradas.

La comparación se realiza por SHA-256 de contenidos. Se excluyen cachés,
no los fuentes, Word, PDF, figuras ni archivos ocultos de configuración.
"""
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT.parent
BASE = FOLDER / 'Aula_Computadora_C23_0_1_GLOBAL.zip'
FULL = FOLDER / 'Aula_Computadora_C24_0_1_GLOBAL.zip'
PATCH = FOLDER / 'Aula_Computadora_C23_0_1_A_C24_0_1_PATCH.zip'
PREFIX = 'Aula-Computadora/'


def inventory():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and not any(part in {'.git','__pycache__','.pytest_cache','.mypy_cache'}
                              for part in p.relative_to(ROOT).parts)
                  and not p.name.endswith(('.pyc','.pyo')))


def packaged_name(path):
    return PREFIX + path.relative_to(ROOT).as_posix()


def run():
    if not BASE.is_file():
        raise FileNotFoundError(f'Base obligatoria de comparación: {BASE}')
    for output in (FULL,PATCH):
        if output.exists():
            raise FileExistsError(f'No se permite sobrescribir: {output}')
    with ZipFile(BASE) as archive:
        assert archive.testzip() is None
        old={row.filename:sha256(archive.read(row)).digest()
             for row in archive.infolist() if not row.is_dir()}
    batch=inventory()
    current={packaged_name(p):sha256(p.read_bytes()).digest() for p in batch}
    removed=sorted(set(old)-set(current))
    if removed:
        raise ValueError(f'El paquete anterior tiene {len(removed)} archivos ausentes; '
                         f'un parche por superposición no podría quitarlos: {removed[:10]}')
    changed=[p for p in batch if old.get(packaged_name(p))!=current[packaged_name(p)]]
    for target,items in ((FULL,batch),(PATCH,changed)):
        with ZipFile(target,'x',ZIP_DEFLATED,compresslevel=6) as archive:
            for p in items:
                archive.write(p,packaged_name(p))
        with ZipFile(target) as archive:
            assert archive.testzip() is None
        print(f'{target.name}: {len(items)} archivos, {target.stat().st_size:,} bytes')
    # Un parche por superposición debe reconstruir exactamente el ZIP global
    # como conjunto de rutas/hash, aunque metadatos de contenedor difieran.
    with ZipFile(PATCH) as zip_patch:
        overlay={**old,**{r.filename:sha256(zip_patch.read(r)).digest()
                          for r in zip_patch.infolist() if not r.is_dir()}}
    assert overlay==current,'La superposición del parche no coincide con el GLOBAL'
    print(f'FUSIÓN SHA-256 VALIDADA: {len(current)} rutas; {len(changed)} modificadas/nuevas.')
    print('Los paquetes C23 de entrada permanecen intactos.')


if __name__=='__main__':
    run()
