#!/usr/bin/env python3
"""Contrasta tablas del libro (C03-C07) contra modelos lógicos independientes.

NO es prueba de tiempos, PCB, integrados eléctricos ni CPU en ejecución.
Las tablas impresas en los capítulos se comprueban en casos clave, pero el
script no demuestra que un dibujo de cables coincida con una netlist física.
"""

from __future__ import annotations

from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CH = ROOT / "libro" / "capitulos"
OUT = ROOT / "c28_l" / "auditoria"


def nand(a: int, b: int) -> int:
    return 1 - (a & b)


def four_nand_xor(a: int, b: int) -> tuple[int, int, int, int]:
    n1 = nand(a, b)
    n2 = nand(a, n1)
    n3 = nand(b, n1)
    result = nand(n2, n3)
    return n1, n2, n3, result


def stable_sr(q: int, q_bar: int, s_bar: int, r_bar: int) -> tuple[int, int]:
    """Busca estado estable en NAND cruzadas; no resuelve metastabilidad."""
    for _ in range(8):
        next_q = nand(s_bar, q_bar)
        next_bar = nand(r_bar, q)
        if (next_q, next_bar) == (q, q_bar):
            return q, q_bar
        q, q_bar = next_q, next_bar
    raise AssertionError("El modelo no alcanzó estado estable")


def d_latch(q: int, data: int, enable: int) -> int:
    return data if enable else q


def d_flipflop(q: int, data: int, prev_clk: int, clk: int) -> int:
    return data if prev_clk == 0 and clk == 1 else q


def register8(q: int, incoming: int, load: int) -> int:
    # Ocho multiplexores de bit y ocho capturas simultáneas ideales.
    next_bits = []
    for bit in range(8):
        retained = (q >> bit) & 1
        fresh = (incoming >> bit) & 1
        mux = (load & fresh) | ((1 - load) & retained)
        next_bits.append(mux)
    return sum(bit << i for i, bit in enumerate(next_bits))


