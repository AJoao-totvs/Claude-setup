import pytest

from scripts.validators import (
    ValidationError,
    validate_line_length,
)


def test_validate_line_length_ok():
    lines = ["x" * 500, "y" * 500]
    validate_line_length(lines)  # no raise


def test_validate_line_length_short_raises():
    lines = ["x" * 500, "short"]
    with pytest.raises(ValidationError, match=r"line 2.*length 5.*expected 500"):
        validate_line_length(lines)


def test_validate_line_length_long_raises():
    lines = ["x" * 501]
    with pytest.raises(ValidationError, match=r"line 1.*length 501"):
        validate_line_length(lines)


from scripts.validators import FieldDefinition, parse_field_definition


def test_parse_field_definition_basic():
    # Reg (0-2): "24"
    # Sub (2-4): "H "
    # Name (4-20): "DOC            " (16 chars, right-padded)
    # Pos (20-27): "0490500" (start=049, end=050, flag=0)
    # Exp (27+): "IIF(...)"
    name = "DOC".ljust(16)
    pos = "0490500"
    expr = 'IIF(SEA->EA_MODELO $ "17", "09","01")'
    raw = "24H " + name + pos + expr
    line = raw + " " * (500 - len(raw))
    assert len(line) == 500
    fd = parse_field_definition(line)
    assert fd.register == "24"
    assert fd.subtype == "H"
    assert fd.name == "DOC"
    assert fd.start == 49
    assert fd.end == 50
    assert fd.flag == "0"
    assert fd.expression == expr


def test_parse_field_definition_constant_value():
    name = "TIPO REGISTRO".ljust(16)
    pos = "0010010"
    expr = '"M"'
    raw = '25D ' + name + pos + expr
    line = raw + " " * (500 - len(raw))
    fd = parse_field_definition(line)
    assert fd.register == "25"
    assert fd.subtype == "D"
    assert fd.name == "TIPO REGISTRO"
    assert fd.start == 1
    assert fd.end == 1
    assert fd.flag == "0"
    assert fd.expression == '"M"'


def test_parse_field_definition_d1_subtype():
    name = "DETALHE SEGTO J-52".ljust(16)
    pos = "0000000"  # D1 subtype with position
    expr = "IIF(.T.,.F.)"
    raw = '13D1' + name + pos + expr
    line = raw + " " * (500 - len(raw))
    fd = parse_field_definition(line)
    assert fd.subtype == "D1"
    assert fd.name == "DETALHE SEGTO J-"  # Truncated to 16 chars


def test_parse_field_definition_blank_expression():
    name = "COD RECEITA".ljust(16)
    pos = "0100130"
    expr = ""
    raw = '25D ' + name + pos + expr
    line = raw + " " * (500 - len(raw))
    fd = parse_field_definition(line)
    assert fd.register == "25"
    assert fd.name == "COD RECEITA"
    assert fd.start == 10
    assert fd.end == 13
    assert fd.expression == ""
