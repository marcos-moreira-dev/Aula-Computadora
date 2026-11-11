#!/usr/bin/env python3
"""Modelo anfitrión de memoria con dos carriles y documentos de C22.

No implementa una CPU, arbitraje físico, retardos ni señales de una placa.
"""
from verificar_capitulos_16_17_comun import verificar_documentos

RAM_BYTES = 0x8000
RAM_ROWS = RAM_BYTES // 2


class ModeloBancos:
    def __init__(self):
        self.low = bytearray(RAM_ROWS)
        self.high = bytearray(RAM_ROWS)

    @staticmethod
    def check_byte(addr):
        if not 0 <= addr < RAM_BYTES:
            raise ValueError('dirección fuera de RAM de ejemplo')

    def read_byte(self, addr):
        self.check_byte(addr)
        return (self.high if addr & 1 else self.low)[addr >> 1]

    def write_byte(self, addr, value):
        self.check_byte(addr)
        if not 0 <= value < 256:
            raise ValueError('byte fuera de rango')
        (self.high if addr & 1 else self.low)[addr >> 1] = value

    @staticmethod
    def check_word(addr):
        if addr & 1:
            raise ValueError('palabra desalineada')
        if not 0 <= addr < RAM_BYTES - 1:
            raise ValueError('palabra fuera de RAM')

    def read_word(self, addr):
        self.check_word(addr)
        return self.low[addr >> 1] | (self.high[addr >> 1] << 8)

    def write_word(self, addr, value):
        self.check_word(addr)
        if not 0 <= value <= 0xFFFF:
            raise ValueError('palabra fuera de rango')
        self.low[addr >> 1] = value & 0xFF
        self.high[addr >> 1] = value >> 8


def main():
    mem = ModeloBancos()
    checks = 0
    assert RAM_ROWS == 1 << 14
    assert 0x2000 >> 1 == 0x1000
    assert (0x2000 >> 1) & 0x3FFF == 0x1000
    checks += 3
    for address in range(RAM_BYTES):
        assert (address >> 1) == address // 2
        assert (address & 1) == address % 2
        mem.write_byte(address, address & 0xFF)
        assert mem.read_byte(address) == (address & 0xFF)
        checks += 3
    for address in range(0, RAM_BYTES - 1, 2):
        low, high = mem.read_byte(address), mem.read_byte(address + 1)
        assert mem.read_word(address) == low | (high << 8)
        checks += 1
    for value in range(0, 65536, 17):
        mem.write_word(0x2000, value)
        assert mem.read_byte(0x2000) == (value & 0xFF)
        assert mem.read_byte(0x2001) == (value >> 8)
        assert mem.read_word(0x2000) == value
        checks += 3
    mem.write_word(0x2000, 0x1234)
    mem.write_byte(0x2001, 0xAB)
    assert mem.read_word(0x2000) == 0xAB34
    assert mem.read_byte(0x2000) == 0x34
    checks += 2
    for address in range(1, RAM_BYTES, 2):
        try:
            mem.write_word(address, 0)
        except ValueError:
            pass
        else:
            raise AssertionError(f'word impar permitida: {address:04X}')
        checks += 1
    for addr in (-1, RAM_BYTES, 0xC020, 0xFFFF):
        for fn in (mem.read_byte, lambda a: mem.write_byte(a, 1),
                   mem.read_word, lambda a: mem.write_word(a, 1)):
            try:
                fn(addr)
            except ValueError:
                checks += 1
            else:
                raise AssertionError((addr, fn))
    mem.write_word(RAM_BYTES - 2, 0xBEEF)
    assert mem.read_byte(RAM_BYTES - 2) == 0xEF
    assert mem.read_byte(RAM_BYTES - 1) == 0xBE
    checks += 2
    checks += verificar_documentos('22', 'un_bus_externo_de_16_bits', (
        'c22_fig01_bancos_y_carriles', 'c22_fig02_palabra_y_little_endian',
        'c22_fig03_matriz_operaciones', 'c22_fig04_casos_fallo_bus',
    ), PAGINAS_C22, ('bus externo', '0x2001', 'little-endian', 'C020',
                    'Aula-16', '0x1234', 'capítulo 23'), ecuaciones=13)
    print(f'Capítulo 22: {checks} comprobaciones de modelo y Word/PDF; sin señales físicas.')


PAGINAS_C22 = 8  # Comprobado mediante renderizado e inspección del PDF.


if __name__ == '__main__':
    main()
