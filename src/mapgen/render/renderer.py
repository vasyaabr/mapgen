from pathlib import Path
from typing import Tuple, List
from PIL import Image, ImageDraw
from ..omap.io import load_omap
from .style import RenderStyle


def render_omap_to_png(
    omap_path: str | Path,
    out_png_path: str | Path,
    bbox: Tuple[float, float, float, float],
    size_px: Tuple[int, int],
) -> None:
    """
    Renders a subset of .omap objects to a PNG.

    Args:
        omap_path: Path to the .omap file.
        out_png_path: Path to save the PNG.
        bbox: (xmin, ymin, xmax, ymax) in map units.
        size_px: (width, height) in pixels.
    """
    omap_doc = load_omap(omap_path)
    colors = omap_doc.get_colors()
    symbols = omap_doc.get_symbols()
    objects = omap_doc.get_objects()

    style = RenderStyle(colors, symbols)

    # Use white background as default
    img = Image.new("RGB", size_px, (255, 255, 255))
    draw = ImageDraw.Draw(img)

    xmin, ymin, xmax, ymax = bbox
    w_px, h_px = size_px
    
    # Avoid division by zero
    dx = (xmax - xmin) if xmax != xmin else 1.0
    dy = (ymax - ymin) if ymax != ymin else 1.0

    def map_to_px(x: float, y: float) -> Tuple[float, float]:
        # x increases right, y increases up (map)
        # x increases right, y increases down (image)
        px_x = (x - xmin) / dx * w_px
        px_y = (ymax - y) / dy * h_px
        return px_x, px_y

    # For determinism, we should draw objects in a fixed order.
    # OMap objects in XML are usually in draw order, or have a priority.
    # For now, let's just use the XML order.
    
    for obj in objects:
        if not obj.coords:
            continue
        
        px_coords = [map_to_px(x, y) for (x, y) in obj.coords]
        
        # Determine symbol style
        if obj.type == 2:  # Line
            color, width = style.get_line_style(obj.symbol_id)
            # Scale line width to pixels? 
            # In OMap, line_width=140 means 0.14 mm. 
            # If the map scale is 1:15000, 0.14 mm on paper is 2.1 m.
            # But the renderer is deterministic with fixed DPI.
            # Let's assume the bbox width matches W pixels.
            # pixel_size_in_map_units = dx / w_px
            # width_px = (width / 1000.0) / pixel_size_in_map_units ?
            # No, let's use a simpler approach: line_width is in map units.
            # Actually, line_width="140" is in 1/100 mm in many formats.
            # Let's just use a fixed scaling factor for now to see anything.
            
            # TODO: Scientific scaling of line widths
            draw.line(px_coords, fill=color, width=max(1, int(width / 50)))
            
        elif obj.type == 3:  # Area (polygon)
            color = style.get_fill_style(obj.symbol_id)
            if len(px_coords) >= 3:
                draw.polygon(px_coords, fill=color)
            
            # Also draw the border if it has a line symbol
            # (Note: OMap area symbols can have a border color defined)
            # For simplicity, just fill for now.

    img.save(out_png_path, "PNG")
