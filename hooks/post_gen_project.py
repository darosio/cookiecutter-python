"""Post generation hook."""

import shutil
from pathlib import Path

shutil.move("project.toml", "pyproject.toml")

project_type = "{{ cookiecutter.project_type }}"
if project_type == "Data Analysis Project":
    shutil.move("docs/index4data.rst", "docs/index.rst")
    notebook = Path("docs/{{ cookiecutter.date }}.ipynb")
    notebook.symlink_to("../analyses/{{ cookiecutter.date }}.ipynb")


remove_paths = [
    '{% if cookiecutter.project_type != "Python Project" %}.github{% endif %}',
    '{% if cookiecutter.project_type != "Python Project" %}.readthedocs.yml{% endif %}',
    '{% if cookiecutter.project_type != "Python Project" %}README.md{% endif %}',
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
        commitizen_hook = "- id: commitizen-branch\n        stages: [push]"
        analysis_exclude = ""
    elif project_type == "Data Analysis Project":
        python_hooks = ""
        commitizen_hook = ""
        analysis_exclude = "exclude: ^data/.*\n"
    else:
        python_hooks = ""
        commitizen_hook = ""
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
        elif "# OPTIONAL_COMMITIZEN_BRANCH" in line:
            if commitizen_hook:
                new_lines.append(
                    line.replace("# OPTIONAL_COMMITIZEN_BRANCH", commitizen_hook)
                )
        elif "# DATA_ANALYSIS_EXCLUDE" in line:
            if analysis_exclude:
                new_lines.append(
                    line.replace("# DATA_ANALYSIS_EXCLUDE", analysis_exclude)
                )
        else:
            new_lines.append(line)
    # Write the new content back to the file
    config_path.write_text("\n".join(new_lines) + "\n")


# Execute function
modify_pre_commit_config()
