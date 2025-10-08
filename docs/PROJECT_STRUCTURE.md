# Project Structure

This document provides an overview of the blocknote-py project structure and organization.

## Directory Layout

```
blocknote-py/
├── .github/                      # GitHub specific files
│   ├── workflows/                # GitHub Actions workflows
│   │   ├── ci.yml               # Continuous Integration
│   │   └── publish.yml          # PyPI publishing
│   ├── ISSUE_TEMPLATE/          # Issue templates
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md # PR template
│
├── docs/                         # Documentation
│   ├── PROJECT_STRUCTURE.md     # This file
│   └── RELEASE.md               # Release process guide
│
├── examples/                     # Usage examples
│   ├── README.md                # Examples documentation
│   └── basic_usage.py           # Basic usage examples
│
├── src/                          # Source code
│   ├── __init__.py              # Main package init
│   ├── schema/                  # Schema definitions
│   │   ├── __init__.py          # Schema exports
│   │   └── types.py             # Pydantic models (Block, InlineContent)
│   └── converter/               # Conversion functions
│       ├── __init__.py          # Converter exports
│       ├── dict_to_blocknote.py # Dict → Block conversion
│       ├── blocknote_to_dict.py # Block → Dict conversion
│       ├── md_to_blocknote.py   # Markdown → Block conversion
│       ├── blocknote_to_md.py   # Block → Markdown conversion
│       └── __tests__/           # Test files
│           ├── __init__.py
│           ├── test_dict_to_blocknote.py
│           ├── test_blocknote_to_dict.py
│           ├── test_md_to_blocknote.py
│           └── test_blocknote_to_md.py
│
├── .codecov.yml                 # Codecov configuration
├── .gitignore                   # Git ignore rules
├── .pre-commit-config.yaml      # Pre-commit hooks
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
├── Makefile                     # Development commands
├── pyproject.toml               # Project configuration
├── README.md                    # Main documentation
├── SECURITY.md                  # Security policy
└── uv.lock                      # Dependency lock file
```

## Core Modules

### Schema (`src/schema/`)

Defines the core data structures using Pydantic models:

- **`types.py`**: Contains `Block` and `InlineContent` models with validation
  - `BlockType`: Enum of supported block types
  - `InlineContentType`: Enum of inline content types
  - `Block`: Main block model with content and children
  - `InlineContent`: Inline content with text and styling

### Converter (`src/converter/`)

Provides conversion functions between different formats:

- **`dict_to_blocknote.py`**: Convert dictionaries to Block objects
  - `dict_to_blocks()`: Main conversion function
  - Validates and normalizes block dictionaries

- **`blocknote_to_dict.py`**: Convert Block objects to dictionaries
  - `blocks_to_dict()`: Main conversion function
  - Serializes blocks to JSON-compatible dicts

- **`md_to_blocknote.py`**: Parse markdown to Block objects
  - `markdown_to_blocks()`: Main parsing function
  - Uses markdown-it-py for parsing

- **`blocknote_to_md.py`**: Convert Block objects to markdown
  - `blocks_to_markdown()`: Main conversion function
  - Supports headings, lists, and text formatting

## Configuration Files

### `pyproject.toml`

Main project configuration file containing:
- Package metadata (name, version, description)
- Dependencies and dev dependencies
- Build system configuration (hatchling)
- Tool configurations (black, isort, flake8, mypy, pytest)

### `Makefile`

Development commands:
- `make test`: Run tests
- `make lint`: Run linting
- `make format`: Format code
- `make check-all`: Run all checks
- `make clean`: Clean build artifacts

### `.pre-commit-config.yaml`

Pre-commit hooks for:
- Code formatting (black, isort)
- Linting (flake8)
- Type checking (mypy)
- General checks (trailing whitespace, etc.)

## Testing

Tests are located in `src/converter/__tests__/` and use pytest:

- **Test Coverage**: Aim for >80% coverage
- **Test Structure**: One test file per module
- **Fixtures**: Reusable test data defined with `@pytest.fixture`
- **Parametrized Tests**: Using `@pytest.mark.parametrize`

Run tests:
```bash
make test                    # Run all tests
make test-cov               # Run with coverage report
pytest -k test_name         # Run specific test
```

## CI/CD

### GitHub Actions Workflows

1. **CI Workflow** (`.github/workflows/ci.yml`)
   - Runs on: push to main/develop, PRs
   - Tests on: Ubuntu, macOS, Windows
   - Python versions: 3.7, 3.8, 3.9, 3.10, 3.11, 3.12
   - Jobs: test, lint, type-check

2. **Publish Workflow** (`.github/workflows/publish.yml`)
   - Runs on: GitHub releases
   - Builds and publishes to PyPI

## Documentation

- **README.md**: Main project documentation
- **CONTRIBUTING.md**: Contribution guidelines
- **CHANGELOG.md**: Version history
- **SECURITY.md**: Security policy
- **docs/RELEASE.md**: Release process
- **examples/**: Usage examples

## Development Workflow

1. **Setup**: `make setup-dev`
2. **Make changes**: Edit code in `src/`
3. **Add tests**: Add tests in `src/converter/__tests__/`
4. **Run checks**: `make check-all`
5. **Format code**: `make fix-all`
6. **Run tests**: `make test`
7. **Commit**: Use conventional commits
8. **Push**: Create PR for review

## Package Distribution

Built using hatchling:
- Source distribution (`.tar.gz`)
- Wheel distribution (`.whl`)

Package structure maps `src/` to `blocknote/`:
```python
from blocknote.schema import Block, InlineContent
from blocknote.converter import dict_to_blocks, blocks_to_markdown
```

## Dependencies

### Runtime Dependencies
- `pydantic`: Data validation and models
- `markdown-it-py`: Markdown parsing

### Development Dependencies
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting
- `black`: Code formatting
- `isort`: Import sorting
- `flake8`: Linting
- `mypy`: Type checking
- `pre-commit`: Git hooks

## Code Style

- **Formatting**: Black (line length: 100)
- **Import sorting**: isort (black compatible)
- **Linting**: flake8 (max complexity: 10)
- **Type hints**: Required for public APIs
- **Docstrings**: Google style

## Version Control

- **Main branch**: `main` - stable releases
- **Development**: Feature branches from `main`
- **Releases**: Tagged with `vX.Y.Z`
- **Commit format**: Conventional Commits

## Future Enhancements

Potential areas for expansion:
- Additional block types (code blocks, images, etc.)
- HTML conversion
- Advanced markdown features
- Plugin system for custom converters
- Performance optimizations
