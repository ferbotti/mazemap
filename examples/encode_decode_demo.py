from __future__ import annotations

"""Demonstration of encoding and decoding a maze using BMN."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from bmn import decode_bmn, encode_bmn, read_maze  # noqa: E402


def main() -> None:
    """Load a maze, print its BMN notation, and reconstruct the matrix."""
    maze_path = ROOT / "mazefile" / "mazeBin1.mz"
    matrix = read_maze(maze_path)
    bmn_string = encode_bmn(matrix)
    print("BMN:", bmn_string)
    decoded = decode_bmn(bmn_string)
    print("Decoded matrix:")
    for row in decoded:
        print("".join(str(bit) for bit in row))


if __name__ == "__main__":
    main()
