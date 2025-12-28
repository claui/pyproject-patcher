"""Manage the `setuptools` tool in a `pyproject.toml`."""

from collections.abc import MutableMapping
from dataclasses import dataclass
from typing import TYPE_CHECKING

import tomlkit

# This guard avoids circular imports
if TYPE_CHECKING:
    from ..patcher import PyprojectPatcher

TOOL_NAME = 'setuptools'


@dataclass(frozen=True)
class Setuptools:
    """This class wraps a `pyproject.toml` model and provides
    methods to interact with the `tools.setuptools`
    section and other entries related to it.
    """

    patcher: 'PyprojectPatcher'

    def exclude_package_data(self) -> None:
        """Sets `include-package-data` to False."""
        self.include_package_data(False)

    def include_package_data(self, value: bool = True) -> None:
        """Sets `include-package-data` to the given `value`."""
        self.mapping['include-package-data'] = value

    @property
    def mapping(
        self,
    ) -> MutableMapping[str, bool | str | tomlkit.items.Item]:
        """Low-level access to the `tool.setuptools` section of `pyproject.toml`."""
        section = self.patcher.tool.get(TOOL_NAME)
        if not isinstance(section, MutableMapping):
            raise KeyError(
                f'Expected MutableMapping, found {type(section)}: {section}'
            )
        return section
