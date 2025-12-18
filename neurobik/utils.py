import hashlib
import os
from pathlib import Path
from loguru import logger

def verify_checksum(file_path: str, expected_checksum: str) -> bool:
    """Verify file checksum."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest() == expected_checksum

def create_confirmation_file(path: str):
    """Create confirmation file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Path(path).touch()

def setup_logging():
    """Setup logging."""
    logger.add("neurobik.log", rotation="10 MB")
    return logger