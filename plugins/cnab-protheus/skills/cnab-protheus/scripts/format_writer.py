"""Protheus SIGACFG format writer (.2PE / .2PR)."""

import warnings
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

    policy: 'replace' (default) substitutes unencodable chars with '?' and emits a warning.
            'strict' raises UnicodeEncodeError instead.
            'silent' replaces without warning (use only for tests).
    """
    if policy == "silent":
        return s.encode(ENCODING, errors="replace")
    if policy == "strict":
        return s.encode(ENCODING, errors="strict")
    # default "replace" path: try strict first, warn on failure, then replace
    try:
        return s.encode(ENCODING, errors="strict")
    except UnicodeEncodeError as e:
        warnings.warn(
            f"Non-CP1252 chars replaced with '?' (position {e.start}-{e.end}): {s[e.start:e.end]!r}",
            UnicodeWarning,
            stacklevel=2,
        )
        return s.encode(ENCODING, errors="replace")


def write_line(content: str) -> bytes:
    """Pad content to 500 chars, encode CP-1252, append CRLF. Returns 502 bytes."""
    padded = pad_to_500(content)
    return encode_ansi(padded) + LINE_TERMINATOR


def write_file(path: Path, lines: list[str]) -> None:
    """Write all lines to file as Protheus SIGACFG (500 chars + CRLF each).

    Raises:
        OSError: if path's parent directory doesn't exist or write fails.
    """
    try:
        with open(path, "wb") as f:
            for line in lines:
                f.write(write_line(line))
    except OSError as e:
        raise OSError(f"failed to write {path}: {e}") from e
