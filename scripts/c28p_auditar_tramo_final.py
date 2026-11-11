#!/usr/bin/env python3
"""C28-P: contratos matematicos y figuras de los capitulos 15 a 24.

Los modelos son oraculos del anfitrion. No ejecutan la CPU Aula ni prueban
conexiones fisicas, tiempo de propagacion o microcodigo implementado.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "libro" / "capitulos"
FIGURES = ROOT / "libro" / "figuras"
OUTPUT = ROOT / "c28_p" / "auditoria" / "C28_P_RESULTADOS.json"
MATRIX = ROOT / "libro" / "MATRIZ_FIGURAS_C28P_15_A_24.md"

SOURCES = {
    "15": "15_la_instruccion_en_movimiento.md",
    "16": "16_subrutinas_y_pila.md",
    "17": "17_encender_una_computadora.md",
    "18": "18_hablar_con_la_maquina.md",
    "19": "19_guardar_y_recuperar_programas.md",
    "20": "20_programar_un_pequeno_sistema.md",
    "21": "21_que_implica_ampliar_la_palabra.md",
    "22": "22_un_bus_externo_de_16_bits.md",
    "23": "23_programacion_para_aula_16.md",
    "23B": "23v_de_mapas_de_caracteres_a_escritorio_grafico.md",
    "24": "24_una_computadora_que_podemos_explicar.md",
}
FIGURE_COUNTS = {"15": 4, "16": 6, "17": 4, "18": 4, "19": 4,
                 "20": 4, "21": 4, "22": 5, "23": 4, "23B": 7, "24": 4}
FIG_REF = re.compile(r"^\[\[FIG:([^|\n]+)\|([^|\n]+)\|(.+)\]\]$", re.MULTILINE)


def check_sources() -> tuple[dict[str, str], list[dict]]:
    texts = {}
    figures = []
    seen = set()
    for chapter, filename in SOURCES.items():
        path = CHAPTERS / filename
        content = path.read_text(encoding="utf-8")
        texts[chapter] = content
        assert f"# Capítulo {chapter}." in content, filename
        assert "## Solucionario" in content, filename
        refs = FIG_REF.findall(content)
        assert len(refs) == FIGURE_COUNTS[chapter], (chapter, len(refs))
        for identifier, caption, alt in refs:
            assert identifier not in seen, identifier
            seen.add(identifier)
            assert len(caption.strip()) >= 35 and len(alt.strip()) >= 35
            png = FIGURES / f"{identifier}.png"
            svg = FIGURES / f"{identifier}.svg"
            raw = png.read_bytes()
            assert raw[:8] == b"\x89PNG\r\n\x1a\n", png
            width, height = struct.unpack(">II", raw[16:24])
            assert width >= 640 and height >= 350, (identifier, width, height)
            tree = ET.parse(svg)
            assert tree.getroot().tag.endswith("svg"), svg
            figures.append(dict(capitulo=chapter, figura=identifier,
                                descripcion=caption.strip(), alt=alt.strip(),
                                ancho_px=width, alto_px=height,
                                alcance="Ilustracion didactica; topologia electrica no certificada"))
    assert len(figures) == 50
    # Anclas de hechos que se comprobaran matematicamente mas abajo.
    anchors = {
        "15": ("PC después de leer HALT = 0x6007 + 1 = 0x6008", "ST_STAGE_DATA", "8 lecturas"),
        "16": ("SP nuevo = 0x8000 − 2 = 0x7FFE", "10 lecturas + 2 escrituras", "no se toma"),
        "17": ("ROM[FFFC]", "32 × 4 = 128 bytes", "LOAD"),
        "18": ("0xC000", "0xC002", "FW_PUTC", "HOLA"),
        "19": ("C010", "C01E", "256", "217 bytes"),
        "20": ("29 bytes", "0x6018", "F(14)=377", "no cuenta"),
        "21": ("0x01FF + 0x0001 = 0x0200", "bus externo", "64 KiB"),
        "22": ("Fila = dirección_de_byte >> 1", "0xAB34", "dirección impar"),
        "23": ("0x0202", "9489", "ISA"),
        "23B": ("512 bytes", "8192 bytes", "ROM de glifos", "2bpp"),
        "24": ("8704 B", "65536 bytes", "sin"),
    }
    for chapter, fragments in anchors.items():
        for fragment in fragments:
            assert fragment in texts[chapter], f"{chapter}: falta {fragment}"
    return texts, figures


def check_memory_and_mmio(video: dict) -> dict:
    counts = {"ram": 0, "expansion": 0, "mmio": 0, "reserva": 0, "rom": 0}
    for addr in range(65536):
        if addr < 0x8000:
            group = "ram"
        elif addr < 0xC000:
            group = "expansion"
        elif addr < 0xC100:
            group = "mmio"
        elif addr < 0xE000:
            group = "reserva"
        else:
            group = "rom"
        counts[group] += 1
    assert counts == {"ram": 32768, "expansion": 16384, "mmio": 256,
                      "reserva": 7936, "rom": 8192}
    storage = tuple(range(0xC010, 0xC020, 2))
    video_active = tuple(int(r["address"], 16) for r in video["registers"])
    assert storage == (0xC010, 0xC012, 0xC014, 0xC016,
                       0xC018, 0xC01A, 0xC01C, 0xC01E)
    assert video_active == (0xC020, 0xC022, 0xC024, 0xC026, 0xC028, 0xC02A)
    assert not set(storage).intersection(video_active)
    assert set(video_active).isdisjoint((0xC000, 0xC002))
    assert video["mmio_odd_addresses_alias_even"] is False
    assert video["aula16_external_data_bus_bits"] == 16
    assert video["video_ram_directly_cpu_mapped"] is False
    # FFFC/FFFD deben estar en ROM, sin colision con las 32 ranuras publicas.
    slots = [0xFF00 + i * 4 for i in range(32)]
    assert slots[0] == 0xFF00 and slots[-1] == 0xFF7C
    assert max(slots) + 3 == 0xFF7F < 0xFFFC
    assert (0x00 | 0xE0 << 8) == 0xE000
    counts["direcciones_controladas"] = 65536
    counts["ranuras_rom"] = len(slots)
    return counts


def check_call_and_branches(isa: dict) -> dict:
    op = {i["mnemonic"]: int(i["opcode"], 16) for i in isa["instructions"]}
    assert {x: op[x] for x in ("LDI", "RET", "CALL", "DEC", "JNZ", "HALT")} == {
        "LDI": 0x11, "RET": 0x02, "CALL": 0x35,
        "DEC": 0x2A, "JNZ": 0x32, "HALT": 0x01,
    }
    # Escritura little-endian de dos niveles independientes. Se prueban
    # multiples sentinelas de pila; son cuentas, no microsecuencias ejecutadas.
    comparisons = 0
    for initial_sp in range(0x1000, 0x8001, 2):
        stack = {}
        sp = initial_sp
        for return_pc in (0x6003, 0x6013):
            sp -= 2
            stack[sp] = return_pc & 255
            stack[sp + 1] = return_pc >> 8
            comparisons += 2
        for expected in (0x6013, 0x6003):
            actual = stack[sp] | (stack[sp + 1] << 8)
            assert actual == expected
            sp += 2
            comparisons += 2
        assert sp == initial_sp
    # Contador 1..255: DEC y JNZ consumen ambos operandos siempre; la
    # rama se toma N-1 veces y tras el ultimo JNZ se llega a HALT.
    loop = next(e for e in isa["examples"] if e["name"] == "bucle_de_tres")
    assert bytes.fromhex(loop["bytes_hex"]) == bytes.fromhex("11 00 03 2A 00 32 03 60 01")
    iterations = 0
    for start in range(1, 256):
        value = start
        taken = 0
        while value:
            value = (value - 1) & 255
            z = value == 0
            if not z:
                taken += 1
            iterations += 1
        assert taken == start - 1 and value == 0
    # Interprete MINIMO e independiente del recorrido documentado C16;
    # no es la implementacion de las rutas de control de Aula.
    mem = dict(zip((0x6000, 0x6001, 0x6002, 0x6003,
                    0x6010, 0x6011, 0x6012, 0x6013),
                   (0x35, 0x10, 0x60, 0x01, 0x11, 0x00, 0x2A, 0x02)))
    pc, sp, r0, reads, writes = 0x6000, 0x8000, None, 0, 0

    def fetch() -> int:
        nonlocal pc, reads
        value = mem[pc]
        pc += 1
        reads += 1
        return value

    assert fetch() == op["CALL"]
    target = fetch() | fetch() << 8
    sp -= 2
    mem[sp], mem[sp + 1] = pc & 255, pc >> 8
    writes += 2
    pc = target
    assert fetch() == op["LDI"]
    selector, r0 = fetch(), fetch()
    assert selector == 0 and r0 == 0x2A
    assert fetch() == op["RET"]
    return_pc = mem[sp] | (mem[sp + 1] << 8)
    reads += 2
    sp += 2
    pc = return_pc
    assert fetch() == op["HALT"]
    assert (pc, sp, r0, reads, writes) == (0x6004, 0x8000, 0x2A, 10, 2)
    return dict(casos_pila=(0x8000 - 0x1000) // 2 + 1,
                comprobaciones_pila=comparisons, vueltas_dec=iterations,
                accesos_ejemplo_c16={"lecturas": 10, "escrituras": 2})


def check_storage_and_programming() -> dict:
    assert 0x0102 == (0x01 << 8) + 0x02
    assert 0x1000 + 2 * 256 - 1 == 0x11FF
    assert 256 - 7 == 249 and 256 - 32 - 7 == 217
    block_checks = 0
    for useful in range(1, 8161):
        blocks = (32 + useful + 255) // 256
        assert (blocks - 1) * 256 < 32 + useful <= blocks * 256
        block_checks += 1
    # Euclides por restas, sin asumir que Aula ejecuta las instrucciones.
    euclid = 0
    for a in range(1, 65):
        for b in range(1, 65):
            x, y = a, b
            while x != y:
                if x > y:
                    x -= y
                else:
                    y -= x
            assert x == math.gcd(a, b)
            euclid += 1
    def fib(n: int) -> int:
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    assert (fib(6), fib(13), fib(14), fib(25)) == (8, 233, 377, 75025)
    assert 75025 % 65536 == 9489 == 0x2511
    def recursive_calls(n: int) -> int:
        return 1 if n < 2 else 1 + recursive_calls(n - 1) + recursive_calls(n - 2)
    assert recursive_calls(6) == 25
    return dict(tamanos_aex1=block_checks, pares_euclides=euclid,
                fibonacci={"f6": 8, "f13": 233, "f14": 377, "f25": 75025})


def check_bus16_and_video(video: dict) -> dict:
    assert video["text_columns"] * video["text_rows"] == video["text_buffer_bytes"] == 512
    assert video["glyph_count"] * video["glyph_height_pixels"] == video["glyph_rom_bytes"] == 2048
    assert video["graphics_width_pixels"] * video["graphics_height_pixels"] * 2 // 8 == 8192
    assert video["total_video_ram_bytes"] == 8704
    assert video["video_ram_assumed_cleared_on_reset"] is False
    assert video["mode_switch_erases_buffers"] is False
    assert video["firmware_public_slots_added"] == 0
    # Cada par (fila fisica, carril) de 16 KiB cubre exactamente la RAM
    # 0000..7FFF. La pareja se usa solo para palabras en direcciones pares.
    lanes = set()
    words = 0
    for addr in range(0x8000):
        row, lane = addr >> 1, addr & 1
        assert 0 <= row < 16384 and lane in (0, 1)
        lanes.add((row, lane))
        if lane == 0:
            low, high = addr & 255, (addr >> 8) & 255
            assert (low | (high << 8)) == addr
            words += 1
    assert len(lanes) == 32768 and words == 16384
    # Enumeracion completa del espacio de 256x128 pixeles 2bpp.
    pixels = set()
    for y in range(128):
        for x in range(256):
            offset = y * 64 + (x // 4)
            shift = 6 - 2 * (x % 4)
            assert 0 <= offset < 8192 and shift in (0, 2, 4, 6)
            pixels.add((offset, shift))
    assert len(pixels) == 32768
    text_cells = {(y * 32 + x) for y in range(16) for x in range(32)}
    assert text_cells == set(range(512))
    return dict(direcciones_ram_por_carril=len(lanes),
                palabras_alineadas_ram=words, posiciones_pixel=len(pixels),
                celdas_texto=len(text_cells))


def main() -> None:
    texts, figures = check_sources()
    isa = json.loads((ROOT / "simulador-javafx" / "ISA_AULA8_CANDIDATA.json").read_text(encoding="utf-8"))
    video = json.loads((ROOT / "simulador-javafx" / "VIDEO_AULA_V1_CONTRATO.json").read_text(encoding="utf-8"))
    assert isa["status"] == "propuesta_no_aprobada"
    results = {
        "estado": "APROBADO_MODELOS_DOCUMENTALES",
        "capitulos": list(texts),
        "total_capitulos": len(texts),
        "figuras_con_png_y_svg": len(figures),
        "mapa": check_memory_and_mmio(video),
        "pila_y_bucles": check_call_and_branches(isa),
        "almacenamiento_y_programas": check_storage_and_programming(),
        "aula16_y_video": check_bus16_and_video(video),
        "limites": [
            "La revision de anclas y estructuras no es correccion de estilo pagina por pagina",
            "La matematica no demuestra que la CPU o la ISA sean ejecutables",
            "Los 50 diagramas no son planos electricos validados",
            "Las politicas PC anticipado y PC diferido siguen candidatas",
            "El Word/PDF maestro sigue en C28-G; C28-H y atlas son suplementos",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Matriz C28-P de figuras en capítulos 15–24",
        "",
        "**Cobertura:** 11 lecciones, contando 23B, y 50 referencias a",
        "figuras PNG/SVG. El control comprueba archivos, dimensiones, etiquetas",
        "y contratos matemáticos relacionados; **no** deduce netlists ni",
        "integridad eléctrica a partir de un dibujo.",
        "",
        "| Cap. | Identificador | Propósito de la figura | Evidencia y límite |",
        "| --- | --- | --- | --- |",
    ]
    for fig in figures:
        caption = fig["descripcion"].replace("|", "/")
        lines.append(f'| {fig["capitulo"]} | `{fig["figura"]}` | {caption} | '
                     'PNG y SVG correctos; correspondencia de pines/RTL pendiente |')
    lines += ["", "La simulación RTL C28-H corresponde a las **dos políticas",
              "candidatas de lectura secuencial**, no a una validación HDL",
              "automática de estas 50 ilustraciones. No hay placa física."]
    MATRIX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f'C28-P: {len(texts)} lecciones, {len(figures)} figuras; modelos aprobados.')
    print(f'RAM: {results["mapa"]["direcciones_controladas"]} direcciones; '
          f'píxeles: {results["aula16_y_video"]["posiciones_pixel"]}; '
          f'casos Euclides: {results["almacenamiento_y_programas"]["pares_euclides"]}.')
    print("RESULTADO_C28P_APROBADO")


if __name__ == "__main__":
    main()
