# Neurobik Prototype (1 Week MVP)

## Overview
A minimal Python CLI with Textual TUI for downloading AI models/checkpoints or pulling/building OCI containers from a Nix-generated YAML config. Uses sequential downloads/pulls with overall progress; assumes provider formats/names are correct.

## Core Requirements
- Parse and validate YAML config against schema: `{model_provider: "ollama", oci_provider: "podman", models: [{name: "meta-llama/Llama-3-8B", location: "/path", confirmation_file: "/path/.downloaded", checksum: "..."}], oci: [{image: "docker.io/library/alpine:latest", confirmation_file: "/path/.pulled", containerfile?: "/path", build_args?: ["--arg1=value"]}]}` (use pydantic for validation; location optional for OCI since podman pull stores in registry).
- Validate providers: Basic checks; assume formats are correct.
- Download/pull sequential: Use subprocess for HF/Ollama pulls (for GGUFs), direct HTTP for others, podman for OCI.
- Validate podman installed; fail gracefully if not.
- Textual TUI: Display list of items, checkboxes for selection/acknowledgement.
- Create confirmation file upon success; basic error handling and logging.
- Overall progress bars, structured logging (e.g., loguru).
- Output metadata YAML per download/pull.

## Architecture
- `config.py`: YAML parsing + pydantic validation + basic provider checks.
- `downloader.py`: Sequential HTTP downloads with tqdm, subprocess for HF/Ollama/podman.
- `tui.py`: Textual app for lists, checkboxes.
- `cli.py`: `download --config <file.yaml>` command launching TUI.
- `utils.py`: Logging, checksum verification, podman validation.

## Timeline (1 Week)
- Days 1-2: Setup (pyproject.toml), schema validation, YAML parser.
- Days 3-4: Sequential downloader with subprocess, podman validation.
- Days 5-7: Textual TUI, error handling, manual testing.

## Dependencies
- requests, tqdm, pyyaml, click, textual, pydantic, loguru.

## Testing
- **Unit Tests**: Use pytest for config validation (invalid YAML, missing fields), checksum verification.
- **Manual Testing**: Test TUI interactions, downloads with sample YAML, podman validation.
- **Edge Cases**: Network failures, corrupted downloads, missing podman.