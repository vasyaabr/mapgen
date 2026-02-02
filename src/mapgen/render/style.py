from typing import Tuple, Dict
from ..omap.model import Color, Symbol


def get_color_rgb(color: Color) -> Tuple[int, int, int]:
    """Converts (0.0-1.0) RGB to (0-255) RGB tuple."""
    return (
        int(color.rgb[0] * 255),
        int(color.rgb[1] * 255),
        int(color.rgb[2] * 255)
    )


class RenderStyle:
    """Provides styling information for rendering."""

    def __init__(self, colors: Dict[int, Color], symbols: Dict[int, Symbol]):
        self.colors = colors
        self.symbols = symbols

    def get_line_style(self, symbol_id: int) -> Tuple[Tuple[int, int, int], int]:
        """Returns (color_rgb, width_px) for a line symbol."""
        symbol = self.symbols.get(symbol_id)
        if not symbol or symbol.color_id is None:
            return (0, 0, 0), 1
        
        color = self.colors.get(symbol.color_id)
        color_rgb = get_color_rgb(color) if color else (0, 0, 0)
        
        # OMap line_width is in 10^-5 m? 
        # Actually, let's assume it's in 1/1000 mm for now and adjust.
        # Mapper uses points (1/72 inch) or mm. 
        # In XML, line_width="140" often means 0.14 mm.
        line_width = symbol.line_width if symbol.line_width is not None else 100
        
        return color_rgb, line_width

    def get_fill_style(self, symbol_id: int) -> Tuple[int, int, int]:
        """Returns color_rgb for an area symbol."""
        symbol = self.symbols.get(symbol_id)
        if not symbol or symbol.fill_color_id is None:
            return (255, 255, 255)
        
        color = self.colors.get(symbol.fill_color_id)
        return get_color_rgb(color) if color else (255, 255, 255)
