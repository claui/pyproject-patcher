# pyproject-patcher

This Python package is an attempt to make it a little easier to
patch `pyproject.toml` in place.

It is mainly useful for maintainers of system packages.  
If you’re not a maintainer of system packages, or if you don’t know
what that means, then `pyproject-patcher` is probably not for you.

## Features

- Hard code a version number into `project.version`

- Disable all invocations of the dynamic version generator
  `setuptools-git-versioning`

- Remove dependency to `setuptools-git-versioning` from
  `build-system.requires`

- Configure `setuptools-git-versioning` to use a version template
  without a `.dirty` suffix

## Installation

### Installing from PyPI

To install pyproject-patcher from PyPI, open a shell and run:

```shell
pip install pyproject-patcher
```

If that doesn’t work, try:

```shell
python3 -m pip install pyproject-patcher
```

### Installing from the AUR

Direct your favorite
[AUR helper](https://wiki.archlinux.org/title/AUR_helpers) to the
`python-pyproject-patcher` package.

## Usage

See [`USAGE.md`](https://github.com/claui/pyproject-patcher/blob/main/USAGE.md)
for details.

## Contributing to pyproject-patcher

See [`CONTRIBUTING.md`](https://github.com/claui/pyproject-patcher/blob/main/CONTRIBUTING.md).

## License

Copyright (c) 2024–2025 Claudia Pellegrino

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
For a copy of the License, see [LICENSE](https://raw.githubusercontent.com/claui/pyproject-patcher/refs/heads/main/LICENSE).
