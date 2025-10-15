# Converters Overview

BlockNote-py provides several converters to transform BlockNote blocks to and from different formats. Each converter is designed to preserve as much formatting and structure as possible.

## Available Converters

### HTML Converters

- **`blocks_to_html()`** - Convert BlockNote blocks to HTML
- **`html_to_blocks()`** - Parse HTML and convert to BlockNote blocks

### Markdown Converters

- **`blocks_to_markdown()`** - Convert BlockNote blocks to Markdown
- **`markdown_to_blocks()`** - Parse Markdown and convert to BlockNote blocks

### Dictionary Converters

- **`blocks_to_dict()`** - Convert BlockNote blocks to Python dictionaries
- **`dict_to_blocks()`** - Convert dictionaries back to BlockNote blocks

## Import Statement

All converters can be imported from the main converter module:

```python
from blocknote.converter import (
    blocks_to_html,
    html_to_blocks,
    blocks_to_markdown,
    markdown_to_blocks,
    blocks_to_dict,
    dict_to_blocks
)
```

## Supported Block Types

All converters support the following BlockNote block types:

| Block Type | Description | HTML Example | Markdown Example |
|------------|-------------|--------------|------------------|
| `paragraph` | Regular text paragraph | `<p>Text</p>` | `Text` |
| `heading` | Headings (levels 1-6) | `<h1>Title</h1>` | `# Title` |
| `bulletListItem` | Bullet list item | `<ul><li>Item</li></ul>` | `* Item` |
| `numberedListItem` | Numbered list item | `<ol><li>Item</li></ol>` | `1. Item` |
| `checkListItem` | Checkbox list item | `<input type="checkbox">` | Not supported |
| `quote` | Blockquote | `<blockquote>Quote</blockquote>` | `> Quote` |
| `table` | Table (basic support) | `<div class="table-placeholder">` | Not supported |

## Supported Inline Styles

All converters support these inline text styles:

| Style | Description | HTML | Markdown |
|-------|-------------|------|----------|
| `bold` | Bold text | `<strong>text</strong>` | `**text**` |
| `italic` | Italic text | `<em>text</em>` | `*text*` |
| `underline` | Underlined text | `<u>text</u>` | Not supported |
| `strike` | Strikethrough text | `<s>text</s>` | Not supported |
| `code` | Inline code | `<code>text</code>` | `` `text` `` |
| `textColor` | Text color | `<span style="color: red">` | Not supported |
| `backgroundColor` | Background color | `<span style="background-color: yellow">` | Not supported |

## Error Handling

All converters include robust error handling:

```python
from blocknote.converter import blocks_to_html

try:
    html = blocks_to_html(invalid_input)
except TypeError as e:
    print(f"Invalid input type: {e}")
except ValueError as e:
    print(f"Invalid block structure: {e}")
```

Common errors:

- **TypeError**: Input is not the expected type (e.g., passing a string instead of a list)
- **ValueError**: Invalid block structure or content
- **ValidationError**: Pydantic validation errors for invalid block data

## Performance Considerations

- **Memory Usage**: Large documents with many blocks may consume significant memory
- **Processing Time**: Complex nested structures take longer to process
- **Validation Overhead**: Pydantic validation adds some overhead but ensures data integrity

## Best Practices

1. **Validate Input**: Always validate your input data before conversion
2. **Handle Errors**: Wrap converter calls in try-catch blocks
3. **Batch Processing**: For large datasets, consider processing in batches
4. **Preserve IDs**: Block IDs are preserved during conversion when possible

## Conversion Matrix

| From → To | HTML | Markdown | Dictionary | BlockNote |
|-----------|------|----------|------------|-----------|
| **BlockNote** | ✅ `blocks_to_html()` | ✅ `blocks_to_markdown()` | ✅ `blocks_to_dict()` | - |
| **HTML** | - | ❌ | ❌ | ✅ `html_to_blocks()` |
| **Markdown** | ❌ | - | ❌ | ✅ `markdown_to_blocks()` |
| **Dictionary** | ❌ | ❌ | - | ✅ `dict_to_blocks()` |

## Next Steps

Explore detailed documentation for each converter:

- [BlockNote to HTML](blocknote-to-html.md)
- [HTML to BlockNote](html-to-blocknote.md)
- [BlockNote to Markdown](blocknote-to-markdown.md)
- [Markdown to BlockNote](markdown-to-blocknote.md)
- [BlockNote to Dictionary](blocknote-to-dict.md)
- [Dictionary to BlockNote](dict-to-blocknote.md)
