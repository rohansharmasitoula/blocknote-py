---
title: BlockNote-py - Python Library for BlockNote.js
description: BlockNote Python library for converting BlockNote blocks to HTML, Markdown, and JSON. Complete Python support for BlockNote.js with type safety and validation.
keywords: blocknote python, blocknote py, block note python, blocknote.js python, python blocknote library, blocknote converter python, html to blocknote python, markdown to blocknote python
---

# BlockNote-py - Python Library for BlockNote.js

[![PyPI version](https://badge.fury.io/py/blocknote-py.svg)](https://badge.fury.io/py/blocknote-py)
[![Python Support](https://img.shields.io/pypi/pyversions/blocknote-py.svg)](https://pypi.org/project/blocknote-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**BlockNote-py** is the official Python library for [BlockNote.js](https://www.blocknotejs.org/), providing seamless integration and conversion between BlockNote blocks and various formats including HTML, Markdown, and Python dictionaries. Whether you're building a Python backend for a BlockNote editor or need to process BlockNote content server-side, BlockNote-py makes it simple and type-safe.

## Why BlockNote-py?

BlockNote-py bridges the gap between JavaScript's BlockNote.js and Python applications, enabling you to:

- **Process BlockNote content in Python** - Handle BlockNote blocks server-side
- **Convert between formats** - Transform BlockNote to HTML, Markdown, or JSON
- **Type-safe operations** - Built with Pydantic for robust validation
- **Server-side rendering** - Generate HTML from BlockNote blocks for SEO
- **Content migration** - Import/export content between different formats

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

## ☕ Support the Project

If you find BlockNote-py useful, consider supporting its development:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support%20development-orange?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/sitoularohansharma)

Your support helps maintain and improve BlockNote-py for the entire Python community! 🙏

## 🙏 Acknowledgments

- [BlockNote.js](https://www.blocknotejs.org/) - The amazing block-based editor that inspired this library
- [Pydantic](https://pydantic-docs.helpmanual.io/) - For robust data validation
