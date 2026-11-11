#!/usr/bin/env python3
"""Auditoría reproducible del contrato de vídeo; no ejecuta CPU ni periféricos."""

import json
from pathlib import Path

from verificar_modelo_video_texto_grafico import ubicacion_pixel


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "simulador-javafx/VIDEO_AULA_V1_CONTRATO.json"


def verificar() -> int:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    contador = 0

    assert spec["status"] == "diseno_logico_congelado_no_implementado"
    assert spec["cpu_address_width_bits"] == 16
    assert spec["aula8_external_data_bus_bits"] == 8
    assert spec["aula16_external_data_bus_bits"] == 16
    assert spec["cpu_existing_regions_unchanged"] is True
    assert spec["terminal_data_address"] == "0xC000"
    assert spec["terminal_status_address"] == "0xC002"
    assert spec["storage_mmio_start"] == "0xC010"
    assert spec["storage_mmio_end"] == "0xC01F"
    assert spec["video_mmio_start"] == "0xC020"
    assert spec["video_mmio_end"] == "0xC02F"
    assert spec["mmio_odd_addresses_alias_even"] is False
    contador += 12

    registros = spec["registers"]
    assert len(registros) == 6
    assert [(r["name"], int(r["address"], 16)) for r in registros] == [
        ("VIDEO_MODE", 0xC020),
        ("VIDEO_STATUS", 0xC022),
        ("VRAM_ADDR_LO", 0xC024),
        ("VRAM_ADDR_HI", 0xC026),
        ("VRAM_DATA", 0xC028),
        ("VIDEO_CTRL", 0xC02A),
    ]
    assert spec["reserved_even_register_addresses"] == ["0xC02C", "0xC02E"]
    assert len({r["address"] for r in registros}) == len(registros)
    assert all(int(r["address"], 16) % 2 == 0 for r in registros)
    contador += 4

    assert spec["video_mode_codes"] == {"text": 0, "bitmap_four_colors": 1}
    assert spec["video_status_bits"] == {"ready": 0, "error": 7}
    assert spec["video_control_bits"] == {
        "auto_increment": 0,
        "access_plane": 1,
        "text_fg_lsb": 2,
        "text_bg_lsb": 4,
        "reserved": 6,
        "clear_error_write_only": 7,
    }
    assert spec["video_control_reset_value"] == 0x0C
    assert spec["registers"][5]["reset"] == 0x0C
    contador += 5

    assert spec["text_columns"] * spec["text_rows"] * spec["text_cell_bytes"] == spec["text_buffer_bytes"] == 512
    assert spec["glyph_count"] * spec["glyph_height_pixels"] == spec["glyph_rom_bytes"] == 2048
    assert spec["glyph_width_pixels"] == 8
    assert spec["graphics_width_pixels"] == spec["text_columns"] * spec["glyph_width_pixels"] == 256
    assert spec["graphics_height_pixels"] == spec["text_rows"] * spec["glyph_height_pixels"] == 128
    assert spec["graphics_bits_per_pixel"] == 2
    assert spec["graphics_color_count"] == 4
    assert spec["graphics_bytes_per_row"] == 64
    assert (
        spec["graphics_width_pixels"] * spec["graphics_height_pixels"] * spec["graphics_bits_per_pixel"] // 8
        == spec["graphics_buffer_bytes"] == 8192
    )
    assert spec["total_video_ram_bytes"] == 512 + 8192 == 8704
    assert len(spec["color_indices"]) == 4
    contador += 11

    # Sin colisión ni huecos: cada (x,y) corresponde a un campo distinto de 2 bits.
    campos: set[tuple[int, int]] = set()
    for y in range(spec["graphics_height_pixels"]):
        for x in range(spec["graphics_width_pixels"]):
            indice, shift = ubicacion_pixel(x, y, 2)
            assert 0 <= indice < 8192
            assert shift in (6, 4, 2, 0)
            assert (indice, shift) not in campos
            campos.add((indice, shift))
            contador += 3
    assert len(campos) == 256 * 128
    assert ubicacion_pixel(8, 0, 2) == (2, 6)
    assert ubicacion_pixel(255, 127, 2) == (8191, 0)
    contador += 3

    for k in (
        "text_and_graphics_buffers_separate", "display_and_access_planes_independent",
        "cpu_can_read_video_ram_through_mmio", "error_flag_sticky_until_cleared",
        "text_is_displayed_on_reset", "logical_renderer_only",
        "terminal_output_targets_text_plane"
    ):
        assert spec[k] is True, k
        contador += 1
    for k in (
        "mode_switch_erases_buffers", "graphics_instruction_opcodes_added", "video_ram_directly_cpu_mapped",
        "video_ram_assumed_cleared_on_reset", "physical_video_hardware_implemented",
        "text_graphics_hardware_simultaneous", "font_bitmap_bytes_implemented", "register_hardware_implemented",
        "auto_increment_default", "auto_increment_wraps_per_plane"
    ):
        assert spec[k] is False, k
        contador += 1
    assert spec["firmware_public_slots_added"] == 0
    assert spec["invalid_vram_read_value"] == 0xFF
    contador += 2

    assert (ROOT / spec["documentation"]).is_file()
    assert (ROOT / "simulador-javafx/CUESTIONARIO_MAPA_VIDEO_MMIO.md").is_file()
    contador += 2
    print(f"CONTRATO VIDEO AULA V1: {contador} controles documentales/matemáticos aprobados.")
    print("No se ha ejecutado hardware, firmware, CPU ni un controlador de video real.")
    return contador


if __name__ == "__main__":
    verificar()
