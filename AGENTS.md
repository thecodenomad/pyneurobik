# Agent Guidelines for Neurobik

## Commands
- **Build**: `nix build` or `pip install -e .` in Nix dev shell
- **Test all**: `pytest` (in Nix dev shell: `nix-shell dev.nix --run pytest`)
- **Test single**: `pytest -k "test_function_name"`
- **Test file**: `pytest tests/test_filename.py`
- **Lint**: `pylint neurobik tests`
- **Format**: `black neurobik tests`

## Code Style
- **Python version**: 3.12+
- **Imports**: stdlib → third-party → local, one per line
- **Naming**: snake_case for functions/vars, PascalCase for classes
- **Types**: Always use type hints with `typing` module
- **Docstrings**: Use Google style docstrings for all functions/classes
- **Error handling**: Specific exceptions, raise `ValueError` for config issues
- **Logging**: Use loguru for structured logging
- **CLI**: Use click decorators for command-line interfaces
- **Validation**: Use pydantic BaseModel for data structures
- **Testing**: pytest with fixtures for test variations (1 model, 2 models, etc.)
- **Test Docstrings**: Include "Replication steps", "Key validations", and "For other languages" sections (with tips for non-Python languages)

## Project Structure
- Source code in `neurobik/` package
- Tests in `tests/` directory mirroring source structure
- Configuration via `pyproject.toml` and Nix flakes</content>
<parameter name="filePath">AGENTS.md