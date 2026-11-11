#!/usr/bin/env python3
"""Inventario C28-A de todas las figuras: controles geométricos y hojas de contacto.

La detección de colisiones es una *prealerta*, no una certificación visual:
líneas y símbolos pueden atravesar etiquetas aunque no se superpongan textos.
"""

import csv
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'libro' / 'figuras'
OUT = ROOT / 'c28_a' / 'auditoria'
SVG_NS = '{http://www.w3.org/2000/svg}'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

# Seleccion manual tras mirar las diez hojas de contacto. Solo las entradas
# que dicen DETALLE tienen inspeccion individual a resolucion original.
TRIAGE = {
    'c01_fig01_lazo_serie': ('ALTA', 'Cercania entre rotulo de corriente y cable superior; confirmar en contexto de pagina.'),
    'c01_fig04_protoboard_conexiones': ('ALTA', 'Cotejar que las hileras y carriles de protoboard no sugieran conexiones falsas.'),
    'c06_fig01_desde_sr_hasta_d': ('ALTA', 'Conexiones de inversor y NAND densas: requieren inspection de cable contra rotulo.'),
    'c07_fig01_ocho_flips_un_registro': ('ALTA', 'Vista conceptual sin entrada MUX ni habilitacion triestado por celda; ampliar con piloto C28-A.'),
    'c07_fig04_transferencia_a_b': ('MEDIA', 'Abstraccion de transferencia: asociar con circuitos y flancos, sin presentarla como montaje.'),
    'c07_fig05_registro_aula8': ('ALTA', 'DFF dibujados como bloques: complementar, no sustituir, por circuito de bit y ocho carriles.'),
    'c08_fig05_buses_aula8': ('ALTA', 'Vista agregada de buses: sumar descomposicion de ocho lineas cuando se trate conexion real.'),
    'c10_fig02_sumador_completo': ('MEDIA', 'Las vias G/H/P son funcionales; confirmar legibilidad de etiquetas en reduccion a pagina.'),
    'c13_fig01_unidad_control': ('DETALLE', 'En C27 la frase despacho y condiciones ya esta debajo del conductor, sin choque visible en PNG nativo; diferia de pagina 119 antigua.'),
    'c14_fig05_ram_contigua_deposito': ('ALTA', 'Excelente base de memoria contigua; verificar al ampliar flecha RAM→dato y conservar byte a byte.'),
    'c14_fig06_ram_salto': ('ALTA', 'Conservar la flecha de salto sobre RAM contigua; comprobar destino, PC y semantica del flujo.'),
    'c16_fig05_ram_y_pila_call_ret': ('MEDIA', 'Alta densidad: revisar flechas CALL y retorno en imagen completa.'),
    'c16_fig06_ram_bucle_jnz': ('MEDIA', 'Verificar que la flecha JNZ apunte a 0x6003 y no a una fila vecina.'),
    'c22_fig01_bancos_y_carriles': ('ALTA', 'El bus A16 necesita diferenciar los dos carriles de datos y ancho de direccion.'),
    'c22_fig05_dos_bancos_aula16': ('ALTA', 'Aristas gruesas y flechas convergentes: revisar terminaciones y rotulos a escala de pagina.'),
    'p23v_fig05_tres_direcciones': ('MEDIA', 'Explicacion con direcciones CPU y VRAM distintas: comprobar trazabilidad conceptual.'),
}


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, max(10, int(size)))


def audit_svg(path):
    tree = ET.parse(path)
    root = tree.getroot()
    box = [float(x) for x in root.attrib['viewBox'].replace(',', ' ').split()]
    _, _, w, h = box
    labels = []
    for el in root.iter(SVG_NS + 'text'):
        try:
            x = float(el.attrib['x'].split()[0])
            y = float(el.attrib['y'].split()[0])
            size = float(el.attrib.get('font-size', '16').replace('px', ''))
        except (ValueError, KeyError):
            continue
        txt = ' '.join(''.join(el.itertext()).split())
        if not txt:
            continue
        f = font(size, 'bold' in el.attrib.get('font-weight', ''))
        left, top, right, bottom = f.getbbox(txt)
        width = right - left
        if el.attrib.get('text-anchor') == 'middle':
            x -= width / 2
        elif el.attrib.get('text-anchor') == 'end':
            x -= width
        labels.append((x, y - size * .94, x + width, y + size * .21, txt))
    out_of_bounds = sum((a < -1 or b < -1 or c > w + 1 or d > h + 1)
                        for a, b, c, d, _ in labels)
    collisions = []
    for i, (x1, y1, x2, y2, s) in enumerate(labels):
        for a1, b1, a2, b2, t in labels[i + 1:]:
            overlap = max(0, min(x2, a2) - max(x1, a1)) * max(0, min(y2, b2) - max(y1, b1))
            shorter = min((x2 - x1) * (y2 - y1), (a2 - a1) * (b2 - b1))
            if shorter and overlap / shorter > .2:
                collisions.append((s[:32], t[:32]))
    return len(labels), out_of_bounds, collisions


