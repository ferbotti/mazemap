from __future__ import annotations

"""Utilities for encoding and decoding mazes in Botti-Maze Notation (BMN).

This module provides helper functions to read a maze represented as a
binary matrix from a file, encode that matrix into the compact BMN
representation, and decode BMN strings back into a binary matrix.
"""

from base64 import b64decode, b64encode
from pathlib import Path
from typing import List


def read_maze(path: str | Path) -> List[List[int]]:
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
    return [[int(char) for char in line] for line in lines]


def encode_bmn(matrix: List[List[int]]) -> str:
    """Encode a binary maze matrix into BMN format.

    The BMN string has the form ``"{width}x{height}:{base64}"`` where
    the matrix is first flattened into a binary string, converted to
    bytes and finally encoded using Base64.

    Parameters
    ----------
    matrix:
        Binary maze matrix where ``0`` denotes a path and ``1`` denotes a wall.

    Returns
    -------
    str
        The maze encoded in BMN notation.
    """

    if not matrix:
        raise ValueError("Matrix is empty")

    height = len(matrix)
    width = len(matrix[0])
    binary_string = "".join("".join(str(bit) for bit in row) for row in matrix)

    # Pad the binary string to a multiple of eight bits before converting
    padding = (8 - len(binary_string) % 8) % 8
    padded_binary = binary_string + "0" * padding
    byte_data = int(padded_binary, 2).to_bytes(len(padded_binary) // 8, "big")
    encoded = b64encode(byte_data).decode("ascii")

    return f"{width}x{height}:{encoded}"


def decode_bmn(bmn: str) -> List[List[int]]:
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

    dims, encoded = bmn.split(":", 1)
    width_str, height_str = dims.lower().split("x")
    width, height = int(width_str), int(height_str)

    byte_data = b64decode(encoded)
    binary_string = "".join(f"{byte:08b}" for byte in byte_data)
    relevant = binary_string[: width * height]

    matrix = [
        [int(relevant[row * width + col]) for col in range(width)]
        for row in range(height)
    ]
    return matrix


if __name__ == "__main__":
    matrix = read_maze("mazefile/mazeBin1.mz")
    bmn_string = encode_bmn(matrix)
    print("BMN:", bmn_string)
    decoded = decode_bmn(bmn_string)
    print("Decoded matrix:")
    for row in decoded:
        print("".join(str(bit) for bit in row))
