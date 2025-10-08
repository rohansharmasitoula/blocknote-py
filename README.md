# blocknote-py 🐍✨

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/blocknote-py.svg)](https://pypi.org/project/blocknote-py/)
[![CI](https://github.com/rohansharmasitoula/blocknote-py/workflows/CI/badge.svg)](https://github.com/rohansharmasitoula/blocknote-py/actions)

> **Transform your BlockNote.js blocks like magic!** ✨ Convert between dictionaries, markdown, and BlockNote blocks with full type safety and validation.

Built with ❤️ using [Gemini CLI](https://codeium.com/windsurf) (Cascade)

## ✨ Why blocknote-py?

Ever wanted to work with BlockNote.js blocks in Python? Now you can! 🎉

- 🔄 **Bidirectional Magic**: Dict ↔ Blocks ↔ Markdown (it just works!)
- 🛡️ **Type-Safe**: Pydantic models keep your data squeaky clean
- 🎨 **Style Support**: Bold, italic, and more formatting options
- 📝 **Lists Galore**: Bullets, numbers, checks - we got 'em all
- 🧪 **Battle-Tested**: 43 tests and counting
- 🚀 **Fast & Easy**: Simple API, powerful results

## 📦 Installation

```bash
# With uv (recommended)
uv add blocknote-py

# Or with pip
pip install blocknote-py
```

That's it! You're ready to roll! 🎸

## 🚀 Quick Start

### The Magic in Action

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

## 🤝 Contributing

We love contributions! Got an idea? Found a bug? Let's make this better together! 

1. 🍴 Fork it
2. 🌿 Create your feature branch (`git checkout -b feature/awesome-feature`)
3. ✨ Commit your changes (`git commit -m 'Add awesome feature'`)
4. 🚀 Push to the branch (`git push origin feature/awesome-feature`)
5. 🎉 Open a Pull Request

Check out [CONTRIBUTING.md](CONTRIBUTING.md) for more details!

## 📄 License

MIT License - go wild! See [LICENSE](LICENSE) for details.

## 🔗 Related Projects

- [BlockNote.js](https://github.com/TypeCellOS/BlockNote) - The awesome JavaScript library that started it all

---

Made with ❤️ and ☕ by [Rohan Sharma](https://github.com/rohansharmasitoula)

**Star this repo if you find it useful!** ⭐

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-☕-yellow.svg)](https://buymeacoffee.com/sitoularohansharma)