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
    def __init__(self, patterns_yaml: Path) -> None:
        try:
            raw = yaml.safe_load(patterns_yaml.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            raise PatternError(f"failed to parse patterns YAML at {patterns_yaml}: {e}") from e
        if not isinstance(raw, dict) or "patterns" not in raw:
            raise PatternError("patterns YAML must have a top-level 'patterns' mapping")
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
