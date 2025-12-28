# pylint: disable=magic-value-comparison, missing-function-docstring, missing-module-docstring, missing-class-docstring, no-self-use, too-many-public-methods

import pytest
import tomlkit

from pyproject_patcher.requirements import RequirementsSection


@pytest.fixture(name='requirements_array')
def fixture_requirements_array() -> tomlkit.items.Array:
    return tomlkit.array(
        '["setuptools", "wheel", "setuptools-git-versioning<2"]'
    )


class TestRequirementsSection:
    @pytest.fixture(name='section')
    def fixture_section(
        self, requirements_array: tomlkit.items.Array
    ) -> RequirementsSection:
        return RequirementsSection(requirements_array)

    def test_array(self, section: RequirementsSection) -> None:
        assert isinstance(section.array, tomlkit.items.Array)

    def test_remove_dependency(
        self, section: RequirementsSection
    ) -> None:
        # When
        section.remove_dependency('setuptools-git-versioning')

        # Then
        assert section.array == ['setuptools', 'wheel']

    def test_remove_dependency_nonexistent_prefix(
        self, section: RequirementsSection
    ) -> None:
        # When
        section.remove_dependency('setuptools-git')

        # Then
        assert section.array == [
            'setuptools',
            'wheel',
            'setuptools-git-versioning<2',
        ]

    def test_strip_constraint(
        self, section: RequirementsSection
    ) -> None:
        # When
        section.strip_constraint('setuptools-git-versioning')

        # Then
        assert section.array == [
            'setuptools',
            'wheel',
            'setuptools-git-versioning',
        ]

    def test_strip_constraint_nonexistent_prefix(
        self, section: RequirementsSection
    ) -> None:
        # When
        section.strip_constraint('setuptools-git')

        # Then
        assert section.array == [
            'setuptools',
            'wheel',
            'setuptools-git-versioning<2',
        ]
