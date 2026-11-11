#!/usr/bin/env python3
"""Comprueba fórmulas de vídeo hipotéticas sin simular CPU ni hardware físico.

Uso: python3 scripts/verificar_modelo_video_texto_grafico.py
No modifica archivos, no reserva MMIO y no aprueba un controlador gráfico.
"""

from __future__ import annotations


WIDTH = 256
HEIGHT = 128
COLS = WIDTH // 8
ROWS = HEIGHT // 8


def ubicacion_pixel(x: int, y: int, bits: int) -> tuple[int, int]:
    """Devuelve (índice de byte, desplazamiento) con píxeles MSB primero."""
    if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
        raise ValueError("Píxel fuera de pantalla")
    if bits not in (1, 2):
        raise ValueError("Solo modelos de 1 o 2 bpp")
    pixeles_por_byte = 8 // bits
    bytes_fila = WIDTH // pixeles_por_byte
    return y * bytes_fila + x // pixeles_por_byte, (pixeles_por_byte - 1 - (x % pixeles_por_byte)) * bits


def escribir_pixel(vram: bytearray, x: int, y: int, bits: int, valor: int) -> None:
    if not 0 <= valor < (1 << bits):
        raise ValueError("Índice de color fuera de rango")
    indice, desplazamiento = ubicacion_pixel(x, y, bits)
    mascara = ((1 << bits) - 1) << desplazamiento
    vram[indice] = (vram[indice] & (~mascara & 0xFF)) | (valor << desplazamiento)


def leer_pixel(vram: bytearray, x: int, y: int, bits: int) -> int:
    indice, desplazamiento = ubicacion_pixel(x, y, bits)
    return (vram[indice] >> desplazamiento) & ((1 << bits) - 1)


def glifo_encendido(fuente: bytes, codigo: int, u: int, v: int) -> bool:
    if not (len(fuente) == 256 * 8 and 0 <= codigo < 256 and 0 <= u < 8 and 0 <= v < 8):
        raise ValueError("Glifo o coordenada inválida")
    return bool(fuente[codigo * 8 + v] & (0x80 >> u))


def verificar() -> int:
    comprobaciones = 0
    assert COLS == 32 and ROWS == 16
    assert COLS * ROWS == 512
    assert 256 * 8 == 2048  # ROM de 256 glifos de 8 filas.
    assert WIDTH * HEIGHT // 8 == 4096
    assert WIDTH * HEIGHT * 2 // 8 == 8192
    assert WIDTH * HEIGHT * 4 // 8 == 16384
    assert WIDTH * HEIGHT * 8 // 8 == 32768
    comprobaciones += 8

    for bits, tamano in ((1, 4096), (2, 8192)):
        vram = bytearray(tamano)
        posiciones: set[tuple[int, int]] = set()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                indice, desplazamiento = ubicacion_pixel(x, y, bits)
                assert 0 <= indice < tamano
                assert 0 <= desplazamiento <= 8 - bits
                assert (indice, desplazamiento) not in posiciones
                posiciones.add((indice, desplazamiento))
                comprobaciones += 3
        assert len(posiciones) == WIDTH * HEIGHT
        comprobaciones += 1

        for x, y in ((0, 0), (7, 0), (8, 0), (255, 127), (0, 127), (255, 0)):
            for valor in range(1 << bits):
                escribir_pixel(vram, x, y, bits, valor)
                assert leer_pixel(vram, x, y, bits) == valor
                comprobaciones += 1

        for x, y in ((0, 0), (7, 0), (8, 0), (255, 127), (0, 127), (255, 0)):
            escribir_pixel(vram, x, y, bits, 0)
            assert leer_pixel(vram, x, y, bits) == 0
            comprobaciones += 1

    assert ubicacion_pixel(0, 0, 1) == (0, 7)
    assert ubicacion_pixel(7, 0, 1) == (0, 0)
    assert ubicacion_pixel(8, 0, 1) == (1, 7)
    assert ubicacion_pixel(255, 127, 1) == (4095, 0)
    assert ubicacion_pixel(255, 127, 2) == (8191, 0)
    comprobaciones += 5

    # Patrón original y explícito, sin copiar ROM o fuente comercial.
    a_original = bytes((0x18, 0x24, 0x42, 0x7E, 0x42, 0x42, 0x42, 0x00))
    fuente = bytearray(256 * 8)
    fuente[ord("A") * 8 : ord("A") * 8 + 8] = a_original
    for v, fila in enumerate(a_original):
        for u in range(8):
            assert glifo_encendido(fuente, ord("A"), u, v) == bool(fila & (0x80 >> u))
            comprobaciones += 1
    assert not any(glifo_encendido(fuente, ord("B"), u, v) for u in range(8) for v in range(8))
    comprobaciones += 1

    for x, y, bits in ((-1, 0, 1), (256, 0, 1), (0, 128, 2), (0, 0, 4)):
        try:
            ubicacion_pixel(x, y, bits)
        except ValueError:
            comprobaciones += 1
        else:
            raise AssertionError("Se aceptó coordenada o bpp inválidos")

    print(f"MATEMATICA DE PIXELES 1/2 BPP: {comprobaciones} comprobaciones de modelo anfitrión correctas.")
    print("Hay un contrato lógico Aula V1 de cuatro colores; no hay CPU, controlador ni monitor físico ejecutados.")
    return comprobaciones


if __name__ == "__main__":
    verificar()
