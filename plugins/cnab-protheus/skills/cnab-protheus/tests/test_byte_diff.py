"""Tests for byte_diff module."""

from pathlib import Path

import pytest

from scripts.byte_diff import diff_files


def test_identical_files(tmp_path):
    """Test that identical files produce no diffs."""
    content = b"line 1\r\nline 2\r\nline 3\r\n"
    gen = tmp_path / "generated.txt"
    ref = tmp_path / "reference.txt"
    gen.write_bytes(content)
    ref.write_bytes(content)

    result = diff_files(gen, ref)
    assert result.identical is True
    assert len(result.diffs) == 0


def test_different_content(tmp_path):
    """Test that different content produces diffs."""
    gen = tmp_path / "generated.txt"
    ref = tmp_path / "reference.txt"
    gen.write_bytes(b"line 1\r\nline 2\r\n")
    ref.write_bytes(b"line 1\r\nline 2 modified\r\n")

    result = diff_files(gen, ref)
    assert result.identical is False
    assert len(result.diffs) == 1
    assert result.diffs[0].line == 2
    assert result.diffs[0].expected == b"line 2 modified"
    assert result.diffs[0].actual == b"line 2"


def test_different_line_counts_missing_lines(tmp_path):
    """Test when actual file has fewer lines than expected."""
    gen = tmp_path / "generated.txt"
    ref = tmp_path / "reference.txt"
    gen.write_bytes(b"line 1\r\nline 2\r\n")
    ref.write_bytes(b"line 1\r\nline 2\r\nline 3\r\n")

    result = diff_files(gen, ref)
    assert result.identical is False
    assert len(result.diffs) == 1
    assert result.diffs[0].line == 3
    assert result.diffs[0].actual == b""
    assert result.diffs[0].expected == b"line 3"
    assert "only" in result.diffs[0].message


def test_different_line_counts_extra_lines(tmp_path):
    """Test when actual file has more lines than expected."""
    gen = tmp_path / "generated.txt"
    ref = tmp_path / "reference.txt"
    gen.write_bytes(b"line 1\r\nline 2\r\nline 3\r\n")
    ref.write_bytes(b"line 1\r\nline 2\r\n")

    result = diff_files(gen, ref)
    assert result.identical is False
    assert len(result.diffs) == 1
    assert result.diffs[0].line == 3
    assert result.diffs[0].actual == b"line 3"
    assert result.diffs[0].expected == b""
    assert "extra" in result.diffs[0].message


def test_multiple_diffs(tmp_path):
    """Test file with multiple differences."""
    gen = tmp_path / "generated.txt"
    ref = tmp_path / "reference.txt"
    gen.write_bytes(b"line 1 bad\r\nline 2\r\nline 3\r\n")
    ref.write_bytes(b"line 1 good\r\nline 2\r\nline 3 bad\r\n")

    result = diff_files(gen, ref)
    assert result.identical is False
    assert len(result.diffs) == 2
    assert result.diffs[0].line == 1
    assert result.diffs[1].line == 3
