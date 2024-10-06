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
from dataclasses import dataclass
import functools
import os
from typing import Any
from typing_extensions import deprecated

from in_place import InPlace
import tomlkit

from .logging import get_logger
from .requirements import RequirementsSection
from .tools import Tools

logger = get_logger(__name__)


@dataclass(frozen=True)
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

    def _get_section(
        self, section_name: str
    ) -> MutableMapping[str, str | tomlkit.items.Item]:
        return _get_subsection(self.document, section_name)

    @property
    def build_system(
        self,
    ) -> MutableMapping[str, str | tomlkit.items.Item]:
        """Low-level access to the `build-system` section of
        `pyproject.toml`."""
        return self._get_section('build-system')

    @property
    def build_system_requires(self) -> RequirementsSection:
        """High-level access to the `requires` subsection of the `build-system`
        section."""
        section = _get_subsequence(self.build_system, 'requires')
        if not isinstance(section, tomlkit.items.Array):
            raise KeyError(
                f'Expected tomlkit.items.Array, found {type(section)}: {section}'
            )
        return RequirementsSection(section)

    @property
    def dynamic(self) -> MutableSequence[str]:
        """Low-level access to the `project.dynamic` subsection of
        the `build-system` section."""
        section = _get_subsequence(self.project, 'dynamic')
        if not isinstance(section, tomlkit.items.Array):
            raise KeyError(
                f'Expected tomlkit.items.Array, found {type(section)}: {section}'
            )
        return section

    @property
    def project(self) -> MutableMapping[str, str | tomlkit.items.Item]:
        """Low-level access to the `project` section of `pyproject.toml`."""
        return self._get_section('project')

    @property
    def tool(self) -> MutableMapping[str, str | tomlkit.items.Item]:
        """Low-level access to the `tool` section of `pyproject.toml`."""
        return self._get_section('tool')

    @functools.cached_property
    def tools(self) -> Tools:
        """High-level convenience methods for manipulating tool
        settings, e.g. settings for the `setuptools_git_versioning`
        tool."""
        return Tools(self)

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
            raise KeyError(
                f'`{key}` not set in environment. Did you `export {key}`?'
            )
        logger.debug('Using environment variable: %s', key)
        self.set_project_version(version)

    def remove_build_system_dependency(self, module_name: str) -> None:
        """Removes a Python module dependency from `build-system.requires`."""
        self.build_system_requires.remove_dependency(module_name)

    def strip_build_system_dependency_constraint(
        self, module_name: str
    ) -> None:
        """Modifies an entry in `build-system.requires` to strip its
        version constraint.
        """
        self.build_system_requires.strip_constraint(module_name)

    @deprecated(
        'Use self.tools.setuptools_git_versioning.remove() instead'
    )
    def remove_setuptools_git_versioning_section(self) -> None:
        """Removes the `tool` section for the `setuptools-git-versioning`
        Python model so it no longer attempts to set `project.version`
        dynamically.
        Additionally removes its import declaration from `build-system`
        so that the module doesn’t even have to be installed.
        """
        self.tools.setuptools_git_versioning.remove()


def _get_subsection(
    parent: MutableMapping[str, str | tomlkit.items.Item],
    section_name: str,
) -> MutableMapping[str, str | tomlkit.items.Item]:
    section = parent.get(section_name)
    if not isinstance(section, MutableMapping):
        raise KeyError(
            f'Expected MutableMapping, found {type(section)}: {section}'
        )
    return section


def _get_subsequence(
    parent: MutableMapping[str, str | tomlkit.items.Item],
    section_name: str,
) -> MutableSequence[str]:
    section = parent.get(section_name)
    if not isinstance(section, MutableSequence):
        raise KeyError(
            f'Expected MutableSequence, found {type(section)}: {section}'
        )
    return section


@contextmanager
def patch_in_place(
    path: str | os.PathLike[Any],
) -> Iterator[PyprojectPatcher]:
    """Patches a given `pyproject.toml` file in place."""
    with InPlace(path) as f:
        patcher = PyprojectPatcher(tomlkit.load(f))
        yield patcher
        tomlkit.dump(patcher.document, f)
