"""Manage requirements expressions, with or without version constraints."""

from collections.abc import Iterable

import tomlkit
import distlib.util

from .types import RequirementsContainer


class RequirementsSection:
    """A list of requirements expressions.

    For example:

    ```py
    ["setuptools", "wheel", "setuptools-git-versioning<2"]
    ```
    """

    array: tomlkit.items.Array

    def __init__(self, array: tomlkit.items.Array) -> None:
        self.array = array

    def _requirements(
        self,
    ) -> Iterable[tuple[RequirementsContainer, str]]:
        for dependency_expression in self.array:
            if (
                requirement := distlib.util.parse_requirement(
                    dependency_expression
                )
            ) is not None:
                yield requirement, dependency_expression

    def remove_dependency(self, module_name: str) -> None:
        """Removes a Python module dependency from this section.

        :param module_name:
            The name of a module that is declared in this section.
        """
        for requirement, dependency_expression in self._requirements():
            if requirement.name == module_name:
                self.array.remove(dependency_expression)

    def strip_constraint(self, module_name: str) -> None:
        """For a Python module dependency in this section, remove
        its version constraint.

        :param module_name:
            The name of a module that is declared in this section.
        """
        for requirement, dependency_expression in self._requirements():
            if requirement.name == module_name:
                self.array.remove(dependency_expression)
                self.array.append(requirement.name)
