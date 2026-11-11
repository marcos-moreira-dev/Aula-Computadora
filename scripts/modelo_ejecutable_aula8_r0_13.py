#!/usr/bin/env python3
"""AEX1: referencia de empaquetado y precarga EN ANFITRIÓN, no firmware Aula."""

from __future__ import annotations

from dataclasses import dataclass

from modelo_bloques_aula8_r0_12 import BLOCK_SIZE, FileBlockImage, ImageIOError

MAGIC = b"AEX1"
VERSION = 1
TARGET_AULA8 = 8
HEADER_SIZE = 32
KIND_PRACTICE = 1
KIND_TOOL = 2
WINDOWS = {KIND_PRACTICE: (0x6000, 0x6FFF), KIND_TOOL: (0x1000, 0x2FFF)}
MAX_BLOCKS = 32


class AexError(ValueError):
    """Paquete rechazado antes de modificar una imagen de RAM."""


@dataclass(frozen=True)
class StagedAex:
    kind: int
    origin: int
    entry: int
    payload: bytes
    total_blocks: int
    payload_crc16: int


def crc16_ccitt_false(data: bytes) -> int:
    """CRC-16/CCITT-FALSE: poli=1021, init=FFFF, refin/out=false, xorout=0000."""
    return crc16_ccitt_update(0xFFFF, data)


def crc16_ccitt_update(state: int, data: bytes) -> int:
    """Variante incremental: permite pasar bloques sin guardar todo el binario."""
    result = state
    for byte in data:
        result ^= byte << 8
        for _ in range(8):
            result = ((result << 1) ^ (0x1021 if result & 0x8000 else 0)) & 0xFFFF
    return result


def _u16(raw: bytes) -> int:
    return int.from_bytes(raw, "little")


def _check_location(kind: int, origin: int, entry: int, length: int) -> None:
    if kind not in WINDOWS:
        raise AexError("TIPO_INVALIDO")
    if not 0 <= origin <= 0xFFFF or origin % BLOCK_SIZE:
        raise AexError("ORIGEN_NO_ALINEADO")
    if length < 1 or length > 0xFFFF:
        raise AexError("LONGITUD_INVALIDA")
    start, end = WINDOWS[kind]
    if origin < start or origin + length - 1 > end:
        raise AexError("FUERA_DE_VENTANA_RAM")
    if (HEADER_SIZE + length + BLOCK_SIZE - 1) // BLOCK_SIZE > (end - start + 1) // BLOCK_SIZE:
        raise AexError("DEMASIADOS_BLOQUES_PARA_TIPO")
    if not origin <= entry < origin + length:
        raise AexError("ENTRADA_FUERA_DE_CODIGO")


def pack_aex(payload: bytes, *, kind: int, origin: int, entry: int) -> bytes:
    """Construye bloques de 256 B, con 32 B de cabecera fuera de RAM."""
    if not isinstance(payload, bytes):
        raise AexError("PAYLOAD_NO_BYTES")
    _check_location(kind, origin, entry, len(payload))
    blocks = (HEADER_SIZE + len(payload) + BLOCK_SIZE - 1) // BLOCK_SIZE
    if blocks > MAX_BLOCKS:
        raise AexError("DEMASIADOS_BLOQUES")
    header = bytearray(HEADER_SIZE)
    header[0:4] = MAGIC
    header[4] = VERSION
    header[5] = TARGET_AULA8
    header[6] = kind
    # 07 flags = 0 en v1.
    header[8:10] = origin.to_bytes(2, "little")
    header[10:12] = entry.to_bytes(2, "little")
    header[12:14] = len(payload).to_bytes(2, "little")
    header[14:16] = crc16_ccitt_false(payload).to_bytes(2, "little")
    header[16:18] = blocks.to_bytes(2, "little")
    header[18:20] = crc16_ccitt_false(header[:18]).to_bytes(2, "little")
    return (bytes(header) + payload).ljust(blocks * BLOCK_SIZE, b"\x00")


