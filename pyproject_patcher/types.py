# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring

from typing import NamedTuple, TypedDict


class MarkerExpression(TypedDict):
    op: str
    lhs: "MarkerExpression | str"
    rhs: "MarkerExpression | str"


class RequirementsContainer(NamedTuple):
    name: str
    extras: list[str] | None
    constraints: list[tuple[str, str]] | None
    marker: MarkerExpression | None
    url: str | None
    requirement: str
