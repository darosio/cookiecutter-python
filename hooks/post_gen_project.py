"""Post generation hook."""
import shutil
from pathlib import Path

remove_paths = [
    '{% if cookiecutter.project_type != "Python Project" %}.github{% endif %}',
    '{% if cookiecutter.project_type != "Python Project" %}docs{% endif %}',
    '{% if cookiecutter.project_type != "Python Project" %}cz_customize_info.txt{% endif %}',
    '{% if cookiecutter.project_type != "Python Project" %}.readthedocs.yml{% endif %}',
    '{% if cookiecutter.project_type != "Python Project" %}.python-version{% endif %}',
    '{% if cookiecutter.project_type != "Python Project" %}CHANGELOG.md{% endif %}',
    '{% if cookiecutter.project_type != "Python Project" %}README.md{% endif %}',
    '{% if cookiecutter.project_type != "Data Analysis Project" %}Readme.org{% endif %}',
    '{% if cookiecutter.project_type != "Data Analysis Project" %}analyses{% endif %}',
    '{% if cookiecutter.project_type != "Data Analysis Project" %}data{% endif %}',
    '{% if cookiecutter.project_type != "Data Analysis Project" %}.envrc{% endif %}',
]

for path_str in remove_paths:
    path = Path(path_str) if path_str else None
    if path and path.exists():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
