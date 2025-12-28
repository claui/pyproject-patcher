"""A place for shared paths and settings."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
PACKAGE_ROOT = Path(__file__).parent.absolute()
PYPROJECT_TOML = PROJECT_ROOT / 'pyproject.toml'

PACKAGE_NAME = 'pyproject-patcher'

debugMode = bool(os.getenv('PYPROJECT_PATCHER_DEBUG'))
