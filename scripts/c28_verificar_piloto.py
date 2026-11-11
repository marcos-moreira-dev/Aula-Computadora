#!/usr/bin/env python3
"""Verificacion determinista del contrato C28-A sin simulador HDL externo.

Compara un modelo de compuertas NAND y flanco D con un oraculo conductual.
No verifica demoras, riesgos, cargas electricas ni circuitos de silicio.
"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOTO = ROOT / 'c28_a' / 'piloto_registro8'


def nand(a, b):
    return 1 - (a & b)


def mux_en_nand(seleccion, dato, retenido):
    """MUX de cuatro NAND con inversor de seleccion; no usa if."""
    inv = nand(seleccion, seleccion)
    hacia_retenido = nand(retenido, inv)
    hacia_dato = nand(dato, seleccion)
    return nand(hacia_retenido, hacia_dato)


class Registro8Compuertas:
    def __init__(self):
        self.q = None  # X, nunca se inventa un cero de encendido.
        self.clk_anterior = 0

    def evaluar(self, clk, load, oe_n, dato):
        if self.clk_anterior == 0 and clk == 1:
            if self.q is None:
                # Si LOAD=0, el estado sigue desconocido; LOAD=1 fija cada bit.
                if load:
                    self.q = sum(mux_en_nand(1, (dato >> b) & 1, 0) << b
                                 for b in range(8))
            else:
                self.q = sum(mux_en_nand(load, (dato >> b) & 1,
                                         (self.q >> b) & 1) << b
                             for b in range(8))
        self.clk_anterior = clk
        return 'ZZZZZZZZ' if oe_n else self.q


class Oraculo:
    def __init__(self):
        self.q = None
        self.clock = 0

    def evaluar(self, clk, load, oe_n, dato):
        if clk and not self.clock and load:
            self.q = dato
        self.clock = clk
        return 'ZZZZZZZZ' if oe_n else self.q


def comprobar(estado, reloj, carga, habilitacion_invertida, dato, nombre):
    real = estado.evaluar(reloj, carga, habilitacion_invertida, dato)
    ideal = nombre.evaluar(reloj, carga, habilitacion_invertida, dato)
    assert real == ideal, (real, ideal, reloj, carga, habilitacion_invertida, dato)
    return real


def main():
    contrato = json.loads((PILOTO / 'registro8_contrato.json').read_text(encoding='utf-8'))
    assert contrato['anchura_bits'] == 8 and contrato['celdas'] == 8
    assert [e['tipo'] for e in contrato['elementos_por_celda']] == [
        'multiplexor_2_a_1', 'flip_flop_D', 'buffer_tres_estados']
    assert contrato['sin_reset_implicitamente'] is True
    assert contrato['senales_comunes'] == {
        'CLK': 'flanco_ascendente', 'LOAD': 'activo_alto', 'OE_n': 'activo_bajo'}

    pruebas = 0
    maquina, oraculo = Registro8Compuertas(), Oraculo()
    # Encender sin reset: Q desconocido, independientemente del valor de IN.
    assert comprobar(maquina, 0, 0, 0, 123, oraculo) is None
    pruebas += 1
    assert comprobar(maquina, 0, 0, 1, 123, oraculo) == 'ZZZZZZZZ'
    pruebas += 1
    # El primer flanco con LOAD=0 no corrige el estado desconocido.
    assert comprobar(maquina, 1, 0, 0, 23, oraculo) is None
    pruebas += 1
    comprobar(maquina, 0, 1, 0, 0, oraculo)
    pruebas += 1
    # Agotar 256*256 parejas de antiguo y nuevo; con/sin LOAD, flanco y OE.
    for anterior in range(256):
        comprobar(maquina, 1, 1, 0, anterior, oraculo)
        pruebas += 1
        comprobar(maquina, 0, 0, 1, anterior, oraculo)
        pruebas += 1
        for nuevo in range(256):
            # HOLD con flanco, incluso si cambia IN.
            assert comprobar(maquina, 1, 0, 0, nuevo, oraculo) == anterior
            pruebas += 1
            comprobar(maquina, 0, 1, 1, nuevo, oraculo)
            pruebas += 1
            # LOAD en flanco: Q captura nuevo.
            assert comprobar(maquina, 1, 1, 0, nuevo, oraculo) == nuevo
            pruebas += 1
            # Entrada cambiante con CLK alto: no aparece un segundo flanco.
            assert comprobar(maquina, 1, 1, 0, 255 - nuevo, oraculo) == nuevo
            pruebas += 1
            comprobar(maquina, 0, 1, 0, anterior, oraculo)
            pruebas += 1
            # Restaurar estado anterior antes de la siguiente pareja.
            comprobar(maquina, 1, 1, 0, anterior, oraculo)
            pruebas += 1
            comprobar(maquina, 0, 1, 1, anterior, oraculo)
            pruebas += 1

    rng = random.Random(2808)
    maquina, oraculo = Registro8Compuertas(), Oraculo()
    for _ in range(50000):
        clk, load, oe = rng.randrange(2), rng.randrange(2), rng.randrange(2)
        dato = rng.randrange(256)
        comprobar(maquina, clk, load, oe, dato, oraculo)
        pruebas += 1
    print(f'REGISTRO8 C28-A: {pruebas:,} comparaciones CORRECTAS')
    print('Validado: puertas NAND, flancos, LOAD, HOLD, Z, estado inicial X.')
    print('No validado: Verilog ejecutado, tiempos fisicos, integrados, montaje.')


if __name__ == '__main__':
    main()
