# Markdown to BlockNote Converter

The `markdown_to_blocks()` function parses Markdown content and converts it into BlockNote blocks.

## Function Signature

```python
def markdown_to_blocks(markdown: str) -> List[Block]
```

## Parameters

- **markdown** (`str`): Markdown string to parse and convert

## Returns

- **List[Block]**: List of BlockNote Block objects

## Basic Usage

```python
from blocknote.converter import markdown_to_blocks

markdown = """
# My Document

This is a **bold** paragraph with *italic* text.

## Section

- First item
- Second item

1. Numbered item
2. Another item

> This is a quote
"""

blocks = markdown_to_blocks(markdown)
print(f"Parsed {len(blocks)} blocks")
```

## Supported Markdown Elements

- **Headings**: `#` through `######`
- **Paragraphs**: Plain text
- **Bold**: `**text**` or `__text__`
- **Italic**: `*text*` or `_text_`
- **Lists**: Both `*` and `1.` formats
- **Quotes**: `>` blockquotes

## Error Handling

```python
try:
    blocks = markdown_to_blocks(markdown_content)
except ValueError as e:
    print(f"Parsing failed: {e}")
```

## See Also

- [BlockNote to Markdown Converter](blocknote-to-markdown.md)
- [API Reference](../api/converters.md)
