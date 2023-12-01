# cookiecutter-python

Python best practices project cookiecutter.
<<<<<<< HEAD

## Settings on github

1. Actions permissions

   - Any action or reusable workflow can be used, regardless of who authored it,
     or where it is defined.

2. Pages

   - Source: Github Actions <https://github.com/darosio/imgread/settings/pages>.

3. RtD

   - Go to <https://readthedocs.org/dashboard/> and import project.

4. Codecov

   - Go to <https://app.codecov.io/gh/darosio> and setup.
   - add “CODECOV_TOKEN” as repository secrets.

5. PyPI

   - For the first time you can simply

     hatch run bump

     which will build and publish in TestPyPI; then:

     hatch publish

   - Go to <https://pypi.org/manage/account/>
     (- [Publishing] setup new project)
     - Create project PYPI_TOKEN and copy into github secrets.

## TODO

- Tut2 is empty file.
- Complete ci.yml and docs.yml. {{name}}…
- Update readedocs.yml.
- Update deps use dependabot?
||||||| bbd1879
=======

## Settings on github

1. Actions permissions

   - Any action or reusable workflow can be used, regardless of who authored it,
     or where it is defined.

2. Pages

   - Source: Github Actions <https://github.com/darosio/imgread/settings/pages>.

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
- Complete ci.yml and docs.yml. {{name}}…
- Update readedocs.yml.
- Update deps use dependabot?
>>>>>>> origin/main
