"""Logging configuration utilities."""
from __future__ import annotations

import logging
import sys

from rich.logging import RichHandler

LOG_LEVEL = logging.INFO


def configure_logging(level: int = LOG_LEVEL) -> None:
    """Configure application-wide logging with a consistent format."""
    if logging.getLogger().handlers:
        return

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True, console=None, markup=True, stream=sys.stderr)],
    )
