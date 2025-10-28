# BlockNote-py 🚀 - BlockNote Python Library

[![PyPI version](https://badge.fury.io/py/blocknote-py.svg)](https://pypi.org/project/blocknote-py/)
[![Python Support](https://img.shields.io/pypi/pyversions/blocknote-py.svg)](https://pypi.org/project/blocknote-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://rohansharmasitoula.github.io/blocknote-py/)
[![CI](https://github.com/rohansharmasitoula/blocknote-py/workflows/CI/badge.svg)](https://github.com/rohansharmasitoula/blocknote-py/actions)
[![Downloads](https://pepy.tech/badge/blocknote-py)](https://pepy.tech/project/blocknote-py)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/blocknote-py)](https://pypi.org/project/blocknote-py/)
[![GitHub stars](https://img.shields.io/github/stars/rohansharmasitoula/blocknote-py)](https://github.com/rohansharmasitoula/blocknote-py)

> **🎯 BlockNote Python Library** - Convert [BlockNote.js](https://www.blocknotejs.org/) blocks to HTML, Markdown, PDF & JSON with type-safe Pydantic models. Perfect for Django, FastAPI, Flask backends and headless CMS applications. Server-side BlockNote content processing made simple.

## 🤔 Why BlockNote-py?

**BlockNote-py** is the missing piece for Python developers who want to work with [BlockNote.js](https://www.blocknotejs.org/) content on the server-side. Whether you're building a Django blog, FastAPI content API, or Flask CMS, BlockNote-py provides seamless integration with Python backends.

### 🎯 Perfect For:
- **Django Developers**: Process BlockNote content in Django models and views
- **FastAPI APIs**: Build content APIs with automatic validation and serialization  
- **Flask Applications**: Add rich text processing to Flask apps
- **Headless CMS**: Convert editor content to multiple formats
- **Content Migration**: Batch process and convert existing content
- **PDF Reports**: Generate professional documents from editor content

## ✨ Features

- 🔄 **Multiple Format Support**: HTML, Markdown, PDF, and Dictionary conversion
- 🌐 **HTML Conversion**: Full bidirectional HTML support with styling preservation
- 📝 **Markdown Support**: Convert to/from Markdown with formatting
- 📄 **PDF Generation**: Convert BlockNote blocks to professional PDF documents with WeasyPrint
- 🛡️ **Type Safety**: Built with Pydantic v2 for robust data validation and IDE support
- 🎨 **Rich Formatting**: Bold, italic, colors, lists, quotes, headings, and more
- 🧪 **Well Tested**: Comprehensive test suite with 88+ tests and 95% coverage
- 📚 **Great Documentation**: Detailed docs with real-world examples
- ⚡ **Fast & Lightweight**: Minimal dependencies, maximum performance
- 🔧 **Framework Agnostic**: Works with any Python web framework

## 📦 Installation

### Basic Installation
```bash
pip install blocknote-py
```

### With PDF Support
```bash
pip install 'blocknote-py[pdf]'
```

### Full Installation (all features)
```bash
pip install 'blocknote-py[all]'
```

## 🚀 Quick Start

```python
from blocknote.converter import blocks_to_html, blocks_to_markdown, blocks_to_pdf
from blocknote.schema import Block, InlineContent

# Create BlockNote blocks
blocks = [
    Block(
        id="1",
        type="heading",
        props={"level": 1},
        content=[InlineContent(type="text", text="Welcome to BlockNote-py!")]
    ),
    Block(
        id="2", 
        type="paragraph",
        content=[
            InlineContent(type="text", text="Convert your "),
            InlineContent(type="text", text="BlockNote", styles={"bold": True}),
            InlineContent(type="text", text=" content to multiple formats!")
        ]
    )
]

# Convert to different formats
html_output = blocks_to_html(blocks)
markdown_output = blocks_to_markdown(blocks)
pdf_bytes = blocks_to_pdf(blocks)  # Requires PDF support

print("HTML:", html_output)
print("Markdown:", markdown_output)
```

## 📚 Documentation

**Complete documentation:** https://rohansharmasitoula.github.io/blocknote-py/

### Quick Navigation

| Section | Description |
|---------|-------------|
| [🚀 Quick Start](https://rohansharmasitoula.github.io/blocknote-py/getting-started/quick-start/) | Get up and running in minutes |
| [🔧 API Reference](https://rohansharmasitoula.github.io/blocknote-py/api/schema/) | Complete API documentation |
| [🔄 Converters](https://rohansharmasitoula.github.io/blocknote-py/converters/overview/) | Detailed converter documentation |
| [💡 Examples](https://rohansharmasitoula.github.io/blocknote-py/examples/basic/) | Real-world usage examples |
| [🤝 Contributing](https://rohansharmasitoula.github.io/blocknote-py/contributing/) | How to contribute |

## ❓ Frequently Asked Questions

**What is BlockNote-py?**  
BlockNote-py is the official BlockNote Python library that mirrors the data
model used by [BlockNote.js](https://www.blocknotejs.org/). It lets Python
developers convert BlockNote content to HTML, Markdown, PDF, and JSON without
needing Node.js on the server.

**How do I install the BlockNote Python package with PDF support?**  
Install the PyPI package with the optional PDF extra: `pip install
'blocknote-py[pdf]'`. This pulls in WeasyPrint so you can generate print-ready
PDF documents from BlockNote blocks.

**Can I use BlockNote-py on the backend of a Django or FastAPI project?**  
Yes. BlockNote-py is framework-agnostic and works in any Python backend. The
package is typed with Pydantic models, making it easy to validate incoming
BlockNote payloads in Django REST Framework, FastAPI, Flask, or any custom API.

**Does BlockNote-py stay in sync with BlockNote.js?**  
The converter and schema modules track the BlockNote.js block schema. Whenever
BlockNote introduces new block types or inline styles, BlockNote-py updates aim
to follow quickly so Python projects stay compatible.

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](https://rohansharmasitoula.github.io/blocknote-py/contributing/) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ☕ Support the Project

If you find BlockNote-py useful, consider supporting its development:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support%20development-orange?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/sitoularohansharma)

Your support helps maintain and improve BlockNote-py for the entire Python community! 🙏

## 🙏 Acknowledgments

- [BlockNote.js](https://www.blocknotejs.org/) - The amazing block-based editor
- [Pydantic](https://pydantic-docs.helpmanual.io/) - For robust data validation

---

**[⭐ Star this repo](https://github.com/rohansharmasitoula/blocknote-py)** if you find it useful!
