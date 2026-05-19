from pathlib import Path

import pytest


SKILL_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = SKILL_ROOT / "references" / "fixtures"
MAPPINGS_DIR = SKILL_ROOT / "references" / "mappings"
SPECS_DIR = SKILL_ROOT / "references" / "specs"


@pytest.fixture
def fixture_001pg_2pe_path() -> Path:
    return FIXTURES_DIR / "001PG.2PE"


@pytest.fixture
def fixture_001pg_2pr_path() -> Path:
    return FIXTURES_DIR / "001PG.2PR"


@pytest.fixture
def fixture_001pg_2pe_bytes(fixture_001pg_2pe_path: Path) -> bytes:
    return fixture_001pg_2pe_path.read_bytes()


@pytest.fixture
def bb_pagamento_spec_path() -> Path:
    return SPECS_DIR / "bb" / "pagamento.yaml"


@pytest.fixture
def field_patterns_path() -> Path:
    return MAPPINGS_DIR / "field-patterns.yaml"


@pytest.fixture
def source_mappings_path() -> Path:
    return MAPPINGS_DIR / "source-mappings.yaml"
