"""
This module parses a `pyproject.toml` file, hard codes a given
version number into its `project.version`, and disables all
invocations of dynamic version generators (or removes those
invocations from the model altogether.)

This is useful for system packages, which are typically built
from source tarballs, where Git tags or commits aren’t available.
"""

from collections.abc import Iterator, MutableMapping, MutableSequence
from contextlib import contextmanager
import os
from typing import Any

import distlib.util  # type: ignore
from in_place import InPlace
import tomlkit

from .logging import get_logger

logger = get_logger(__name__)


class PyprojectPatcher:
    """This class accepts a `pyproject.toml` model, allows to inject
    a static version number as its `project.version`, disables all
    invocations of dynamic version generators, and removes those
    invocations and references from the model altogether.

    Some upstream projects use setuptools add-ons that allow their
    build pipeline to dynamically obtain the package version number
    from Git tags or commits. That’s a good thing in principle,
    because it helps the project to have a single point of truth
    for the version number. Typical add-ons are `setuptools-scm`
    and `setuptools-git-versioning`.

    For that to work, these add-ons generally expect a Git repository
    to be present so they can dynamically obtain the version number.
    However, a system package is typically built from a source
    tarball, which usually includes no Git tags and commits.

    To facilitate the needs of system-level package maintainers,
    `setuptools-scm` supports a `SETUPTOOLS_SCM_PRETEND_VERSION`
    environment variable, and uses its value as the version number
    if set.
    The `setuptools-git-versioning` plugin, however, doesn’t offer
    such an environment variable. Instead, it supports reading a
    version number from a file [1].
    In contrast to `SETUPTOOLS_SCM_PRETEND_VERSION`, the version file
    requires a `version_file` property to be added to `pyproject.toml`.
    Upstream projects usually don’t do that, so a system package
    maintainer would need to patch that into `pyproject.toml`.

    Instead of adding a `version_file` configuration property, this
    class removes all references to `setuptools-git-versioning` from
    `pyproject.toml`. This technique has the same effect as adding
    `version_file` but is slightly easier to use, and also guards
    against failing dependency checks caused by e.g. `<2` version
    constraints in the `build-system.requires` field.

    [1]: https://setuptools-git-versioning.readthedocs.io/en/stable/schemas/file/index.html
    """
    document: tomlkit.TOMLDocument

    def __init__(self, document: tomlkit.TOMLDocument) -> None:
        self.document = document


    def _get_section(self, section_name: str) -> tomlkit.items.Table:
        return _get_subsection(self.document, section_name)


    @property
    def build_system(self) -> tomlkit.items.Table:
        """The `build-system` section of `pyproject.toml`."""
        return self._get_section('build-system')


    @property
    def project(self) -> tomlkit.items.Table:
        """The `project` section of `pyproject.toml`."""
        return self._get_section('project')


    @property
    def tool(self) -> tomlkit.items.Table:
        """The `tool` section of `pyproject.toml`."""
        return self._get_section('tool')


    def set_project_version(self, version: str) -> None:
        """Sets `project.version` to the given value.

        :param version:
            The version to set.
        """
        self.project['version'] = version


    def set_project_version_from_env(self, key: str) -> None:
        """Sets `project.version` from the given environment variable.

        :param key:
            The name of the environment variable to whose value the
            `project.version` property is to be set.
        """
        if not (version := os.getenv(key)):
            raise KeyError(f'`{key}` not set in environment. Did you `export {key}`?')
        self.set_project_version(version)


    def remove_build_system_dependency(self, module_name: str) -> None:
        """Removes a Python module dependency from `build-system.requires`."""
        requires_section = _get_subsequence(self.build_system, 'requires')
        if not isinstance(requires_section, MutableSequence):
            raise KeyError(
                f'Expected MutableSequence, found {type(requires_section)}: {requires_section}')
        _remove_dependency(requires_section, module_name)


    def remove_setuptools_git_versioning_section(self) -> None:
        """Removes the `tool` section for the `setuptools-git-versioning`
        Python model so it no longer attempts to set `project.version`
        dynamically.
        Additionally removes its import declaration from `build-system`
        so that the module doesn’t even have to be installed.
        """
        _get_subsequence(self.project, 'dynamic').remove('version')
        self.tool.pop('setuptools-git-versioning')
        self.remove_build_system_dependency('setuptools-git-versioning')


def _get_subsection(
    parent: MutableMapping[str, tomlkit.items.Item],
    section_name: str,
) -> tomlkit.items.Table:
    section = parent.get(section_name)
    if not isinstance(section, tomlkit.items.Table):
        raise KeyError(f'Expected TOMLKit table, found {type(section)}: {section}')
    return section


def _get_subsequence(
    parent: MutableMapping[str, tomlkit.items.Item],
    section_name: str,
) -> MutableSequence[str]:
    section = parent.get(section_name)
    if not isinstance(section, MutableSequence):
        raise KeyError(f'Expected MutableSequence, found {type(section)}: {section}')
    return section


def _remove_dependency(section: MutableSequence[str], module_name: str) -> None:
    """Removes a Python module dependency from the given section.

    :param section:
        The TOML section container from which to remove a dependency.
        Example: `pyproject_patcher.build_system["requires"]`

    :param module_name:
        The name of a module that is declared in the `section`
    """
    for dependency_expression in section:
        requirement = distlib.util.parse_requirement(dependency_expression)
        if requirement.name == module_name:
            section.remove(dependency_expression)


@contextmanager
def patch_in_place(path: str | os.PathLike[Any]) -> Iterator[PyprojectPatcher]:
    """Patches a given `pyproject.toml` file in place."""
    with InPlace(path) as f:
        patcher = PyprojectPatcher(tomlkit.load(f))
        yield patcher
        tomlkit.dump(patcher.document, f)
