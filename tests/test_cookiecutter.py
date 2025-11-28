"""Tests for the cookiecutter template generation."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_cookies.plugin import Cookies, Result


def _init_git_repo(project_path: Path) -> None:
    """Initialize a git repository in the project directory.

    Parameters
    ----------
    project_path
        Path to the project directory

    """
    subprocess.run(["git", "init"], cwd=project_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=project_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=project_path,
        check=True,
        capture_output=True,
    )


def _check_uv_available() -> bool:
    """Check if uv is available in the system PATH.

    Returns
    -------
    bool
        True if uv is available, False otherwise

    """
    return shutil.which("uv") is not None


def test_bake_project_python(cookies: Cookies) -> None:
    """Test that the Python Project template bakes successfully."""
    result: Result = cookies.bake(extra_context={"project_type": "Python Project"})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path is not None
    assert result.project_path.name == "complexity"
    assert result.project_path.is_dir()


def test_bake_project_data_analysis(cookies: Cookies) -> None:
    """Test that the Data Analysis Project template bakes successfully."""
    result: Result = cookies.bake(
        extra_context={"project_type": "Data Analysis Project"}
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path is not None
    assert result.project_path.name == "complexity"
    assert result.project_path.is_dir()


def test_python_project_structure(cookies: Cookies) -> None:
    """Test that the Python Project has the expected structure."""
    result: Result = cookies.bake(extra_context={"project_type": "Python Project"})

    assert result.exit_code == 0
    assert result.project_path is not None

    project_path = result.project_path

    # Check expected files and directories exist
    expected_files = [
        "pyproject.toml",
        "Makefile",
        "README.md",
        ".gitignore",
        ".pre-commit-config.yaml",
        ".readthedocs.yml",
        "CHANGELOG.md",
        "LICENSE.txt",
    ]
    for filename in expected_files:
        filepath = project_path / filename
        assert filepath.exists(), f"Expected file {filename} not found"

    expected_dirs = [
        "src",
        "src/complexity",
        "tests",
        "docs",
        ".github",
    ]
    for dirname in expected_dirs:
        dirpath = project_path / dirname
        assert dirpath.is_dir(), f"Expected directory {dirname} not found"

    # Check files that should NOT exist in Python Project
    excluded_files = [
        "analyses",
        "data",
        "Readme.org",
        "docs/tutorials",
    ]
    for excluded in excluded_files:
        excluded_path = project_path / excluded
        assert not excluded_path.exists(), f"Unexpected {excluded} found"


def test_data_analysis_project_structure(cookies: Cookies) -> None:
    """Test that the Data Analysis Project has the expected structure."""
    result: Result = cookies.bake(
        extra_context={"project_type": "Data Analysis Project"}
    )

    assert result.exit_code == 0
    assert result.project_path is not None

    project_path = result.project_path

    # Check expected files and directories exist
    expected_files = [
        "pyproject.toml",
        "Makefile",
        "Readme.org",
        ".gitignore",
        ".pre-commit-config.yaml",
        "CHANGELOG.md",
        "LICENSE.txt",
    ]
    for filename in expected_files:
        filepath = project_path / filename
        assert filepath.exists(), f"Expected file {filename} not found"

    expected_dirs = [
        "src",
        "src/complexity",
        "tests",
        "docs",
        "analyses",
        "data",
    ]
    for dirname in expected_dirs:
        dirpath = project_path / dirname
        assert dirpath.is_dir(), f"Expected directory {dirname} not found"

    # Check files that should NOT exist in Data Analysis Project
    excluded_files = [
        ".github",
        ".readthedocs.yml",
        "README.md",
        "renovate.json",
    ]
    for excluded in excluded_files:
        excluded_path = project_path / excluded
        assert not excluded_path.exists(), f"Unexpected {excluded} found"


def test_custom_project_name(cookies: Cookies) -> None:
    """Test template generation with custom project name."""
    result: Result = cookies.bake(
        extra_context={
            "project_type": "Python Project",
            "project_name": "My Test Project",
        }
    )

    assert result.exit_code == 0
    assert result.project_path is not None
    # project_slug is derived from project_name
    assert result.project_path.name == "my_test_project"

    # Check that the source directory uses the slug
    src_dir = result.project_path / "src" / "my_test_project"
    assert src_dir.is_dir()


def test_pyproject_toml_content(cookies: Cookies) -> None:
    """Test that pyproject.toml has correct content."""
    result: Result = cookies.bake(
        extra_context={
            "project_type": "Python Project",
            "project_name": "Test Project",
            "author_name": "Test Author",
            "email": "test@example.com",
            "project_short_description": "A test description",
        }
    )

    assert result.exit_code == 0
    assert result.project_path is not None

    pyproject_path = result.project_path / "pyproject.toml"
    content = pyproject_path.read_text()

    assert 'name = "test_project"' in content
    assert "Test Author" in content  # author name in authors list
    assert "test@example.com" in content  # email in authors list
    assert "A test description" in content


@pytest.mark.slow
def test_generated_project_installs(cookies: Cookies, tmp_path: Path) -> None:
    """Test that the generated Python project can be installed."""
    if not _check_uv_available():
        pytest.skip("uv not available for installation test")

    result: Result = cookies.bake(
        extra_context={
            "project_type": "Python Project",
            "project_name": "installtest",
        }
    )

    assert result.exit_code == 0
    assert result.project_path is not None

    # Initialize git (required for some tools)
    _init_git_repo(result.project_path)

    # Try to install the project with uv
    install_result = subprocess.run(
        ["uv", "sync", "--group", "tests"],
        cwd=result.project_path,
        capture_output=True,
        text=True,
    )

    assert install_result.returncode == 0, f"Install failed: {install_result.stderr}"


@pytest.mark.slow
def test_generated_project_tests_pass(cookies: Cookies) -> None:
    """Test that the generated Python project's tests pass."""
    if not _check_uv_available():
        pytest.skip("uv not available for test execution")

    result: Result = cookies.bake(
        extra_context={
            "project_type": "Python Project",
            "project_name": "testproject",
        }
    )

    assert result.exit_code == 0
    assert result.project_path is not None

    # Initialize git
    _init_git_repo(result.project_path)

    # Install the project
    install_result = subprocess.run(
        ["uv", "sync", "--group", "tests"],
        cwd=result.project_path,
        capture_output=True,
        text=True,
    )

    if install_result.returncode != 0:
        pytest.skip(f"Installation failed: {install_result.stderr}")

    # Run pytest on the generated project
    test_result = subprocess.run(
        ["uv", "run", "pytest", "-v"],
        cwd=result.project_path,
        capture_output=True,
        text=True,
    )

    assert test_result.returncode == 0, f"Tests failed: {test_result.stdout}\n{test_result.stderr}"
