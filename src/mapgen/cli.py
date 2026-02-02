"""CLI interface for mapgen."""

import argparse
import sys
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point for the mapgen CLI.

    Args:
        argv: Command line arguments.

    Returns:
        Exit code.
    """
    parser = argparse.ArgumentParser(
        prog="mapgen",
        description="Deterministic orienteering map generator.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # OMap commands
    omap_parser = subparsers.add_parser("omap", help="OMap file operations")
    omap_subparsers = omap_parser.add_subparsers(dest="omap_command", help="Available OMap commands")

    roundtrip_parser = omap_subparsers.add_parser("roundtrip", help="Round-trip an OMap file")
    roundtrip_parser.add_argument("--in", dest="input_file", required=True, help="Input OMap file")
    roundtrip_parser.add_argument("--out", dest="output_file", required=True, help="Output OMap file")

    # Render command
    render_parser = subparsers.add_parser("render", help="Render OMap to PNG")
    render_parser.add_argument("--in", dest="input_file", required=True, help="Input OMap file")
    render_parser.add_argument("--out", dest="output_file", required=True, help="Output PNG file")
    render_parser.add_argument("--bbox", required=True, help="Bounding box as xmin,ymin,xmax,ymax")
    render_parser.add_argument("--size", required=True, help="Output size as width,height")

    # Placeholder for future commands
    subparsers.add_parser("generate", help="Generate a map (placeholder)")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "omap":
        if args.omap_command == "roundtrip":
            from mapgen.omap import load_omap, save_omap
            doc = load_omap(args.input_file)
            save_omap(doc, args.output_file)
            
            # Print summary
            symbol_count = len(doc.root.findall(".//{http://openorienteering.org/apps/mapper/xml/v2}symbol"))
            print(f"Round-tripped OMap: {args.input_file} -> {args.output_file}")
            print(f"Version: {doc.version}")
            print(f"Symbols found: {symbol_count}")
            return 0
        else:
            omap_parser.print_help()
            return 0
    elif args.command == "render":
        from mapgen.render.renderer import render_omap_to_png
        try:
            bbox_parts = args.bbox.split(",")
            if len(bbox_parts) != 4:
                raise ValueError("bbox must have 4 components")
            bbox = tuple(map(float, bbox_parts))
            
            size_parts = args.size.split(",")
            if len(size_parts) != 2:
                raise ValueError("size must have 2 components")
            size = tuple(map(int, size_parts))
        except ValueError as e:
            print(f"Error: Invalid bbox or size format: {e}")
            return 1
            
        render_omap_to_png(args.input_file, args.output_file, (bbox[0], bbox[1], bbox[2], bbox[3]), (size[0], size[1]))
        print(f"Rendered {args.input_file} to {args.output_file}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
