#!/usr/bin/env python3
"""Aplica la auditoría de la edición maestra al archivo C27 independiente."""

import generar_libro_maestro as maestro
import verificar_libro_maestro as verificador


verificador.OUTPUT = maestro.ROOT / 'libro' / 'Aula_Computadora_C27_0_1_MAESTRO.docx'
verificador.PDF = verificador.OUTPUT.with_suffix('.pdf')
verificador.PAGE_INDEX = maestro.ROOT / 'libro' / 'INDICE_C27_0_1.json'


if __name__ == '__main__':
    verificador.verify()
