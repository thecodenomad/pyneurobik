# Neurobik Prototype (1 Week MVP)

## Overview
A minimal Python CLI with questionary-based interactive prompts for downloading AI models/checkpoints or pulling/building OCI containers from a Nix-generated YAML config. Uses sequential downloads/pulls with overall progress; assumes provider formats/names are correct. Includes Nix integration for packaging and development. Features fancy ASCII art headers with themed boxes.

## Core Requirements
- Parse and validate YAML config against schema: `{model_provider: "ramalama", oci_provider: "podman", models: [{repo_name: "meta-llama/Llama-3-8B", model_name: "model-file.gguf", location: "/path", confirmation_file: "/path/.downloaded", checksum: "..."}], oci: [{image: "docker.io/library/alpine:latest", confirmation_file: "/path/.pulled", containerfile?: "/path", build_args?: ["--arg1=value"]}]}` (use pydantic for validation; expand env vars like $HOME; location optional for OCI since podman pull stores in registry).
- Validate providers: Basic checks; assume formats are correct.
- Download/pull sequential: Use subprocess for Ollama/HF pulls (for models), direct HTTP for files, podman for OCI (pull/build).
- Validate podman installed; fail gracefully if not.
- Questionary TUI: Interactive checkbox list for selecting items to download (use questionary.checkbox to avoid complex async UI). Only shows models that haven't been downloaded yet (no confirmation file exists); OCI items always shown.
- Support multiple models: Downloads all selected models; creates symlink `default-model.gguf` in models directory (parent of first model's confirmation file) pointing to first model (relative path for portability). Each model has its own confirmation file; a provider confirmation file (.neurobik-ready in the models directory) is created when any model is downloaded.
- Create confirmation files after symlinking; basic error handling, logging, and fancy ASCII art messages.
- Output default model path on completion; overall progress bars, structured logging (e.g., loguru).
- Support NixOS integration: flake.nix for packaging, dev.nix for development environment.
- Include ASCII art in cli.py for fancy headers/footers:
  - Initial runtime header:
    ```
    ╭─═══════════════════════════════════════════════════════════════════════════─╮
                       _   _                      _     _ _
                      | \ | | ___ _   _ _ __ ___ | |__ (_) | __
                      |  \| |/ _ \ | | | '__/ _ \| '_ \| | |/ /
                      | |\  |  __/ |_| | | | (_) | |_) | |   <
                      |_| \_|\___|\__,_|_|  \___/|_.__/|_|_|\_\

                             The premier thawing agent.
    ╰─═══════════════════════════════════════════════════════════════════════════─╯
    ```
  - Downloads starting box:
    ```
    ╭─┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈─╮
    ┊                           🚀 Downloads Starting...                          ┊
    ╰─┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈─╯
    ```
  - Completion with neural art and themed box:
    ```
    ╭─┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈─╮
    ┊          🎉 All Downloads Complete - Your AI Overlords Approve! 🎉          ┊
    ╰─┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈─╯

    ╭─═══════════════════════════════════════════════════════════════════════════─╮
                                                               ·◎◎··●·
                                                            ·○○··········
                                                          ·◎········· ····
                                                         ·················●
                                                         ··········     ····
                                                      ··◉○·○······      ···○○·
                                                    ·○○○○·○○············  ··◎·
                                                  ·○○◉···○○◉· ···············
                                            ●◉◉●○···◉·····○○···   ········○·
                                            ●◉◉◉··        ●················
                                           ◉○◎◎○○·○◎·      ··○··  ····●···
               _ _                      ··●·○●◉◉◎◎◎◎◎●       ··●···●·
          _   _| |__ (_) | __           ·◉○○◎◎◎◎◎○··○◎
         | | | | '_ \| | |/ /           ·◉○○◎◎◎◎◎○··○◎●·
         | |_| | |_) | |   <            ·●○·○◎◎◎◎◎○··○◉·
          \__,_|_.__/|_|_|\_\           ··◎·○◎◎◎◎◎○··○◎·
                                          ◉○○◎◎◎◎◎◎○··◎●·
         Safe when used as directed.      ·◎·○◎◎◎◎◎○··○◉·
                                          ·◎·○◎◎◎◎◎○○·○◎◎
                                           ●○·○◎◎◎◎◎○··◎◉·
                                           ·◎·○◎◎◎◎◎○··○◎·
                                            ◉○○◎◎◎◎◎◎○·○◎●
                                            ●○·○◎◎◎◎◎○··○◉·
                                            ·◎·○◎◎◎◎◎○○·○◎·
                                             ◉○○○◎◎◎◎◎○○○◎◉
                                             ·◎○○◎◎◎◎◎○○○○◎·
                                             ·◉○○◎◎◎◎◎○○◉○◎·
                                              ●○○○○◎●○··
    ╰─═══════════════════════════════════════════════════════════════════════════─╯
    ```

## Architecture
- `config.py`: YAML parsing + pydantic validation + provider checks + env var expansion + provider confirmation file derivation.
- `downloader.py`: Sequential downloads with tqdm, subprocess for Ollama/HF/podman, directory creation, symlinking logic for default model.
- `tui.py`: Questionary-based selection prompts (questionary.checkbox for simple interactive selection).
- `cli.py`: Click CLI launching TUI (filters models by confirmation file existence), with ASCII art headers/footers (include themed boxes and neural art as shown), post-download symlinking and confirmation file creation (per-model and provider).
- `utils.py`: Logging, checksum verification, confirmation files.
- `pyproject.toml`: Python packaging with dependencies.
- `flake.nix`: Nix flake for building and installing neurobik.
- `dev.nix`: Nix shell for development with deps.

## Timeline (1 Week)
- Days 1-2: Setup (pyproject.toml, Nix files), schema validation, YAML parser.
- Days 3-4: Sequential downloader with subprocess, podman validation.
- Days 5-7: Questionary TUI, error handling, ASCII art, manual testing.

## Dependencies
- Python: requests, tqdm, pyyaml, click, pydantic, loguru, questionary.
- Nix: Standard nixpkgs Python packages.

## Testing
- **Unit Tests**: pytest for config validation (invalid YAML, missing fields), provider confirmation file derivation, checksum verification, confirmation file creation (with mocked subprocess for success/failure), symlinking logic (success/failure cases), CLI entry points, model filtering by confirmation files.
- **Manual Testing**: Test TUI interactions, downloads with sample YAML, podman validation, multiple model symlinking, filtering of downloaded models.
- **Edge Cases**: Network failures, corrupted downloads, missing podman, env var expansion, symlink removal failures, provider confirmation file creation.
- **Coverage**: Achieved 75% with pytest-cov; includes CLI error handling, TUI mocks, downloader HTTP mocks, symlinking, confirmation file filtering.

## Nix Integration
- Use `flake.nix` to build and install neurobik as a system package.
- Use `dev.nix` for development shell with all deps and PYTHONPATH set.