# Neurobik (Full Project in Rust + Ratatui)

## Overview
A polished Rust CLI with Ratatui TUI for downloading AI models/checkpoints or pulling/building OCI containers from a Nix-generated YAML config. Uses async downloads/pulls with progress; assumes provider formats/names are correct. Includes Nix integration for packaging and development. Features fancy ASCII art headers with themed boxes.

## Core Requirements
- Parse and validate YAML config against schema: `{model_provider: "ollama", oci_provider: "podman", models: [{name: "meta-llama/Llama-3-8B", location: "/path", confirmation_file: "/path/.downloaded", checksum: "..."}], oci: [{image: "docker.io/library/alpine:latest", confirmation_file: "/path/.pulled", containerfile?: "/path", build_args?: ["--arg1=value"]}]}` (use serde for validation; expand env vars like $HOME; location optional for OCI since podman pull stores in registry).
- Validate providers: Basic checks; assume formats are correct.
- Downloads/pulls: Async/resume (tokio with reqwest streams), progress bars, checksum verification/redownload; tokio::process for podman (pull/build).
- Validate podman installed; fail gracefully if not.
- TUI: Ratatui for interactive checkboxes/menus with async updates (use ratatui widgets for simple selection).
- Create confirmation files upon success; robust error handling, retries, tracing logging, and fancy ASCII art messages.
- Support NixOS integration: flake.nix for packaging, dev.nix for development environment.
- Include ASCII art in main.rs for fancy headers/footers (same as MVP: initial runtime header, downloads starting box, completion with neural art and themed box).

## Architecture
- `src/config.rs`: YAML parsing + serde validation + provider checks + env var expansion.
- `src/downloader.rs`: Async downloads with reqwest/tokio, subprocess for Ollama/HF/podman, directory creation.
- `src/tui.rs`: Ratatui app with event loop for lists, checkboxes, progress.
- `src/main.rs`: CLI entry with ASCII art headers/footers (include themed boxes and neural art as shown in MVP).
- `src/utils.rs`: Logging (tracing), checksum verification, confirmation files.
- `Cargo.toml`: Rust dependencies.
- `flake.nix`: Nix flake for building and installing neurobik.
- `dev.nix`: Nix shell for development with deps.

## Timeline (Extended)
- Weeks 1-2: Rust setup, schema validation, async downloads with resume.
- Weeks 3-4: Ratatui TUI with async updates, podman integration.
- Weeks 5-6: Full features (checksums, retries), NixOS packaging.
- Weeks 7-8: Polish, testing, release.

## Dependencies
- tokio, reqwest, ratatui, serde, serde_yaml, tracing, sha2, clap (for CLI), indicatif (for progress).

## Testing
- **Unit Tests**: Use cargo test for config deserialization (invalid YAML, schema mismatches), provider validation, checksum verification, confirmation file creation (with mocked tokio::process for success/failure).
- **Integration Tests**: Mock async downloads (reqwest), podman tokio::process, TUI events (ratatui test utils or manual).
- **Edge Cases**: Resume interrupted downloads, podman build failures (invalid containerfile), large file handling, env var expansion.
- **NixOS Specific**: Cross-compile and test in NixOS; ensure Nix flake builds binary; verify service signaling via confirmation files.
- **Coverage**: Use cargo-tarpaulin for 75%+; focus on core modules (config, downloader, utils).