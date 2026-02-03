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

    # Score command
    score_parser = subparsers.add_parser("score", help="Compute similarity score between images")
    score_parser.add_argument("--ref", required=True, help="Reference PNG image")
    score_parser.add_argument("--cand", required=True, help="Candidate PNG image")
    score_parser.add_argument("--metric", default="ssim", choices=["ssim"], help="Similarity metric")
    score_parser.add_argument("--out", required=True, help="Output JSON score file")
    score_parser.add_argument("--threshold", type=float, help="Similarity threshold")

    # Acceptance commands
    acceptance_parser = subparsers.add_parser("acceptance", help="Run acceptance tests")
    acceptance_subparsers = acceptance_parser.add_subparsers(dest="acceptance_command", help="Available acceptance commands")

    run_parser = acceptance_subparsers.add_parser("run", help="Run acceptance for a single AOI")
    run_parser.add_argument("--aoi", required=True, help="AOI name (folder name in tests/golden)")
    run_parser.add_argument("--artifacts", default="artifacts/acceptance", help="Directory for artifacts")

    run_all_parser = acceptance_subparsers.add_parser("run-all", help="Run acceptance for all AOIs")
    run_all_parser.add_argument("--golden-dir", default="tests/golden", help="Directory containing golden AOIs")
    run_all_parser.add_argument("--artifacts", default="artifacts/acceptance", help="Directory for artifacts")

    # Raster commands
    from mapgen.raster import register_raster_commands
    register_raster_commands(subparsers)

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

    elif args.command == "score":
        import json
        from mapgen.metrics.similarity import compute_ssim
        
        try:
            if args.metric == "ssim":
                score = compute_ssim(args.ref, args.cand)
            else:
                print(f"Error: Unknown metric {args.metric}")
                return 1
            
            result = {
                "metric": args.metric,
                "score": score,
                "reference": args.ref,
                "candidate": args.cand,
            }
            
            if args.threshold is not None:
                result["threshold"] = args.threshold
                result["pass"] = score >= args.threshold
            
            with open(args.out, "w") as f:
                json.dump(result, f, indent=2)
            
            print(f"Score ({args.metric}): {score:.6f}")
            
            if args.threshold is not None:
                if score >= args.threshold:
                    print("Status: PASS")
                    return 0
                else:
                    print(f"Status: FAIL (threshold: {args.threshold})")
                    return 2
            
            return 0
        except FileNotFoundError as e:
            print(f"Error: File not found: {e}")
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 1

    elif args.command == "acceptance":
        from pathlib import Path
        from mapgen.acceptance.run import run_aoi, run_all
        
        golden_root = Path("tests/golden")
        artifacts_root = Path(args.artifacts)
        
        if args.acceptance_command == "run":
            aoi_dir = golden_root / args.aoi
            if not aoi_dir.exists():
                print(f"Error: AOI directory {aoi_dir} does not exist.")
                return 1
            
            result = run_aoi(aoi_dir, artifacts_root / args.aoi)
            return 0 if result["pass"] else 2
            
        elif args.acceptance_command == "run-all":
            results = run_all(Path(args.golden_dir), artifacts_root)
            all_passed = all(r["pass"] for r in results)
            return 0 if all_passed else 2
        else:
            acceptance_parser.print_help()
            return 0

    elif args.command == "raster":
        from mapgen.raster import handle_raster_command
        return handle_raster_command(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
