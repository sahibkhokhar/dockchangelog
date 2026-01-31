# contributing to dockchangelog

thanks for your interest in contributing!

## philosophy

dockchangelog is a simple, focused tool with these principles:

- **safe by default** - checking is read-only, updates require explicit flags
- **clean and simple** - easy to understand code, clear purpose
- **helpful output** - beautiful, informative terminal UI
- **minimal dependencies** - only what's necessary

## development setup

```bash
# clone the repo
git clone https://github.com/yourusername/dockchangelog
cd dockchangelog

# install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on windows
uv pip install -e ".[dev]"
```

## code style

- use black for formatting: `black dockchangelog/`
- use ruff for linting: `ruff check dockchangelog/`
- write docstrings for public functions
- keep functions focused and simple
- add comments for non-obvious logic

## testing

```bash
# run tests
pytest

# run with coverage
pytest --cov=dockchangelog
```

## submitting changes

1. fork the repository
2. create a feature branch: `git checkout -b feature-name`
3. make your changes
4. test your changes
5. commit with clear message: `git commit -m "add feature: description"`
6. push to your fork: `git push origin feature-name`
7. open a pull request

## what to contribute

**welcome contributions:**
- bug fixes
- improved release note parsing
- additional image mappings
- documentation improvements
- test coverage

**discuss first:**
- new commands or features
- major architectural changes
- new dependencies

## adding image mappings

if you know the github repo for a popular docker image, add it to `mapper.py`:

```python
self.common_mappings = {
    "image/name": "owner/repo",
    # add your mapping here
}
```

## questions?

open an issue or discussion on github!
