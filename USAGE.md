<!-- markdownlint-configure-file { "MD041": { "level": 1 } } -->

# Description

This Python package is an attempt to make it a little easier to
patch `pyproject.toml` in place.

It is mainly useful for maintainers of system packages.  
If you’re not a maintainer of system packages, or if you don’t know
what that means, then `pyproject-patcher` is probably not for you.

# Examples

## Recommended import statement

The following examples all assume the following import statement:

```py
from pyproject_patcher import patch_in_place
```

## Set a static project version

```py
with patch_in_place('pyproject.toml') as toml:
    toml.set_project_version('1.2.3')
```

## Strip the version constraint of a dependency

```py
with patch_in_place('pyproject.toml') as toml:
    toml.strip_build_system_dependency_constraint('setuptools-git-versioning')
    # or, equivalently:
    # toml.build_system_requires.strip_constraint('setuptools-git-versioning')
```

## Remove an entry from a dependency list

```py
with patch_in_place('pyproject.toml') as toml:
    toml.remove_build_system_dependency('setuptools-git-versioning')
    # or, equivalently:
    # toml.build_system_requires.remove_dependency('setuptools-git-versioning')
```

## Remove `setuptools-git-versioning` from `pyproject.toml` entirely

```py
with patch_in_place('pyproject.toml') as toml:
    toml.set_project_version('1.2.3')
    toml.tools.setuptools_git_versioning.remove()
```

## Configure a version template without a `.dirty` suffix

```py
with patch_in_place('pyproject.toml') as toml:
    toml.tools.setuptools_git_versioning.template_ignore_dirty_git()
```

# Environment

pyproject-patcher supports the following environment variable:

`PYPROJECT_PATCHER_DEBUG`
: If set to a non-zero value, causes pyproject-patcher to enable debug-level
: logging.
