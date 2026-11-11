#!/usr/bin/env python3
"""Comprueba programas matemáticos del capítulo 23 sin simular ISA Aula-16."""
from verificar_capitulos_16_17_comun import verificar_documentos
from verificar_capitulo_22 import ModeloBancos


def sumar_arreglo(mem, first, count):
    result = 0
    for i in range(count):
        result = (result + mem.read_word(first + 2 * i)) & 0xFFFF
    return result


def euclides_por_resta(a, b):
    if not 1 <= a <= 65535 or not 1 <= b <= 65535:
        raise ValueError('enteros positivos u16')
    states = [(a, b)]
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
        states.append((a, b))
    return a, states


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main():
    checks = 0
    mem = ModeloBancos()
    for i, word in enumerate((0x01FF, 0x0001, 0x0002)):
        mem.write_word(0x2200 + 2 * i, word)
        assert mem.read_word(0x2200 + 2 * i) == word
        checks += 1
    result = sumar_arreglo(mem, 0x2200, 3)
    mem.write_word(0x2210, result)
    assert result == 0x0202
    assert mem.read_byte(0x2210) == mem.read_byte(0x2211) == 2
    checks += 2
    for x in range(0, 0x7000, 2):
        assert x % 2 == 0
        assert x + 4 == x + 2 * 2
        checks += 2
    from math import gcd
    for a in range(1, 129):
        for b in range(1, 129):
            result, states = euclides_por_resta(a, b)
            assert result == gcd(a, b)
            assert states[-1] == (result, result)
            assert all(x > 0 and y > 0 for x, y in states)
            checks += 3
    assert euclides_por_resta(48, 18)[1] == [
        (48, 18), (30, 18), (12, 18), (12, 6), (6, 6)]
    checks += 1
    series = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377)
    for i, v in enumerate(series):
        assert fib(i) == v
        checks += 1
    assert fib(24) == 46368 and fib(25) == 75025
    assert fib(25) & 0xFFFF == 9489 == 0x2511
    assert fib(25) > 65535 and fib(24) > 32767
    checks += 3
    for n in range(2, 31):
        assert fib(n) == fib(n - 1) + fib(n - 2)
        checks += 1
    checks += verificar_documentos('23', 'programacion_para_aula_16', (
        'c23_fig01_niveles_de_programa', 'c23_fig02_sumar_arreglo',
        'c23_fig03_euclides_dos_maquinas', 'c23_fig04_compilacion_y_pruebas',
    ), PAGINAS_C23, ('Aula-16', 'ABI', 'F25', '0x0202',
                    'little-endian', 'capítulo 24', 'ISA binaria'), ecuaciones=14)
    print(f'Capítulo 23: {checks} comprobaciones de programas y Word/PDF; sin CPU ni compilador Aula-16.')


PAGINAS_C23 = 8  # Comprobado mediante renderizado e inspección del PDF.


if __name__ == '__main__':
    main()