def _inspect_header(first_block: bytes, expected_target: int) -> tuple[int, int, int, int, int, int]:
    if len(first_block) < HEADER_SIZE:
        raise AexError("CABECERA_INCOMPLETA")
    header = first_block[:HEADER_SIZE]
    if header[:4] != MAGIC:
        raise AexError("FIRMA_INVALIDA")
    if header[4] != VERSION:
        raise AexError("VERSION_NO_SOPORTADA")
    if header[5] != expected_target:
        raise AexError("CPU_INCORRECTA")
    if header[7] or any(header[20:]):
        raise AexError("CAMPOS_RESERVADOS_NO_CERO")
    if _u16(header[18:20]) != crc16_ccitt_false(header[:18]):
        raise AexError("CRC_CABECERA_INVALIDO")
    kind, origin, entry, length = header[6], _u16(header[8:10]), _u16(header[10:12]), _u16(header[12:14])
    _check_location(kind, origin, entry, length)
    blocks = _u16(header[16:18])
    expected = (HEADER_SIZE + length + BLOCK_SIZE - 1) // BLOCK_SIZE
    if blocks != expected or not 1 <= blocks <= MAX_BLOCKS:
        raise AexError("CONTEO_DE_BLOQUES_INVALIDO")
    return kind, origin, entry, length, blocks, _u16(header[14:16])


def decode_aex(data: bytes, *, expected_target: int = TARGET_AULA8) -> StagedAex:
    """Valida la imagen completa ANTES de entregarla a un cargador."""
    if len(data) < BLOCK_SIZE or len(data) % BLOCK_SIZE:
        raise AexError("LONGITUD_DE_CONTENEDOR_INVALIDA")
    kind, origin, entry, length, blocks, crc = _inspect_header(data[:BLOCK_SIZE], expected_target)
    if len(data) != blocks * BLOCK_SIZE:
        raise AexError("CONTENEDOR_TRUNCADO_O_EXTRA")
    payload = data[HEADER_SIZE:HEADER_SIZE + length]
    if any(data[HEADER_SIZE + length:]):
        raise AexError("RELLENO_NO_CERO")
    if crc16_ccitt_false(payload) != crc:
        raise AexError("CRC_PAYLOAD_INVALIDO")
    return StagedAex(kind, origin, entry, payload, blocks, crc)


def stage_from_block_image(image: FileBlockImage, first_block: int) -> StagedAex:
    """Lee bloques crudos R0.12 y valida todo; no escribe RAM ni ejecuta."""
    if not isinstance(first_block, int) or not 0 <= first_block < image.blocks:
        raise AexError("BLOQUE_INICIAL_FUERA_DE_RANGO")
    try:
        first = image.read_block(first_block)
        _, _, _, _, blocks, _ = _inspect_header(first, TARGET_AULA8)
        if first_block + blocks > image.blocks:
            raise AexError("IMAGEN_SIN_BLOQUES_SUFICIENTES")
        raw = first + b"".join(image.read_block(i) for i in range(first_block + 1, first_block + blocks))
    except (ValueError, OSError, ImageIOError) as exc:
        if isinstance(exc, AexError):
            raise
        raise AexError("ERROR_DE_LECTURA_DE_BLOQUE") from exc
    return decode_aex(raw)


def preview_load_ram(ram: bytes, staged: StagedAex) -> bytes:
    """Copia a NUEVA RAM de 32768 B solo un objeto ya validado; nunca a CPU."""
    if len(ram) != 32768:
        raise AexError("TAMANIO_RAM_INVALIDO")
    _check_location(staged.kind, staged.origin, staged.entry, len(staged.payload))
    if staged.total_blocks != (HEADER_SIZE + len(staged.payload) + 255) // 256:
        raise AexError("METADATOS_INCOHERENTES")
    if crc16_ccitt_false(staged.payload) != staged.payload_crc16:
        raise AexError("CRC_PAYLOAD_INVALIDO")
    result = bytearray(ram)
    result[staged.origin:staged.origin + len(staged.payload)] = staged.payload
    return bytes(result)
