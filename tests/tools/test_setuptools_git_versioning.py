# pylint: disable=magic-value-comparison, missing-function-docstring, missing-module-docstring, missing-class-docstring, no-self-use, too-few-public-methods

from collections.abc import Mapping
from pathlib import Path

import tomlkit

from pyproject_patcher.patcher import patch_in_place


class TestSetuptoolsGitVersioning:
    def test_remove(self, toml_with_git_versioning_lt_2: Path) -> None:
        # When
        with patch_in_place(toml_with_git_versioning_lt_2) as toml:
            toml.tools.setuptools_git_versioning.remove()

        # Then
        with toml_with_git_versioning_lt_2.open() as file:
            section = tomlkit.load(file).get("tool")
            assert isinstance(section, Mapping)
            assert "setuptools-git-versioning" not in section
