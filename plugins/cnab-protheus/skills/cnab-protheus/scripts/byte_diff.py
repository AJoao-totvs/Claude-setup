"""Byte-exact diff between generated and reference Protheus SIGACFG files."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LineDiff:
    line: int
    expected: bytes
    actual: bytes
    message: str = ""


@dataclass
class DiffResult:
    identical: bool
    diffs: list[LineDiff] = field(default_factory=list)


def diff_files(generated: Path, reference: Path) -> DiffResult:
    """Compare generated vs reference. Reference is the ground-truth fixture."""
    actual = generated.read_bytes().split(b"\r\n")
    expected = reference.read_bytes().split(b"\r\n")
    if actual and actual[-1] == b"":
        actual = actual[:-1]
    if expected and expected[-1] == b"":
        expected = expected[:-1]
    diffs: list[LineDiff] = []
    n = max(len(actual), len(expected))
    for i in range(n):
        a = actual[i] if i < len(actual) else b""
        e = expected[i] if i < len(expected) else b""
        if a != e:
            msg = ""
            if i >= len(actual):
                msg = f"actual file has only {len(actual)} lines; missing line {i+1}"
            elif i >= len(expected):
                msg = f"actual file has extra line {i+1} ({len(actual)} lines vs expected {len(expected)})"
            diffs.append(LineDiff(line=i + 1, expected=e, actual=a, message=msg))
    return DiffResult(identical=len(diffs) == 0, diffs=diffs)
