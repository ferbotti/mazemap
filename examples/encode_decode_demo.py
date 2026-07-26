from __future__ import annotations

"""Demonstration of encoding and decoding a maze using BMN."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from bmn import decode_bmn_with_metadata, encode_bmn, read_maze, render_maze_svg  # noqa: E402


def main() -> None:
    """Load a maze, print its BMN notation, and reconstruct the matrix."""
    maze_path = ROOT / "mazefile" / "mazeBin1.mz"
    matrix = read_maze(maze_path)
    bmn_string = encode_bmn(
        matrix,
        metadata={
            "entrance": (3, 0),
            "exit": (3, 11),
            "start": (3, 0),
            "goal": (3, 11),
        },
    )
    print("BMN:", bmn_string)
    decoded, metadata = decode_bmn_with_metadata(bmn_string)
    print("Metadata:", metadata)
    print("Decoded matrix:")
    for row in decoded:
        print("".join(str(bit) for bit in row))
    render_maze_svg(decoded, ROOT / "maze1.svg", cell_size=16)
    print("SVG: maze1.svg")


if __name__ == "__main__":
    main()
