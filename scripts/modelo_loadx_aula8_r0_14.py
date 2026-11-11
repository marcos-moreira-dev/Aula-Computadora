#!/usr/bin/env python3
"""LOADX de dos pasadas sobre archivo de HOST. NO es firmware/CPU Aula-8.

No garantiza atomicidad de la RAM ni resistencia ante cortes; en error
desactiva la elegibilidad de ejecutar el código cargado parcialmente.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from modelo_bloques_aula8_r0_12 import BLOCK_SIZE, FileBlockImage, ImageIOError
from modelo_ejecutable_aula8_r0_13 import (
    AexError, HEADER_SIZE, TARGET_AULA8, _inspect_header, crc16_ccitt_update,
)


@dataclass(frozen=True)
class LoadXReport:
    status: str
    ram: bytes
    bytes_copied: int
    verified_blocks: int
    max_temporary_block_bytes: int
    entry_if_ready: int | None
    kind_if_ready: int | None
    reason: str

    @property
    def eligible_for_supervised_execution(self) -> bool:
        """Solo indica resultado del modelo; no habilita RUN/CPU de verdad."""
        return self.status == "ready" and self.entry_if_ready is not None


def _check_sector(source: bytes, index: int, total_blocks: int, payload_size: int) -> memoryview:
    """Separa datos útiles de cabecera/relleno en un bloque físico de 256 B."""
    if len(source) != BLOCK_SIZE:
        raise AexError("SECTOR_INCOMPLETO")
    offset = HEADER_SIZE if index == 0 else 0
    consumed_before = 0 if index == 0 else (BLOCK_SIZE - HEADER_SIZE) + (index - 1) * BLOCK_SIZE
    useful = min(BLOCK_SIZE - offset, max(0, payload_size - consumed_before))
    if index < total_blocks - 1 and useful != BLOCK_SIZE - offset:
        raise AexError("BLOQUES_DECLARADOS_INCOHERENTES")
    if any(source[offset + useful:]):
        raise AexError("RELLENO_NO_CERO")
    return memoryview(source)[offset:offset + useful]


def _stream_pass(image: FileBlockImage, first: int, blocks: int, size: int,
                 expected_crc: int, *, header: bytes,
                 writer: Callable[[int, memoryview], None] | None) -> tuple[int, int]:
    """CRC incremental, validación de relleno; staging máximo de 256 B."""
    crc = 0xFFFF
    consumed = 0
    checked = 0
    for index in range(blocks):
        raw = image.read_block(first + index)
        if index == 0 and raw[:HEADER_SIZE] != header:
            raise AexError("CABECERA_CAMBIO_ENTRE_LECTURAS")
        portion = _check_sector(raw, index, blocks, size)
        crc = crc16_ccitt_update(crc, portion)
        if writer is not None:
            writer(consumed, portion)
        consumed += len(portion)
        checked += 1
    if consumed != size:
        raise AexError("TAMANIO_EFECTIVO_INVALIDO")
    if crc != expected_crc:
        raise AexError("CRC_PAYLOAD_INVALIDO")
    return checked, consumed


def loadx_two_pass_host(image: FileBlockImage, first_block: int, ram: bytes,
                        *, between_passes: Callable[[], None] | None = None) -> LoadXReport:
    """Pase 1 solo verifica; pase 2 copia a RAM de HOST de 256 B en 256 B.

    between_passes es gancho exclusivo de pruebas de mutación/fallo.
    El resultado ready es requisito lógico de EJECUCIÓN SUPERVISADA FUTURA,
    no habilita RUN ni prueba que el programa sea código máquina válido.
    """
    if len(ram) != 32768:
        raise AexError("TAMANIO_RAM_INVALIDO")
    if not isinstance(first_block, int) or not 0 <= first_block < image.blocks:
        raise AexError("BLOQUE_INICIAL_FUERA_DE_RANGO")
    result = bytearray(ram)
    copied = 0
    checked = 0
    try:
        header_block = image.read_block(first_block)
        kind, origin, entry, size, blocks, crc = _inspect_header(header_block, TARGET_AULA8)
        if first_block + blocks > image.blocks:
            raise AexError("BLOQUES_FUERA_DEL_DISPOSITIVO")
        header = header_block[:HEADER_SIZE]
        checked, _ = _stream_pass(image, first_block, blocks, size, crc, header=header, writer=None)
    except (AexError, ImageIOError, OSError, ValueError) as exc:
        return LoadXReport("preflight_error", bytes(result), 0, checked, BLOCK_SIZE, None, None, str(exc))

    if between_passes is not None:
        between_passes()

    def write_chunk(offset: int, data: memoryview) -> None:
        nonlocal copied
        start = origin + offset
        result[start:start + len(data)] = data
        copied += len(data)

    try:
        _stream_pass(image, first_block, blocks, size, crc, header=header, writer=write_chunk)
    except (AexError, ImageIOError, OSError, ValueError) as exc:
        return LoadXReport("copy_error", bytes(result), copied, checked, BLOCK_SIZE, None, None, str(exc))
    return LoadXReport("ready", bytes(result), copied, checked, BLOCK_SIZE, entry, kind, "OK")
