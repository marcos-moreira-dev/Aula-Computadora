#!/usr/bin/env python3
"""Contrasta bloque de 256, lectura/escritura y artefactos C19 en anfitrión."""

import json
from pathlib import Path
import tempfile

from generar_diagramas_tecnicos_aula8 import check_contracts
from modelo_bloques_aula8_r0_12 import (
    BLOCK_SIZE, COMMAND, REGISTER_MAP, STATUS, BlockController, FileBlockImage,
    plan_future_load,
)
from verificar_capitulos_16_17_comun import ROOT, verificar_documentos


def main():
    _, spec, _, regs = check_contracts()
    assert not spec['native_loader_implemented'] and not spec['filesystem_implemented']
    assert not spec['physical_power_loss_safe'] and not spec['firmware_implemented']
    assert BLOCK_SIZE == spec['transfer']['block_bytes'] == 256
    checks = 3

    for block in range(65536):
        address = block*256
        assert address % 256 == 0
        assert address+255 == (block+1)*256-1
        assert (block & 0xFF) | ((block >> 8) << 8) == block
        checks += 3

    assert [int(regs[name], 16) for name in (
        'COMMAND','STATUS','BLOCK_LO','BLOCK_HI','DATA','ERROR','COUNT_LO','COUNT_HI')
            ] == [0xC010,0xC012,0xC014,0xC016,0xC018,0xC01A,0xC01C,0xC01E]
    assert STATUS == {'BUSY':1, 'DRQ':2, 'DONE':4, 'ERROR':8}
    checks += 2

    future = spec['future_load']
    assert plan_future_load('LOAD 0002 1000 02', 8, future) == [
        (2, 0x1000), (3, 0x1100)]
    assert plan_future_load('LOAD 0001 6000 01', 8, future) == [
        (1, 0x6000)]
    checks += 2

    for count in range(1, 8193):
        expected = (count+255)//256
        assert (expected-1)*256 < count <= expected*256
        checks += 1
    assert (4096+255)//256 == 16
    assert (4097+255)//256 == 17
    assert (32+7+255)//256 == 1 and 256-32-7 == 217
    assert 0x1000+2*256-1 == 0x11FF
    checks += 4

    # El periférico de archivo del anfitrión comprueba el hito de 256 bytes.
    with tempfile.TemporaryDirectory(prefix='aula_c19_') as folder:
        image_file = Path(folder)/'imagen.bin'
        image = FileBlockImage.create(image_file, 8)
        controller = BlockController(image)
        for first_byte in range(0,256,16):
            block = bytes([first_byte])+bytes(range(1,256))
            controller.write(REGISTER_MAP['BLOCK_LO'], 1)
            controller.write(REGISTER_MAP['BLOCK_HI'], 0)
            controller.write(REGISTER_MAP['COMMAND'], COMMAND['WRITE'])
            assert controller.read(REGISTER_MAP['STATUS']) == 3
            for byte in block[:255]:
                controller.write(REGISTER_MAP['DATA'], byte)
            assert FileBlockImage(image_file).read_block(1) != block
            assert controller.read(REGISTER_MAP['COUNT_LO']) == 255
            controller.write(REGISTER_MAP['DATA'], block[255])
            assert controller.read(REGISTER_MAP['STATUS']) == 4
            assert FileBlockImage(image_file).read_block(1) == block
            controller.write(REGISTER_MAP['COMMAND'], COMMAND['RESET'])
            controller.write(REGISTER_MAP['COMMAND'], COMMAND['READ'])
            echoed = bytes(controller.read(REGISTER_MAP['DATA']) for _ in range(256))
            assert echoed == block
            assert controller.read(REGISTER_MAP['COUNT_LO']) == 0
            assert controller.read(REGISTER_MAP['COUNT_HI']) == 1
            assert controller.read(REGISTER_MAP['STATUS']) == 4
            checks += 9

    raw_program=bytes.fromhex(spec['acceptance_sample']['initial_code_hex'])
    assert raw_program == bytes.fromhex('11 00 41 35 00 FF 02')
    assert len(raw_program)==7
    assert spec['acceptance_sample']['trailing_bytes']==249
    assert not spec['acceptance_sample']['executable_tested_on_aula_cpu']
    checks += 4

    checks += verificar_documentos('19','guardar_y_recuperar_programas',(
        'c19_fig01_bloques_y_offsets','c19_fig02_registros_controlador',
        'c19_fig03_estados_transferencia','c19_fig04_carga_cruda_y_aex1',
    ),8,('256','C018','STATUS','0002','0100','LOAD','LOADX',
          'AEX1','CRC','C010','capítulo 20'),ecuaciones=15)
    print(f'Capítulo 19: {checks} comprobaciones de bloques/contratos/Word/PDF correctas; no CPU, ROM ni soporte físico probados.')


if __name__=='__main__':
    main()
