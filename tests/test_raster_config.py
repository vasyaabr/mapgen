"""Tests for raster processing configuration."""

import pytest
from mapgen.raster.config import RasterConfig


def test_raster_config_defaults():
    """Verify default values for RasterConfig."""
    config = RasterConfig()
    assert config.denoise is True
    assert config.thresholds == [0.5]
    assert config.morphology_iterations == 2
    assert config.margin_px == 100


def test_raster_config_custom():
    """Verify custom values for RasterConfig."""
    config = RasterConfig(
        denoise=False,
        thresholds=[0.3, 0.7],
        morphology_iterations=5,
        margin_px=200
    )
    assert config.denoise is False
    assert config.thresholds == [0.3, 0.7]
    assert config.morphology_iterations == 5
    assert config.margin_px == 200


def test_raster_config_validation():
    """Verify validation for RasterConfig (optional, based on pydantic)."""
    with pytest.raises(ValueError):
        # thresholds should be a list
        RasterConfig(thresholds="not a list") # type: ignore
