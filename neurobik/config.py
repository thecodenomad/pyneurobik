"""Configuration module for Neurobik.

This module defines the data models for YAML configuration parsing and validation
using Pydantic BaseModel. It handles model and OCI container configurations with
environment variable expansion and provider validation.
"""

import os
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field, ValidationError


class ModelItem(BaseModel):
    """Configuration item for a single AI model.

    Attributes:
        repo_name: Hugging Face repository name (e.g., 'unsloth/Qwen3-0.6B-GGUF')
        model_name: Specific model filename (e.g., 'Qwen3-0.6B-Q6_K.gguf')
        location: Full path where the model should be stored
        confirmation_file: Path to confirmation file for download tracking
        checksum: Optional SHA256 checksum for verification
    """

    repo_name: str
    model_name: str
    location: str
    confirmation_file: str
    checksum: Optional[str] = None


class OciItem(BaseModel):
    """Configuration item for a single OCI container.

    Attributes:
        image: Container image name/tag (e.g., 'localhost/comfyui:latest')
        confirmation_file: Path to confirmation file for pull/build tracking
        containerfile: Optional path to Containerfile for building
        build_args: Optional list of build arguments
    """

    image: str
    confirmation_file: str
    containerfile: Optional[str] = None
    build_args: Optional[List[str]] = Field(default_factory=list)


class Config(BaseModel):
    """Main configuration class for Neurobik.

    Attributes:
        model_provider: AI model provider ('ollama', 'llama.cpp', or 'ramalama')
        oci_provider: OCI container provider (currently only 'podman' supported)
        default_gguf: Optional default model filename for symlinking
        models: List of model configurations
        oci: List of OCI container configurations
    """

    model_provider: Optional[str] = None
    oci_provider: str = "podman"
    default_gguf: Optional[str] = None
    models: List[ModelItem] = Field(default_factory=list)
    oci: List[OciItem] = Field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: str):
        """Load configuration from a YAML file."""
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        try:
            config = cls(**data)
            config.expand_vars()
            config.validate_config()
            return config
        except ValidationError as e:
            raise ValueError(f"Invalid config: {e}") from e

    def expand_vars(self):
        """Expand environment variables in paths."""
        for model in self.models:
            model.location = os.path.expandvars(model.location)
            model.confirmation_file = os.path.expandvars(model.confirmation_file)
        for oci_item in self.oci:
            oci_item.confirmation_file = os.path.expandvars(oci_item.confirmation_file)

    def validate_config(self):
        """Validate configuration values and relationships."""
        # Basic checks
        if self.model_provider and self.models:
            if self.model_provider not in ["ollama", "llama.cpp", "ramalama"]:
                raise ValueError(f"Unsupported model_provider: {self.model_provider}")
        if self.oci and self.oci_provider != "podman":
            raise ValueError("Only podman supported for OCI")
        # Validate default_gguf only if models are configured
        if self.default_gguf and self.models:
            model_names = [model.model_name for model in self.models]
            if self.default_gguf not in model_names:
                raise ValueError(f"default_gguf '{self.default_gguf}' not found in configured models")

    @property
    def provider_confirmation_file(self):
        """Get the provider confirmation file path."""
        if not self.models:
            return None
        provider_dir = os.path.dirname(self.models[0].confirmation_file)
        return os.path.join(provider_dir, ".neurobik-ready")
