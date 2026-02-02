import json
import numpy as np
from PIL import Image
from mapgen.cli import main
import pytest

def test_score_cli_pass(tmp_path):
    ref_path = tmp_path / "ref.png"
    cand_path = tmp_path / "cand.png"
    out_path = tmp_path / "score.json"
    
    img = Image.fromarray(np.full((100, 100), 128, dtype=np.uint8))
    img.save(ref_path)
    img.save(cand_path)
    
    exit_code = main(["score", "--ref", str(ref_path), "--cand", str(cand_path), "--out", str(out_path), "--threshold", "0.99"])
    
    assert exit_code == 0
    assert out_path.exists()
    with open(out_path) as f:
        data = json.load(f)
        assert data["score"] >= 0.99
        assert data["pass"] is True

def test_score_cli_fail(tmp_path):
    ref_path = tmp_path / "ref.png"
    cand_path = tmp_path / "cand.png"
    out_path = tmp_path / "score.json"
    
    # Different images
    Image.fromarray(np.full((100, 100), 0, dtype=np.uint8)).save(ref_path)
    Image.fromarray(np.full((100, 100), 255, dtype=np.uint8)).save(cand_path)
    
    exit_code = main(["score", "--ref", str(ref_path), "--cand", str(cand_path), "--out", str(out_path), "--threshold", "0.9"])
    
    assert exit_code == 2
    with open(out_path) as f:
        data = json.load(f)
        assert data["score"] < 0.1
        assert data["pass"] is False

def test_score_cli_missing_file(tmp_path):
    out_path = tmp_path / "score.json"
    exit_code = main(["score", "--ref", "nonexistent.png", "--cand", "nonexistent.png", "--out", str(out_path)])
    assert exit_code == 1
