"""Version number management."""

from contextlib import suppress
import importlib.metadata

from tomlkit.toml_file import TOMLFile

from .settings import PYPROJECT_TOML


def version() -> str | None:
    """Attempts to return a version number for this project.

    Checks both `pyproject.toml` in the development tree and the
    `importlib.metadata` facility for an installed package, with the
    `pyproject.toml` file taking precedence if it exists.

    :return:
        a version string if one is found, None otherwise.
    """
    with suppress(FileNotFoundError):
        document = TOMLFile(PYPROJECT_TOML).read()
        return document['tool']['poetry']['version']

    with suppress(FileNotFoundError):
        return importlib.metadata.version(
            __package__ or __name__.split('.', maxsplit=1)[0])

    return None
