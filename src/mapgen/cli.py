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

    return 0


if __name__ == "__main__":
    sys.exit(main())
