from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
import yaml
import os

class ModelItem(BaseModel):
    name: str
    location: str
    confirmation_file: str
    checksum: Optional[str] = None

class OciItem(BaseModel):
    image: str
    confirmation_file: str
    containerfile: Optional[str] = None
    build_args: Optional[List[str]] = Field(default_factory=list)

class Config(BaseModel):
    model_provider: Optional[str] = None
    oci_provider: str = "podman"
    models: List[ModelItem] = Field(default_factory=list)
    oci: List[OciItem] = Field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        try:
            config = cls(**data)
            config.expand_vars()
            return config
        except ValidationError as e:
            raise ValueError(f"Invalid config: {e}")

    def expand_vars(self):
        """Expand environment variables in paths."""
        import os
        for model in self.models:
            model.location = os.path.expandvars(model.location)
            model.confirmation_file = os.path.expandvars(model.confirmation_file)
        for oci in self.oci:
            oci.confirmation_file = os.path.expandvars(oci.confirmation_file)

    def validate(self):
        # Basic checks
        if self.model_provider and self.models:
            if self.model_provider not in ['ollama', 'llama.cpp', 'ramalama']:
                raise ValueError(f"Unsupported model_provider: {self.model_provider}")
        if self.oci and self.oci_provider != 'podman':
            raise ValueError("Only podman supported for OCI")