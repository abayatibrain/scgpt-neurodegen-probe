"""Smoke test: import + version + CLI invocation."""
from __future__ import annotations

from typer.testing import CliRunner


def test_import_and_version() -> None:
    import scgpt_neurodegen_probe

    assert scgpt_neurodegen_probe.__version__ == "0.1.0"


def test_cli_version() -> None:
    from scgpt_neurodegen_probe.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "scgpt-neurodegen-probe" in result.stdout.lower() or "0.1.0" in result.stdout
