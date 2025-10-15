# HTML to BlockNote Converter

The `html_to_blocks()` function parses HTML content and converts it into BlockNote blocks.

## Function Signature

```python
def html_to_blocks(html: str) -> List[Block]
```

## Parameters

- **html** (`str`): HTML string to parse and convert

## Returns

- **List[Block]**: List of BlockNote Block objects

## Basic Usage

```python
from blocknote.converter import html_to_blocks

html = "<h1>Title</h1><p>This is a paragraph.</p>"
blocks = html_to_blocks(html)

print(len(blocks))  # 2
print(blocks[0].type)  # heading
print(blocks[0].props["level"])  # 1
print(blocks[1].type)  # paragraph
```

## Supported HTML Elements

### Headings

```python
html = "<h1>H1</h1><h2>H2</h2><h6>H6</h6>"
blocks = html_to_blocks(html)

# Results in 3 heading blocks with levels 1, 2, and 6
```

### Paragraphs

```python
html = "<p>Simple paragraph</p>"
blocks = html_to_blocks(html)

# Results in 1 paragraph block
```

### Lists

#### Unordered Lists
```python
html = """
<ul>
    <li>First item</li>
    <li>Second item</li>
</ul>
"""
blocks = html_to_blocks(html)

# Results in 2 bulletListItem blocks
```

#### Ordered Lists
```python
html = """
<ol>
    <li>First step</li>
    <li>Second step</li>
</ol>
"""
blocks = html_to_blocks(html)

# Results in 2 numberedListItem blocks
```

### Blockquotes

```python
html = "<blockquote>Important quote</blockquote>"
blocks = html_to_blocks(html)

# Results in 1 quote block
```

### Checkboxes

```python
html = """
<div><input type="checkbox" checked> Completed task</div>
<div><input type="checkbox"> Pending task</div>
"""
blocks = html_to_blocks(html)

# Results in 2 checkListItem blocks
# First with checked=True, second with checked=False
```

## Text Styling

### Basic Styles

```python
html = "<p><strong>Bold</strong> and <em>italic</em> text</p>"
blocks = html_to_blocks(html)

block = blocks[0]
print(len(block.content))  # 3 inline content items
print(block.content[0].styles)  # {"bold": True}
print(block.content[2].styles)  # {"italic": True}
```

### Supported Style Tags

| HTML Tag | BlockNote Style | Example |
|----------|-----------------|---------|
| `<strong>`, `<b>` | `{"bold": True}` | **bold** |
| `<em>`, `<i>` | `{"italic": True}` | *italic* |
| `<u>` | `{"underline": True}` | <u>underline</u> |
| `<s>` | `{"strike": True}` | ~~strikethrough~~ |
| `<code>` | `{"code": True}` | `code` |

### CSS Styles

```python
html = '<p><span style="color: red; background-color: yellow;">Colored text</span></p>'
blocks = html_to_blocks(html)

content = blocks[0].content[0]
print(content.styles)  # {"textColor": "red", "backgroundColor": "yellow"}
```

### Nested Styles

```python
html = "<p><strong><em>Bold and italic</em></strong></p>"
blocks = html_to_blocks(html)

content = blocks[0].content[0]
print(content.styles)  # {"bold": True, "italic": True}
```

## Complex HTML Examples

### Mixed Content Document

```python
html = """
<h1>Document Title</h1>
<p>This is a <strong>paragraph</strong> with <em>mixed</em> formatting.</p>
<ul>
    <li>First bullet point</li>
    <li>Second bullet point</li>
</ul>
<blockquote>An important quote</blockquote>
<div><input type="checkbox" checked> Completed task</div>
"""

blocks = html_to_blocks(html)
print(f"Parsed {len(blocks)} blocks")

for i, block in enumerate(blocks):
    print(f"Block {i}: {block.type}")
    if block.content:
        text = "".join(c.text for c in block.content)
        print(f"  Content: {text}")
```

### Table Handling

```python
html = '<div class="blocknote-table">Table content</div>'
blocks = html_to_blocks(html)

print(blocks[0].type)  # table
```

## Error Handling

```python
from blocknote.converter import html_to_blocks

# Invalid input type
try:
    blocks = html_to_blocks(123)
except TypeError as e:
    print(f"Error: {e}")  # Input must be a string

# Empty input
blocks = html_to_blocks("")
print(len(blocks))  # 0

# Malformed HTML (handled gracefully)
blocks = html_to_blocks("<p>Unclosed paragraph")
print(len(blocks))  # Still parses what it can
```

## HTML Sanitization

The parser automatically handles potentially unsafe HTML:

```python
html = '<p><script>alert("xss")</script>Safe content</p>'
blocks = html_to_blocks(html)

# Script tags are ignored, only safe content is preserved
print(blocks[0].content[0].text)  # "Safe content"
```

## Advanced Usage

### Custom Block Detection

The parser can detect custom BlockNote block types:

```python
html = '<div class="blocknote-customType">Custom content</div>'
blocks = html_to_blocks(html)

# If customType is a valid BlockType, it will be preserved
# Otherwise, defaults to paragraph
```

### Whitespace Handling

```python
html = "<p>Text with    multiple   spaces</p>"
blocks = html_to_blocks(html)

# Whitespace is preserved as-is
print(blocks[0].content[0].text)  # "Text with    multiple   spaces"
```

### Empty Elements

```python
html = "<p></p><h1></h1>"
blocks = html_to_blocks(html)

print(len(blocks))  # 2
print(len(blocks[0].content))  # 0 (empty content)
print(len(blocks[1].content))  # 0 (empty content)
```

## Performance Considerations

### Large Documents

For large HTML documents:

```python
def parse_large_html(html_content):
    # Consider chunking very large documents
    if len(html_content) > 1_000_000:  # 1MB
        print("Warning: Large document, parsing may be slow")
    
    return html_to_blocks(html_content)
```

### Memory Usage

The parser creates Block objects in memory. For very large documents, consider:

1. Processing in chunks
2. Streaming processing
3. Limiting the depth of nested elements

## Limitations

1. **Complex Tables**: Only basic table support
2. **Media Elements**: Images, videos not supported
3. **Custom Elements**: Unknown HTML elements are ignored
4. **CSS Styles**: Only basic inline styles are supported

## Best Practices

### Input Validation

```python
def safe_html_parse(html_input):
    if not isinstance(html_input, str):
        raise TypeError("HTML input must be a string")
    
    if not html_input.strip():
        return []
    
    return html_to_blocks(html_input)
```

### Error Recovery

```python
def robust_html_parse(html_input):
    try:
        return html_to_blocks(html_input)
    except Exception as e:
        print(f"HTML parsing failed: {e}")
        # Return a safe fallback
        return [Block(
            id="error",
            type="paragraph",
            content=[InlineContent(type="text", text="Content could not be parsed")]
        )]
```

## See Also

- [BlockNote to HTML Converter](blocknote-to-html.md)
- [Schema Documentation](../api/schema.md)
- [Examples](../examples/basic.md)
