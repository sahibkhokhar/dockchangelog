# dockchangelog development

quick setup with uv.

## setup

```bash
# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# clone and setup
git clone https://github.com/yourusername/dockchangelog
cd dockchangelog

# create venv and install
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# or just use uv directly
uv run pytest
uv run dockchangelog check
```

## commands

```bash
# run tests
uv run pytest

# format code
uv run black src/

# lint
uv run ruff check src/

# run tool
uv run dockchangelog check
```

## structure

```
src/dockchangelog/   - main package
tests/               - test suite
example/             - example compose files
```

see [ARCHITECTURE.md](ARCHITECTURE.md) for more details.
