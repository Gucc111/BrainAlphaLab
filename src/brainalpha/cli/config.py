"""Configuration management commands."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from brainalpha.config.manager import BrainAlphaConfig, ConfigManager

console = Console()
config_app = typer.Typer(help="Manage authentication and runtime configuration")


@config_app.command("init")
def init_config(
    api_key: str = typer.Option(
        "", prompt="WorldQuant Brain API key", hide_input=True, confirmation_prompt=True
    ),
    base_url: str = typer.Option(
        "https://www.worldquantbrain.com/api", prompt="API base URL"
    ),
    storage_path: Optional[Path] = typer.Option(
        None,
        help="Optional override for local data storage path.",
    ),
) -> None:
    """Initialize the local configuration file with credentials and defaults."""
    manager = ConfigManager()
    config = BrainAlphaConfig(api_key=api_key, base_url=base_url, storage_path=storage_path)
    manager.save(config)
    console.print(f"Configuration written to {manager.config_path}")


@config_app.command("show")
def show_config() -> None:
    """Display the current configuration (hiding secrets)."""
    manager = ConfigManager()
    config = manager.load()
    table = Table(title="BrainAlpha Configuration")
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("base_url", config.base_url)
    table.add_row("api_key", "***" if config.api_key else "(not set)")
    table.add_row("storage_path", str(config.storage_path))
    console.print(table)
