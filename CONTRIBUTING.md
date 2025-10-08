# Contributing to blocknote-py

Thank you for your interest in contributing to blocknote-py! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to foster an inclusive and welcoming community.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/blocknote-py.git
   cd blocknote-py
   ```

3. Install dependencies:
   ```bash
   uv sync --dev
   ```

4. Install pre-commit hooks (optional but recommended):
   ```bash
   uv run pre-commit install
   ```

## Development Workflow

### Running Tests

Run the full test suite:
```bash
PYTHONPATH=src uv run python -m pytest -v
```

Run specific tests:
```bash
PYTHONPATH=src uv run python -m pytest src/converter/__tests__/test_dict_to_blocknote.py -v
```

Run with coverage:
```bash
PYTHONPATH=src uv run python -m pytest --cov=src --cov-report=html
```

### Code Quality

We use several tools to maintain code quality:

#### Format Code
```bash
uv run black src
uv run isort src
```

#### Lint Code
```bash
uv run flake8 src
```

#### Type Check
```bash
uv run mypy src
```

#### Run All Checks
```bash
# Check everything
uv run flake8 src && uv run black --check src && uv run isort --check-only src && uv run mypy src

# Auto-fix formatting
uv run black src && uv run isort src
```

### Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following our coding standards:
   - Write clear, descriptive commit messages
   - Add tests for new functionality
   - Update documentation as needed
   - Follow PEP 8 style guidelines
   - Use type hints where appropriate

3. Ensure all tests pass and code quality checks succeed

4. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

### Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add support for code blocks
fix: resolve markdown parsing issue with nested lists
docs: update API reference for blocks_to_dict
test: add tests for table block conversion
```

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the CHANGELOG.md following the Keep a Changelog format
3. Ensure all tests pass and code quality checks succeed
4. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Open a Pull Request against the `main` branch
6. Fill out the PR template with:
   - Description of changes
   - Related issue numbers (if applicable)
   - Type of change (bugfix, feature, etc.)
   - Checklist confirmation

7. Wait for review and address any feedback

## Project Structure

```
blocknote-py/
├── src/
│   ├── __init__.py              # Main package init
│   ├── schema/
│   │   ├── __init__.py          # Schema exports
│   │   └── types.py             # Pydantic models
│   └── converter/
│       ├── __init__.py          # Converter exports
│       ├── dict_to_blocknote.py # Dict → Block conversion
│       ├── blocknote_to_dict.py # Block → Dict conversion
│       ├── md_to_blocknote.py   # Markdown → Block conversion
│       ├── blocknote_to_md.py   # Block → Markdown conversion
│       └── __tests__/           # Test files
├── pyproject.toml               # Project configuration
├── README.md                    # Main documentation
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # This file
└── LICENSE                      # MIT License
```

## Adding New Features

### Adding a New Block Type

1. Update `BlockType` enum in `src/schema/types.py`
2. Update the `Block` model validation if needed
3. Add conversion logic in relevant converter files
4. Add tests for the new block type
5. Update documentation

### Adding a New Converter

1. Create a new file in `src/converter/`
2. Implement the conversion function
3. Export it in `src/converter/__init__.py`
4. Add comprehensive tests in `src/converter/__tests__/`
5. Update README.md with usage examples

## Testing Guidelines

- Write tests for all new functionality
- Aim for high test coverage (>80%)
- Use descriptive test names
- Include both positive and negative test cases
- Test edge cases and error conditions
- Use pytest fixtures for reusable test data

Example test structure:
```python
import pytest
from blocknote.converter import your_function

@pytest.fixture
def sample_data():
    """Fixture providing sample data for testing."""
    return {...}

def test_your_function_basic(sample_data):
    """Test basic functionality."""
    result = your_function(sample_data)
    assert result == expected

def test_your_function_edge_case():
    """Test edge case handling."""
    with pytest.raises(ValueError):
        your_function(invalid_input)
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions and classes
- Include type hints in function signatures
- Provide usage examples for new features
- Update CHANGELOG.md for all changes

## Questions or Need Help?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Check existing issues and PRs before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
