"""Configuration data classes and persistence utilities."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

DEFAULT_CONFIG_DIR = Path.home() / ".brainalpha"
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "config.yml"
DEFAULT_STORAGE_PATH = DEFAULT_CONFIG_DIR / "storage"


@dataclass
class BrainAlphaConfig:
    """User configuration for accessing WorldQuant Brain APIs."""

    api_key: str = ""
    base_url: str = "https://www.worldquantbrain.com/api"
    storage_path: Path = field(default_factory=lambda: DEFAULT_STORAGE_PATH)

    def to_dict(self) -> dict:
        data = {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "storage_path": str(self.storage_path),
        }
        return data

    @classmethod
    def from_dict(cls, raw: dict) -> "BrainAlphaConfig":
        return cls(
            api_key=raw.get("api_key", ""),
            base_url=raw.get("base_url", "https://www.worldquantbrain.com/api"),
            storage_path=Path(raw.get("storage_path", DEFAULT_STORAGE_PATH)),
        )


class ConfigManager:
    """Load and persist configuration to disk."""

    def __init__(self, config_path: Optional[Path] = None) -> None:
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config_dir = self.config_path.parent

    def ensure_config_dir(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> BrainAlphaConfig:
        if not self.config_path.exists():
            return BrainAlphaConfig()
        with self.config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return BrainAlphaConfig.from_dict(data)

    def save(self, config: BrainAlphaConfig) -> None:
        self.ensure_config_dir()
        with self.config_path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(config.to_dict(), f, default_flow_style=False)
        if "posix" in os.name:
            os.chmod(self.config_path, 0o600)
