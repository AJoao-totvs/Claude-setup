import pytest

from scripts.format_writer import pad_to_500


def test_pad_to_500_short_string():
    result = pad_to_500("hello")
    assert len(result) == 500
    assert result.startswith("hello")
    assert result[5:] == " " * 495


def test_pad_to_500_empty_string():
    result = pad_to_500("")
    assert len(result) == 500
    assert result == " " * 500


def test_pad_to_500_exact_500():
    s = "x" * 500
    result = pad_to_500(s)
    assert result == s
    assert len(result) == 500


def test_pad_to_500_too_long_raises():
    s = "x" * 501
    with pytest.raises(ValueError, match="exceeds 500 chars"):
        pad_to_500(s)
