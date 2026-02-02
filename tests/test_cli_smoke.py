"""Smoke tests for the mapgen CLI."""

import subprocess
import sys


def test_cli_help() -> None:
    """Verify that 'mapgen --help' works and returns expected output."""
    result = subprocess.run(
        [sys.executable, "-m", "mapgen.cli", "--help"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.returncode == 0
    assert "usage: mapgen" in result.stdout
    assert "generate" in result.stdout  # Ensure our placeholder command is visible
