# blocknote-py

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/blocknote-py.svg)](https://pypi.org/project/blocknote-py/)

A Python library for working with Blocknote.js blocks. Convert between dictionaries, markdown, and Blocknote block objects with full type safety and validation.

## Features

- **Type-safe Blocknote blocks**: Pydantic models with full validation
- **Bidirectional conversion**: Convert between dictionaries, markdown, and Blocknote blocks
- **Dictionary conversion**: Convert dictionaries to validated Block objects
- **Markdown parsing**: Parse markdown into Blocknote blocks
- **Markdown generation**: Convert Blocknote blocks back to markdown
- **Text styling support**: Bold and italic text formatting
- **Lists**: Both ordered and unordered lists
- **Extensible architecture**: Easy to add new block types and converters
- **Comprehensive testing**: Full test coverage with pytest

## Installation

```bash
uv add blocknote-py
```

Or install from source:

```bash
git clone https://github.com/yourusername/blocknote-py.git
cd blocknote-py
uv sync --dev
```

## Quick Start

### Basic Usage

```python
from blocknote.converter import dict_to_blocks, markdown_to_blocks, blocks_to_markdown, blocks_to_dict
from blocknote.schema import Block, InlineContent

# Convert dictionaries to blocks
data = [
    {
        "id": "1",
        "type": "paragraph",
        "content": [
            {"type": "text", "text": "Hello, "},
            {"type": "text", "text": "world!", "styles": {"bold": True}},
        ],
    }
]

blocks = dict_to_blocks(data)
print(blocks[0].content[0].text)  # "Hello, "

# Parse markdown with basic formatting
markdown = """# Hello World

This is **bold** and *italic* text.

- Bullet item 1
- Bullet item 2

1. Numbered item 1
2. Numbered item 2
"""

blocks = markdown_to_blocks(markdown)
print(f"Parsed {len(blocks)} blocks")

# Convert blocks back to markdown
back_to_md = blocks_to_markdown(blocks)
print("Round-trip conversion successful!")
```

### Working with Block Objects

```python
from blocknote.schema import Block, InlineContent

# Create blocks programmatically
block = Block(
    id="unique-id",
    type="paragraph",
    content=[
        InlineContent(type="text", text="Hello ", styles={}),
        InlineContent(type="text", text="world", styles={"bold": True})
    ],
    props={},
    children=[]
)

print(block.type)  # "paragraph"
print(len(block.content))  # 2
```

## API Reference

### Core Classes

#### `Block`
Represents a Blocknote block with content and children.

- `id: str` - Unique identifier
- `type: BlockType` - Block type (paragraph, heading, bulletListItem, orderedListItem)
- `props: Dict[str, Any]` - Block-specific properties
- `content: Union[str, List[InlineContent]]` - Block content
- `children: List[Block]` - Child blocks

#### `InlineContent`
Represents inline content within a block.

- `type: InlineContentType` - Content type (currently only "text")
- `text: str` - The text content
- `styles: Dict[str, Any]` - Text styling (bold, italic, etc.)

### Converter Functions

#### `dict_to_blocks(data: List[Dict[str, Any]]) -> List[Block]`
Converts a list of dictionaries to validated Block objects.

```python
from blocknote.converter import dict_to_blocks

data = [{"id": "1", "type": "paragraph", "content": "Hello"}]
blocks = dict_to_blocks(data)
```

#### `blocks_to_dict(blocks: List[Block]) -> List[Dict[str, Any]]`
Converts a list of Block objects to dictionaries.

```python
from blocknote.converter import blocks_to_dict

dict_data = blocks_to_dict(blocks)
```

#### `markdown_to_blocks(markdown: str) -> List[Block]`
Converts a markdown string to a list of Block objects.

```python
from blocknote.converter import markdown_to_blocks

blocks = markdown_to_blocks("# Hello\n\nWorld")
```

#### `blocks_to_markdown(blocks: List[Block]) -> str`
Converts a list of Block objects to a markdown string.

```python
from blocknote.converter import blocks_to_markdown

markdown = blocks_to_markdown(blocks)
```

## Supported Block Types

- **Paragraph**: Basic text paragraphs with styling support
- **Heading**: Headings with levels (H1, H2, H3)
- **Bullet Lists**: Unordered lists with list items
- **Numbered Lists**: Ordered lists with list items
- **Check Lists**: Checklist items with checked/unchecked state
- **Toggle Lists**: Collapsible list items
- **Quotes**: Blockquote text blocks
- **Tables**: Table structures (basic support)

## Supported Text Formatting

- **Bold text**: `**bold**` or `__bold__`
- **Italic text**: `*italic*` or `_italic_`
- **Plain text**: Regular text content

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/blocknote-py.git
cd blocknote-py

# Install dependencies (including development tools)
uv sync --dev

# Setup pre-commit hooks (optional)
uv run pre-commit install
```

### Code Quality

This project uses several tools to maintain code quality:

- **[Black](https://black.readthedocs.io/)**: Code formatting
- **[isort](https://pycqa.github.io/isort/)**: Import sorting
- **[flake8](https://flake8.pycqa.org/)**: Linting
- **[mypy](https://mypy.readthedocs.io/)**: Type checking

### Available Commands

```bash
# Run tests
make test

# Check code quality (lint + format check + type check)
make check-all

# Auto-fix formatting and import issues
make fix-all

# Run individual tools
make lint          # flake8
make format        # black + isort
make type-check    # mypy

# Development setup
make setup-dev     # Install everything + setup pre-commit
```

Or using hatch environments:

```bash
# Check all
hatch run check-all

# Fix all
hatch run fix-all

# Individual tools
hatch run lint
hatch run format
hatch run type-check
```

### Project Structure

```
src/
├── blocknote/
│   ├── __init__.py          # Main package exports
│   ├── schema/
│   │   ├── __init__.py      # Schema exports
│   │   └── types.py         # Pydantic models
│   └── converter/
│       ├── __init__.py      # Converter exports
│       ├── dict_to_blocknote.py  # Dict conversion
│       ├── md_to_blocknote.py    # Markdown conversion
│       └── __tests__/       # Tests
│           ├── test_dict_to_blocknote.py
│           └── test_md_to_blocknote.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [Blocknote.js](https://github.com/TypeCellOS/BlockNote) - The original JavaScript library