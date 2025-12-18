import pytest
from neurobik.config import Config

def test_valid_config():
    # Assuming sample_config.yaml exists
    cfg = Config.from_yaml('sample_config.yaml')
    cfg.validate()
    assert cfg.model_provider == 'ollama'
    assert len(cfg.models) == 1
    assert len(cfg.oci) == 1

def test_invalid_provider():
    with pytest.raises(ValueError):
        cfg = Config(model_provider='invalid', oci_provider='podman', models=[{"name": "test", "location": "/tmp", "confirmation_file": "/tmp/c", "checksum": "abc"}], oci=[])
        cfg.validate()