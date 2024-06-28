"""Test ``clop`` cli."""

from pathlib import Path

import pytest
from click.testing import CliRunner
from {{cookiecutter.project_slug}}.__main__ import {{ cookiecutter.cliname }}

# tests path
tpath = Path(__file__).parent


def test_version() -> None:
    """Report correct version."""
    expected_version = "0.0.1"
    runner = CliRunner()
    result = runner.invoke({{cookiecutter.cliname}}, ["--version"])
    assert result.output.startswith(expected_version)


def test_help() -> None:
    """It runs XXX ... generates correct results and graphs."""
    runner = CliRunner()
    result = runner.invoke({{cookiecutter.cliname}}, ["--help"])
    assert result.exit_code == 0
