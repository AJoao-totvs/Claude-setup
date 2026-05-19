"""Generate Protheus SIGACFG .2PE/.2PR configuration from spec + pattern applier."""

import sys
from pathlib import Path

from .format_writer import write_file
from .pattern_applier import PatternApplier
from .spec_loader import Declaration, FieldSpec, Spec, load_spec


def render_declaration(d: Declaration) -> str:
    """Render section-1 (declaration) line.

    Layout: RR T NomeDoRegistro<pad até col 37>CONDIÇÃO
    Columns:
      0-1:  register (2 chars)
      2-3:  subtype (padded to 2 chars)
      4-36: name (padded to 33 chars)
      37+:  condition
    """
    register = d.register
    subtype = d.subtype.ljust(2)  # "H " or "D1"
    name = d.name.ljust(33)  # pad to 33 chars
    condition = d.condition
    return f"{register}{subtype}{name}{condition}"


def render_field(f: FieldSpec, applier: PatternApplier) -> str:
    """Render section-2 (field) line.

    Layout: RR T NomeCampo<pad var>SSSEEEF<expression>
    Columns:
      0-1:  register (2 chars)
      2-3:  subtype + space (2 chars, e.g. "D " or "H ")
      4+:   name (from spec, which may be 14 or 15 chars - use as-is)
      +:    position block (SSS EEE F where S=start, E=end, F=flag, 7 chars)
      +:    expression

    Note: Most spec names are pre-padded to 15 chars. A few exceptional names
    (e.g., "USO FEBRA/CNAB") are stored in spec as-is (14 chars).
    """
    register = f.register
    subtype = f.subtype.ljust(2)
    name = f.name  # Use name exactly as stored in spec (no additional padding)
    position = f"{f.start:03d}{f.end:03d}{f.flag}"
    expression = applier.apply(f)
    return f"{register}{subtype}{name}{position}{expression}"


def generate(spec: Spec, applier: PatternApplier) -> list[str]:
    """Generate all lines: declarations first, then fields."""
    lines: list[str] = []
    for decl in spec.declaracoes:
        lines.append(render_declaration(decl))
    for field in spec.campos:
        lines.append(render_field(field, applier))
    return lines


def main() -> None:
    """CLI: load spec, apply patterns, write output file."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Protheus SIGACFG configuration"
    )
    parser.add_argument(
        "--spec", required=True, type=Path, help="Path to spec YAML"
    )
    parser.add_argument(
        "--patterns", required=True, type=Path, help="Path to field-patterns YAML"
    )
    parser.add_argument(
        "--output", required=True, type=Path, help="Output .2PE/.2PR file"
    )

    args = parser.parse_args()

    spec = load_spec(args.spec)
    applier = PatternApplier(args.patterns)
    lines = generate(spec, applier)
    write_file(args.output, lines)

    print(f"Generated {len(lines)} lines to {args.output}")


if __name__ == "__main__":
    main()
