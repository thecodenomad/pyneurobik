import pytest
from unittest.mock import patch
from neurobik.cli import download
from click.testing import CliRunner

@pytest.fixture
def runner():
    return CliRunner()

@patch('neurobik.cli.Config.from_yaml')
def test_cli_invalid_config(mock_config_from_yaml, runner):
    mock_config_from_yaml.side_effect = ValueError("Invalid config")
    
    result = runner.invoke(download, ['--config', 'test.yaml'])
    assert result.exit_code == 1
    assert "Error: Invalid config" in result.output