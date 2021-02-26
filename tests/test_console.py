# tests/test_console.py
import click.testing
import pytest

from hypermodern_python_series import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


def test_main_succeeds(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0