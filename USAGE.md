<!-- markdownlint-configure-file { "MD041": { "level": 1 } } -->

# Example

```py
from pyproject_patcher import patch_in_place

with patch_in_place('pyproject.toml') as toml:
    toml.set_project_version('1.2.3')
    toml.remove_build_system_dependency('setuptools-git-versioning')
    toml.remove_setuptools_git_versioning()
```
