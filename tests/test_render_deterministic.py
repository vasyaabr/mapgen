import hashlib
from pathlib import Path
from mapgen.render.renderer import render_omap_to_png


def test_render_is_deterministic(tmp_path):
    omap_path = Path("tests/fixtures/minimal.omap")
    out1 = tmp_path / "out1.png"
    out2 = tmp_path / "out2.png"
    
    bbox = (0, 0, 100, 100)
    size = (512, 512)
    
    render_omap_to_png(omap_path, out1, bbox, size)
    render_omap_to_png(omap_path, out2, bbox, size)
    
    # Compare file hashes
    hash1 = hashlib.sha256(out1.read_bytes()).hexdigest()
    hash2 = hashlib.sha256(out2.read_bytes()).hexdigest()
    
    assert hash1 == hash2, "Renders of the same input should be identical"
