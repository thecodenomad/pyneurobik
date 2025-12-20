# Neurobik

A CLI tool for downloading AI models and OCI images based on a Nix-generated YAML config.

## Installation

### Via Nix (Recommended for NixOS)

Add to your NixOS configuration:

```nix
# In your flake.nix or configuration.nix
{
  inputs.neurobik.url = "path:/path/to/neurobik";  # Or "github:your/repo" if hosted
  # ...
  environment.systemPackages = [
    inputs.neurobik.packages.${system}.neurobik
  ];
}
```

Then rebuild: `sudo nixos-rebuild switch`

### Via Pip

```bash
pip install -e .
```

## Configuration

Create a YAML config file with the following structure:

```yaml
model_provider: ramalama  # or ollama, llama.cpp
oci_provider: podman

models:  # Supports multiple models, each with individual confirmation files
  - repo_name: unsloth/Qwen3-0.6B-GGUF
    model_name: Qwen3-0.6B-Q6_K.gguf
    location: $HOME/.local/share/ubikos-services/ramalama/models/unsloth/Qwen3-0.6B-GGUF/Qwen3-0.6B-Q6_K.gguf
    confirmation_file: $HOME/.local/share/ubikos-services/ramalama/.neurobik-ready-qwen
    checksum: abc123  # optional
  - repo_name: microsoft/DialoGPT-medium
    model_name: pytorch_model.bin
    location: $HOME/models/dialogpt-medium.bin
    confirmation_file: $HOME/models/.dialogpt_downloaded

oci:
  - image: docker.io/library/alpine:latest
    confirmation_file: $HOME/images/.alpine_pulled
    containerfile: /path/to/Containerfile  # optional
    build_args: ["--build-arg=VERSION=latest"]  # optional
```

When multiple models are configured and downloaded, Neurobik automatically creates a symlink `default-model.gguf` (or appropriate extension) in the models directory pointing to the first model in the config order. This provides a consistent default model reference.

Each model has its own confirmation file. When any model is downloaded for a provider, a provider confirmation file (`.neurobik-ready`) is also created in the models directory.

See `sample_config.yaml` for a complete example.

## Usage

Run:
```bash
neurobik --config your_config.yaml
```

The interactive prompt will show only models that haven't been downloaded yet (based on confirmation file existence), along with all configured OCI images. Select items to download. After successful downloads, you'll see:

```
Default model (first in config): /full/path/to/first/model.gguf
```

This indicates which model is symlinked as `default-model.gguf` in the models directory. A provider confirmation file (`.neurobik-ready`) is created when any model is downloaded.

## Development

### Nix Development Environment

Enter the dev shell:
```bash
nix-shell dev.nix
```

Inside the shell, run tests:
```bash
pytest
```

The shell provides all dependencies and sets up the Python path for development.

### Manual Setup

Ensure Python 3.8+ and install dependencies:
```bash
pip install -r requirements.txt  # Hypothetical, or install from pyproject.toml
pip install -e .
pytest
```

## Acknowledgements

This project was developed with assistance from [opencode](https://opencode.ai) (Grok Code Fast 1), an AI-powered coding assistant that aided in planning, implementation, testing, and documentation. Special thanks to the opencode team for their support in building robust, well-tested software. 🚀