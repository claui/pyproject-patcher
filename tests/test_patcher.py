# pylint: disable=magic-value-comparison, missing-function-docstring, missing-module-docstring, no-self-use, too-many-public-methods

import tomlkit
import pytest

from pyproject_patcher.patcher import PyprojectPatcher


# from in_place import InPlace

# with InPlace('pyproject_toml') as f:
#     model = PyprojectPatcher(tomlkit.load(f))
#     model.set_project_version('1.2.7')
#     model.remove_setuptools_git_versioning()
#     tomlkit.dump(model, f)


@pytest.fixture(name='patcher')
def fixture_patcher() -> PyprojectPatcher:
    return PyprojectPatcher(tomlkit.load('foo/pyproject.toml'))
