"""
Tools (as in the `tool` section of a `pyproject.toml` file).
"""

from dataclasses import dataclass
import functools
from typing import TYPE_CHECKING

# Re-export these symbols
from ..tools.setuptools import Setuptools as Setuptools
from ..tools.setuptools_git_versioning import (
    SetuptoolsGitVersioning as SetuptoolsGitVersioning,
)

# This guard avoids circular imports
if TYPE_CHECKING:
    from ..patcher import PyprojectPatcher


@dataclass(frozen=True)
class Tools:
    """Accessor for tools, such as `setuptools` or
    `setuptools_git_versioning`."""

    patcher: 'PyprojectPatcher'

    @functools.cached_property
    def setuptools(self) -> Setuptools:
        """An object that provides methods to interact with the
        `tools.setuptools` section of `pyproject.toml` and other entries
        related to it.
        """
        return Setuptools(self.patcher)

    @functools.cached_property
    def setuptools_git_versioning(self) -> SetuptoolsGitVersioning:
        """An object that provides methods to interact with the
        `tools.setuptools_git_versioning` section of `pyproject.toml`
        and other entries related to it.
        """
        return SetuptoolsGitVersioning(self.patcher)
