# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyproject-patcher'
executable_name = 'pyproject-patcher'
author = 'Claudia Pellegrino <clau@tiqua.de>'
description = 'Collection of convenience functions to patch `pyproject.toml` in place'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

myst_enable_extensions = [
    'deflist',
]

templates_path = []
exclude_patterns = []

# Man page output

man_pages = [(
    'index',
    'pyproject-patcher',
    description,
    [author],
    3,
)]
