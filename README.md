# mapgen

Deterministic, test-driven Python command-line tool that generates orienteering maps in .omap format.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install the package in editable mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Usage

```bash
mapgen --help
```

## Development

### Testing
Run tests using `pytest`:
```bash
pytest
```

### Linting and Formatting
Lint and format code using `ruff`:
```bash
ruff check .
ruff format .
```

### Type Checking
Run type checks using `mypy`:
```bash
mypy src
```
