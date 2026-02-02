"""Core logic for running end-to-end acceptance tests."""

import json
import os
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
from PIL import Image, ImageChops

from mapgen.render.renderer import render_omap_to_png
from mapgen.metrics.similarity import compute_ssim


def run_aoi(aoi_dir: Path, output_dir: Path) -> Dict[str, Any]:
    """Run acceptance test for a single AOI.

    Args:
        aoi_dir: Directory containing AOI golden files.
        output_dir: Directory to save artifacts.

    Returns:
        Result dictionary.
    """
    ref_omap = aoi_dir / "ref.omap"
    ref_png = aoi_dir / "ref.png"
    config_path = aoi_dir / "render_config.json"
    threshold_path = aoi_dir / "threshold.txt"

    if not config_path.exists():
        raise FileNotFoundError(f"Missing render_config.json in {aoi_dir}")

    with open(config_path, "r") as f:
        config = json.load(f)

    threshold = 1.0
    if threshold_path.exists():
        with open(threshold_path, "r") as f:
            threshold = float(f.read().strip())

    output_dir.mkdir(parents=True, exist_ok=True)
    candidate_png = output_dir / "candidate.png"
    result_json = output_dir / "result.json"
    diff_png = output_dir / "diff.png"

    # Render candidate
    bbox = tuple(config["bbox"])
    size = tuple(config["size"])
    render_omap_to_png(ref_omap, candidate_png, bbox, size)

    # Score
    score = compute_ssim(str(ref_png), str(candidate_png))
    passed = score >= threshold

    # Generate diff
    with Image.open(ref_png) as ref_img, Image.open(candidate_png) as cand_img:
        diff = ImageChops.difference(ref_img.convert("RGB"), cand_img.convert("RGB"))
        diff.save(diff_png)

    result = {
        "aoi": aoi_dir.name,
        "score": score,
        "threshold": threshold,
        "pass": passed,
        "artifacts": {
            "candidate": str(candidate_png),
            "diff": str(diff_png),
        }
    }

    with open(result_json, "w") as f:
        json.dump(result, f, indent=2)

    return result


def run_all(golden_dir: Path, artifacts_dir: Path) -> List[Dict[str, Any]]:
    """Run acceptance tests for all AOIs in the golden directory.

    Args:
        golden_dir: Directory containing AOI subdirectories.
        artifacts_dir: Directory to save artifacts.

    Returns:
        List of result dictionaries.
    """
    results = []
    for entry in golden_dir.iterdir():
        if entry.is_dir() and (entry / "render_config.json").exists():
            print(f"Running AOI: {entry.name}...")
            result = run_aoi(entry, artifacts_dir / entry.name)
            results.append(result)
            status = "PASS" if result["pass"] else "FAIL"
            print(f"  Score: {result['score']:.6f} (threshold: {result['threshold']:.6f}) -> {status}")
    
    return results
