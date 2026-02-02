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
    # Placeholder for future commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Example command placeholder to satisfy the smoke test requirement
    subparsers.add_parser("generate", help="Generate a map (placeholder)")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