def figures_from_sources():
    out = {}
    for md in sorted((ROOT / 'libro' / 'capitulos').glob('*.md')):
        for line in md.read_text(encoding='utf-8').splitlines():
            if not (line.startswith('[[FIG:') and line.endswith(']]')):
                continue
            fid, caption, alt = line[6:-2].split('|', 2)
            if fid in out:
                raise AssertionError(f'Figura repetida: {fid}')
            out[fid] = (md.stem, caption, alt)
    return out


def contacts(rows):
    # 12 miniaturas por página, suficientemente amplias para triage visual.
    per_page = 12
    columns = 3
    tile_w, tile_h = 480, 335
    for page_no in range(math.ceil(len(rows) / per_page)):
        sheet = Image.new('RGB', (columns * tile_w, 4 * tile_h), '#f0f2f4')
        draw = ImageDraw.Draw(sheet)
        for j, row in enumerate(rows[page_no * per_page:(page_no + 1) * per_page]):
            x, y = (j % columns) * tile_w, (j // columns) * tile_h
            path = FIG / (row['id'] + '.png')
            with Image.open(path) as original:
                img = original.convert('RGB')
                img.thumbnail((tile_w - 22, tile_h - 79), Image.Resampling.LANCZOS)
            sheet.paste(img, (x + (tile_w - img.width) // 2, y + 49))
            draw.text((x + 13, y + 8), f"{row['orden']:03d}  {row['id']}",
                      font=font(15, True), fill='#1b4558')
            draw.text((x + 12, y + tile_h - 25),
                      f"{row['capitulo']} · alertas: {row['alertas_geometricas']}",
                      font=font(13), fill='#4b5861')
        path = OUT / f'contactos_{page_no + 1:02}.jpg'
        sheet.save(path, quality=86)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    refs = figures_from_sources()
    all_svg = {p.stem for p in FIG.glob('*.svg')}
    assert len(refs) == 115, len(refs)
    missing = set(refs) - all_svg
    assert not missing, f'Faltan SVG citados por el libro: {missing}'
    # Los pilotos C28 incluyen laminas SVG que todavia NO forman parte
    # de las 115 referencias del maestro. No confundirlos con figuras rotas.
    extras = all_svg - set(refs)
    known_pilots = ('c28c_', 'c28d_', 'c28e_', 'c28f_', 'c28g_', 'c28h_')
    unexpected = {name for name in extras if not name.startswith(known_pilots)}
    assert not unexpected, f'SVG sin origen editorial conocido: {unexpected}'
    rows = []
    with (OUT / 'alertas_texto.txt').open('w', encoding='utf-8') as out:
        for order, (fid, (chap, caption, alt)) in enumerate(refs.items(), 1):
            path = FIG / (fid + '.png')
            with Image.open(path) as img:
                img.verify()
            with Image.open(path) as img:
                w, h = img.size
            labels, edges, overlaps = audit_svg(FIG / (fid + '.svg'))
            alert = edges + len(overlaps)
            for a, b in overlaps:
                out.write(f'{fid}\tPOSIBLE CHOQUE TEXTO-TEXTO\t{a!r} / {b!r}\n')
            if edges:
                out.write(f'{fid}\t{edges} TEXTOS FUERA DEL LIENZO (ESTIMACIÓN)\n')
            rows.append({
                'orden': order, 'id': fid, 'capitulo': chap, 'ancho_png': w,
                'alto_png': h, 'textos_svg': labels, 'alertas_geometricas': alert,
                'colisiones_texto': len(overlaps), 'texto_fuera_lienzo': edges,
                'clasificacion': ('INSPECCION_DETALLADA' if TRIAGE.get(fid, ('',))[0] == 'DETALLE'
                                 else 'CONTACTO_REVISADO_PENDIENTE_DETALLE'),
                'prioridad': (TRIAGE.get(fid, ('MEDIA',))[0]
                              if not alert else 'ALTA'),
                'nota_revision_visual': TRIAGE.get(fid, ('', 'Sin incidencia obvia en miniatura; falta verificar escala final.'))[1],
                'leyenda': caption, 'texto_alternativo': alt,
            })
    with (OUT / 'matriz_115_figuras.csv').open('w', encoding='utf-8', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    contacts(rows)
    print(f'INVENTARIO C28-A: {len(rows)} figuras SVG+PNG verificadas')
    print(f'FIGURAS EXTRA DE PILOTOS C28: {len(extras)}; no están citadas por el maestro')
    print(f'CONTACTOS: {math.ceil(len(rows)/12)} hojas; alertas geométricas: '
          f'{sum(r["alertas_geometricas"] for r in rows)} '
          '(son candidatos, no errores confirmados)')


if __name__ == '__main__':
    main()
