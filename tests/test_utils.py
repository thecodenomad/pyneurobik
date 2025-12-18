import pytest
import tempfile
import os
from neurobik.utils import verify_checksum, create_confirmation_file

def test_verify_checksum():
    # Create a temp file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b'hello')
        temp_file = f.name
    checksum = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'  # sha256 of 'hello'
    assert verify_checksum(temp_file, checksum)
    os.unlink(temp_file)

def test_create_confirmation_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, '.confirmed')
        create_confirmation_file(path)
        assert os.path.exists(path)