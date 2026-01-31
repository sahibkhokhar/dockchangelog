# architecture overview

clean, simple architecture for dockchangelog.

## design principles

1. **modular** - each file has one clear responsibility
2. **simple** - easy to understand and modify
3. **well-documented** - comments explain the why, not just the what
4. **testable** - functions are small and focused

## project structure

```
dockchangelog/
├── src/
│   └── dockchangelog/
│       ├── cli.py              # command-line interface (entry point)
│       ├── checker.py          # docker compose parsing and checking
│       ├── config.py           # configuration loading and validation
│       ├── formatter.py        # terminal output formatting (Rich)
│       ├── github_client.py    # github api client with caching
│       ├── mapper.py           # map docker images to github repos
│       └── parser.py           # parse and categorize release notes
├── tests/
├── pyproject.toml
└── readme.md
```

## data flow

```
1. User runs command
   ↓
2. CLI (cli.py) parses arguments
   ↓
3. Config (config.py) loads settings
   ↓
4. Checker (checker.py) finds compose files
   ↓
5. Checker parses services from compose files
   ↓
6. Mapper (mapper.py) maps images to github repos
   ↓
7. GitHub Client (github_client.py) fetches releases
   ↓
8. Parser (parser.py) extracts features/fixes/etc
   ↓
9. Formatter (formatter.py) displays results
```

## component details

### cli.py

**purpose**: command-line interface using Typer

**key functions**:
- `check()` - main command, orchestrates everything
- `init()` - create example config
- `version()` - show version

**responsibilities**:
- parse command arguments
- coordinate between components
- handle errors gracefully

### checker.py

**purpose**: interact with docker and compose files

**key classes**:
- `DockerImage` - parses image strings (registry/name:tag)
- `ComposeService` - represents a service from compose file
- `DockerChecker` - finds and parses compose files

**responsibilities**:
- find all compose files in directory
- parse YAML to extract services
- extract image names and labels

### config.py

**purpose**: configuration management with Pydantic

**key classes**:
- `Config` - main configuration model
- `CacheConfig` - cache settings
- `OutputConfig` - output format settings
- `UpdateConfig` - update mode settings (future)

**responsibilities**:
- load config from YAML file
- validate configuration
- provide sensible defaults
- handle environment variables

### formatter.py

**purpose**: beautiful terminal output using Rich

**key class**:
- `OutputFormatter` - formats all terminal output

**responsibilities**:
- display headers and summaries
- format service update information
- color-code different types of information
- show parsed release notes

### github_client.py

**purpose**: interact with github api

**key classes**:
- `Release` - represents a github release
- `GitHubClient` - api client with caching

**responsibilities**:
- fetch latest releases from github
- handle authentication (optional token)
- cache responses to disk
- respect rate limits

### mapper.py

**purpose**: map docker images to github repositories

**key class**:
- `ImageMapper` - mapping logic

**strategies** (in order):
1. explicit config mappings
2. docker labels (org.opencontainers.image.source)
3. common known mappings
4. heuristics (ghcr.io/owner/repo → owner/repo)

**responsibilities**:
- determine github repo for each image
- handle various image formats
- provide database of known mappings

### parser.py

**purpose**: parse release notes into structured format

**key classes**:
- `ParsedNotes` - structured release notes
- `ReleaseNotesParser` - parsing logic

**strategies**:
1. structured parsing (look for headings)
2. heuristic parsing (categorize by keywords)

**categories**:
- features (✨)
- fixes (🐛)
- breaking changes (⚠️)
- security (🔒)
- dependencies (📦)
- other

## adding new features

### adding a new cli command

edit `cli.py`:

```python
@app.command()
def mycommand(
    option: str = typer.Option(..., "--option", help="description")
):
    """command description"""
    # implementation
```

### adding new image mappings

edit `mapper.py`:

```python
def _load_common_mappings(self) -> dict[str, str]:
    return {
        "image/name": "owner/repo",
        # add new mapping here
    }
```

### improving release note parsing

edit `parser.py`:

- add new categories to `ParsedNotes`
- update `_detect_section_heading()` for new keywords
- update `_categorize_item()` for heuristic matching

### customizing output format

edit `formatter.py`:

- update `show_service_update()` for different layout
- update `_show_release_notes()` for different formatting
- use Rich components (Panel, Table, etc)

## testing

```bash
# run all tests
pytest

# run specific test file
pytest tests/test_basic.py

# run with coverage
pytest --cov=dockchangelog

# run specific test
pytest tests/test_basic.py::TestDockerImage::test_simple_image
```

## dependencies

**production**:
- `typer` - cli framework (type-safe, auto-help)
- `rich` - beautiful terminal output
- `httpx` - modern http client
- `pydantic` - data validation
- `pyyaml` - yaml parsing

**development**:
- `pytest` - testing framework
- `black` - code formatting
- `ruff` - linting

## code style

- use **black** for formatting (100 char lines)
- use **ruff** for linting
- use type hints everywhere
- write docstrings for public functions
- keep functions small and focused
- prefer composition over inheritance

## error handling

- catch specific exceptions, not bare `except:`
- log errors clearly
- fail gracefully (don't crash on one bad service)
- provide helpful error messages

## performance

- cache github api responses (24 hour TTL)
- use async where it helps (future improvement)
- minimize docker calls
- keep in memory what makes sense

## security

- no secrets in code
- use environment variables for tokens
- don't execute arbitrary commands
- validate all inputs
- read-only by default (updates are explicit opt-in)

## future improvements

potential areas for enhancement:

1. **async io** - parallel github api calls
2. **more sources** - gitlab, codeberg, etc
3. **web ui** - simple dashboard
4. **notifications** - discord, email, etc
5. **better caching** - smarter invalidation
6. **plugin system** - custom parsers/formatters

keep it simple - only add complexity when needed.
