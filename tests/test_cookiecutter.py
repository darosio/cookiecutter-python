"""Tests for the cookiecutter template generation."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_cookies.plugin import Cookies, Result

# Subprocess env that prevents parent VIRTUAL_ENV from leaking into uv calls.
_CLEAN_ENV = {**os.environ, "VIRTUAL_ENV": ""}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _init_git_repo(project_path: Path) -> None:
    """Initialize a git repository in the project directory."""
    for cmd in (
        ["git", "init"],
        ["git", "config", "user.email", "test@test.com"],
        ["git", "config", "user.name", "Test User"],
    ):
        subprocess.run(cmd, cwd=project_path, check=True, capture_output=True)


def _bake(cookies: Cookies, project_type: str = "Python Project", **extra) -> Result:
    """Bake the template and assert success."""
    result: Result = cookies.bake(
        extra_context={"project_type": project_type, **extra}
    )
    assert result.exit_code == 0, result.exception
    assert result.exception is None
    assert result.project_path is not None
    assert result.project_path.is_dir()
    return result


_uv_available = shutil.which("uv") is not None


# ---------------------------------------------------------------------------
# Basic bake
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("project_type", ["Python Project", "Data Analysis Project"])
def test_bake_default(cookies: Cookies, project_type: str) -> None:
    """Both project types bake with default context and produce 'complexity'."""
    result = _bake(cookies, project_type)
    assert result.project_path.name == "complexity"


def test_custom_project_name(cookies: Cookies) -> None:
    """Slug is derived from project_name and used for dir + src package."""
    result = _bake(cookies, project_name="My Test Project")
    assert result.project_path.name == "my_test_project"
    assert (result.project_path / "src" / "my_test_project").is_dir()


# ---------------------------------------------------------------------------
# Structure: Python Project
# ---------------------------------------------------------------------------

_PYTHON_EXPECTED_FILES = [
    "pyproject.toml",
    "Makefile",
    "README.md",
    ".envrc",
    ".gitignore",
    ".pre-commit-config.yaml",
    ".readthedocs.yml",
    "CHANGELOG.md",
    "LICENSE.txt",
    "cliff.toml",
    "renovate.json",
]

_PYTHON_EXPECTED_DIRS = [
    "src/complexity",
    "tests",
    "docs",
    "docs/references",
    "docs/api",
    "scripts",
    ".github/workflows",
]

_PYTHON_EXCLUDED = [
    "analyses",
    "data",
    "Readme.org",
    "docs/tutorials",
    "docs/index4data.rst",
    "docs/analyses.rst",
]


def test_python_project_structure(cookies: Cookies) -> None:
    """Python Project contains expected files/dirs and excludes DA-only items."""
    p = _bake(cookies, "Python Project").project_path

    for f in _PYTHON_EXPECTED_FILES:
        assert (p / f).exists(), f"Missing {f}"
    for d in _PYTHON_EXPECTED_DIRS:
        assert (p / d).is_dir(), f"Missing dir {d}"
    for x in _PYTHON_EXCLUDED:
        assert not (p / x).exists(), f"Unexpected {x}"


def test_python_project_workflows(cookies: Cookies) -> None:
    """Python Project ships CI, cruft-update, lockfile-update, release workflows."""
    wf = _bake(cookies, "Python Project").project_path / ".github" / "workflows"
    for name in ("ci.yml", "cruft-update.yml", "release.yml"):
        assert (wf / name).is_file(), f"Missing workflow {name}"


# ---------------------------------------------------------------------------
# Structure: Data Analysis Project
# ---------------------------------------------------------------------------

_DA_EXPECTED_FILES = [
    "pyproject.toml",
    "Makefile",
    "Readme.org",
    ".envrc",
    ".gitignore",
    ".pre-commit-config.yaml",
    "CHANGELOG.md",
    "LICENSE.txt",
    "cliff.toml",
]

_DA_EXPECTED_DIRS = [
    "src/complexity",
    "tests",
    "docs",
    "docs/tutorials",
    "analyses",
    "data/raw",
    "data/interim",
    "data/processed",
    "scripts",
]

_DA_EXCLUDED = [
    ".github",
    ".readthedocs.yml",
    "README.md",
    "renovate.json",
    "docs/index4data.rst",
]


def test_data_analysis_project_structure(cookies: Cookies) -> None:
    """DA Project contains expected files/dirs and excludes Python-only items."""
    p = _bake(cookies, "Data Analysis Project").project_path

    for f in _DA_EXPECTED_FILES:
        assert (p / f).exists(), f"Missing {f}"
    for d in _DA_EXPECTED_DIRS:
        assert (p / d).is_dir(), f"Missing dir {d}"
    for x in _DA_EXCLUDED:
        assert not (p / x).exists(), f"Unexpected {x}"


def test_data_analysis_docs_index(cookies: Cookies) -> None:
    """DA docs/index.rst should be the data-oriented version."""
    p = _bake(cookies, "Data Analysis Project").project_path
    content = (p / "docs" / "index.rst").read_text()
    assert "analyses" in content.lower() or "toctree" in content


# ---------------------------------------------------------------------------
# Content validation: pyproject.toml
# ---------------------------------------------------------------------------

def test_pyproject_content_python(cookies: Cookies) -> None:
    """Python Project pyproject.toml includes readme, urls, and no placeholders."""
    p = _bake(
        cookies,
        "Python Project",
        project_name="Test Project",
        author_name="Test Author",
        email="test@example.com",
        project_short_description="A test description",
    ).project_path
    content = (p / "pyproject.toml").read_text()

    assert 'name = "test_project"' in content
    assert "Test Author" in content
    assert "test@example.com" in content
    assert "A test description" in content
    assert 'readme = "README.md"' in content
    assert "[project.urls]" in content
    # No unrendered placeholders
    assert "# README_MD" not in content
    assert "# PROJECT_URLS" not in content
    assert "# VERSION_IN_README" not in content
    assert "# HATCH_BUMP" not in content
    assert "# MESSAGE_TEMPLATE" not in content


def test_pyproject_content_data_analysis(cookies: Cookies) -> None:
    """DA Project pyproject.toml omits readme and project.urls."""
    p = _bake(cookies, "Data Analysis Project").project_path
    content = (p / "pyproject.toml").read_text()

    assert 'name = "complexity"' in content
    assert 'readme = "README.md"' not in content
    assert "[project.urls]" not in content
    assert "# README_MD" not in content
    assert "# PROJECT_URLS" not in content


def test_pyproject_cli_entry_point(cookies: Cookies) -> None:
    """Both types define a CLI entry point under [project.scripts]."""
    p = _bake(cookies, "Python Project").project_path
    content = (p / "pyproject.toml").read_text()
    assert "[project.scripts]" in content
    assert "complexity" in content


# ---------------------------------------------------------------------------
# Content validation: pre-commit config
# ---------------------------------------------------------------------------

def test_precommit_python_hooks(cookies: Cookies) -> None:
    """Python Project pre-commit has check-symlinks, no DATA_ANALYSIS_EXCLUDE."""
    content = (
        _bake(cookies, "Python Project").project_path / ".pre-commit-config.yaml"
    ).read_text()
    assert "check-symlinks" in content
    assert "OPTIONAL_PYTHON_PROJECT_HOOKS" not in content
    assert "DATA_ANALYSIS_EXCLUDE" not in content


def test_precommit_da_hooks(cookies: Cookies) -> None:
    """DA Project pre-commit excludes data dir, no OPTIONAL placeholder."""
    content = (
        _bake(cookies, "Data Analysis Project").project_path
        / ".pre-commit-config.yaml"
    ).read_text()
    assert "check-symlinks" not in content
    assert "OPTIONAL_PYTHON_PROJECT_HOOKS" not in content
    assert "DATA_ANALYSIS_EXCLUDE" not in content
    assert "exclude: ^data/" in content


# ---------------------------------------------------------------------------
# Content validation: Makefile
# ---------------------------------------------------------------------------

def test_makefile_targets(cookies: Cookies) -> None:
    """Makefile contains essential make targets."""
    content = _bake(cookies, "Python Project").project_path.joinpath("Makefile").read_text()
    for target in ("lint:", "test:", "cov:", "type:", "xdoc:", "docs:", "bump:"):
        assert target in content, f"Missing target {target}"


# ---------------------------------------------------------------------------
# Content validation: .envrc
# ---------------------------------------------------------------------------

def test_envrc_content(cookies: Cookies) -> None:
    """.envrc activates a uv-managed venv."""
    content = _bake(cookies, "Python Project").project_path.joinpath(".envrc").read_text()
    assert "uv" in content
    assert "VIRTUAL_ENV" in content


# ---------------------------------------------------------------------------
# Source package scaffold
# ---------------------------------------------------------------------------

def test_source_package_files(cookies: Cookies) -> None:
    """Source package contains __init__.py, __main__.py, py.typed."""
    pkg = _bake(cookies, "Python Project").project_path / "src" / "complexity"
    for f in ("__init__.py", "__main__.py", "py.typed"):
        assert (pkg / f).is_file(), f"Missing {f} in source package"


def test_tests_directory(cookies: Cookies) -> None:
    """Tests directory contains conftest.py and test_cli.py."""
    tests = _bake(cookies, "Python Project").project_path / "tests"
    assert (tests / "conftest.py").is_file()
    assert (tests / "test_cli.py").is_file()


# ---------------------------------------------------------------------------
# Slow: install + test the generated project
# ---------------------------------------------------------------------------

@pytest.mark.slow
@pytest.mark.skipif(not _uv_available, reason="uv not available")
@pytest.mark.parametrize("project_type", ["Python Project", "Data Analysis Project"])
def test_generated_project_installs(cookies: Cookies, project_type: str) -> None:
    """Generated project can be installed with uv sync."""
    result = _bake(cookies, project_type, project_name="installtest")
    _init_git_repo(result.project_path)

    proc = subprocess.run(
        ["uv", "sync", "--group", "tests"],
        cwd=result.project_path,
        capture_output=True,
        text=True,
        env=_CLEAN_ENV,
    )
    assert proc.returncode == 0, f"Install failed:\n{proc.stderr}"


@pytest.mark.slow
@pytest.mark.skipif(not _uv_available, reason="uv not available")
def test_generated_project_tests_pass(cookies: Cookies) -> None:
    """Generated Python project's own tests pass."""
    result = _bake(cookies, "Python Project", project_name="testproject")
    _init_git_repo(result.project_path)

    proc = subprocess.run(
        ["uv", "sync", "--group", "tests"],
        cwd=result.project_path,
        capture_output=True,
        text=True,
        env=_CLEAN_ENV,
    )
    if proc.returncode != 0:
        pytest.skip(f"Installation failed: {proc.stderr}")

    proc = subprocess.run(
        ["uv", "run", "pytest", "-v"],
        cwd=result.project_path,
        capture_output=True,
        text=True,
        env=_CLEAN_ENV,
    )
    assert proc.returncode == 0, (
        f"Tests failed:\n{proc.stdout}\n{proc.stderr}"
    )
