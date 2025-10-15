# Installation

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Install from PyPI

The easiest way to install BlockNote-py is from PyPI using pip:

```bash
pip install blocknote-py
```

## Install from Source

If you want to install the latest development version or contribute to the project:

```bash
# Clone the repository
git clone https://github.com/rohansharmasitoula/blocknote-py.git
cd blocknote-py

# Install in development mode
pip install -e .
```

## Install with Development Dependencies

For development and testing:

```bash
# Using uv (recommended)
uv sync --dev

# Or using pip
pip install -e ".[dev,test]"
```

## Verify Installation

To verify that BlockNote-py is installed correctly:

```python
import blocknote
print(blocknote.__version__)
```

Or test a simple conversion:

```python
from blocknote.converter import blocks_to_html
from blocknote.schema import Block, InlineContent

# Create a simple block
block = Block(
    id="test",
    type="paragraph",
    content=[InlineContent(type="text", text="Installation successful!")]
)

# Convert to HTML
html = blocks_to_html([block])
print(html)  # Should output: <p>Installation successful!</p>
```

## Dependencies

BlockNote-py has minimal dependencies:

- **pydantic**: For data validation and serialization
- **markdown-it-py**: For Markdown parsing (used in markdown converters)

These will be automatically installed when you install BlockNote-py.

## Troubleshooting

### Common Issues

**ImportError: No module named 'blocknote'**

Make sure you've installed the package correctly:

```bash
pip list | grep blocknote-py
```

**Version conflicts**

If you encounter version conflicts, try installing in a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install blocknote-py
```

### Getting Help

If you encounter any issues:

1. Check the [GitHub Issues](https://github.com/rohansharmasitoula/blocknote-py/issues)
2. Create a new issue with details about your problem
3. Include your Python version and operating system
