import pytest
import tempfile
import os
from unittest.mock import patch
from neurobik.config import Config
from neurobik.downloader import Downloader

@pytest.fixture
def sample_config():
    config_data = {
        "model_provider": "ollama",
        "oci_provider": "podman",
        "models": [
            {
                "name": "test-model",
                "location": "/tmp/test-model.gguf",
                "confirmation_file": "/tmp/test-model.confirmed",
                "checksum": "dummy"
            }
        ],
        "oci": [
            {
                "image": "test-image:latest",
                "confirmation_file": "/tmp/test-image.confirmed"
            }
        ]
    }
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        import yaml
        yaml.dump(config_data, f)
        f.flush()
        yield f.name
    os.unlink(f.name)

@patch('neurobik.downloader.subprocess.run')
def test_confirmation_files_created_on_success(mock_subprocess, sample_config):
    cfg = Config.from_yaml(sample_config)
    downloader = Downloader()
    
    # Mock successful subprocess calls
    mock_subprocess.return_value.returncode = 0
    
    # Test model pull
    model = cfg.models[0]
    downloader.pull_model(cfg.model_provider, model.name, model.location, model.confirmation_file)
    assert os.path.exists(model.confirmation_file)
    
    # Test OCI pull
    oci = cfg.oci[0]
    downloader.pull_oci(oci.image, oci.confirmation_file)
    assert os.path.exists(oci.confirmation_file)
    
    # Cleanup
    os.unlink(model.confirmation_file)
    os.unlink(oci.confirmation_file)

@patch('neurobik.downloader.subprocess.run')
def test_confirmation_files_not_created_on_failure(mock_subprocess, sample_config):
    cfg = Config.from_yaml(sample_config)
    downloader = Downloader()
    
    # Mock failed subprocess calls
    mock_subprocess.return_value.returncode = 1
    mock_subprocess.side_effect = Exception("Command failed")
    
    model = cfg.models[0]
    oci = cfg.oci[0]
    
    # Test model pull failure
    with pytest.raises(Exception):
        downloader.pull_model(cfg.model_provider, model.name, model.location, model.confirmation_file)
    assert not os.path.exists(model.confirmation_file)
    
    # Test OCI pull failure
    with pytest.raises(Exception):
        downloader.pull_oci(oci.image, oci.confirmation_file)
    assert not os.path.exists(oci.confirmation_file)

@patch('neurobik.downloader.requests.get')
def test_download_file_success(mock_get, sample_config):
    cfg = Config.from_yaml(sample_config)
    downloader = Downloader()
    
    # Mock requests
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.headers = {'content-length': '4'}
    mock_response.iter_content.return_value = [b'test']
    
    model = cfg.models[0]
    dest = model.location
    downloader.download_file("http://example.com", dest, "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08")  # sha256 of 'test'
    
    assert os.path.exists(dest)
    assert os.path.exists(dest + '.confirmed')
    
    # Cleanup
    os.unlink(dest)
    os.unlink(dest + '.confirmed')

@patch('neurobik.downloader.requests.get')
def test_download_file_checksum_mismatch(mock_get, sample_config):
    cfg = Config.from_yaml(sample_config)
    downloader = Downloader()
    
    # Mock requests
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.headers = {'content-length': '4'}
    mock_response.iter_content.return_value = [b'test']
    
    model = cfg.models[0]
    dest = model.location
    with pytest.raises(ValueError, match="Checksum mismatch"):
        downloader.download_file("http://example.com", dest, "wrong")
    
    # Cleanup if exists
    if os.path.exists(dest):
        os.unlink(dest)