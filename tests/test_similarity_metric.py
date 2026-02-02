import numpy as np
from PIL import Image
import pytest
from mapgen.metrics.similarity import compute_ssim
import os

def test_identical_images(tmp_path):
    img_path = tmp_path / "img.png"
    img = Image.fromarray(np.full((100, 100), 128, dtype=np.uint8))
    img.save(img_path)
    
    score = compute_ssim(str(img_path), str(img_path))
    assert score >= 0.999

def test_slightly_modified_image(tmp_path):
    ref_path = tmp_path / "ref.png"
    cand_path = tmp_path / "cand.png"
    
    ref = Image.fromarray(np.full((100, 100), 128, dtype=np.uint8))
    ref.save(ref_path)
    
    # Add a single dot
    cand_arr = np.full((100, 100), 128, dtype=np.uint8)
    cand_arr[50, 50] = 0
    cand = Image.fromarray(cand_arr)
    cand.save(cand_path)
    
    score = compute_ssim(str(ref_path), str(cand_path))
    assert score < 0.999
    assert score > 0.9

def test_shifted_image(tmp_path):
    ref_path = tmp_path / "ref.png"
    cand_path = tmp_path / "cand.png"
    
    # Create a simple pattern
    ref_arr = np.zeros((100, 100), dtype=np.uint8)
    ref_arr[40:60, 40:60] = 255
    Image.fromarray(ref_arr).save(ref_path)
    
    # Shift by 1px
    cand_arr = np.zeros((100, 100), dtype=np.uint8)
    cand_arr[41:61, 41:61] = 255
    Image.fromarray(cand_arr).save(cand_path)
    
    score = compute_ssim(str(ref_path), str(cand_path))
    # Shifting by 1px significantly reduces SSIM for sharp edges
    assert score < 0.99
    assert score > 0.5  # Still recognizes similarity

def test_different_dimensions(tmp_path):
    img1_path = tmp_path / "img1.png"
    img2_path = tmp_path / "img2.png"
    
    Image.fromarray(np.zeros((100, 100), dtype=np.uint8)).save(img1_path)
    Image.fromarray(np.zeros((50, 50), dtype=np.uint8)).save(img2_path)
    
    with pytest.raises(ValueError, match="Image dimensions do not match"):
        compute_ssim(str(img1_path), str(img2_path))
