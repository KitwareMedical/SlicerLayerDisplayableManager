# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

from exhale import utils

cur_path = Path(__file__).parent
sys.path.insert(0, cur_path.parent.as_posix())

# -- Project information -----------------------------------------------------

project = "Slicer Layer Displayable Manager"
copyright = "2025, Kitware"
author = "Kitware"

# -- General configuration ---------------------------------------------------

extensions = [
    "breathe",
    "exhale",
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.duration",
    "sphinx.ext.graphviz",
    "sphinx.ext.imgconverter",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.mermaid",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Breathe ----------------------------------------------------------
breathe_projects = {"Slicer Layer Displayable Manager": "./doxygen/xml"}
breathe_default_members = ('members', 'undoc-members')
breathe_default_project = "Slicer Layer Displayable Manager"


# -- Exhale -----------------------------------------------------------


def custom_exhale_mapping(kind):
    """
    Override to add dot graphs to generation.
    """
    if kind in ("class", "struct"):
        return [
            ":members:",
            ":protected-members:",
            ":undoc-members:",
            ":allow-dot-graphs:",
        ]
    return []


exhale_args = {
    "containmentFolder": "./api",
    "rootFileName": "library_root.rst",
    "rootFileTitle": "C++ API Reference",
    "doxygenStripFromPath": "..",
    "customSpecificationsMapping": utils.makeCustomSpecificationsMapping(custom_exhale_mapping),
}

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = "bysource"
autodoc_mock_imports = ["slicer", "LayerDMLib", "vtkITK"]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]

# -- Graphviz options -------------------------------------------------
graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Grankdir=BT",
]
