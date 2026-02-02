import hashlib
from pathlib import Path
from mapgen.render.renderer import render_omap_to_png


def test_render_matches_golden(tmp_path):
    omap_path = Path("tests/fixtures/minimal.omap")
    golden_path = Path("tests/golden/render_minimal/expected.png")
    out_path = tmp_path / "actual.png"
    
    bbox = (0, 0, 100, 100)
    size = (512, 512)
    
    render_omap_to_png(omap_path, out_path, bbox, size)
    
    actual_data = out_path.read_bytes()
    expected_data = golden_path.read_bytes()
    
    # Compare pixel-by-pixel (or just bytes if we expect exact match)
    # The requirement says "exact byte match is too fragile, compare pixel arrays exactly"
    # But since it's the same environment and same Pillow version, bytes should be stable.
    # Let's try byte match first, and if it fails due to PNG metadata, we'll use pixel comparison.
    
    # For now, let's use pixel comparison with Pillow to be safe.
    from PIL import Image
    import numpy as np
    
    actual_img = np.array(Image.open(out_path))
    expected_img = np.array(Image.open(golden_path))
    
    assert np.array_equal(actual_img, expected_img), "Rendered image does not match golden reference"
