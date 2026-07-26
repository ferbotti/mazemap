from __future__ import annotations

"""Utilities for encoding and decoding mazes in Botti-Maze Notation (BMN).

This module provides helper functions to read a maze represented as a
binary matrix from a file, encode that matrix into the compact BMN
representation, and decode BMN strings back into a binary matrix.
"""

from base64 import b64decode, b64encode
from binascii import Error as Base64Error
from pathlib import Path
from typing import List, Mapping, Sequence
from urllib.parse import quote, unquote

Matrix = List[List[int]]
Metadata = dict[str, str]
MetadataValue = str | int | tuple[int, int] | list[int]


def read_maze(path: str | Path) -> Matrix:
    """Read a maze file and return it as a matrix of integers.

    The file is expected to contain a binary matrix where each line
    represents a row of the maze and every character is either ``0`` or ``1``.

    Parameters
    ----------
    path:
        Path to the file containing the maze.

    Returns
    -------
    List[List[int]]
        A two-dimensional list of integers representing the maze.
    """

    with open(Path(path), "r", encoding="utf-8") as fh:
        lines = [line.strip() for line in fh if line.strip()]

    matrix: Matrix = []
    for line_number, line in enumerate(lines, start=1):
        invalid = sorted({char for char in line if char not in {"0", "1"}})
        if invalid:
            raise ValueError(
                f"Maze file contains invalid character(s) on line {line_number}: "
                f"{', '.join(invalid)}"
            )
        matrix.append([int(char) for char in line])

    return validate_maze(matrix)


def validate_maze(matrix: Sequence[Sequence[int]]) -> Matrix:
    """Validate and return a rectangular binary maze matrix.

    BMN stores the matrix dimensions once, so every row must have the same
    width and every cell must be either ``0`` or ``1``.
    """

    if not matrix:
        raise ValueError("Maze matrix is empty")

    first_row = matrix[0]
    if not first_row:
        raise ValueError("Maze matrix rows cannot be empty")

    width = len(first_row)
    validated: Matrix = []
    for row_index, row in enumerate(matrix):
        if len(row) != width:
            raise ValueError(
                "Maze matrix must be rectangular: "
                f"row 0 has width {width}, but row {row_index} has width {len(row)}"
            )

        validated_row: list[int] = []
        for column_index, value in enumerate(row):
            if value not in (0, 1):
                raise ValueError(
                    "Maze matrix must contain only 0 or 1 values: "
                    f"found {value!r} at row {row_index}, column {column_index}"
                )
            validated_row.append(int(value))
        validated.append(validated_row)

    return validated


def encode_bmn(
    matrix: Sequence[Sequence[int]],
    metadata: Mapping[str, MetadataValue] | None = None,
) -> str:
    """Encode a binary maze matrix into BMN format.

    The BMN string has the form ``"{width}x{height}:{base64}"`` where
    the matrix is first flattened into a binary string, converted to
    bytes and finally encoded using Base64.

    Parameters
    ----------
    matrix:
        Binary maze matrix where ``0`` denotes a path and ``1`` denotes a wall.
    metadata:
        Optional key/value data such as ``start``, ``goal``, ``entrance`` or
        ``exit``. Tuple/list values with two integers are encoded as
        coordinates in ``x,y`` form.

    Returns
    -------
    str
        The maze encoded in BMN notation.
    """

    matrix = validate_maze(matrix)
    height = len(matrix)
    width = len(matrix[0])
    binary_string = "".join("".join(str(bit) for bit in row) for row in matrix)

    # Pad the binary string to a multiple of eight bits before converting
    padding = (8 - len(binary_string) % 8) % 8
    padded_binary = binary_string + "0" * padding
    byte_data = int(padded_binary, 2).to_bytes(len(padded_binary) // 8, "big")
    encoded = b64encode(byte_data).decode("ascii")
    metadata_segment = _encode_metadata(metadata or {})

    return f"{width}x{height}:{encoded}{metadata_segment}"


def decode_bmn(bmn: str) -> Matrix:
    """Decode a BMN string back into a binary maze matrix.

    Parameters
    ----------
    bmn:
        String containing the BMN encoded maze.

    Returns
    -------
    List[List[int]]
        The decoded binary maze matrix.
    """

    matrix, _metadata = decode_bmn_with_metadata(bmn)
    return matrix


def decode_bmn_with_metadata(bmn: str) -> tuple[Matrix, Metadata]:
    """Decode a BMN string into a binary matrix and optional metadata."""

    width, height, encoded, metadata = _parse_bmn(bmn)

    try:
        byte_data = b64decode(encoded, validate=True)
    except Base64Error as exc:
        raise ValueError(f"BMN payload is not valid Base64: {exc}") from exc

    required_bits = width * height
    available_bits = len(byte_data) * 8
    if available_bits < required_bits:
        raise ValueError(
            "BMN payload is too short for its dimensions: "
            f"{available_bits} bit(s) available, {required_bits} required"
        )

    binary_string = "".join(f"{byte:08b}" for byte in byte_data)
    relevant = binary_string[:required_bits]

    matrix = [
        [int(relevant[row * width + col]) for col in range(width)]
        for row in range(height)
    ]
    return matrix, metadata


def render_maze_svg(
    matrix: Sequence[Sequence[int]],
    path: str | Path | None = None,
    *,
    cell_size: int = 24,
    wall_color: str = "#111827",
    path_color: str = "#ffffff",
    grid_color: str | None = "#d1d5db",
) -> str:
    """Render a maze matrix as an SVG image.

    If ``path`` is provided, the SVG is also written to that file. The SVG
    string is always returned so callers can embed it directly in HTML or tests.
    """

    matrix = validate_maze(matrix)
    if cell_size <= 0:
        raise ValueError("cell_size must be a positive integer")

    height = len(matrix)
    width = len(matrix[0])
    svg_width = width * cell_size
    svg_height = height * cell_size

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" '
            f'height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" '
            'role="img" aria-label="BMN maze">'
        ),
        f'<rect width="100%" height="100%" fill="{path_color}"/>',
    ]

    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            if value == 1:
                x = column_index * cell_size
                y = row_index * cell_size
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{cell_size}" '
                    f'height="{cell_size}" fill="{wall_color}"/>'
                )

    if grid_color:
        for column_index in range(width + 1):
            x = column_index * cell_size
            parts.append(
                f'<line x1="{x}" y1="0" x2="{x}" y2="{svg_height}" '
                f'stroke="{grid_color}" stroke-width="1"/>'
            )
        for row_index in range(height + 1):
            y = row_index * cell_size
            parts.append(
                f'<line x1="0" y1="{y}" x2="{svg_width}" y2="{y}" '
                f'stroke="{grid_color}" stroke-width="1"/>'
            )

    parts.append("</svg>")
    svg = "\n".join(parts)

    if path is not None:
        Path(path).write_text(svg, encoding="utf-8")

    return svg


