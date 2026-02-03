"""Configuration models for raster processing."""

from pydantic import BaseModel, Field


class RasterConfig(BaseModel):
    """Configuration for raster processing stage.
    
    Attributes:
        denoise: Whether to apply a denoising filter.
        thresholds: List of intensity thresholds for binarization.
        morphology_iterations: Number of salt/pepper removal iterations.
        margin_px: Margin in pixels around the AOI to include in processing.
    """
    denoise: bool = Field(default=True, description="Apply denoising filter")
    thresholds: list[float] = Field(
        default_factory=lambda: [0.5],
        description="Intensity thresholds for binarization"
    )
    morphology_iterations: int = Field(
        default=2,
        description="Iterations for morphological operations"
    )
    margin_px: int = Field(
        default=100,
        description="Margin in pixels around the AOI"
    )
