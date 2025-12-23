"""Downloader module for Neurobik.

This module handles downloading AI models and pulling OCI containers
using appropriate providers and tools.
"""

import os
import shutil
import subprocess
from typing import List, Optional

import requests
from tqdm import tqdm

from neurobik.utils import create_confirmation_file, verify_checksum


class Downloader:
    """Handles downloading of AI models and OCI containers."""

    def __init__(self, progress_callback=None):
        """Initialize downloader with optional progress callback."""
        self.progress_callback = progress_callback

    def download_file(self, url: str, dest: str, checksum: Optional[str] = None):
        """Download a file from URL with progress bar and optional checksum verification."""
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        with (
            open(dest, "wb", encoding=None) as f,
            tqdm(
                desc=f"Downloading {dest}",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as progress_bar,
        ):
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                progress_bar.update(len(chunk))
        if checksum and not verify_checksum(dest, checksum):
            raise ValueError(f"Checksum mismatch for {dest}")
        create_confirmation_file(dest + ".confirmed")
        print(f"✅ Downloaded {os.path.basename(dest)} successfully!")

    def pull_model(
        self,
        _provider: Optional[str],
        repo_name: str,
        model_name: str,
        location: str,
        _confirmation_file: str,
    ):
        """Download a model using the appropriate provider."""
        dest_dir = os.path.dirname(location)
        os.makedirs(dest_dir, exist_ok=True)
        subprocess.run(
            ["hf", "download", repo_name, model_name, "--local-dir", dest_dir],
            check=True,
        )
        # Confirmation file creation moved to after symlinking

    def pull_oci(
        self,
        image: str,
        confirmation_file: str,
        containerfile: Optional[str] = None,
        build_args: Optional[List[str]] = None,
    ):
        """Pull or build an OCI container."""
        os.makedirs(os.path.dirname(confirmation_file), exist_ok=True)
        if containerfile:
            context = os.path.dirname(containerfile)
            cmd = ["podman", "build", "-t", image]
            if build_args:
                for arg in build_args:
                    cmd.extend(["--build-arg", arg])
            cmd.extend(["-f", containerfile, context])
            subprocess.run(cmd, check=True)
        else:
            subprocess.run(["podman", "pull", image], check=True)
        create_confirmation_file(confirmation_file)

    @staticmethod
    def check_podman():
        """Check if podman is installed."""
        if not shutil.which("podman"):
            raise RuntimeError("Podman not installed")

    @staticmethod
    def check_huggingface_cli():
        """Check if huggingface CLI is installed."""
        if not shutil.which("hf"):
            raise RuntimeError("hf CLI not installed. Install with: pip install huggingface_hub")

    @staticmethod
    def create_default_symlink(models_dir: str, first_model_location: str):
        """Create a symlink 'default-model.gguf' pointing to the specified model."""
        symlink_path = os.path.join(models_dir, "default-model.gguf")
        target = os.path.relpath(first_model_location, models_dir)

        # Remove existing symlink if it exists
        if os.path.lexists(symlink_path):
            try:
                os.unlink(symlink_path)
            except OSError as e:
                raise RuntimeError(f"Failed to remove existing symlink {symlink_path}: {e}") from e

        # Create new symlink
        try:
            os.symlink(target, symlink_path)
        except OSError as e:
            raise RuntimeError(f"Failed to create symlink {symlink_path} -> {target}: {e}") from e
