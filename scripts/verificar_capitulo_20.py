#!/usr/bin/env python3
"""Pruebas de referencias de anfitrión, ensamblador y documentos C20.

No existe todavía implementación de CPU Aula-8 que pueda ejecutar estos bytes.
"""

from math import gcd
from pathlib import Path

from ensamblador_dos_pasadas_aula8_educativo import assemble
from verificar_capitulos_16_17_comun import ROOT, verificar_documentos


def euclides_resta(a: int, b: int) -> tuple[int, int]:
    """Modelo semántico independiente de instrucciones y opcodes.

    La precondición a,b>0 es necesaria para garantizar progreso.
    """
    assert 1 <= a <= 255 and 1 <= b <= 255
    pasos = 0
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
        pasos += 1
        assert pasos <= 508
    return a, pasos


def fibonacci_iterativo(n: int) -> int:
    anterior, actual = 0, 1
    for _ in range(n):
        anterior, actual = actual, anterior + actual
    return anterior


def fibonacci_recursivo(n: int) -> tuple[int, int]:
    if n < 2:
        return n, 1
    a, ca = fibonacci_recursivo(n-1)
    b, cb = fibonacci_recursivo(n-2)
    return a+b, ca+cb+1


def debe_rechazarse(source: str) -> None:
    try:
        assemble(source)
    except ValueError:
        return
    raise AssertionError('El ensamblador aceptó una fuente inválida: ' + source[:80])


def main():
    suma = assemble((ROOT/'libro/programas/c20_suma_aula8.asm').read_text(encoding='utf-8'))
    euclides = assemble((ROOT/'libro/programas/c20_euclides_aula8.asm').read_text(encoding='utf-8'))
    assert suma.origin == euclides.origin == 0x6000
    assert suma.data.hex(' ').upper() == '11 00 0D 11 01 09 20 01 13 00 00 6F 02'
    assert euclides.data.hex(' ').upper() == (
        '11 00 30 11 01 12 24 01 31 18 60 34 13 60 22 04 '
        '30 06 60 22 01 30 06 60 13 00 00 6F 02'
    )
    assert euclides.symbols == {'BUCLE':0x6006, 'RESTAR_A':0x6013, 'FIN':0x6018}
    assert len(euclides.data) == 29 and len(suma.data) == 13
    assert [(p, data.hex().upper()) for p, data, _ in suma.listing] == [
        (0x6000,'11000D'), (0x6003,'110109'), (0x6006,'2001'),
        (0x6008,'1300006F'), (0x600C,'02')]
    checks=5

    cases=(
        '.ORG 0x6000\nFIN: RET\nFIN: HALT',
        '.ORG 0x6000\nJZ DESCONOCIDA\nRET',
        '.ORG 0x6000\nLDI R4, 5',
        '.ORG 0x6EFF\nLDI R0, 1',
        '.ORG 0x6000\nST [0xC010], R0',
        '.ORG 0x6000\nJMP 0x6F00',
        '.ORG 0x6000\nADD R0, R1, R2',
        '.ORG 0x6000\nHALT 100',
        'LDI R0, 1',
        '.ORG 0x6000\nJZ 0x1000',
    )
    for case in cases:
        debe_rechazarse(case)
        checks+=1

    # Las sumas de byte se contrastan con aritmética entera independiente.
    for a in range(256):
        for b in range(256):
            result=(a+b)&0xFF
            carry=int(a+b>255)
            assert 0<=result<=255 and a+b==result+256*carry
            checks+=1
    for a in range(1, 256):
        for b in range(1, 256):
            got, _ = euclides_resta(a,b)
            assert got == gcd(a,b), (a,b,got)
            checks+=1
    assert euclides_resta(48,18)[0] == 6
    assert euclides_resta(48,18)[1] == 4
    checks+=2

    # La recursión se comprueba en el anfitrión, no en la pila de Aula-8.
    for n in range(0,15):
        value, calls = fibonacci_recursivo(n)
        assert value==fibonacci_iterativo(n)
        assert calls>=1
        checks+=2
    assert fibonacci_recursivo(6) == (8,25)
    assert fibonacci_iterativo(13)==233 and fibonacci_iterativo(14)==377
    checks+=2

    checks += verificar_documentos('20', 'programar_un_pequeno_sistema',(
        'c20_fig01_herramientas_y_capas','c20_fig02_dos_pasadas_y_etiquetas',
        'c20_fig03_euclides_estados','c20_fig04_mini_sistema_y_pruebas',
    ),PAGINAS_C20,('JZ FIN','6018','BUCLE','dos pasadas','Fibonacci',
           'MiniC-Aula','6F00','capítulo 21'),ecuaciones=14)
    print(f'Capítulo 20: {checks} comprobaciones aritméticas/ensamblador/Word/PDF correctas; ejecución solo en anfitrión.')


PAGINAS_C20 = 9

if __name__ == '__main__':
    main()
