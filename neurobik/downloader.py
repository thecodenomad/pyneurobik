import requests
from tqdm import tqdm
import subprocess
import shutil
import os
from typing import Optional, List
from neurobik.utils import create_confirmation_file, verify_checksum

class Downloader:
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback

    def download_file(self, url: str, dest: str, checksum: Optional[str] = None):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        with open(dest, 'wb') as f, tqdm(
            desc=f"Downloading {dest}",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))
        if checksum and not verify_checksum(dest, checksum):
            raise ValueError(f"Checksum mismatch for {dest}")
        create_confirmation_file(dest + '.confirmed')
        print(f"✅ Downloaded {os.path.basename(dest)} successfully!")

    def pull_model(self, provider: str, name: str, location: str, confirmation_file: str):
        os.makedirs(os.path.dirname(location), exist_ok=True)
        if '/' not in name:
            raise ValueError(f"Model name must be in 'repo/filename' format for Hugging Face download, got: {name}")
        parts = name.split('/')
        repo = '/'.join(parts[:-1])
        filename = parts[-1]
        dest_dir = os.path.dirname(location)
        subprocess.run(['hf', 'download', repo, filename, '--local-dir', dest_dir], check=True)
        create_confirmation_file(confirmation_file)

    def pull_oci(self, image: str, confirmation_file: str, containerfile: Optional[str] = None, build_args: Optional[List[str]] = None):
        os.makedirs(os.path.dirname(confirmation_file), exist_ok=True)
        if containerfile:
            context = os.path.dirname(containerfile)
            cmd = ['podman', 'build', '-t', image]
            if build_args:
                cmd.extend(build_args)
            cmd.extend(['-f', containerfile, context])
            subprocess.run(cmd, check=True)
        else:
            subprocess.run(['podman', 'pull', image], check=True)
        create_confirmation_file(confirmation_file)

    @staticmethod
    def check_podman():
        if not shutil.which('podman'):
            raise RuntimeError("Podman not installed")

    @staticmethod
    def check_huggingface_cli():
        if not shutil.which('hf'):
            raise RuntimeError("hf CLI not installed. Install with: pip install huggingface_hub")