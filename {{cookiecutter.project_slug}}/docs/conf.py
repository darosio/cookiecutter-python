# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# TODO: Remove the unneeded.

project = "{{ cookiecutter.project_name }}"
copyright = "{{ cookiecutter.year }}, {{ cookiecutter.author_name }}"  # noqa: A001
author = "{{ cookiecutter.author_name }}"
release = "{{ cookiecutter.version }}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []
extensions = [
    "sphinx.ext.autodoc",
    "autodocsumm",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinxcontrib.plantuml",
    "nbsphinx",
    "sphinx_click",
]
# Napoleon settings to Default
napoleon_use_ivar = False

napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_rtype = False

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": False,
    "autosummary": True,
}
autodoc_typehints = "description"


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


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
