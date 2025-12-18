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

## Usage

Create a YAML config file (see `sample_config.yaml`).

Run:
```bash
neurobik --config sample_config.yaml
```

The interactive prompt will show items to select for download.

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