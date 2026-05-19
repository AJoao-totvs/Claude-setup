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


from scripts.validators import Declaration, parse_declaration


def test_parse_declaration_always_true():
    # Reg (0-2): "10"
    # Sub (2-4): "H "
    # Name (4-37): "Header de Arquivo" (33 chars, right-padded)
    # Cond (37+): ".T."
    name = "Header de Arquivo".ljust(33)
    cond = ".T."
    raw = "10H " + name + cond
    line = raw + " " * (500 - len(raw))
    d = parse_declaration(line)
    assert d.register == "10"
    assert d.subtype == "H"
    assert d.name == "Header de Arquivo"
    assert d.condition == ".T."


def test_parse_declaration_iif_condition():
    name = "DETALHE - SEGTO A".ljust(33)
    cond = 'IIF(SEA->EA_MODELO $ "01/03/05/02/41/43",.T.,.F.)'
    raw = '11D ' + name + cond
    line = raw + " " * (500 - len(raw))
    d = parse_declaration(line)
    assert d.register == "11"
    assert d.subtype == "D"
    assert d.condition == cond


def test_parse_declaration_d1_subtype():
    name = "DETALHE SEGTO J-52".ljust(33)
    cond = "IIF(.T.,.F.)"
    raw = '13D1' + name + cond
    line = raw + " " * (500 - len(raw))
    d = parse_declaration(line)
    assert d.subtype == "D1"
    assert d.name == "DETALHE SEGTO J-52"


from scripts.validators import split_sections, validate_file_structure


def test_split_sections_basic():
    lines = [
        "10H " + "Header de Arquivo".ljust(33) + ".T." + " " * (500 - 40),
        "11D " + "DETALHE - SEGTO A".ljust(33) + ".T." + " " * (500 - 40),
        "20H " + "DOC".ljust(16) + "0010010" + '"001"' + " " * (500 - 32),
        "21D " + "NAME".ljust(16) + "0010010" + '"001"' + " " * (500 - 32),
    ]
    section1, section2 = split_sections(lines)
    assert len(section1) == 2
    assert len(section2) == 2
    assert section1[0].startswith("10H")
    assert section2[0].startswith("20H")


def test_validate_file_structure_round_trip(fixture_001pg_2pe_path):
    raw = fixture_001pg_2pe_path.read_bytes()
    text = raw.decode("cp1252")
    lines = text.split("\r\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    validate_file_structure(lines)  # should not raise


def test_validate_file_structure_unknown_register_raises():
    raw = "99X " + "Test".ljust(33) + ".T."
    lines = [raw + " " * (500 - len(raw))]
    assert len(lines[0]) == 500
    with pytest.raises(ValidationError, match=r"unknown register"):
        validate_file_structure(lines)


def test_validate_file_structure_section_order_violation():
    # Section 1 after section 2 should raise
    line1 = "25D " + "NAME".ljust(16) + "0010010" + '"001"' + " " * (500 - 32)  # section 2
    line2 = "10H " + "Header".ljust(33) + ".T." + " " * (500 - 40)  # section 1 - OUT OF ORDER
    lines = [line1, line2]
    with pytest.raises(ValidationError, match=r"section-1 register.*after section-2"):
        validate_file_structure(lines)


def test_parse_field_definition_with_flag():
    # Test the flag extraction (line 44 coverage)
    name = "TEST".ljust(16)
    pos = "0100101"  # start=010, end=010, flag=1
    expr = "EXPR"
    raw = '24H ' + name + pos + expr
    line = raw + " " * (500 - len(raw))
    fd = parse_field_definition(line)
    assert fd.flag == "1"
    assert fd.start == 10
    assert fd.end == 10


def test_split_sections_with_mixed_types():
    # Test that split_sections handles both section 1 and 2 registers correctly
    line1 = "10H " + "Header".ljust(33) + ".T." + " " * (500 - 40)
    line2 = "25D " + "FIELD1".ljust(16) + "0010010" + '"001"' + " " * (500 - 32)
    line3 = "11D " + "Detail".ljust(33) + "IIF(.T.)" + " " * (500 - 45)
    line4 = "24T " + "TRAILER".ljust(16) + "0100100" + '"002"' + " " * (500 - 32)
    lines = [line1, line2, line3, line4]
    section1, section2 = split_sections(lines)
    # Should have section 1 registers 10, 11
    assert len(section1) == 2
    # Should have section 2 registers 25, 24
    assert len(section2) == 2
    assert section1[0][0:2] == "10"
    assert section1[1][0:2] == "11"
    assert section2[0][0:2] == "25"
    assert section2[1][0:2] == "24"


def test_parse_field_definition_variable_length_name():
    """Fixture has some lines where name is 15 chars and runs directly into position with no trailing space."""
    # INSC DIV ATI/ET (15 chars) followed by 0460620
    name = "INSC DIV ATI/ET"  # exactly 15 chars, no padding
    pos = "0460620"  # start=046, end=062, flag=0
    raw = "25D " + name + pos
    line = raw + " " * (500 - len(raw))
    assert len(line) == 500
    fd = parse_field_definition(line)
    assert fd.register == "25"
    assert fd.subtype == "D"
    assert fd.name == "INSC DIV ATI/ET"
    assert fd.start == 46
    assert fd.end == 62
    assert fd.flag == "0"
    assert fd.expression == ""


def test_parse_field_definition_variable_length_with_expression():
    """Another variant: name is 15 chars, position block, then expression."""
    # This tests the regex correctly finds position and extracts expression
    name = "SOME LONG NAME"  # 14 chars
    pos = "0010050"  # start=001, end=005, flag=0
    expr = "EXPR()"
    raw = "24H " + name + pos + expr
    line = raw + " " * (500 - len(raw))
    assert len(line) == 500
    fd = parse_field_definition(line)
    assert fd.register == "24"
    assert fd.subtype == "H"
    assert fd.name == "SOME LONG NAME"
    assert fd.start == 1
    assert fd.end == 5
    assert fd.flag == "0"
    assert fd.expression == "EXPR()"
