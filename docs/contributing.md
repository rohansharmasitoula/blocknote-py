# Contributing to BlockNote-py

We welcome contributions to BlockNote-py! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Git

### Setting up the Development Environment

1. **Fork and clone the repository:**

```bash
git clone https://github.com/yourusername/blocknote-py.git
cd blocknote-py
```

2. **Install dependencies:**

```bash
# Using uv (recommended)
uv sync --dev

# Or using pip
pip install -e ".[dev,test]"
```

3. **Install pre-commit hooks:**

```bash
pre-commit install
```

4. **Verify the setup:**

```bash
# Run tests
make test

# Run linting
make lint

# Check types
make type-check
```

## Development Workflow

### Making Changes

1. **Create a new branch:**

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes:**
   - Write code following the existing style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests and checks:**

```bash
# Run all tests
make test

# Run specific test file
uv run pytest src/converter/__tests__/test_your_feature.py -v

# Check code formatting
make check-all

# Fix formatting issues
make fix-all
```

4. **Commit your changes:**

```bash
git add .
git commit -m "feat: add your feature description"
```

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `chore:` - Maintenance tasks

Examples:
```
feat: add HTML to BlockNote converter
fix: handle empty blocks in markdown converter
docs: update installation instructions
test: add tests for styled content conversion
```

## Code Style

### Python Code Style

We use several tools to maintain code quality:

- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking

Run all checks:
```bash
make check-all
```

Fix formatting issues:
```bash
make fix-all
```

### Documentation Style

- Use clear, concise language
- Include code examples for new features
- Follow the existing documentation structure
- Test all code examples

## Testing

### Writing Tests

- Place tests in the `src/converter/__tests__/` directory
- Use descriptive test names: `test_blocks_to_html_with_styling`
- Include both positive and negative test cases
- Test error conditions and edge cases

### Test Structure

```python
import pytest
from blocknote.converter import your_function
from blocknote.schema import Block, InlineContent

def test_your_function_basic_case():
    """Test basic functionality."""
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = your_function(input_data)
    
    # Assert
    assert result == expected_result

def test_your_function_error_handling():
    """Test error handling."""
    with pytest.raises(ValueError, match="Expected error message"):
        your_function(invalid_input)
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test
uv run pytest src/converter/__tests__/test_specific.py::test_function -v
```

## Adding New Features

### Adding a New Converter

1. **Create the converter file:**

```python
# src/converter/new_format_converter.py
from typing import List
from blocknote.schema import Block

def blocks_to_new_format(blocks: List[Block]) -> str:
    """Convert BlockNote blocks to new format."""
    # Implementation here
    pass

def new_format_to_blocks(content: str) -> List[Block]:
    """Convert new format to BlockNote blocks."""
    # Implementation here
    pass
```

2. **Add tests:**

```python
# src/converter/__tests__/test_new_format_converter.py
import pytest
from blocknote.converter.new_format_converter import blocks_to_new_format

def test_blocks_to_new_format_basic():
    """Test basic conversion."""
    # Test implementation
    pass
```

3. **Update exports:**

```python
# src/converter/__init__.py
from .new_format_converter import blocks_to_new_format, new_format_to_blocks

__all__ = [
    # ... existing exports
    "blocks_to_new_format",
    "new_format_to_blocks"
]
```

4. **Add documentation:**

Create `docs/converters/new-format.md` with usage examples and API documentation.

### Adding New Block Types

1. **Update the schema:**

```python
# src/schema/types.py
class BlockType(str, Enum):
    # ... existing types
    NEW_BLOCK_TYPE = "newBlockType"
```

2. **Update converters:**

Add support for the new block type in all relevant converters.

3. **Add tests:**

Test the new block type in all converters.

4. **Update documentation:**

Document the new block type and provide examples.

## Documentation

### Building Documentation Locally

```bash
# Install documentation dependencies
uv pip install mkdocs-material mkdocstrings[python]

# Serve documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build
```

### Documentation Structure

```
docs/
├── index.md                    # Homepage
├── getting-started/
│   ├── installation.md
│   ├── quick-start.md
│   └── basic-usage.md
├── converters/
│   ├── overview.md
│   ├── blocknote-to-html.md
│   └── ...
├── api/
│   ├── schema.md
│   └── converters.md
├── examples/
│   ├── basic.md
│   └── advanced.md
├── contributing.md
└── changelog.md
```

## Pull Request Process

1. **Ensure your branch is up to date:**

```bash
git checkout main
git pull upstream main
git checkout your-branch
git rebase main
```

2. **Run all checks:**

```bash
make check-all
make test
```

3. **Create a pull request:**
   - Use a descriptive title
   - Include a detailed description of changes
   - Reference any related issues
   - Include screenshots for UI changes

4. **Pull request template:**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## Release Process

Releases are handled by maintainers:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a release tag
4. GitHub Actions automatically publishes to PyPI

## Getting Help

- **GitHub Issues** - Report bugs or request features
- **GitHub Discussions** - Ask questions or discuss ideas
- **Documentation** - Check the docs for detailed information

## Code of Conduct

Please note that this project is released with a [Code of Conduct](https://github.com/rohansharmasitoula/blocknote-py/blob/main/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- GitHub contributors page

Thank you for contributing to BlockNote-py! 🎉
