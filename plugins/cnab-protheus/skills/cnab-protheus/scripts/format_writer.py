"""Protheus SIGACFG format writer (.2PE / .2PR)."""

LINE_LENGTH = 500
ENCODING = "cp1252"


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
