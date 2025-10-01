# {{ cookiecutter.project_name }}

[![PyPI](https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg)](https://pypi.org/project/{{ cookiecutter.project_slug }}/)
[![CI](https://github.com/darosio/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml/badge.svg)](https://github.com/darosio/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/darosio/{{ cookiecutter.project_slug }}/branch/main/graph/badge.svg?token=OU6F9VFUQ6)](https://codecov.io/gh/darosio/{{ cookiecutter.project_slug }})
[![RtD](https://readthedocs.org/projects/{{ cookiecutter.project_slug }}/badge/)](https://{{ cookiecutter.project_slug }}.readthedocs.io/)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue?logo=github)](https://darosio.github.io/{{ cookiecutter.project_slug }}/)

{{ cookiecutter.project_name }} provides a command line interface and Python API for …

## Features

- FIRST
- SECOND

## Installation

From PyPI with pip:

```bash
pip install {{ cookiecutter.project_slug }}
```

Or isolate with pipx:

```bash
pipx install {{ cookiecutter.project_slug }}
```

Shell completion (Click/Typer):

- Bash:

```bash
  _{{ cookiecutter.cliname|upper }}_COMPLETE=bash_source {{ cookiecutter.cliname }} > ~/.local/bin/{{ cookiecutter.cliname }}-complete.bash
  source ~/.local/bin/{{ cookiecutter.cliname }}-complete.bash
```

- Fish:

```bash
  _{{ cookiecutter.cliname|upper }}_COMPLETE=fish_source {{ cookiecutter.cliname }} | source
```

## Usage

Docs: https://{{ cookiecutter.project_slug }}.readthedocs.io/

CLI:

```bash
{{ cookiecutter.cliname }} --help
```

Python:

```python
from {{ cookiecutter.project_slug }} import …
```
## Development

Requires Python `uv`.

With uv:
```bash
# one-time
pre-commit install
# dev tools and deps
uv sync --group dev
# lint/test
uv run ruff check .  (or: make lint)
uv run pytest -q  (or: make test)
```

## Dependency updates (Renovate)

We use Renovate to keep dependencies current.

Enable Renovate:

1. Install the GitHub App: https://github.com/apps/renovate (Settings → Integrations → GitHub Apps → Configure → select this repo/org).
1. This repo includes a `renovate.json` policy. Renovate will open a “Dependency Dashboard” issue and PRs accordingly.

Notes:

- Commit style: `build(deps): bump <dep> from <old> to <new>`
- Pre-commit hooks are grouped and labeled; Python version bumps in `pyproject.toml` are disabled by policy.

Migrating from Dependabot:

- You may keep “Dependabot alerts” ON for vulnerability visibility, but disable Dependabot security PRs.

## Template updates (Cruft)

This project is linked to its Cookiecutter template with Cruft.

- Check for updates: `cruft check`
- Apply updates: `cruft update -y` (resolve conflicts, then commit)

CI runs a weekly job to open a PR when template updates are available.

First-time setup if you didn’t generate with Cruft:

```bash
pipx install cruft  # or: pip install --user cruft
cruft link --checkout main https://github.com/darosio/cookiecutter-python.git
```

Notes:

- The CI workflow skips if `.cruft.json` is absent.
- If you maintain a stable template branch (e.g., `v1`), link with `--checkout v1`. You can also update within that line using `cruft update -y --checkout v1`.

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
