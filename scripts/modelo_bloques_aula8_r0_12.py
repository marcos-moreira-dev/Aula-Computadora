#!/usr/bin/env python3
"""Modelo anfitrión del contrato candidato de controlador de bloques R0.12.

NO es controlador de CPU Aula, firmware, simulador de circuitos ni MiniSO.
"""

from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path


BLOCK_SIZE = 256
REGISTER_MAP = {
    "COMMAND": 0xC010,
    "STATUS": 0xC012,
    "BLOCK_LO": 0xC014,
    "BLOCK_HI": 0xC016,
    "DATA": 0xC018,
    "ERROR": 0xC01A,
    "COUNT_LO": 0xC01C,
    "COUNT_HI": 0xC01E,
}
COMMAND = {"NOP": 0, "READ": 1, "WRITE": 2, "RESET": 3}
STATUS = {"BUSY": 1, "DRQ": 2, "DONE": 4, "ERROR": 8}
ERROR = {
    "NONE": 0,
    "BAD_COMMAND": 1,
    "BLOCK_OUT_OF_RANGE": 2,
    "DATA_DIRECTION_OR_STATE": 3,
    "BUSY_RECONFIGURED": 4,
    "IMAGE_IO_FAILURE": 5,
}


class ImageIOError(Exception):
    """Fallo de imagen, distinto de dirección de bloque inválida."""


