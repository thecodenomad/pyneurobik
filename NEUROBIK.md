# Neurobik (Full Project in Rust + Ratatui)

## Overview
A polished Rust CLI with Ratatui TUI for downloading AI models/checkpoints. Reads Nix YAML config, supports async/resume downloads, corruption checks, and interactive checkboxes.

## Core Requirements
- Parse and validate YAML config against schema (same separated structure with location optional for OCI; use serde for validation).
- Validate providers (GGUF for model_provider; oci_provider for podman pulls/builds).
- Downloads/pulls: Async/resume (tokio with reqwest streams), progress bars, checksum verification/redownload; tokio::process for podman.
- Create confirmation file upon success; robust error handling with retries and tracing logging.
- TUI: Ratatui for paginated checkboxes/menus with async updates.
- Metadata: YAML output.
- GPL3, NixOS packaging with Nix flake for reproducible builds.

## Architecture
- `src/config.rs`: YAML parsing + serde validation + provider checks.
- `src/downloader.rs`: Async HTTP (resume via ranges) with tokio/reqwest + tokio::process for podman.
- `src/tui.rs`: Ratatui app with async event loop for lists, checkboxes, progress.
- `src/main.rs`: CLI entry.
- Add `src/utils.rs`: Logging (tracing), checksums.

## Timeline (Extended)
- Weeks 1-2: Rust setup, schema validation, async downloads with resume.
- Weeks 3-4: Ratatui TUI with async updates, podman integration.
- Weeks 5-6: Full features (checksums, retries), NixOS packaging.
- Weeks 7-8: Polish, testing, release.

## Dependencies
- tokio, reqwest, ratatui, serde, serde_yaml, tracing, sha2.

## Testing
- **Unit Tests**: Use cargo test for config deserialization (invalid YAML, schema mismatches), provider validation (GGUF checks), checksum hashing.
- **Integration Tests**: Mock async downloads (reqwest), podman tokio::process, TUI events (ratatui test utils or manual).
- **Edge Cases**: Resume interrupted downloads, podman build failures (invalid containerfile), large file handling (memory limits), concurrent TUI updates.
- **NixOS Specific**: Cross-compile and test in NixOS; ensure Nix flake builds binary; verify service signaling via confirmation files.
- **Coverage**: Use cargo-tarpaulin for 80%+; integration tests for async flows and error recovery.