import pytest

from bmn import encode_bmn, decode_bmn


def test_encode_decode_round_trip():
    matrix = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ]
    bmn_string = encode_bmn(matrix)
    decoded = decode_bmn(bmn_string)
    assert decoded == matrix


def test_decode_bmn_invalid_dimension_characters():
    with pytest.raises(ValueError):
        decode_bmn("3xa:AA==")


def test_decode_bmn_inconsistent_dimensions():
    matrix = [[1, 0], [0, 1]]
    bmn_string = encode_bmn(matrix)
    tampered = bmn_string.replace("2x2", "3x3")
    with pytest.raises(IndexError):
        decode_bmn(tampered)
