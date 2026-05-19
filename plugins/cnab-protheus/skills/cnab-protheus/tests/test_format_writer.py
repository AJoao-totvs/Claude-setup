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


from scripts.format_writer import encode_ansi


def test_encode_ansi_pure_ascii():
    result = encode_ansi("hello")
    assert result == b"hello"


def test_encode_ansi_accented_pt_br():
    result = encode_ansi("ação")
    assert result == "ação".encode("cp1252")


def test_encode_ansi_replaces_unencodable():
    # Emoji not in cp1252; with default policy "replace", becomes "?"
    result = encode_ansi("hi 🚀")
    assert result == b"hi ?"


def test_encode_ansi_strict_raises_on_unencodable():
    with pytest.raises(UnicodeEncodeError):
        encode_ansi("hi 🚀", policy="strict")


from scripts.format_writer import write_line


def test_write_line_returns_bytes_of_length_502():
    # 500 content + CRLF = 502
    result = write_line("hello")
    assert len(result) == 502
    assert result.endswith(b"\r\n")


def test_write_line_pads_with_spaces():
    result = write_line("hello")
    assert result[:5] == b"hello"
    assert result[5:500] == b" " * 495


def test_write_line_encodes_accented():
    result = write_line("ação")
    assert result[:4] == "ação".encode("cp1252")


def test_write_line_too_long_raises():
    with pytest.raises(ValueError, match="exceeds 500 chars"):
        write_line("x" * 501)


from pathlib import Path

from scripts.format_writer import write_file


def test_write_file_writes_lines_with_crlf(tmp_path):
    output = tmp_path / "out.2PE"
    write_file(output, ["line1", "line2", "line3"])
    raw = output.read_bytes()
    assert len(raw) == 502 * 3
    assert raw[500:502] == b"\r\n"
    assert raw[1002:1004] == b"\r\n"
    assert raw[1504:1506] == b"\r\n"


def test_write_file_no_trailing_extra_newline(tmp_path):
    output = tmp_path / "out.2PE"
    write_file(output, ["only"])
    raw = output.read_bytes()
    # Exactly 502 bytes — 500 content + CRLF — no extra
    assert len(raw) == 502
    assert raw[-2:] == b"\r\n"


def test_write_file_empty_list(tmp_path):
    output = tmp_path / "out.2PE"
    write_file(output, [])
    assert output.read_bytes() == b""
