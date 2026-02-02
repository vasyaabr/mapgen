import subprocess
import sys
from pathlib import Path

FIXTURE_PATH = Path("tests/fixtures/complex.omap")


def test_cli_roundtrip(tmp_path: Path):
    """
    Tests the `mapgen omap roundtrip` CLI command.
    """
    output_path = tmp_path / "cli_roundtrip.omap"
    
    # Run the command
    result = subprocess.run(
        [sys.executable, "-m", "mapgen.cli", "omap", "roundtrip", "--in", str(FIXTURE_PATH), "--out", str(output_path)],
        capture_output=True,
        text=True,
        check=True
    )
    
    assert result.returncode == 0
    assert "Round-tripped OMap" in result.stdout
    assert output_path.exists()
    
    # Verify the output is valid XML
    import xml.etree.ElementTree as ET
    ET.parse(output_path)