def _encode_metadata(metadata: Mapping[str, MetadataValue]) -> str:
    segments: list[str] = []
    for key, raw_value in metadata.items():
        if not key:
            raise ValueError("BMN metadata keys cannot be empty")
        if any(char in key for char in ":;="):
            raise ValueError(f"BMN metadata key contains a reserved character: {key!r}")

        value = _format_metadata_value(raw_value)
        encoded_key = quote(str(key), safe="-_.~")
        encoded_value = quote(value, safe=",.-_~")
        segments.append(f"{encoded_key}={encoded_value}")

    return "".join(f";{segment}" for segment in segments)


def _format_metadata_value(value: MetadataValue) -> str:
    if isinstance(value, (tuple, list)):
        if len(value) != 2 or not all(isinstance(item, int) for item in value):
            raise ValueError(
                "Coordinate metadata values must contain exactly two integers"
            )
        return f"{value[0]},{value[1]}"
    return str(value)


def _parse_bmn(bmn: str) -> tuple[int, int, str, Metadata]:
    if not isinstance(bmn, str) or not bmn:
        raise ValueError("BMN must be a non-empty string")

    if ":" not in bmn:
        raise ValueError("BMN must contain ':' separating dimensions and payload")

    dims, rest = bmn.split(":", 1)
    if not dims:
        raise ValueError("BMN dimensions are missing")
    if not rest:
        raise ValueError("BMN payload is missing")

    encoded, *metadata_segments = rest.split(";")
    if not encoded:
        raise ValueError("BMN Base64 payload is missing")

    dimension_parts = dims.lower().split("x")
    if len(dimension_parts) != 2:
        raise ValueError(
            "BMN dimensions must use the '<width>x<height>' format"
        )

    width_str, height_str = dimension_parts
    try:
        width, height = int(width_str), int(height_str)
    except ValueError as exc:
        raise ValueError(
            "BMN dimensions must be positive integers in '<width>x<height>' format"
        ) from exc

    if width <= 0 or height <= 0:
        raise ValueError("BMN dimensions must be positive integers")

    metadata = _parse_metadata(metadata_segments)
    return width, height, encoded, metadata


def _parse_metadata(segments: Sequence[str]) -> Metadata:
    metadata: Metadata = {}
    for segment in segments:
        if not segment:
            raise ValueError("BMN metadata segment is empty")
        if "=" not in segment:
            raise ValueError(
                f"BMN metadata segment must use key=value format: {segment!r}"
            )

        key, value = segment.split("=", 1)
        key = unquote(key)
        if not key:
            raise ValueError("BMN metadata keys cannot be empty")
        metadata[key] = unquote(value)

    return metadata


if __name__ == "__main__":
    matrix = read_maze("mazefile/mazeBin1.mz")
    bmn_string = encode_bmn(matrix)
    print("BMN:", bmn_string)
    decoded = decode_bmn(bmn_string)
    print("Decoded matrix:")
    for row in decoded:
        print("".join(str(bit) for bit in row))
