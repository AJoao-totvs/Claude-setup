"""Load and validate YAML spec describing one (bank, operation, direction) layout."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


class SpecValidationError(Exception):
    pass


_VALID_DIRECTIONS = {"remessa", "retorno"}
_VALID_SUBTYPES = {"H", "T", "D", "D1"}


@dataclass
class Declaration:
    register: str
    subtype: str
    name: str
    condition: str


@dataclass
class FieldSpec:
    register: str
    subtype: str
    name: str
    start: int
    end: int
    flag: str
    pattern: str
    args: dict[str, Any] = field(default_factory=dict)


@dataclass
class Spec:
    banco: str
    operacao: str
    direcao: str
    declaracoes: list[Declaration]
    campos: list[FieldSpec]


def load_spec(path: Path) -> Spec:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise SpecValidationError("spec root must be a mapping")
    for required in ("banco", "operacao", "direcao", "declaracoes", "campos"):
        if required not in raw:
            raise SpecValidationError(f"missing required key: {required}")
    if raw["direcao"] not in _VALID_DIRECTIONS:
        raise SpecValidationError(
            f"direcao must be one of {_VALID_DIRECTIONS}, got {raw['direcao']!r}"
        )
    declaracoes = [_parse_declaration(d) for d in raw["declaracoes"]]
    campos = [_parse_field(f) for f in raw["campos"]]
    _check_no_overlap(campos)
    return Spec(
        banco=str(raw["banco"]),
        operacao=str(raw["operacao"]),
        direcao=str(raw["direcao"]),
        declaracoes=declaracoes,
        campos=campos,
    )


def _parse_declaration(d: dict[str, Any]) -> Declaration:
    for k in ("register", "subtype", "name", "condition"):
        if k not in d:
            raise SpecValidationError(f"declaration missing key: {k}")
    if d["subtype"] not in _VALID_SUBTYPES:
        raise SpecValidationError(f"invalid subtype: {d['subtype']!r}")
    return Declaration(
        register=str(d["register"]),
        subtype=str(d["subtype"]),
        name=str(d["name"]),
        condition=str(d["condition"]),
    )


def _parse_field(f: dict[str, Any]) -> FieldSpec:
    for k in ("register", "subtype", "name", "start", "end", "flag", "pattern"):
        if k not in f:
            raise SpecValidationError(f"field missing key: {k}")
    if f["subtype"] not in _VALID_SUBTYPES:
        raise SpecValidationError(f"invalid subtype: {f['subtype']!r}")
    if int(f["start"]) > int(f["end"]):
        raise SpecValidationError(f"start > end in field {f['name']!r}")
    return FieldSpec(
        register=str(f["register"]),
        subtype=str(f["subtype"]),
        name=str(f["name"]),
        start=int(f["start"]),
        end=int(f["end"]),
        flag=str(f["flag"]),
        pattern=str(f["pattern"]),
        args=dict(f.get("args", {})),
    )


def _check_no_overlap(campos: list[FieldSpec]) -> None:
    # Per register+subtype, sort by start and check no overlap
    groups: dict[tuple[str, str], list[FieldSpec]] = {}
    for c in campos:
        groups.setdefault((c.register, c.subtype), []).append(c)
    for key, fields in groups.items():
        sorted_fields = sorted(fields, key=lambda x: x.start)
        for prev, curr in zip(sorted_fields, sorted_fields[1:]):
            if curr.start <= prev.end:
                raise SpecValidationError(
                    f"register {key[0]}{key[1]}: field {curr.name!r} (start {curr.start}) "
                    f"overlaps with {prev.name!r} (end {prev.end})"
                )
