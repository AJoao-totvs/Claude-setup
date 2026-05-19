"""Protheus SIGACFG format writer (.2PE / .2PR)."""

from pathlib import Path

LINE_LENGTH = 500
ENCODING = "cp1252"
LINE_TERMINATOR = b"\r\n"


def pad_to_500(s: str) -> str:
    if len(s) > LINE_LENGTH:
        raise ValueError(f"Content exceeds 500 chars: {len(s)}")
    return s.ljust(LINE_LENGTH, " ")


def encode_ansi(s: str, policy: str = "replace") -> bytes:
    """Encode string to Windows-1252 (Protheus SIGACFG canonical encoding).

    policy: 'replace' (default) substitutes unencodable chars with '?'.
            'strict' raises UnicodeEncodeError instead.
    """
    return s.encode(ENCODING, errors=policy)


def write_line(content: str) -> bytes:
    """Pad content to 500 chars, encode CP-1252, append CRLF. Returns 502 bytes."""
    padded = pad_to_500(content)
    return encode_ansi(padded) + LINE_TERMINATOR


def write_file(path: Path, lines: list[str]) -> None:
    """Write all lines to file as Protheus SIGACFG (500 chars + CRLF each)."""
    with open(path, "wb") as f:
        for line in lines:
            f.write(write_line(line))
