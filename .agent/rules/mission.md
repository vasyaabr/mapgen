---
trigger: always_on
---

# Project Mission

Build a deterministic, test-driven Python command-line tool that generates an orienteering map in the .omap format (compatible with OpenOrienteering Mapper) from three data sources: georeferenced raster maps, OpenStreetMap data, and Google aerial imagery (downloaded via an approved provider and used only within licensing constraints).

The tool must be structured as a set of independently runnable pipeline steps (each exposed as its own CLI command) so that every new capability can be executed, tested, and verified in isolation. Each step must produce explicit, reproducible artifacts in a workspace (cached inputs, intermediate products, and the final .omap) and must be covered by automated unit and integration tests.

The definition of “success” is quantitative: for each test area (AOI), the generated .omap must be rendered to a PNG using a deterministic renderer and scored against an agreed golden reference image using an image-similarity metric. Progress is demonstrated by stable or improving similarity scores, while regressions are prevented by CI gates and per-AOI thresholds.

Above all, optimize for correctness, reproducibility, and verifiable incremental progress: every change should clearly improve the pipeline, maintain deterministic outputs, respect data licensing/compliance, and keep all tests and similarity gates passing.