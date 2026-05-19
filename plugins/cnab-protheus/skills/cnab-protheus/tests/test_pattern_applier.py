from pathlib import Path

import pytest

from scripts.pattern_applier import (
    PatternApplier,
    PatternError,
)
from scripts.spec_loader import FieldSpec


@pytest.fixture
def applier(field_patterns_path):
    return PatternApplier(field_patterns_path)


def test_apply_literal_constant(applier):
    fs = FieldSpec(
        register="20", subtype="H", name="BANCO",
        start=1, end=3, flag="0",
        pattern="literal_constant", args={"value": "001"},
    )
    assert applier.apply(fs) == '"001"'


def test_apply_date_ddmmaaaa(applier):
    fs = FieldSpec(
        register="20", subtype="H", name="DATA",
        start=144, end=151, flag="0",
        pattern="date_ddmmaaaa", args={"src": "DDATABASE"},
    )
    result = applier.apply(fs)
    assert result == "SUBS(DTOS(DDATABASE),7,2)+SUBS(DTOS(DDATABASE),5,2)+SUBS(DTOS(DDATABASE),1,4)"


def test_apply_value_centavos_zeropad(applier):
    fs = FieldSpec(
        register="25", subtype="D", name="VALOR",
        start=103, end=119, flag="0",
        pattern="value_centavos_zeropad",
        args={"src": "SE2->E2_JUROS", "length": 17},
    )
    assert applier.apply(fs) == "STRZERO(INT(SE2->E2_JUROS*100), 17)"


def test_apply_filler_spaces(applier):
    fs = FieldSpec(
        register="20", subtype="H", name="FILLER",
        start=212, end=240, flag="0",
        pattern="filler_spaces", args={"length": 29},
    )
    assert applier.apply(fs) == "SPACE(29)"


def test_apply_unknown_pattern_raises(applier):
    fs = FieldSpec(
        register="20", subtype="H", name="X",
        start=1, end=2, flag="0",
        pattern="totally_not_a_pattern", args={},
    )
    with pytest.raises(PatternError, match="unknown pattern"):
        applier.apply(fs)


def test_apply_missing_arg_raises(applier):
    fs = FieldSpec(
        register="20", subtype="H", name="X",
        start=1, end=2, flag="0",
        pattern="literal_constant", args={},  # missing "value"
    )
    with pytest.raises(PatternError, match="missing arg"):
        applier.apply(fs)
