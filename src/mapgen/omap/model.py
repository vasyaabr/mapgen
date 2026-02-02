import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple


@dataclass
class Color:
    """Represents an OMap color."""
    priority: int
    name: str
    rgb: Tuple[float, float, float]  # 0.0 to 1.0


@dataclass
class Symbol:
    """Represents an OMap symbol."""
    id: int
    code: str
    name: str
    type: int  # 1: point, 2: line, 4: area
    line_width: Optional[int] = None  # in 1/10 mm? No, actually OMap uses weird units.
    color_id: Optional[int] = None
    fill_color_id: Optional[int] = None


@dataclass
class Object:
    """Represents an OMap map object."""
    symbol_id: int
    coords: List[Tuple[float, float]]
    type: int  # 1: point, 2: line, 3: area (in <object type="...">)


class OMapDocument:
    """
    A thin wrapper around an XML tree representing an .omap document.
    """

    def __init__(self, root: ET.Element):
        """
        Initializes the OMapDocument with an XML root element.

        Args:
            root: The root element of the .omap XML tree.
        """
        self.root = root
        self.ns = {"omap": "http://openorienteering.org/apps/mapper/xml/v2"}

    @property
    def version(self) -> Optional[str]:
        """
        Returns the version of the .omap format.
        """
        return self.root.get("version")

    def get_colors(self) -> Dict[int, Color]:
        """
        Extracts colors from the document.
        """
        colors = {}
        # Find <colors> tag
        colors_elem = self.root.find("omap:colors", self.ns)
        if colors_elem is not None:
            for color_elem in colors_elem.findall("omap:color", self.ns):
                priority = int(color_elem.get("priority", "0"))
                name = color_elem.get("name", "")
                # Get RGB from <rgb r="..." g="..." b="..."/>
                rgb_elem = color_elem.find("omap:rgb", self.ns)
                if rgb_elem is not None:
                    r = float(rgb_elem.get("r", "0"))
                    g = float(rgb_elem.get("g", "0"))
                    b = float(rgb_elem.get("b", "0"))
                    colors[priority] = Color(priority, name, (r, g, b))
        return colors

    def get_symbols(self) -> Dict[int, Symbol]:
        """
        Extracts symbols from the document.
        """
        symbols = {}
        # Find <symbols> tag
        symbols_elem = self.root.find("omap:symbols", self.ns)
        if symbols_elem is not None:
            for symbol_elem in symbols_elem.findall("omap:symbol", self.ns):
                s_id = int(symbol_elem.get("id", "0"))
                code = symbol_elem.get("code", "")
                name = symbol_elem.get("name", "")
                s_type = int(symbol_elem.get("type", "0"))
                
                symbol = Symbol(id=s_id, code=code, name=name, type=s_type)
                
                # Check for line_symbol
                line_elem = symbol_elem.find("omap:line_symbol", self.ns)
                if line_elem is not None:
                    symbol.line_width = int(line_elem.get("line_width", "0"))
                    symbol.color_id = int(line_elem.get("color", "0"))
                
                # Check for area_symbol
                area_elem = symbol_elem.find("omap:area_symbol", self.ns)
                if area_elem is not None:
                    symbol.fill_color_id = int(area_elem.get("inner_color", "0"))
                
                symbols[s_id] = symbol
        return symbols

    def get_objects(self) -> List[Object]:
        """
        Extracts objects from the document.
        """
        objects = []
        for obj_elem in self.root.findall("omap:object", self.ns):
            symbol_id = int(obj_elem.get("symbol", "-1"))
            obj_type = int(obj_elem.get("type", "0"))
            
            coords_elem = obj_elem.find("omap:coords", self.ns)
            coords = []
            if coords_elem is not None and coords_elem.text:
                # coords are like "x1 y1;x2 y2;..."
                raw_coords = coords_elem.text.strip().split(";")
                for raw_coord in raw_coords:
                    if not raw_coord.strip():
                        continue
                    parts = raw_coord.strip().split()
                    if len(parts) >= 2:
                        coords.append((float(parts[0]), float(parts[1])))
            
            objects.append(Object(symbol_id=symbol_id, coords=coords, type=obj_type))
        return objects