class FileBlockImage:
    """Archivo crudo con N bloques; sustitución completa solo como referencia."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.inject_failure_before_replace = False
        self._validate_size()

    @classmethod
    def create(cls, path: Path, blocks: int) -> FileBlockImage:
        if not 1 <= blocks <= 65536:
            raise ValueError("Bloques deben estar entre 1 y 65536")
        with Path(path).open("xb") as sink:
            sink.write(bytes(blocks * BLOCK_SIZE))
        return cls(path)

    def _validate_size(self) -> None:
        length = self.path.stat().st_size
        if length < BLOCK_SIZE or length % BLOCK_SIZE or length > 65536 * BLOCK_SIZE:
            raise ValueError("La imagen debe contener de 1 a 65536 bloques de 256 bytes")
        self.blocks = length // BLOCK_SIZE

    def read_block(self, number: int) -> bytes:
        if not 0 <= number < self.blocks:
            raise ValueError("BLOCK_OUT_OF_RANGE")
        try:
            with self.path.open("rb") as source:
                source.seek(number * BLOCK_SIZE)
                data = source.read(BLOCK_SIZE)
            if len(data) != BLOCK_SIZE:
                raise ImageIOError("Imagen truncada durante la lectura")
            return data
        except OSError as exc:
            raise ImageIOError(str(exc)) from exc

    def write_block(self, number: int, block: bytes) -> None:
        if not 0 <= number < self.blocks:
            raise ValueError("BLOCK_OUT_OF_RANGE")
        if len(block) != BLOCK_SIZE:
            raise ValueError("Se requiere un bloque completo de 256 bytes")

        try:
            current = self.path.read_bytes()
            if len(current) != self.blocks * BLOCK_SIZE:
                raise ImageIOError("Imagen truncada durante la escritura")
            rewritten = bytearray(current)
            begin = number * BLOCK_SIZE
            rewritten[begin:begin + BLOCK_SIZE] = block
            # Solo referencia para pruebas pequeñas: un archivo temporal del
            # mismo directorio y reemplazo después de escribir el bloque.
            with tempfile.TemporaryDirectory(prefix="aula_r012_", dir=self.path.parent) as tempdir:
                staged_path = Path(tempdir) / "image.raw"
                with staged_path.open("wb") as sink:
                    sink.write(rewritten)
                    sink.flush()
                    os.fsync(sink.fileno())
                if self.inject_failure_before_replace:
                    raise ImageIOError("Fallo inyectado antes del reemplazo")
                os.replace(staged_path, self.path)
        except OSError as exc:
            raise ImageIOError(str(exc)) from exc


class BlockController:
    """Máquina de estados de escritorio para ocho registros MMIO de Aula-8."""

    def __init__(self, image: FileBlockImage) -> None:
        self.image = image
        self.block_lo = 0
        self.block_hi = 0
        self.reset()

    @property
    def block_number(self) -> int:
        return self.block_lo | (self.block_hi << 8)

    @property
    def status(self) -> int:
        if self.state == "transfer":
            return STATUS["BUSY"] | STATUS["DRQ"]
        return {"idle": 0, "done": STATUS["DONE"], "error": STATUS["ERROR"]}[self.state]

    def reset(self) -> None:
        self.state = "idle"
        self.mode = None
        self.count = 0
        self.last_error = ERROR["NONE"]
        self._buffer = bytearray()

    def _fail(self, code: int) -> None:
        self.state = "error"
        self.mode = None
        self.last_error = code
        self._buffer.clear()

    def _start(self, command: int) -> None:
        if self.state == "transfer":
            self._fail(ERROR["BUSY_RECONFIGURED"])
            return
        if command not in (COMMAND["READ"], COMMAND["WRITE"]):
            self._fail(ERROR["BAD_COMMAND"])
            return
        self.count = 0
        self.last_error = ERROR["NONE"]
        self.mode = "read" if command == COMMAND["READ"] else "write"
        if not 0 <= self.block_number < self.image.blocks:
            self._fail(ERROR["BLOCK_OUT_OF_RANGE"])
            return
        if self.mode == "read":
            try:
                self._buffer = bytearray(self.image.read_block(self.block_number))
            except ImageIOError:
                self._fail(ERROR["IMAGE_IO_FAILURE"])
                return
        else:
            self._buffer = bytearray()
        self.state = "transfer"

    def write(self, address: int, data: int) -> None:
        if address not in REGISTER_MAP.values() or not 0 <= data <= 255:
            self._fail(ERROR["DATA_DIRECTION_OR_STATE"])
            return
        if address == REGISTER_MAP["COMMAND"]:
            if data == COMMAND["RESET"]:
                self.reset()
            elif data == COMMAND["NOP"] and self.state == "transfer":
                self._fail(ERROR["BUSY_RECONFIGURED"])
            elif data != COMMAND["NOP"]:
                self._start(data)
            return
        if address in (REGISTER_MAP["BLOCK_LO"], REGISTER_MAP["BLOCK_HI"]):
            if self.state == "transfer":
                self._fail(ERROR["BUSY_RECONFIGURED"])
                return
            if address == REGISTER_MAP["BLOCK_LO"]:
                self.block_lo = data
            else:
                self.block_hi = data
            return
        if address != REGISTER_MAP["DATA"] or self.state != "transfer" or self.mode != "write":
            self._fail(ERROR["DATA_DIRECTION_OR_STATE"])
            return
        self._buffer.append(data)
        self.count += 1
        if self.count == BLOCK_SIZE:
            try:
                self.image.write_block(self.block_number, bytes(self._buffer))
            except ImageIOError:
                self._fail(ERROR["IMAGE_IO_FAILURE"])
                return
            self.state = "done"
            self.mode = None
            self._buffer.clear()

    def read(self, address: int) -> int:
        if address == REGISTER_MAP["STATUS"]:
            return self.status
        if address == REGISTER_MAP["ERROR"]:
            return self.last_error
        if address == REGISTER_MAP["BLOCK_LO"]:
            return self.block_lo
        if address == REGISTER_MAP["BLOCK_HI"]:
            return self.block_hi
        if address == REGISTER_MAP["COUNT_LO"]:
            return self.count & 0xFF
        if address == REGISTER_MAP["COUNT_HI"]:
            return self.count >> 8
        if address != REGISTER_MAP["DATA"] or self.state != "transfer" or self.mode != "read":
            self._fail(ERROR["DATA_DIRECTION_OR_STATE"])
            return 0
        result = self._buffer[self.count]
        self.count += 1
        if self.count == BLOCK_SIZE:
            self.state = "done"
            self.mode = None
            self._buffer.clear()
        return result


def plan_future_load(text: str, image_blocks: int, future_load: dict) -> list[tuple[int, int]]:
    """Valida planificación. NO modifica RAM, imagen ni CPU."""
    words = text.strip().split()
    if len(words) != 4 or words[0].upper() != "LOAD":
        raise ValueError("LOAD_FORMATO")
    patterns = ((words[1], 4), (words[2], 4), (words[3], 2))
    if any(len(token) != width or re.fullmatch(r"[0-9a-fA-F]+", token, re.ASCII) is None
           for token, width in patterns):
        raise ValueError("LOAD_FORMATO")
    source, destination, count = (int(token, 16) for token, _ in patterns)
    minimum, maximum = future_load["block_count_range"]
    if not minimum <= count <= maximum:
        raise ValueError("LOAD_CANTIDAD")
    if destination % future_load["ram_destination_alignment_bytes"]:
        raise ValueError("LOAD_ALINEACION")
    if source + count > image_blocks or source + count > 65536:
        raise ValueError("LOAD_BLOQUE_FUERA")
    windows = future_load["destination_windows"]
    matches = [window for window in windows
               if int(window["start"], 16) <= destination
               and destination + count * BLOCK_SIZE - 1 <= int(window["end"], 16)
               and count <= window["maximum_blocks"]]
    if len(matches) != 1:
        raise ValueError("LOAD_DESTINO")
    return [(source + offset, destination + offset * BLOCK_SIZE) for offset in range(count)]
