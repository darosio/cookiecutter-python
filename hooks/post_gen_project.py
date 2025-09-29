"""Post generation hook."""

import shutil
from pathlib import Path

# shutil.move("project.toml", "pyproject.toml")

project_type = "{{ cookiecutter.project_type }}"
if project_type == "Data Analysis Project":
    shutil.move("docs/index4data.rst", "docs/index.rst")
    notebook = Path("docs/{{ cookiecutter.date }}.ipynb")
    notebook.symlink_to("../analyses/{{ cookiecutter.date }}.ipynb")


remove_paths = [
    '{% if cookiecutter.project_type != "Python Project" %}.github{% endif %}',
    '{% if cookiecutter.project_type != "Python Project" %}.readthedocs.yml{% endif %}',
    '{% if cookiecutter.project_type != "Python Project" %}README.md{% endif %}',
    '{% if cookiecutter.project_type != "Python Project" %}renovate.json{% endif %}',
    '{% if cookiecutter.project_type != "Data Analysis Project" %}docs/tutorials{% endif %}',
    '{% if cookiecutter.project_type != "Data Analysis Project" %}Readme.org{% endif %}',
    '{% if cookiecutter.project_type != "Data Analysis Project" %}analyses{% endif %}',
    '{% if cookiecutter.project_type != "Data Analysis Project" %}data{% endif %}',
    '{% if cookiecutter.project_type != "Data Analysis Project" %}docs/index4data.rst{% endif %}',
    '{% if cookiecutter.project_type != "Data Analysis Project" %}docs/analyses.rst{% endif %}',
    '{% if cookiecutter.project_type != "Data Analysis Project" %}docs/20240101.ipynb{% endif %}',
    # '{% if cookiecutter.project_type != "Data Analysis Project" %}.envrc{% endif %}',
]

for path_str in remove_paths:
    path = Path(path_str) if path_str else None
    if path and path.exists():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


def modify_pre_commit_config():
    project_dir = Path.cwd()
    config_path = project_dir / ".pre-commit-config.yaml"
    # Read the current content of the file
    content = config_path.read_text()
    # Prepare the replacement content based on project type
    project_type = "{{ cookiecutter.project_type }}"
    if project_type == "Python Project":
        python_hooks = "- id: check-symlinks"
        analysis_exclude = ""
    elif project_type == "Data Analysis Project":
        python_hooks = ""
        analysis_exclude = "exclude: ^data/.*\n"
    else:
        python_hooks = ""
        analysis_exclude = ""
    # Perform replacements and remove lines if they should be empty
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if "# OPTIONAL_PYTHON_PROJECT_HOOKS" in line:
            if python_hooks:
                new_lines.append(
                    line.replace("# OPTIONAL_PYTHON_PROJECT_HOOKS", python_hooks)
                )
        elif "# DATA_ANALYSIS_EXCLUDE" in line:
            if analysis_exclude:
                new_lines.append(
                    line.replace("# DATA_ANALYSIS_EXCLUDE", analysis_exclude)
                )
        elif 'exclude: "{{cookiecutter.project_slug}}/"' in line:
            continue
        else:
            new_lines.append(line)
    # Write the new content back to the file
    config_path.write_text("\n".join(new_lines) + "\n")


def modify_pyproject():
    project_dir = Path.cwd()
    config_path = project_dir / "pyproject.toml"
    # Read the current content of the file
    content = config_path.read_text()
    # Prepare the replacement content based on project type
    project_type = "{{ cookiecutter.project_type }}"
    if project_type == "Python Project":
        readme_md = 'readme = "README.md"'
        project_urls = """[project.urls]
"Bug Tracker" = "https://github.com/darosio/{{ cookiecutter.project_name }}/issues"
Changelog = "https://github.com/darosio/{{ cookiecutter.project_name }}/blob/main/CHANGELOG.md"
Discussions = "https://github.com/darosio/{{ cookiecutter.project_name }}/discussions"
Documentation = "https://{{ cookiecutter.project_slug }}.readthedocs.io"
"Github releases" = "https://github.com/darosio/{{ cookiecutter.project_name }}/releases"
Homepage = "https://github.com/darosio/{{ cookiecutter.project_name }}"
"""
        version_in_readme = '"README.md:Version"'
        message_template = '{% raw %}message_template = "{{change_type}}:{% if show_message %} {{message}}{% endif %}"{% endraw %}'
        hatch_bump = ',\n  "hatch build",\n  "export TEST_PYPI_TOKEN=$(pass show cloud/test_pypi | head -n 1) && hatch publish -r test -u __token__ -a $TEST_PYPI_TOKEN"'
    elif project_type == "Data Analysis Project":
        readme_md = ""
        project_urls = ""
        version_in_readme = '"Readme.org:Version"'
        message_template = '{% raw %}message_template = "{{change_type}}:{% if show_message %} {{message}}{% endif %}"{% endraw %}'
        hatch_bump = ""
    else:
        readme_md = ""
        project_urls = ""
        version_in_readme = ""
        message_template = ""
        hatch_bump = ""
    # Perform replacements and remove lines if they should be empty
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if "# README_MD" in line:
            if readme_md:
                new_lines.append(line.replace("# README_MD", readme_md))
        elif "# PROJECT_URLS" in line:
            if project_urls:
                new_lines.append(line.replace("# PROJECT_URLS", project_urls))
        elif "# VERSION_IN_README" in line:
            if version_in_readme:
                new_lines.append(line.replace("# VERSION_IN_README", version_in_readme))
        elif "# HATCH_BUMP" in line:
            if hatch_bump:
                new_lines.append(line.replace("  # HATCH_BUMP", hatch_bump))
        elif "# MESSAGE_TEMPLATE" in line:
            if message_template:
                new_lines.append(line.replace("# MESSAGE_TEMPLATE", message_template))
        else:
            new_lines.append(line)
    # Write the new content back to the file
    config_path.write_text("\n".join(new_lines) + "\n")


# Execute function
modify_pre_commit_config()
modify_pyproject()
