# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# pylint: skip-file
# type: ignore

project = 'pyproject-patcher'
executable = 'pyproject-patcher'
author = 'Claudia Pellegrino <clau@tiqua.de>'
description = 'Collection of convenience functions to patch `pyproject.toml` in place'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'autoapi.extension',
    'myst_parser',
    'sphinx.ext.autodoc',
]

autoapi_dirs = ['../../pyproject_patcher']
autoapi_keep_files = True
autoapi_ignore = ['**/stubs/**']
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
    'special-members',
    'imported-members',
]
autoapi_type = 'python'
autodoc_typehints = 'description'

html_theme = 'sphinx_rtd_theme'

myst_enable_extensions = [
    'deflist',
]


def skip_module(app, what, name, obj, skip, options):
    if what != 'module':
        return skip
    if name in [
        'pyproject_patcher.config',
        'pyproject_patcher.settings',
        'pyproject_patcher.version',
    ]:
        return True
    return skip


def setup(sphinx):
    sphinx.connect('autoapi-skip-member', skip_module)


templates_path = []
exclude_patterns = [
    '**/pyproject_patcher/config/**',
    '**/pyproject_patcher/settings/**',
    '**/pyproject_patcher/version/**',
]

# Man page output

man_pages = [
    (
        'usage',
        'pyproject-patcher',
        description,
        [author],
        3,
    )
]

man_show_urls = True
