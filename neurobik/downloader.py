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
        if provider == 'ollama':
            subprocess.run(['ollama', 'pull', name], check=True)
        elif provider in ['llama.cpp', 'ramalama']:
            # Assume HF download for simplicity
            self.download_file(f"https://huggingface.co/{name}/resolve/main/model.gguf", location)
        create_confirmation_file(confirmation_file)

    def pull_oci(self, image: str, confirmation_file: str, containerfile: Optional[str] = None, build_args: Optional[List[str]] = None):
        os.makedirs(os.path.dirname(confirmation_file), exist_ok=True)
        if containerfile:
            cmd = ['podman', 'build']
            if build_args:
                cmd.extend(build_args)
            cmd.extend(['-f', containerfile, '.'])
            subprocess.run(cmd, check=True)
        else:
            subprocess.run(['podman', 'pull', image], check=True)
        create_confirmation_file(confirmation_file)

    @staticmethod
    def check_podman():
        if not shutil.which('podman'):
            raise RuntimeError("Podman not installed")