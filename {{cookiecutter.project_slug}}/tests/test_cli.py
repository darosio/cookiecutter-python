"""Test ``clop`` cli."""

from pathlib import Path

import pytest
from click.testing import CliRunner
from {{cookiecutter.project_slug}}.__main__ import clop

# tests path
tpath = Path(__file__).parent

# TODO: use cookiecutter names
# TODO: Fix the .github CI
def test_eq1() -> None:
    """It runs XXX pr.tecan and generates correct results and graphs."""
    runner = CliRunner()
    result = runner.invoke(clop, ["eq1", "2", "2", "2"])
    assert result.exit_code == 0
    assert "4." in result.output
