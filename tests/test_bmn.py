import pytest

from bmn import (
    decode_bmn,
    decode_bmn_with_metadata,
    encode_bmn,
    read_maze,
    render_maze_svg,
)


def test_encode_decode_round_trip():
    matrix = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ]
    bmn_string = encode_bmn(matrix)
    decoded = decode_bmn(bmn_string)
    assert decoded == matrix


def test_encode_rejects_non_rectangular_matrix():
    with pytest.raises(ValueError, match="rectangular"):
        encode_bmn([[1, 0], [0]])


def test_encode_rejects_non_binary_values():
    with pytest.raises(ValueError, match="only 0 or 1"):
        encode_bmn([[1, 2]])


def test_read_maze_rejects_invalid_characters(tmp_path):
    maze_path = tmp_path / "bad.mz"
    maze_path.write_text("101\n10x\n", encoding="utf-8")

    with pytest.raises(ValueError, match="invalid character"):
        read_maze(maze_path)


def test_decode_bmn_invalid_dimension_characters():
    with pytest.raises(ValueError, match="dimensions"):
        decode_bmn("3xa:AA==")


def test_decode_bmn_inconsistent_dimensions():
    matrix = [[1, 0], [0, 1]]
    bmn_string = encode_bmn(matrix)
    tampered = bmn_string.replace("2x2", "3x3")
    with pytest.raises(ValueError, match="too short"):
        decode_bmn(tampered)


def test_decode_bmn_missing_separator():
    with pytest.raises(ValueError, match="separating dimensions"):
        decode_bmn("3x3AA==")


def test_decode_bmn_invalid_base64():
    with pytest.raises(ValueError, match="Base64"):
        decode_bmn("3x3:not-base64!")


def test_encode_decode_metadata():
    matrix = [[0, 1], [1, 0]]
    bmn_string = encode_bmn(
        matrix,
        metadata={
            "entrance": (0, 0),
            "exit": (1, 1),
            "label": "demo maze",
        },
    )

    decoded, metadata = decode_bmn_with_metadata(bmn_string)

    assert decoded == matrix
    assert metadata == {
        "entrance": "0,0",
        "exit": "1,1",
        "label": "demo maze",
    }


def test_decode_plain_bmn_ignores_metadata_for_backward_compatibility():
    matrix = [[0, 1], [1, 0]]
    bmn_string = encode_bmn(matrix, metadata={"start": (0, 0)})

    assert decode_bmn(bmn_string) == matrix


def test_render_maze_svg_returns_and_writes_svg(tmp_path):
    output_path = tmp_path / "maze.svg"

    svg = render_maze_svg([[1, 0], [0, 1]], output_path, cell_size=10)

    assert '<svg xmlns="http://www.w3.org/2000/svg"' in svg
    assert 'width="20"' in svg
    assert output_path.read_text(encoding="utf-8") == svg
