# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring, no-self-use, too-few-public-methods

from pyproject_patcher.types import RequirementsContainer

def parse_requirement(__req: str) -> RequirementsContainer | None: ...
