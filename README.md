# cookiecutter-python

Python best practices project cookiecutter.

    cookiecutter workspace/cookiecutter-python/
    cookiecutter https://github.com/darosio/cookiecutter-python

## Settings on github

1. Actions permissions

   - Any action or reusable workflow can be used, regardless of who authored it,
     or where it is defined.
     **Workflow permissions**
     Read and Write Permissions
     [x] Allow Github Actions to create and approve pull requests

2. Pages

   - Source: Github Actions <https://github.com/darosio/imgread/settings/pages>.
     Deploy from a branch gh-pages as using `jamesives/github-pages-deploy-action@v4`

3. RtD

   - Go to <https://readthedocs.org/dashboard/> and import project.

4. Codecov

   - Go to <https://app.codecov.io/gh/darosio> and setup.
   - add “CODECOV_TOKEN” as repository secrets.

5. PyPI

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

## TODO

- Tut2 is empty file.
- Update readedocs.yml.
- Update deps use dependabot?

## Check and edit

- pyproject.toml
- .github/
- .gitignore
- .pre-commit-config.yaml
- .readthedocs.yml
