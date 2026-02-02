import xml.etree.ElementTree as ET
from typing import Optional


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

    @property
    def version(self) -> Optional[str]:
        """
        Returns the version of the .omap format.
        """
        return self.root.get("version")
