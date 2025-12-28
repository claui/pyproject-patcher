# pylint: disable=magic-value-comparison, missing-function-docstring, missing-module-docstring, no-self-use, too-many-public-methods

from collections.abc import Mapping
from pathlib import Path

import pytest
import tomlkit

from pyproject_patcher.patcher import patch_in_place


def test_set_project_version(
    toml_with_git_versioning_lt_2: Path,
) -> None:
    # When
    with patch_in_place(toml_with_git_versioning_lt_2) as toml:
        toml.set_project_version('1.2.3')

    # Then
    with toml_with_git_versioning_lt_2.open() as file:
        section = tomlkit.load(file).get('project')
        assert isinstance(section, Mapping)
        assert 'version' in section
        assert section.get('version') == '1.2.3'


def test_set_project_version_with_interleaved_sections(
    toml_with_interleaved_sections: Path,
) -> None:
    # When
    with patch_in_place(toml_with_interleaved_sections) as toml:
        toml.set_project_version('1.2.3')

    # Then
    with toml_with_interleaved_sections.open() as file:
        section = tomlkit.load(file).get('project')
        assert isinstance(section, Mapping)
        assert 'version' in section
        assert section.get('version') == '1.2.3'


def test_set_project_version_from_env(
    toml_with_git_versioning_lt_2: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Given
    monkeypatch.setenv('pkgver', '2.0.1')

    # When
    with patch_in_place(toml_with_git_versioning_lt_2) as toml:
        toml.set_project_version_from_env('pkgver')

    # Then
    with toml_with_git_versioning_lt_2.open() as file:
        section = tomlkit.load(file).get('project')
        assert isinstance(section, Mapping)
        assert 'version' in section
        assert section.get('version') == '2.0.1'


def test_set_project_version_env_missing(
    toml_with_git_versioning_lt_2: Path,
) -> None:
    with patch_in_place(toml_with_git_versioning_lt_2) as toml:
        with pytest.raises(
            KeyError, match=r'`pkgver` not set in environment'
        ):
            toml.set_project_version_from_env('pkgver')


def test_remove_build_system_dependency(
    toml_with_git_versioning_lt_2: Path,
) -> None:
    # When
    with patch_in_place(toml_with_git_versioning_lt_2) as toml:
        toml.remove_build_system_dependency('setuptools-git-versioning')

    # Then
    with toml_with_git_versioning_lt_2.open() as file:
        section = tomlkit.load(file).get('build-system')
        assert isinstance(section, Mapping)
        assert 'requires' in section
        assert section.get('requires') == ['setuptools', 'wheel']


def test_remove_build_system_dependency_nonexistent_prefix(
    toml_with_git_versioning_lt_2: Path,
) -> None:
    # When
    with patch_in_place(toml_with_git_versioning_lt_2) as toml:
        toml.remove_build_system_dependency('setuptools-git')

    # Then
    with toml_with_git_versioning_lt_2.open() as file:
        section = tomlkit.load(file).get('build-system')
        assert isinstance(section, Mapping)
        assert 'requires' in section
        assert section.get('requires') == [
            'setuptools',
            'wheel',
            'setuptools-git-versioning<2',
        ]


def test_remove_build_system_dependency_constraint(
    toml_with_git_versioning_lt_2: Path,
) -> None:
    # When
    with patch_in_place(toml_with_git_versioning_lt_2) as toml:
        toml.strip_build_system_dependency_constraint(
            'setuptools-git-versioning'
        )

    # Then
    with toml_with_git_versioning_lt_2.open() as file:
        section = tomlkit.load(file).get('build-system')
        assert isinstance(section, Mapping)
        assert 'requires' in section
        assert section.get('requires') == [
            'setuptools',
            'wheel',
            'setuptools-git-versioning',
        ]
