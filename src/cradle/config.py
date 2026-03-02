"""Configuration management for cradle.

>>> sorted(DEFAULT_CONFIG["templates"].keys())
['experiments', 'package', 'paper']
"""

from pathlib import Path
from typing import Any, cast

import yaml

# Default configuration directory
CONFIG_DIR = Path.home() / ".cradle"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

# Default configuration
DEFAULT_CONFIG = {
    "templates": {
        "experiments": {
            "url": "https://github.com/tschm/experiments",
            "description": "Template for experimental projects with Marimo notebooks",
        },
        "package": {
            "url": "https://github.com/tschm/package",
            "description": "Template for Python packages with PyPI publishing support",
        },
        "paper": {
            "url": "https://github.com/tschm/paper",
            "description": "Template for academic papers with LaTeX support",
        },
    }
}


def _ensure_config_file() -> None:
    """Ensure the configuration file exists."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)

    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f)


def _read_config(config_file: Path | None = None) -> dict[str, Any]:
    """Read the configuration file."""
    if config_file is None:
        _ensure_config_file()
        config_file = CONFIG_FILE

    with open(config_file) as f:
        return cast(dict[str, Any], yaml.safe_load(f))


def get_all_templates(config_file: Path | None = None) -> dict[str, dict[str, Any]]:
    """Get information about all templates.

    >>> import tempfile, yaml
    >>> cfg = {"templates": {"demo": {"url": "https://github.com/x/demo", "description": "Demo"}}}
    >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
    ...     yaml.dump(cfg, f)
    ...     name = f.name
    >>> get_all_templates(Path(name))
    {'demo': {'description': 'Demo', 'url': 'https://github.com/x/demo'}}
    >>> Path(name).unlink()
    """
    config = _read_config(config_file)
    return cast(dict[str, dict[str, Any]], config.get("templates", {}))
