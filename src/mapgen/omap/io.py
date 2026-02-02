import xml.etree.ElementTree as ET
from pathlib import Path
from .model import OMapDocument

# OpenOrienteering Mapper XML namespace
OMAP_NAMESPACE = "http://openorienteering.org/apps/mapper/xml/v2"


def load_omap(path: str | Path) -> OMapDocument:
    """
    Loads an .omap file into an OMapDocument.

    Args:
        path: Path to the .omap file.

    Returns:
        An OMapDocument instance.
    """
    tree = ET.parse(path)
    return OMapDocument(tree.getroot())


def save_omap(doc: OMapDocument, path: str | Path) -> None:
    """
    Writes an OMapDocument to disk.

    Args:
        doc: The OMapDocument instance.
        path: Path where to save the .omap file.
    """
    ET.register_namespace("", OMAP_NAMESPACE)
    tree = ET.ElementTree(doc.root)

    # Note: xml.etree.ElementTree.write doesn't support attribute sorting natively in all versions
    # but we can try to achieve some level of determinism.
    # We will use indent for better readability and structure preservation.
    ET.indent(tree, space=" ", level=0)

    with open(path, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)
