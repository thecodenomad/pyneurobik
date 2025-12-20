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
model_provider: ollama  # or llama.cpp, ramalama
oci_provider: podman

models:  # Supports multiple models
  - repo_name: TheBloke/Llama-2-7B-Chat-GGUF
    model_name: llama-2-7b-chat.Q4_K_M.gguf
    location: $HOME/models/llama-2-7b-chat.Q4_K_M.gguf
    confirmation_file: $HOME/models/.llama_downloaded
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

See `sample_config.yaml` for a complete example.

## Usage

Run:
```bash
neurobik --config your_config.yaml
```

The interactive prompt will show items to select for download. After successful downloads, you'll see:

```
Default model (first in config): /full/path/to/first/model.gguf
```

This indicates which model is symlinked as `default-model.gguf` in the models directory.

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