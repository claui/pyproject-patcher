<!-- markdownlint-configure-file { "MD041": { "level": 1 } } -->

# Example

```py
from pyproject_patcher import PyprojectPatcher
from in_place import InPlace
import tomlkit

with InPlace('pyproject_toml') as f:
    model = PyprojectPatcher(tomlkit.load(f))
    model.set_project_version('1.2.7')
    model.remove_setuptools_git_versioning()
    tomlkit.dump(model, f)
```