def verify() -> dict:
    records = []
    count = 0

    # Comparar con filas ESPERADAS (no derivadas de la misma red de NAND).
    expected_nand = {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 0}
    expected_xor = {
        (0, 0): (1, 1, 1, 0),
        (0, 1): (1, 1, 0, 1),
        (1, 0): (1, 0, 1, 1),
        (1, 1): (0, 1, 1, 0),
    }
    for a, b in product((0, 1), repeat=2):
        assert nand(a, b) == expected_nand[(a, b)]
        assert four_nand_xor(a, b) == expected_xor[(a, b)]
        count += 2
    records.append({"circuito": "NAND y XOR con 4 NAND", "casos": count})

    # Evaluar las tres construcciones universales de C03 por separado.
    # Las expectativas son tablas de verdad, no una segunda llamada al
    # mismo circuito usado para calcular cada salida.
    c03 = (CH / "03_de_interruptores_a_logica.md").read_text(encoding="utf-8")
    formulas = (
        "¬A = NAND(A, A)",
        "A ∧ B = NAND(NAND(A, B), NAND(A, B))",
        "A ∨ B = NAND(NAND(A, A), NAND(B, B))",
    )
    for formula in formulas:
        assert formula in c03, f"Expresión de C03 alterada: {formula}"
        count += 1
    for a, b in product((0, 1), repeat=2):
        inverted = nand(a, a)
        intermediate = nand(a, b)
        reconstructed_and = nand(intermediate, intermediate)
        reconstructed_or = nand(nand(a, a), nand(b, b))
        assert inverted == 1 - a
        assert reconstructed_and == int(a == 1 and b == 1)
        assert reconstructed_or == int(a == 1 or b == 1)
        count += 3
    records.append({"circuito": "NOT, AND y OR construidas con NAND (C03)", "casos": 15})

    c04 = (CH / "04_construir_funciones_con_compuertas.md").read_text(encoding="utf-8")
    for equation in ("N1 = NAND(A, B)", "N2 = NAND(A, N1)",
                     "N3 = NAND(B, N1)", "D = NAND(N2, N3)"):
        assert equation in c04, f"La fórmula no coincide en C04: {equation}"
    assert "c04_fig03_xor_cuatro_nand" in c04
    records.append({"circuito": "Fórmulas y referencia gráfica C04", "casos": 5})
    count += 5

    c05 = (CH / "05_la_realimentacion_conserva_informacion.md").read_text(encoding="utf-8")
    for row in ("| 0 1 | 1 | 0 |", "| 1 0 | 0 | 1 |",
                "| 1 1 | Q anterior | Q_n anterior |", "| 0 0 | 1 | 1 |"):
        assert row in c05, f"La tabla del latch cambió en C05: {row}"
    for initial in ((0, 1), (1, 0)):
        assert stable_sr(*initial, 1, 1) == initial  # HOLD
        assert stable_sr(*initial, 0, 1) == (1, 0)  # SET
        assert stable_sr(*initial, 1, 0) == (0, 1)  # RESET
        assert stable_sr(*initial, 0, 0) == (1, 1)  # INVALIDO
        count += 4
    # Repetir los cinco momentos concretos del libro C05.
    q, qb = 0, 1
    seq = [(1, 1, 0), (0, 1, 1), (1, 1, 1), (1, 0, 0), (1, 1, 0)]
    for sb, rb, expected in seq:
        q, qb = stable_sr(q, qb, sb, rb)
        assert q == expected and qb == 1 - expected
        count += 1
    records.append({"circuito": "Latch SR NAND: SET, RESET, HOLD, inválido", "casos": 13})

    c06 = (CH / "06_memorizar_en_el_tiempo.md").read_text(encoding="utf-8")
    assert "## 5. Un flip-flop D de flanco ascendente" in c06
    assert "c06_fig03_flancos_y_capturas" in c06
    for q, data, enable in product((0, 1), repeat=3):
        assert d_latch(q, data, enable) == (data if enable else q)
        count += 1
    for q, data, prev, clk in product((0, 1), repeat=4):
        assert d_flipflop(q, data, prev, clk) == (data if prev == 0 and clk == 1 else q)
        count += 1
    clock_and_data = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0), (1, 0), (1, 1)]
    q, prev = 0, 0
    for (clk, data), expected in zip(clock_and_data, (0, 0, 1, 1, 1, 0, 0)):
        q = d_flipflop(q, data, prev, clk)
        assert q == expected
        prev = clk
        count += 1
    records.append({"circuito": "Latch D y flip-flop D: nivel contra flanco", "casos": 31})

    c07 = (CH / "07_del_bit_al_registro.md").read_text(encoding="utf-8")
    assert "D_i = (LOAD ∧ IN_i) ∨ (NOT LOAD ∧ Q_i)" in c07
    assert "c07_fig02_multiplexor_y_carga" in c07
    for old, new in product(range(256), repeat=2):
        assert register8(old, new, 0) == old
        assert register8(old, new, 1) == new
        count += 2
    records.append({"circuito": "Registro8 con LOAD: 2 × 256²", "casos": 131072})

    info = {
        "etapa": "C28-L / contraste matemático de circuitos iniciales",
        "total_comparaciones": count,
        "casos_individuales": records,
        "limitaciones": [
            "La función XOR se modeló desde fórmulas del texto; el circuito real no se montó",
            "El estado inválido 00 del latch no se resuelve al liberarlo simultáneamente",
            "Las capturas D y LOAD son modelos de flanco ideal y no miden setup/hold",
            "No certifica cada ruta de un dibujo SVG ni retardos eléctricos",
        ],
    }
    return info


def main() -> None:
    data = verify()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "C28_L_RESULTADOS.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"C28-L: {data['total_comparaciones']:,} comparaciones correctas")
    for row in data["casos_individuales"]:
        print(f"  {row['circuito']}: {row['casos']:,} casos")
    print("Límites: simulación lógica ideal; NO esquemas eléctricos ni hardware certificado")


if __name__ == "__main__":
    main()
