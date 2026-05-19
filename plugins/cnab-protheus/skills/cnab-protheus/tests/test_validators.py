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
