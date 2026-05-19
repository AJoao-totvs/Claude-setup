"""Integration test: BB pagamento byte-identical to 001PG.2PE fixture."""

from pathlib import Path

import pytest

from scripts.byte_diff import diff_files
from scripts.format_writer import write_file
from scripts.gen_protheus_config import generate
from scripts.pattern_applier import PatternApplier
from scripts.spec_loader import load_spec


def test_bb_pagamento_byte_identical(
    tmp_path: Path,
    bb_pagamento_spec_path: Path,
    field_patterns_path: Path,
    fixture_001pg_2pe_path: Path,
) -> None:
    """Generate 001PG.2PE from spec and compare byte-by-byte to fixture."""
    spec = load_spec(bb_pagamento_spec_path)
    applier = PatternApplier(field_patterns_path)
    lines = generate(spec, applier)
    output = tmp_path / "001PG.2PE"
    write_file(output, lines)

    result = diff_files(output, fixture_001pg_2pe_path)
    if not result.identical:
        msg_lines = [f"diff count: {len(result.diffs)}"]
        for d in result.diffs[:10]:
            msg_lines.append(
                f"  line {d.line}: expected={d.expected!r}, actual={d.actual!r}"
            )
            if d.message:
                msg_lines.append(f"    message: {d.message}")
        pytest.fail("\n".join(msg_lines))
    assert result.identical, "byte-diff against 001PG.2PE fixture failed"
