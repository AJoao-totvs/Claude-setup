from pathlib import Path

import pytest
import yaml

from scripts.spec_loader import (
    Declaration,
    FieldSpec,
    Spec,
    SpecValidationError,
    load_spec,
)


@pytest.fixture
def minimal_spec_yaml(tmp_path) -> Path:
    spec = {
        "banco": "001",
        "operacao": "pagamento",
        "direcao": "remessa",
        "declaracoes": [
            {"register": "10", "subtype": "H", "name": "Header", "condition": ".T."},
        ],
        "campos": [
            {
                "register": "20",
                "subtype": "H",
                "name": "BANCO",
                "start": 1,
                "end": 3,
                "flag": "0",
                "pattern": "literal_constant",
                "args": {"value": "001"},
            }
        ],
    }
    path = tmp_path / "spec.yaml"
    path.write_text(yaml.safe_dump(spec))
    return path


def test_load_spec_basic(minimal_spec_yaml):
    spec = load_spec(minimal_spec_yaml)
    assert isinstance(spec, Spec)
    assert spec.banco == "001"
    assert spec.operacao == "pagamento"
    assert spec.direcao == "remessa"
    assert len(spec.declaracoes) == 1
    assert spec.declaracoes[0].register == "10"
    assert len(spec.campos) == 1
    assert spec.campos[0].pattern == "literal_constant"


def test_load_spec_missing_banco_raises(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text("operacao: pagamento\ndireção: remessa\n")
    with pytest.raises(SpecValidationError, match="banco"):
        load_spec(path)


def test_load_spec_invalid_direcao_raises(tmp_path):
    bad = {
        "banco": "001",
        "operacao": "pagamento",
        "direcao": "lateral",  # invalid
        "declaracoes": [],
        "campos": [],
    }
    path = tmp_path / "bad.yaml"
    path.write_text(yaml.safe_dump(bad))
    with pytest.raises(SpecValidationError, match="direcao"):
        load_spec(path)


def test_load_spec_different_flag_overlap_allowed(tmp_path):
    # Overlapping fields with different flags are allowed (conditional rendering).
    spec_data = {
        "banco": "001",
        "operacao": "pagamento",
        "direcao": "remessa",
        "declaracoes": [],
        "campos": [
            {
                "register": "20", "subtype": "H", "name": "A",
                "start": 1, "end": 5, "flag": "0",
                "pattern": "filler_spaces", "args": {"length": 5},
            },
            {
                "register": "20", "subtype": "H", "name": "B",
                "start": 4, "end": 10, "flag": "1",  # overlaps with A but DIFFERENT flag
                "pattern": "filler_spaces", "args": {"length": 7},
            },
        ],
    }
    path = tmp_path / "spec.yaml"
    path.write_text(yaml.safe_dump(spec_data))
    # Should load successfully (different flags allow overlaps)
    spec = load_spec(path)
    assert len(spec.campos) == 2


def test_load_spec_same_flag_overlap_raises(tmp_path):
    # Overlapping fields with the same flag should raise.
    spec_data = {
        "banco": "001",
        "operacao": "pagamento",
        "direcao": "remessa",
        "declaracoes": [],
        "campos": [
            {
                "register": "20", "subtype": "H", "name": "A",
                "start": 1, "end": 5, "flag": "0",
                "pattern": "filler_spaces", "args": {"length": 5},
            },
            {
                "register": "20", "subtype": "H", "name": "B",
                "start": 4, "end": 10, "flag": "0",  # overlaps with A, SAME flag
                "pattern": "filler_spaces", "args": {"length": 7},
            },
        ],
    }
    path = tmp_path / "spec.yaml"
    path.write_text(yaml.safe_dump(spec_data))
    # Should raise due to overlap with same flag
    with pytest.raises(SpecValidationError, match="overlaps"):
        load_spec(path)


def test_load_spec_malformed_yaml_raises(tmp_path):
    # Invalid YAML should be wrapped in SpecValidationError with context.
    path = tmp_path / "bad.yaml"
    path.write_text("invalid: yaml: content:\n  - unbalanced")
    with pytest.raises(SpecValidationError, match="failed to parse YAML"):
        load_spec(path)
