# cookiecutter-python

Python best practices project cookiecutter.

```
cookiecutter workspace/cookiecutter-python/
cookiecutter https://github.com/darosio/cookiecutter-python
```

## Settings on github

1. Actions permissions

   - Any action or reusable workflow can be used, regardless of who authored it,
     or where it is defined.
     **Workflow permissions**
     Read and Write Permissions
     \[x\] Allow Github Actions to create and approve pull requests

1. Pages

   - Source: Github Actions <https://github.com/darosio/imgread/settings/pages>.
     Deploy from a branch gh-pages as using `jamesives/github-pages-deploy-action@v4`

1. RtD

   - Go to <https://readthedocs.org/dashboard/> and import project.

1. Codecov

   - Go to <https://app.codecov.io/gh/darosio> and setup.
   - add “CODECOV_TOKEN” as repository secrets.

1. PyPI

   - For the first time you can simply

     hatch run bump

     which will build and publish in TestPyPI; then:

     pipx run twine upload dist/\*
     ((hatch publish))

     ~/.pypirc
     [pypi]
     username = **token**
     password = pypi-AgEIcH…

     If you have 2FA in PyPI

   - Go to <https://pypi.org/manage/account/>
     (- [Publishing] setup new project)

     - Create project PYPI_TOKEN and copy into github secrets.

## Python version policy

Renovate does not bump `.python-version`. Adding or dropping a Python version
is a coordinated change: bumping `.python-version` alone makes local dev and
the release workflow use an interpreter that CI never exercises, and often
pulls in dependencies that do not support it yet.

Do the upgrade in one PR and update **all** of the following:

- `.python-version` — the newest supported version (local dev/release default)
- `pyproject.toml` — `requires-python`, the `Programming Language :: Python :: 3.x`
  classifiers, and `[tool.ruff] target-version` (the minimum supported)
- `.github/workflows/ci.yml` — the `tests.strategy.matrix.python` list, which
  must contain every supported version
- `.readthedocs.yml` — `build.tools.python`
- run `uv lock` and commit the refreshed lock file

`tests/test_cookiecutter.py::test_python_versions_are_consistent` fails CI if
these files drift apart, so a future isolated bump cannot be merged.

## Check and edit

- pyproject.toml
- .github/
- .gitignore
- .pre-commit-config.yaml
- .readthedocs.yml
