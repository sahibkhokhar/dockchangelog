# dockchangelog development

quick setup with uv.

## setup

```bash
# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# clone and setup
git clone https://github.com/sahibkhokhar/dockchangelog
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
scripts/             - helper scripts
.github/workflows/   - CI/CD pipelines
```

## publishing

see [PUBLISHING.md](PUBLISHING.md) for release workflow.

**quick version bump:**
```bash
./scripts/bump_version.sh 0.5.1
git add .
git commit -m "Release v0.5.1"
git tag v0.5.1
git push origin main --tags
```

then create github release - CI will auto-publish to pypi!
