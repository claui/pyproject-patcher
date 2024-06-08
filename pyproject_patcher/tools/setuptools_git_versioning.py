"""Manage the `setuptools_git_versioning` tool in a `pyproject.toml`."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

# This guard avoids circular imports
if TYPE_CHECKING:
    from ..patcher import PyprojectPatcher


@dataclass(frozen=True)
class SetuptoolsGitVersioning:
    """This class wraps a `pyproject.toml` model and provides
    methods to interact with the `tools.setuptools_git_versioning`
    part and other entries related to it.
    """

    patcher: "PyprojectPatcher"

    def remove(self) -> None:
        """Removes all references to `setuptools-git-versioning` from
        this model.
        This includes removal of the `dynamic = ["version"]` entry
        and the entry in the `build-system.requires` section that
        requires the `setuptools-git-versioning` module.
        """
        self.patcher.dynamic.remove("version")
        self.patcher.tool.pop("setuptools-git-versioning")
        self.patcher.remove_build_system_dependency("setuptools-git-versioning")
