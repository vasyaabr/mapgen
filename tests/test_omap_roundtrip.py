import os
from pathlib import Path
import xml.etree.ElementTree as ET
from mapgen.omap import load_omap, save_omap

FIXTURE_PATH = Path("tests/fixtures/complex.omap")


def test_omap_roundtrip(tmp_path: Path):
    """
    Tests that an .omap file can be loaded and saved back, maintaining basic structure.
    """
    output_path = tmp_path / "roundtrip.omap"
    
    # 1. Load
    doc = load_omap(FIXTURE_PATH)
    assert doc.root.tag == "{http://openorienteering.org/apps/mapper/xml/v2}map"
    
    # 2. Save
    save_omap(doc, output_path)
    assert output_path.exists()
    
    # 3. Load again and compare
    doc2 = load_omap(output_path)
    assert doc2.root.tag == doc.root.tag
    assert doc2.version == doc.version
    
    # Compare symbol counts
    symbols1 = doc.root.findall(".//{http://openorienteering.org/apps/mapper/xml/v2}symbol")
    symbols2 = doc2.root.findall(".//{http://openorienteering.org/apps/mapper/xml/v2}symbol")
    assert len(symbols1) == len(symbols2)


def test_xml_canonical_equivalence(tmp_path: Path):
    """
    Verifies that the round-trip produces semantically equivalent XML.
    """
    output_path = tmp_path / "roundtrip_canonical.omap"
    doc = load_omap(FIXTURE_PATH)
    save_omap(doc, output_path)
    
    # Load both and compare using ET.tostring with canonicalization if possible, 
    # but here we just check if they parse and have same structure.
    tree1 = ET.parse(FIXTURE_PATH)
    tree2 = ET.parse(output_path)
    
    def elements_equal(e1, e2):
        if e1.tag != e2.tag: return False
        if (e1.text or '').strip() != (e2.text or '').strip(): return False
        if (e1.tail or '').strip() != (e2.tail or '').strip(): return False
        if e1.attrib != e2.attrib: return False
        if len(e1) != len(e2): return False
        return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))

    assert elements_equal(tree1.getroot(), tree2.getroot())
