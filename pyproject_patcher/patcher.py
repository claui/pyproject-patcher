"""
This module parses a `pyproject.toml` file, hard codes a given
version number into its `project.version`, and disables all
invocations of dynamic version generators (or removes those
invocations from the model altogether.)

This is useful for system packages, which are typically built
from source tarballs, where Git tags or commits aren’t available.
"""

import os

import distlib.util
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


    def set_project_version(self, version):
        """Sets `project.version` to the given value.

        :param version:
            The version to set.
        """
        self.document["project"]["version"] = version


    def set_project_version_from_env(self, key):
        """Sets `project.version` from the given environment variable."""
        if not (version := os.getenv(key)):
            raise KeyError(f'Error: `{key}` not set in environment. Did you `export {key}`?')
        self.set_project_version(version)


    def remove_dependency(self, section, module_name):
        """Removes a Python module dependency from the given section."""
        for dependency_expression in section:
            requirement = distlib.util.parse_requirement(dependency_expression)
            if requirement.name == module_name:
                section.remove(dependency_expression)


    def remove_build_system_dependency(self, module_name):
        """Removes a Python module dependency from `build-system.requires`."""
        self.remove_dependency(self.document["build-system"]["requires"], module_name)


    def remove_setuptools_git_versioning(self):
        """Removes the `tool` section for the `setuptools-git-versioning`
        Python model so it no longer attempts to set `project.version`
        dynamically.
        Additionally removes its import declaration from `build-system`
        so that the module doesn’t even have to be installed.
        """
        self.document["project"]["dynamic"].remove("version")
        self.document["tool"].pop("setuptools-git-versioning")
        self.remove_build_system_dependency("setuptools-git-versioning")
