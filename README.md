# Neurobik

A CLI tool for downloading AI models and OCI images based on a Nix-generated YAML config.

## Installation

```bash
pip install -e .
```

## Usage

Create a YAML config file (see sample_config.yaml).

Run:
```bash
neurobik --config sample_config.yaml
```

The TUI will show items to select for download.

## Development

Run tests:
```bash
pytest
```