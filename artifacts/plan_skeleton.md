# Plan: Project Skeleton Initialization

Date: 2026-02-02
Goal: Create a clean, reproducible Python CLI project skeleton.

## Steps
1. Initialize `pyproject.toml` with `setuptools` or `hatchling`.
2. Create `src/mapgen` package.
3. Implement `cli.py` with basic `argparse` support.
4. Set up `pytest` and `tests/`.
5. Configure `ruff` for linting/formatting.
6. Configure `mypy` for static typing.

## Verification
- `pytest` passes.
- `mapgen --help` works.
- `ruff` and `mypy` pass.
