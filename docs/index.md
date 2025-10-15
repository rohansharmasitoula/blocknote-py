# BlockNote-py

[![PyPI version](https://badge.fury.io/py/blocknote-py.svg)](https://badge.fury.io/py/blocknote-py)
[![Python Support](https://img.shields.io/pypi/pyversions/blocknote-py.svg)](https://pypi.org/project/blocknote-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**BlockNote-py** is a Python library that provides seamless integration with [BlockNote.js](https://www.blocknotejs.org/), allowing you to convert between BlockNote blocks and various formats including HTML, Markdown, and Python dictionaries.

## ✨ Features

- 🔄 **Bidirectional Conversion**: Convert between BlockNote blocks and multiple formats
- 🌐 **HTML Support**: Full HTML conversion with styling preservation
- 📝 **Markdown Support**: Convert to/from Markdown with formatting
- 📊 **Dictionary Support**: Work with BlockNote data as Python dictionaries
- 🎨 **Rich Formatting**: Support for bold, italic, colors, and more
- 🧪 **Type Safe**: Built with Pydantic for robust type validation
- 🚀 **Easy to Use**: Simple, intuitive API

## 🚀 Quick Start

### Installation

```bash
pip install blocknote-py
```

### Basic Usage

```python
from blocknote.converter import blocks_to_html, html_to_blocks
from blocknote.schema import Block, InlineContent

# Create a BlockNote block
block = Block(
    id="1",
    type="paragraph",
    content=[
        InlineContent(
            type="text", 
            text="Hello, World!", 
            styles={"bold": True}
        )
    ]
)

# Convert to HTML
html = blocks_to_html([block])
print(html)  # <p><strong>Hello, World!</strong></p>

# Convert back to BlockNote
blocks = html_to_blocks(html)
print(blocks[0].content[0].text)  # Hello, World!
```

## 🔧 Supported Conversions

| From/To | HTML | Markdown | Dictionary |
|---------|------|----------|------------|
| **BlockNote** | ✅ | ✅ | ✅ |
| **HTML** | - | ❌ | ❌ |
| **Markdown** | ❌ | - | ❌ |
| **Dictionary** | ❌ | ❌ | - |

## 📚 Documentation

- [Getting Started](getting-started/installation.md) - Installation and setup
- [Converters](converters/overview.md) - Detailed converter documentation
- [API Reference](api/schema.md) - Complete API documentation
- [Examples](examples/basic.md) - Practical examples and use cases

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](contributing.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/rohansharmasitoula/blocknote-py/blob/main/LICENSE) file for details.

## 🙏 Acknowledgments

- [BlockNote.js](https://www.blocknotejs.org/) - The amazing block-based editor that inspired this library
- [Pydantic](https://pydantic-docs.helpmanual.io/) - For robust data validation
