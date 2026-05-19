"""Local syntactic validation of Protheus SIGACFG (.2PE/.2PR) content."""

from dataclasses import dataclass

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


def parse_field_definition(line: str) -> FieldDefinition:
    if len(line) != LINE_LENGTH:
        raise ValidationError(f"line not 500 chars: got {len(line)}")
    register = line[_REGISTER_COLS]
    subtype = line[_SUBTYPE_COLS].rstrip()
    name = line[_NAME_COLS].rstrip()
    position = line[_POSITION_COLS]
    expression = line[_EXPRESSION_COLS].rstrip()
    start = int(position[0:3])
    end = int(position[3:6])
    flag = position[6]
    return FieldDefinition(
        register=register,
        subtype=subtype,
        name=name,
        start=start,
        end=end,
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
