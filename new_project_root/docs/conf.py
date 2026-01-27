"""Configuration file for the Sphinx documentation builder."""

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# TODO: Remove the unneeded.

project = "{{ cookiecutter.project_name }}"
author = "{{ cookiecutter.author_name }}"
copyright = f"{{ cookiecutter.year }}, {author}"  # noqa: A001

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "autodocsumm",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinxcontrib.plantuml",
    "myst_nb",
    "sphinx_click",
]
# Napoleon settings to Default
napoleon_use_ivar = False
# Use __init__ docstring
napoleon_include_init_with_doc = False
# Use _private docstring
napoleon_include_private_with_doc = True
# Use __special__ docstring
napoleon_include_special_with_doc = True

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": False,
    "autosummary": True,
}

autodoc_typehints = "description"

# The suffix of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    # ".md": "markdown",
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
# To prevent latex hanging on symbols supported by xelatex, but RtD uses latex.
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

# Avoid multiprocessing in notebooks during Sphinx builds (pickling issues with
# functions defined in notebook cells under newer Python versions).
os.environ.setdefault("CLOPHFIT_EMCEE_WORKERS", "1")

# Keep notebooks fast when executed by Sphinx.
os.environ.setdefault("CLOPHFIT_DOCS_EMCEE_STEPS", "300")
os.environ.setdefault("CLOPHFIT_DOCS_EMCEE_BURN", "50")
os.environ.setdefault("CLOPHFIT_DOCS_EMCEE_THIN", "10")
os.environ.setdefault("CLOPHFIT_DOCS_EMCEE_NWALKERS", "10")


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
