"""Protheus SIGACFG format writer (.2PE / .2PR)."""

LINE_LENGTH = 500


def pad_to_500(s: str) -> str:
    if len(s) > LINE_LENGTH:
        raise ValueError(f"Content exceeds 500 chars: {len(s)}")
    return s.ljust(LINE_LENGTH, " ")
