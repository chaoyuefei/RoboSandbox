# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../robosandbox"))

# -- Project information -----------------------------------------------------

project = "robosandbox"
copyright = "2025, Chaoyue Fei"
author = "Chaoyue Fei"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",  # Automatically document from docstrings
    "sphinx.ext.autosummary",  # Generate summary tables for modules/functions
    "sphinx.ext.viewcode",  # Include source code in the documentation
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
# Uncomment the line below if using sphinx_rtd_theme instead
# html_theme = 'sphinx_rtd_theme'
html_static_path = ["_static"]
autosummary_generate = True  # Generate autosummary pages
