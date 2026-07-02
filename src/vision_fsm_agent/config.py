"""
Configuration loading and validation for Vision FSM Agent.

Searches common locations for YAML config files and returns a dict.
Supports the new ``config/default.yaml`` layout as well as the legacy
``config.yaml`` at the project root.
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


def load_config(config_path: str | None = None) -> dict[str, Any]:
    """Load a YAML config file, searching common locations.

    Search order:
      1. ``config_path`` argument (if provided)
      2. ``config/default.yaml`` in the current working directory
      3. ``config.yaml`` in the current working directory (legacy)
      4. ``config/default.yaml`` relative to the package
      5. ``config.yaml`` relative to the package (legacy)
    """
    import yaml

    candidates = []
    if config_path:
        candidates.append(config_path)

    cwd = os.getcwd()
    pkg_dir = os.path.dirname(__file__)

    candidates.extend(
        [
            os.path.join(cwd, "config", "default.yaml"),
            os.path.join(cwd, "config.yaml"),  # legacy
            os.path.join(cwd, "examples", "visual_grid_world", "config.yaml"),
            os.path.join(pkg_dir, "..", "..", "config", "default.yaml"),
            os.path.join(pkg_dir, "..", "..", "config.yaml"),  # legacy
        ]
    )

    for path in candidates:
        path = os.path.normpath(path)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            logger.info("Config loaded: %s", path)
            return config

    logger.warning("No config file found; using defaults")
    return {}
