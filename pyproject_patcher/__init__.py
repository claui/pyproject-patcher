"""
.. include:: ../README.md

## API Documentation
"""

# Re-export these symbols
# (This promotes them from pyproject_patcher.patcher to pyproject_patcher)
from pyproject_patcher.patcher import PyprojectPatcher as PyprojectPatcher

from pyproject_patcher.version import version

__all__ = [
    # Tell pdoc to pick up all re-exported symbols
    'PyprojectPatcher',

    # Modules that every subpackage should see
    # (This also exposes them to pdoc)
    'patcher',
    'settings',
]

__version__ = version()
