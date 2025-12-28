# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring

from typing import NamedTuple, TypedDict


class MarkerExpression(TypedDict):
    """See also:
    https://peps.python.org/pep-0508/#environment-markers
    """

    op: str
    lhs: 'MarkerExpression | str'
    rhs: 'MarkerExpression | str'


class RequirementsContainer(NamedTuple):
    """See also:
    https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata-provides-extra
    """

    name: str
    extras: list[str] | None
    constraints: list[tuple[str, str]] | None
    marker: MarkerExpression | None
    url: str | None
    requirement: str
