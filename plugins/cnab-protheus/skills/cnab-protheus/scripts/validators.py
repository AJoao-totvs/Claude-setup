"""Local syntactic validation of Protheus SIGACFG (.2PE/.2PR) content."""

from dataclasses import dataclass
import re

LINE_LENGTH = 500


class ValidationError(Exception):
    pass


def validate_line_length(lines: list[str]) -> None:
    for i, line in enumerate(lines, start=1):
        if len(line) != LINE_LENGTH:
            raise ValidationError(
                f"line {i}: length {len(line)}, expected {LINE_LENGTH}"
            )


@dataclass
class FieldDefinition:
    register: str
    subtype: str
    name: str
    start: int
    end: int
    flag: str
    expression: str


_REGISTER_COLS = slice(0, 2)
_SUBTYPE_COLS = slice(2, 4)
_NAME_COLS = slice(4, 20)
_POSITION_COLS = slice(20, 27)
_EXPRESSION_COLS = slice(27, LINE_LENGTH)

# Section 1 (Declaration) columns
_DECL_NAME_COLS = slice(4, 37)
_DECL_CONDITION_COLS = slice(37, LINE_LENGTH)

# Position block: 6 consecutive digits followed by any single char (the flag)
_POSITION_BLOCK_RE = re.compile(r"(\d{6})(.)")


def parse_field_definition(line: str) -> FieldDefinition:
    if len(line) != LINE_LENGTH:
        raise ValidationError(f"line not 500 chars: got {len(line)}")
    register = line[_REGISTER_COLS]
    subtype = line[_SUBTYPE_COLS].rstrip()

    # Find position block starting at or after col 4 (after register+subtype)
    rest = line[4:]
    match = _POSITION_BLOCK_RE.search(rest)
    if not match:
        raise ValidationError(f"no position block found in line: {line[:80]!r}")

    name = rest[: match.start()].rstrip()
    start_str = match.group(1)[0:3]
    end_str = match.group(1)[3:6]
    flag = match.group(2)
    expression = rest[match.end() :].rstrip()

    return FieldDefinition(
        register=register,
        subtype=subtype,
        name=name,
        start=int(start_str),
        end=int(end_str),
        flag=flag,
        expression=expression,
    )


@dataclass
class Declaration:
    register: str
    subtype: str
    name: str
    condition: str


def parse_declaration(line: str) -> Declaration:
    if len(line) != LINE_LENGTH:
        raise ValidationError(f"line not 500 chars: got {len(line)}")
    register = line[_REGISTER_COLS]
    subtype = line[_SUBTYPE_COLS].rstrip()
    name = line[_DECL_NAME_COLS].rstrip()
    condition = line[_DECL_CONDITION_COLS].rstrip()
    return Declaration(
        register=register,
        subtype=subtype,
        name=name,
        condition=condition,
    )


SECTION_1_REGISTERS = {"10", "11", "12", "13", "14", "15", "16", "17"}
SECTION_2_REGISTERS = {"20", "21", "22", "23", "24", "25", "26", "27"}
KNOWN_REGISTERS = SECTION_1_REGISTERS | SECTION_2_REGISTERS


def split_sections(lines: list[str]) -> tuple[list[str], list[str]]:
    """Split lines into section 1 (declarations) and section 2 (field definitions)."""
    section1 = []
    section2 = []
    for line in lines:
        reg = line[_REGISTER_COLS]
        if reg in SECTION_1_REGISTERS:
            section1.append(line)
        elif reg in SECTION_2_REGISTERS:
            section2.append(line)
    return section1, section2


def validate_file_structure(lines: list[str]) -> None:
    """Validate entire file structure: all lines 500 chars, all registers known, no out-of-order sections."""
    validate_line_length(lines)
    seen_section_2 = False
    for i, line in enumerate(lines, start=1):
        reg = line[_REGISTER_COLS]
        if reg not in KNOWN_REGISTERS:
            raise ValidationError(f"line {i}: unknown register '{reg}'")
        if reg in SECTION_2_REGISTERS:
            seen_section_2 = True
        elif seen_section_2 and reg in SECTION_1_REGISTERS:
            raise ValidationError(
                f"line {i}: section-1 register '{reg}' after section-2 started"
            )
