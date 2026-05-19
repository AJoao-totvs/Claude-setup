"""Apply field-pattern templates to FieldSpec to produce ADVPL expression strings."""

import re
import string
from pathlib import Path
from typing import Any

import yaml

from scripts.spec_loader import FieldSpec


class PatternError(Exception):
    pass


# Match {name} placeholders in templates
_PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")


class PatternApplier:
    def __init__(self, patterns_yaml: Path):
        raw = yaml.safe_load(patterns_yaml.read_text(encoding="utf-8"))
        self.patterns: dict[str, dict[str, Any]] = raw["patterns"]

    def apply(self, field: FieldSpec) -> str:
        if field.pattern not in self.patterns:
            raise PatternError(f"unknown pattern: {field.pattern!r}")
        template = self.patterns[field.pattern]["template"]
        if template == "":
            return ""
        placeholders = set(_PLACEHOLDER_RE.findall(template))
        for ph in placeholders:
            if ph not in field.args:
                raise PatternError(
                    f"missing arg {ph!r} for pattern {field.pattern!r} "
                    f"in field {field.name!r}"
                )
        # str.format-style substitution
        return template.format(**field.args)
