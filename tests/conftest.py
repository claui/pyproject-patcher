# pylint: disable=missing-function-docstring, missing-module-docstring

from pathlib import Path
from textwrap import dedent

import pytest


@pytest.fixture(name='toml_with_git_versioning_lt_2')
def fixture_toml_with_git_versioning_lt_2(tmp_path: Path) -> Path:
    path = tmp_path / 'pyproject_toml'
    with open(path, encoding='utf-8', mode='w') as file:
        file.write(
            dedent("""\
            [build-system]
            requires = ["setuptools", "wheel", "setuptools-git-versioning<2"]
            build-backend = "setuptools.build_meta"

            [project]
            name = "toml_with_git_versioning_lt_2"
            description = "Test"
            dynamic = ["version"]

            [tool.setuptools]
            packages = ["toml_with_git_versioning_lt_2"]

            [tool.setuptools-git-versioning]
            enabled = true
            starting_version = "0.1.0"
            """)
        )
    return path


@pytest.fixture(name='toml_with_interleaved_sections')
def fixture_toml_with_interleaved_sections(tmp_path: Path) -> Path:
    path = tmp_path / 'pyproject_toml'
    with open(path, encoding='utf-8', mode='w') as file:
        file.write(
            dedent("""\
            [build-system]
            requires = ["setuptools", "wheel", "setuptools-git-versioning<2"]
            build-backend = "setuptools.build_meta"

            [project]
            name = "toml_with_interleaved_sections"
            description = "Test with interleaved `project` and `tool` sections"
            dynamic = ["version"]

            [tool.setuptools]
            packages = ["toml_with_interleaved_sections"]

            [project.scripts]
            foo = "toml_with_interleaved_sections.foo:main"

            [tool.setuptools-git-versioning]
            enabled = true
            starting_version = "1.0.0"
            """)
        )
    return path
