# pylint: disable=magic-value-comparison, missing-function-docstring, missing-module-docstring, missing-class-docstring, no-self-use, too-few-public-methods

from collections.abc import Mapping
from pathlib import Path

import tomlkit

from pyproject_patcher.patcher import patch_in_place


class TestSetuptools:
    def test_exclude_package_data(
        self, toml_with_package_data_included: Path
    ) -> None:
        # When
        with patch_in_place(toml_with_package_data_included) as toml:
            toml.tools.setuptools.exclude_package_data()

        # Then
        with toml_with_package_data_included.open() as file:
            tool_section = tomlkit.load(file).get('tool')
            assert isinstance(tool_section, Mapping)
            assert 'setuptools' in tool_section
            setuptools_section = tool_section.get('setuptools')
            assert isinstance(setuptools_section, Mapping)
            assert 'include-package-data' in setuptools_section
            assert (
                setuptools_section.get('include-package-data') is False
            )
