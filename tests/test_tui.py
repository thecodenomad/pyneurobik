import pytest
from unittest.mock import patch
from neurobik.tui import NeurobikTUI

def test_tui_run():
    items = [
        {'name': 'model1', 'type': 'model'},
        {'name': 'image1', 'type': 'oci'}
    ]
    tui = NeurobikTUI(items)
    
    with patch('questionary.checkbox') as mock_checkbox:
        mock_checkbox.return_value.ask.return_value = ['model: model1']
        result = tui.run()
        assert result == [{'name': 'model1', 'type': 'model'}]
        mock_checkbox.assert_called_once()