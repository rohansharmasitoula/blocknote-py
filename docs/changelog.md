# Changelog

All notable changes to BlockNote-py will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-10-16

### Added
- **HTML Conversion Support**: Full bidirectional HTML conversion
  - `html_to_blocks()`: Parse HTML and convert to BlockNote blocks
  - `blocks_to_html()`: Convert BlockNote blocks to clean, semantic HTML
- **Rich Text Styling**: Complete styling support
  - Bold, italic, underline, strikethrough formatting
  - Text and background colors
  - Inline code formatting
  - Custom CSS styles preservation
- **Enhanced Block Support**: 
  - Checkbox list items with checked/unchecked state
  - All major BlockNote block types (paragraphs, headings, lists, quotes, tables)
  - Nested block structures
- **Security Features**:
  - HTML sanitization and XSS protection
  - Safe HTML entity escaping
- **Professional Documentation**:
  - Complete MkDocs documentation site with Material theme
  - Comprehensive guides (installation, quick start, basic usage)
  - Detailed converter documentation for all 6 converters
  - API reference with auto-generated documentation
  - Real-world usage examples (basic and advanced patterns)
  - GitHub Pages deployment with automatic updates
- **Testing**: Comprehensive test suite with 74+ tests covering all functionality

### Changed
- **Enhanced PyPI Metadata**: Better discoverability with keywords, classifiers, and project URLs
- **Improved README**: Clean, focused design directing users to comprehensive documentation
- **Better Dependencies**: More precise version constraints and optional dependency groups
- **Enhanced Error Handling**: Improved error messages and validation across all converters
- **Type Safety**: Enhanced Pydantic validation and type hints

### Fixed
- HTML parsing edge cases and malformed HTML handling
- Style preservation in HTML conversion
- Empty block handling in all converters
- Dependency conflicts in development environment

### Security
- Added HTML sanitization to prevent XSS attacks
- Safe escaping of HTML special characters

## [0.1.0] - 2025-10-08

### Added
- Initial release of BlockNote-py
- Core schema definitions (`Block`, `InlineContent`)
- BlockNote to Dictionary converter (`blocks_to_dict()`)
- Dictionary to BlockNote converter (`dict_to_blocks()`)
- BlockNote to Markdown converter (`blocks_to_markdown()`)
- Markdown to BlockNote converter (`markdown_to_blocks()`)
- Pydantic-based data validation
- Basic documentation and examples
- MIT license
- GitHub repository setup
- CI/CD pipeline with GitHub Actions
- PyPI package publishing

### Supported Block Types
- Paragraph blocks
- Heading blocks (levels 1-6)
- Bullet list items
- Numbered list items
- Quote blocks
- Basic table support

### Supported Inline Styles
- Bold text
- Italic text
- Basic text formatting

---

## Release Notes

### Version 0.1.0

This is the initial release of BlockNote-py, providing Python developers with tools to work with BlockNote.js data structures. The library focuses on type safety, ease of use, and comprehensive format conversion capabilities.

**Key Features:**
- 🔄 Bidirectional conversion between BlockNote and multiple formats
- 🛡️ Type-safe operations with Pydantic validation
- 📝 Support for rich text formatting
- 🧪 Comprehensive test coverage
- 📚 Detailed documentation and examples

**Getting Started:**
```bash
pip install blocknote-py
```

**Basic Usage:**
```python
from blocknote.converter import blocks_to_html
from blocknote.schema import Block, InlineContent

block = Block(
    id="1",
    type="paragraph",
    content=[InlineContent(type="text", text="Hello, World!")]
)

html = blocks_to_html([block])
print(html)  # <p>Hello, World!</p>
```

---

## Migration Guide

### From Pre-release to 0.1.0

If you were using pre-release versions, please note:

1. **Import Changes:**
   ```python
   # Old
   from blocknote import Block, InlineContent
   
   # New
   from blocknote.schema import Block, InlineContent
   ```

2. **Converter Imports:**
   ```python
   # Old
   from blocknote.converters import blocks_to_dict
   
   # New
   from blocknote.converter import blocks_to_dict
   ```

3. **Schema Updates:**
   - Block validation is now stricter
   - Content field must be a list of InlineContent objects
   - Props field is now optional and defaults to empty dict

---

## Upcoming Features

### Planned for v0.2.0
- [ ] Advanced table support with cell formatting
- [ ] Image and media block support
- [ ] Custom block type extensibility
- [ ] Performance optimizations for large documents
- [ ] Additional export formats (PDF, DOCX)

### Planned for v0.3.0
- [ ] Real-time collaboration support
- [ ] Plugin system for custom converters
- [ ] Advanced styling options
- [ ] Internationalization support

---

## Contributing

We welcome contributions! See our [Contributing Guide](contributing.md) for details on how to get started.

### Recent Contributors

- [@rohansharmasitoula](https://github.com/rohansharmasitoula) - Project creator and maintainer

---

## Support

- 📖 [Documentation](https://rohansharmasitoula.github.io/blocknote-py/)
- 🐛 [Issue Tracker](https://github.com/rohansharmasitoula/blocknote-py/issues)
- 💬 [Discussions](https://github.com/rohansharmasitoula/blocknote-py/discussions)
- 📦 [PyPI Package](https://pypi.org/project/blocknote-py/)

---

*This changelog is automatically updated with each release. For the most up-to-date information, check the [GitHub releases page](https://github.com/rohansharmasitoula/blocknote-py/releases).*
