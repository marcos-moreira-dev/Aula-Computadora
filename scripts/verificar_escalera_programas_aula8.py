#!/usr/bin/env python3
"""Matemática independiente de la escalera futura; NO CPU ni ensamblador."""

from math import gcd
from verificar_capitulos_16_17_comun import ROOT


def euclides_por_restas(a,b):
    assert a>0 and b>0
    while a!=b:
        if a>b:
            a-=b
        else:
            b-=a
    return a


def fib_iterative(n):
    a,b=0,1
    for _ in range(n):
        a,b=b,a+b
    return a


def fib_recursive(n):
    return n if n<2 else fib_recursive(n-1)+fib_recursive(n-2)


def main():
    doc=(ROOT/'libro/ESCALERA_DE_PROGRAMAS_AULA8.md').read_text(encoding='utf-8')
    assert 'Fibonacci' in doc and 'Euclides' in doc and 'Guardar una variable' in doc
    checks=3
    for a in range(1,65):
        for b in range(1,65):
            assert euclides_por_restas(a,b)==gcd(a,b)
            checks+=1
    assert euclides_por_restas(48,18)==6
    for n in range(11):
        assert fib_iterative(n)==fib_recursive(n)
        checks+=1
    assert fib_iterative(6)==8
    assert 13+9==22 and (13+9)&0xFF==0x16
    checks+=3
    print(f'Escalera de programas: {checks} comprobaciones matemáticas en anfitrión; nada ejecutado en Aula-8.')


if __name__=='__main__':
    main()
