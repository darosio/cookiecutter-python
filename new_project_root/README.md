# {{ cookiecutter.project_name }}

[![PyPI](https://img.shields.io/pypi/v/{{ cookiecutter.project_name }}.svg)](https://pypi.org/project/{{ cookiecutter.project_name }}/)
[![CI](https://github.com/darosio/{{ cookiecutter.project_name }}/actions/workflows/ci.yml/badge.svg)](https://github.com/darosio/{{ cookiecutter.project_name }}/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/darosio/{{ cookiecutter.project_name }}/branch/main/graph/badge.svg?token=OU6F9VFUQ6)](https://codecov.io/gh/darosio/{{ cookiecutter.project_name }})
[![RtD](https://readthedocs.org/projects/{{ cookiecutter.project_slug }}/badge/)](https://{{ cookiecutter.project_slug }}.readthedocs.io/)

This package provides a command line interface for …

- Version: "{{ cookiecutter.version }}"


## Installation

You can get the library directly from [PyPI](https://pypi.org/project/{{ cookiecutter.project_name }}/)
using `pip`:

    pip install {{ cookiecutter.project_slug }}

Alternatively, you can use [pipx](https://pypa.github.io/pipx/) to install it in
an isolated environment:

    pipx install {{ cookiecutter.project_slug }}

To enable auto completion for the `cli` command, follow these steps:

1.  Generate the completion script by running the following command:

        _{{ cookiecutter.cliname.upper() }}_COMPLETE=bash_source {{ cookiecutter.cliname }} > ~/.local/bin/{{ cookiecutter.cliname }}-complete.bash

2.  Source the generated completion script to enable auto completion:

        source ~/.local/bin/{{ cookiecutter.cliname }}-complete.bash

## Usage

You can check out the documentation on <https://darosio.github.io/{{ cookiecutter.project_name }}> for
up to date usage information and examples.

### CLI

{{ cookiecutter.project_name }} provides several command line interface tools for …

    cliname --help

### Python

{{ cookiecutter.project_name }} can be imported and used as a Python package. The following modules are
available:

    {{ cookiecutter.project_slug }}. - DESCRIBE

To use {{ cookiecutter.project_name }} in your python:

    from {{ cookiecutter.project_slug }} import …

## Features

- FIRST.
- SECOND.

## License

We use a shared copyright model that enables all contributors to maintain the
copyright on their contributions.

All code is licensed under the terms of the [revised BSD license](LICENSE.txt).

## Contributing

If you are interested in contributing to the project, please read our
[contributing](https://darosio.github.io/{{ cookiecutter.project_name }}/references/contributing.html)
and
[development environment](https://darosio.github.io/{{ cookiecutter.project_name }}/references/development.html)
guides, which outline the guidelines and conventions that we follow for
contributing code, documentation, and other resources.
