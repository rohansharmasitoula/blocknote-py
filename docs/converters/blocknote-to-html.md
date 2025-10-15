# BlockNote to HTML Converter

The `blocks_to_html()` function converts BlockNote blocks into clean, semantic HTML.

## Function Signature

```python
def blocks_to_html(blocks: List[Block]) -> str
```

## Parameters

- **blocks** (`List[Block]`): A list of BlockNote Block objects to convert

## Returns

- **str**: HTML string representation of the blocks

## Basic Usage

```python
from blocknote.converter import blocks_to_html
from blocknote.schema import Block, InlineContent

blocks = [
    Block(
        id="1",
        type="heading",
        props={"level": 1},
        content=[InlineContent(type="text", text="My Document")]
    ),
    Block(
        id="2",
        type="paragraph",
        content=[InlineContent(type="text", text="This is a paragraph.")]
    )
]

html = blocks_to_html(blocks)
print(html)
```

**Output:**
```html
<h1>My Document</h1>
<p>This is a paragraph.</p>
```

## Block Type Conversions

### Headings

```python
heading_blocks = [
    Block(id="h1", type="heading", props={"level": 1}, 
          content=[InlineContent(type="text", text="Heading 1")]),
    Block(id="h2", type="heading", props={"level": 2}, 
          content=[InlineContent(type="text", text="Heading 2")]),
    Block(id="h6", type="heading", props={"level": 6}, 
          content=[InlineContent(type="text", text="Heading 6")])
]

html = blocks_to_html(heading_blocks)
```

**Output:**
```html
<h1>Heading 1</h1>
<h2>Heading 2</h2>
<h6>Heading 6</h6>
```

### Lists

#### Bullet Lists
```python
bullet_list = [
    Block(
        id="ul1",
        type="bulletListItem",
        content=[InlineContent(type="text", text="First item")],
        children=[
            Block(id="ul1-1", type="paragraph", 
                  content=[InlineContent(type="text", text="Nested item")])
        ]
    )
]

html = blocks_to_html(bullet_list)
```

**Output:**
```html
<ul><li>Nested item</li></ul>
```

#### Numbered Lists
```python
numbered_list = [
    Block(
        id="ol1",
        type="numberedListItem",
        content=[InlineContent(type="text", text="First item")],
        children=[
            Block(id="ol1-1", type="paragraph", 
                  content=[InlineContent(type="text", text="First numbered")])
        ]
    )
]

html = blocks_to_html(numbered_list)
```

**Output:**
```html
<ol><li>First numbered</li></ol>
```

### Checklists

```python
checklist = [
    Block(
        id="check1",
        type="checkListItem",
        props={"checked": True},
        content=[InlineContent(type="text", text="Completed task")]
    ),
    Block(
        id="check2",
        type="checkListItem",
        props={"checked": False},
        content=[InlineContent(type="text", text="Pending task")]
    )
]

html = blocks_to_html(checklist)
```

**Output:**
```html
<div><input type="checkbox" checked disabled> Completed task</div>
<div><input type="checkbox"  disabled> Pending task</div>
```

### Quotes

```python
quote_block = [
    Block(
        id="quote1",
        type="quote",
        content=[InlineContent(type="text", text="To be or not to be")]
    )
]

html = blocks_to_html(quote_block)
```

**Output:**
```html
<blockquote>To be or not to be</blockquote>
```

## Text Styling

### Basic Styles

```python
styled_block = [
    Block(
        id="styled",
        type="paragraph",
        content=[
            InlineContent(type="text", text="This is "),
            InlineContent(type="text", text="bold", styles={"bold": True}),
            InlineContent(type="text", text=" and "),
            InlineContent(type="text", text="italic", styles={"italic": True}),
            InlineContent(type="text", text=" text.")
        ]
    )
]

html = blocks_to_html(styled_block)
```

**Output:**
```html
<p>This is <strong>bold</strong> and <em>italic</em> text.</p>
```

### All Supported Styles

| Style | HTML Output | Example |
|-------|-------------|---------|
| `bold` | `<strong>text</strong>` | **bold** |
| `italic` | `<em>text</em>` | *italic* |
| `underline` | `<u>text</u>` | <u>underline</u> |
| `strike` | `<s>text</s>` | ~~strikethrough~~ |
| `code` | `<code>text</code>` | `code` |

### Colors

```python
colored_block = [
    Block(
        id="colored",
        type="paragraph",
        content=[
            InlineContent(
                type="text",
                text="Colored text",
                styles={
                    "textColor": "red",
                    "backgroundColor": "yellow"
                }
            )
        ]
    )
]

html = blocks_to_html(colored_block)
```

**Output:**
```html
<p><span style="color: red"><span style="background-color: yellow">Colored text</span></span></p>
```

## HTML Safety

The converter automatically escapes HTML special characters to prevent XSS attacks:

```python
unsafe_block = [
    Block(
        id="unsafe",
        type="paragraph",
        content=[InlineContent(type="text", text="<script>alert('xss')</script>")]
    )
]

html = blocks_to_html(unsafe_block)
```

**Output:**
```html
<p>&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;</p>
```

## Error Handling

```python
from blocknote.converter import blocks_to_html

# Invalid input type
try:
    html = blocks_to_html("not a list")
except TypeError as e:
    print(f"Error: {e}")  # Input must be a list of Block objects

# Invalid block object
try:
    html = blocks_to_html([{"invalid": "block"}])
except TypeError as e:
    print(f"Error: {e}")  # Item at index 0 must be a Block object
```

## Advanced Usage

### Custom Block Types

For unsupported block types, the converter wraps them in a div with a CSS class:

```python
# Note: This would require extending the BlockType enum
custom_block = [
    Block(
        id="custom",
        type="table",  # Supported but basic
        content=[InlineContent(type="text", text="Table content")]
    )
]

html = blocks_to_html(custom_block)
```

**Output:**
```html
<div class='table-placeholder'>Table content</div>
```

### Empty Blocks

Empty blocks are handled gracefully:

```python
empty_block = [
    Block(id="empty", type="paragraph", content=[])
]

html = blocks_to_html(empty_block)
```

**Output:**
```html
<p></p>
```

## Performance Tips

1. **Batch Processing**: Process multiple blocks at once rather than one by one
2. **Memory Management**: For very large documents, consider processing in chunks
3. **Validation**: Input validation is performed automatically but adds overhead

## See Also

- [HTML to BlockNote Converter](html-to-blocknote.md)
- [Schema Documentation](../api/schema.md)
- [Examples](../examples/basic.md)
