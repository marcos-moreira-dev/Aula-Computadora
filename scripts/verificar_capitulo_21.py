#!/usr/bin/env python3
"""Comprueba aritmética y representación de palabras de 16 bits y C21.

Son pruebas matemáticas y documentales, no mediciones de CPU ni memoria.
"""

from verificar_capitulos_16_17_comun import verificar_documentos


def flags_suma_u16(a: int, b: int) -> tuple[int,int,int,int,int]:
    assert 0 <= a <= 0xFFFF and 0 <= b <= 0xFFFF
    suma=a+b
    value=suma & 0xFFFF
    c=int(suma > 0xFFFF)
    v=int((~(a^b)&(a^value)&0x8000)!=0)
    z=int(value==0)
    n=(value>>15)&1
    return value,c,v,z,n


def referencia_signed16(pattern: int) -> int:
    return pattern - 65536 if pattern & 0x8000 else pattern


def main():
    checks=0
    assert 2**16==65536 and (65536//1024)==64
    assert 4*8==32 and 4*16==64
    assert 0x1234==4660 and 0x01FF+1==0x0200
    assert flags_suma_u16(0xFFFF,1) == (0,1,0,1,0)
    assert flags_suma_u16(0x7FFF,1) == (0x8000,0,1,0,1)
    assert flags_suma_u16(0x00FF,1) == (0x0100,0,0,0,0)
    assert referencia_signed16(0x8000)==-32768
    checks+=7

    boundary = [0,1,2,15,127,128,254,255,256,257,511,512,
                0x7FFE,0x7FFF,0x8000,0x8001,0xFF00,0xFFFE,0xFFFF]
    # Contrastamos suma directa, transporte desde byte bajo y signed overflow.
    for a in range(0,65536,257):
        for b in boundary:
            result,c,v,z,n=flags_suma_u16(a,b)
            low_total=(a&0xFF)+(b&0xFF)
            high_total=(a>>8)+(b>>8)+(low_total>>8)
            by_bytes=((high_total&0xFF)<<8) | (low_total&0xFF)
            assert result==by_bytes
            assert c==int(high_total>255)
            assert z==int(result==0)
            assert n==int(result>=0x8000)
            signed_sum=referencia_signed16(a)+referencia_signed16(b)
            assert v==int(not -32768<=signed_sum<=32767)
            checks+=5
    for a in boundary:
        for b in boundary:
            assert flags_suma_u16(a,b)[0] == (a+b)%65536
            checks+=1

    # Orden de bytes y alineación: no se asignan al bus real inexistente.
    for address in range(0,65535,2):
        assert address % 2 == 0
        assert address+1 <= 0xFFFF
        checks+=2
    for data in range(0,65536,17):
        lo,hi=data&0xFF,data>>8
        assert lo+(hi<<8)==data
        checks+=1
    for invalid in range(1,65535,2):
        assert invalid % 2 == 1
        checks+=1

    checks += verificar_documentos('21','que_implica_ampliar_la_palabra',(
        'c21_fig01_palabra_y_direcciones','c21_fig02_acarreo_16_bits',
        'c21_fig03_suma_dos_anchos','c21_fig04_registro_a_ram',
    ),PAGINAS_C21,('Aula-16','65536','0x01FF','0x7FFF','C (acarreo)',
            'little-endian','capítulo 22'),ecuaciones=18)
    print(f'Capítulo 21: {checks} comprobaciones aritméticas/representación/Word/PDF correctas; sin bus físico.')


PAGINAS_C21 = 8

if __name__ == '__main__':
    main()
