"""Manage the `setuptools_git_versioning` tool in a `pyproject.toml`."""

from collections.abc import MutableMapping
from dataclasses import dataclass
from typing import TYPE_CHECKING

# This guard avoids circular imports
if TYPE_CHECKING:
    from ..patcher import PyprojectPatcher

TOOL_NAME = 'setuptools-git-versioning'


@dataclass(frozen=True)
class SetuptoolsGitVersioning:
    """This class wraps a `pyproject.toml` model and provides
    methods to interact with the `tools.setuptools_git_versioning`
    part and other entries related to it.
    """

    patcher: 'PyprojectPatcher'

    def remove(self) -> None:
        """Removes all references to `setuptools-git-versioning` from
        this model.
        This includes removal of the `dynamic = ["version"]` entry
        and the entry in the `build-system.requires` section that
        requires the `setuptools-git-versioning` module.
        """
        self.patcher.dynamic.remove('version')
        self.patcher.tool.pop(TOOL_NAME)
        self.patcher.remove_build_system_dependency(TOOL_NAME)

    def template_ignore_dirty_git(self) -> None:
        """Changes `dirty_template` so that it no longer contains a
        `.dirty` suffix.

        Useful for building system packages based on a VCS revision
        checked out with Git in cases where `pyproject.toml` has
        been modified before `setuptools_git_versioning` is run.
        In that case, having a `.dirty` suffix would be misleading.
        """
        section = self.patcher.tool.get(TOOL_NAME)
        if not isinstance(section, MutableMapping):
            raise KeyError(
                f'Expected MutableMapping, found {type(section)}: {section}'
            )
        section['dirty_template'] = '{tag}.post{ccount}+git.{sha}'
