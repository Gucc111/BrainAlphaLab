"""Command-line interface for BrainAlpha."""
from __future__ import annotations

import typer
from rich.console import Console

from brainalpha import __app_name__, __version__
from brainalpha.cli.config import config_app
from brainalpha.logging import configure_logging

console = Console()
app = typer.Typer(help="CLI toolkit for WorldQuant Brain alpha workflows")
app.add_typer(config_app, name="config")


@app.callback()
def main(ctx: typer.Context) -> None:
    """Configure global options and logging."""
    configure_logging()
    ctx.obj = {}


@app.command()
def version() -> None:
    """Show the installed version of brainalpha."""
    console.print(f"{__app_name__} v{__version__}")


def run() -> None:
    """Entry point for console_scripts."""
    app()


if __name__ == "__main__":
    run()
