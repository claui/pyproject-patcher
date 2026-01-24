# pylint: disable=magic-value-comparison, missing-function-docstring, missing-module-docstring, missing-class-docstring, no-self-use, too-few-public-methods

from collections.abc import Mapping
from pathlib import Path

try:
    # setuptools-git-versioning >= 3.0.0
    from setuptools_git_versioning.defaults import DEFAULT_DEV_TEMPLATE
except ImportError:
    # setuptools-git-versioning < 3.0.0
    from setuptools_git_versioning import DEFAULT_DEV_TEMPLATE

import tomlkit

from pyproject_patcher.patcher import patch_in_place


class TestSetuptoolsGitVersioning:
    def test_remove(self, toml_with_git_versioning_lt_2: Path) -> None:
        # When
        with patch_in_place(toml_with_git_versioning_lt_2) as toml:
            toml.tools.setuptools_git_versioning.remove()

        # Then
        with toml_with_git_versioning_lt_2.open() as file:
            section = tomlkit.load(file).get('tool')
            assert isinstance(section, Mapping)
            assert 'setuptools-git-versioning' not in section

    def test_ignore_dirty_git(
        self, toml_with_git_versioning_lt_2: Path
    ) -> None:
        # When
        with patch_in_place(toml_with_git_versioning_lt_2) as toml:
            toml.tools.setuptools_git_versioning.template_ignore_dirty_git()

        # Then
        with toml_with_git_versioning_lt_2.open() as file:
            l1_section = tomlkit.load(file).get('tool')
            assert isinstance(l1_section, Mapping)
            assert 'setuptools-git-versioning' in l1_section
            l2_section = l1_section.get('setuptools-git-versioning')
            assert isinstance(l2_section, Mapping)
            assert (
                l2_section.get('dirty_template') == DEFAULT_DEV_TEMPLATE
            )
