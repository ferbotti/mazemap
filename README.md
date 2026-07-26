# Botti-Maze Notation (BMN)

**Botti-Maze Notation (BMN)** is a compact text notation for rectangular binary mazes.

BMN stores a maze as:

```text
<width>x<height>:<base64-payload>[;metadata=value]
```

In the binary matrix, `1` represents a wall and `0` represents an open path.

## Example

The sample maze in `mazefile/mazeBin1.mz` has 11 columns and 12 rows:

```text
11101111111
10100000001
10111110101
10000010101
11111010101
10001010111
10101010001
10101011101
10100000101
10111111101
10010000001
11110111111
```

The current implementation encodes it as:

```text
11x12:7/QG+sFfqxXqjV2gt/ZA+/A=
```

Metadata can be appended without breaking the original format:

```text
11x12:7/QG+sFfqxXqjV2gt/ZA+/A=;entrance=3,0;exit=3,11
```

## Install

For local development:

```bash
pip install -e .
```

For development with tests:

```bash
pip install -e ".[dev]"
```

## Usage

```python
from bmn import (
    decode_bmn,
    decode_bmn_with_metadata,
    encode_bmn,
    read_maze,
    render_maze_svg,
)

matrix = read_maze("mazefile/mazeBin1.mz")

bmn = encode_bmn(
    matrix,
    metadata={
        "entrance": (3, 0),
        "exit": (3, 11),
        "start": (3, 0),
        "goal": (3, 11),
    },
)

decoded = decode_bmn(bmn)
decoded_with_metadata, metadata = decode_bmn_with_metadata(bmn)
svg = render_maze_svg(decoded, "maze.svg")
```

## API

- `read_maze(path)`: reads a text file containing a binary maze matrix.
- `validate_maze(matrix)`: validates that a matrix is non-empty, rectangular, and contains only `0` and `1`.
- `encode_bmn(matrix, metadata=None)`: encodes a validated binary maze as BMN.
- `decode_bmn(bmn)`: decodes BMN back into a matrix, ignoring optional metadata for backward compatibility.
- `decode_bmn_with_metadata(bmn)`: decodes BMN and returns `(matrix, metadata)`.
- `render_maze_svg(matrix, path=None, ...)`: renders the matrix as an SVG image and optionally writes it to disk.

## Validation

The encoder rejects:

- empty matrices;
- rows with different widths;
- empty rows;
- values other than `0` or `1`.

The decoder raises explanatory `ValueError` exceptions for:

- missing `:` separators;
- invalid dimensions;
- missing payloads;
- invalid Base64 payloads;
- payloads that are too short for the declared dimensions;
- malformed metadata segments.

## Running The Demo

```bash
python examples/encode_decode_demo.py
```

The demo loads `mazefile/mazeBin1.mz`, prints the BMN string, decodes it, prints metadata, reconstructs the matrix, and renders an SVG.

## Running Tests

```bash
pytest -q
```

## Why BMN?

BMN is inspired by compact board-state notations such as chess FEN. Its goal is to make maze structures easy to store, transmit, compare, and reconstruct in games, simulations, pathfinding experiments, and AI studies.
