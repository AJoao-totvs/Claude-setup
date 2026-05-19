"""Local syntactic validation of Protheus SIGACFG (.2PE/.2PR) content."""

LINE_LENGTH = 500


class ValidationError(Exception):
    pass


def validate_line_length(lines: list[str]) -> None:
    for i, line in enumerate(lines, start=1):
        if len(line) != LINE_LENGTH:
            raise ValidationError(
                f"line {i}: length {len(line)}, expected {LINE_LENGTH}"
            )
