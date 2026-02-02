"""Similarity metrics for map comparisons."""

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim


def compute_ssim(ref_path: str, cand_path: str) -> float:
    """Compute Structural Similarity Index (SSIM) between two images.

    Args:
        ref_path: Path to the reference image.
        cand_path: Path to the candidate image.

    Returns:
        SSIM score in range [0, 1].

    Raises:
        FileNotFoundError: If one of the images is not found.
        ValueError: If images have different dimensions after potential resizing.
    """
    # Load images and convert to grayscale
    with Image.open(ref_path) as ref_img:
        ref_gray = np.array(ref_img.convert("L"))

    with Image.open(cand_path) as cand_img:
        cand_gray = np.array(cand_img.convert("L"))

    if ref_gray.shape != cand_gray.shape:
        # For maps, we usually expect exact matching dimensions but 
        # let's be robust if needed or raise error if that's preferred.
        # Requirement says "fixed resizing behavior if needed". 
        # For now, let's raise ValueError to ensure deterministic comparison 
        # of intended render outputs.
        raise ValueError(
            f"Image dimensions do not match: {ref_gray.shape} vs {cand_gray.shape}"
        )

    # Compute SSIM
    # data_range=255 because images are 8-bit grayscale
    score: float = ssim(ref_gray, cand_gray, data_range=255)
    return float(score)
