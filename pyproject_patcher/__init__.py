"""
Usage example:

.. code:: python

   from pyproject_patcher.patcher import Patcher

   patcher = Patcher()
   patcher.hello()
"""

# Re-export these symbols
# (This promotes them from pyproject_patcher.patcher to pyproject_patcher)
from pyproject_patcher.patcher import patch_in_place as patch_in_place

from pyproject_patcher.version import version

__all__ = [
    # Modules that every subpackage should see
    'settings',
]

__version__ = version()
