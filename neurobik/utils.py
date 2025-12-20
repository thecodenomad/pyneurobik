"""Utility functions for Neurobik.

This module contains helper functions for checksum verification,
file operations, and logging setup.
"""

import hashlib
import os
from pathlib import Path

from loguru import logger


def verify_checksum(file_path: str, expected_checksum: str) -> bool:
    """Verify SHA256 checksum of a file.

    Args:
        file_path: Path to the file to check
        expected_checksum: Expected SHA256 hash as hex string

    Returns:
        True if checksum matches, False otherwise
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest() == expected_checksum


def create_confirmation_file(path: str):
    """Create a confirmation file to mark successful download.

    Args:
        path: Path where to create the confirmation file
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Path(path).touch()


def setup_logging():
    """Setup structured logging with file rotation.

    Returns:
        Configured logger instance
    """
    logger.add("neurobik.log", rotation="10 MB")
    return logger
