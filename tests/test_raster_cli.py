"""Smoke tests for the raster CLI commands."""

import subprocess
import sys


def test_raster_help():
    """Verify 'mapgen raster --help' works."""
    result = subprocess.run(
        [sys.executable, "-m", "mapgen.cli", "raster", "--help"],
        capture_output=True,
        text=True,
        check=True
    )
    assert "Available raster commands" in result.stdout
    assert "process" in result.stdout
    assert "denoise" in result.stdout
    assert "binarize" in result.stdout
    assert "morphology" in result.stdout


def test_raster_process_smoke():
    """Verify 'mapgen raster process' executes (even if stubbed)."""
    result = subprocess.run(
        [sys.executable, "-m", "mapgen.cli", "raster", "process", "--aoi", "test_aoi"],
        capture_output=True,
        text=True,
        check=True
    )
    assert "Processing raster for AOI: test_aoi" in result.stdout
    assert "Status: SUCCESS" in result.stdout


def test_raster_denoise_smoke():
    """Verify 'mapgen raster denoise' executes."""
    result = subprocess.run(
        [sys.executable, "-m", "mapgen.cli", "raster", "denoise", "--aoi", "test_aoi"],
        capture_output=True,
        text=True,
        check=True
    )
    assert "Denoising (denoise=True)" in result.stdout


def test_raster_binarize_smoke():
    """Verify 'mapgen raster binarize' executes."""
    result = subprocess.run(
        [sys.executable, "-m", "mapgen.cli", "raster", "binarize", "--aoi", "test_aoi", "--thresholds", "0.4,0.6"],
        capture_output=True,
        text=True,
        check=True
    )
    assert "Binarizing (thresholds=[0.4, 0.6])" in result.stdout


def test_raster_morphology_smoke():
    """Verify 'mapgen raster morphology' executes."""
    result = subprocess.run(
        [sys.executable, "-m", "mapgen.cli", "raster", "morphology", "--aoi", "test_aoi", "--iterations", "5"],
        capture_output=True,
        text=True,
        check=True
    )
    assert "Morphology (iterations=5)" in result.stdout
