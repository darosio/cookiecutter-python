"""Configuration file for the Sphinx documentation builder."""

# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os

# -- Project information -----------------------------------------------------

# TODO: Remove the unneeded.

project = "{{ cookiecutter.project_name }}"
author = "{{ cookiecutter.author_name }}"
copyright = f"{{ cookiecutter.year }}, {author}"  # noqa: A001

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinxcontrib.plantuml",
    "myst_nb",
    "sphinx_click",
]

# Napoleon settings to Default
napoleon_use_ivar = False

# -- sphinx-autoapi configuration --------------------------------------------
autoapi_dirs = ["../src"]
autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
]
autoapi_member_order = "bysource"
autoapi_add_toctree_entry = False
autoapi_keep_files = True
# suppress_warnings = ["autoapi.python_import_resolution"]

# The suffix of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb",
    ".ipynb": "myst-nb",
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "10pt",
    # Additional preamble content
    "preamble": r"""
\usepackage[utf8]{inputenc}
\usepackage{newunicodechar}
\newunicodechar{█}{\rule{1ex}{1ex}}
""",
}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "jupyter_execute",
    "**/.virtual_documents",
    "**/.ipynb_checkpoints",
]

# -- nbsphinx / myst-nb -----------------------------------------------------
# myst-nb configuration
nb_execution_mode = os.environ.get(
    "NB_EXECUTION_MODE", os.environ.get("NBSPHINX_EXECUTE", "auto")
)
nb_execution_timeout = 300  # Increase timeout to 5 minutes
nb_execution_allow_errors = False
nb_execution_raise_on_error = True
nb_execution_show_tb = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
