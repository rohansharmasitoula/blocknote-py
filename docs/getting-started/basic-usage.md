# Basic Usage

This guide covers the fundamental concepts and common usage patterns for BlockNote-py.

## Core Concepts

### Blocks

A **Block** is the fundamental unit of content in BlockNote. Each block has:

- **id**: Unique identifier
- **type**: The kind of block (paragraph, heading, list item, etc.)
- **props**: Block-specific properties (like heading level)
- **content**: The actual content (text with styling)
- **children**: Nested child blocks

### Inline Content

**InlineContent** represents styled text within a block:

- **type**: Content type (currently only "text")
- **text**: The actual text content
- **styles**: Formatting styles (bold, italic, colors, etc.)

## Creating Blocks

### Simple Text Block

```python
from blocknote.schema import Block, InlineContent

simple_block = Block(
    id="simple-1",
    type="paragraph",
    content=[
        InlineContent(
            type="text",
            text="This is a simple paragraph."
        )
    ]
)
```

### Heading Block

```python
heading_block = Block(
    id="heading-1",
    type="heading",
    props={"level": 2},  # H2 heading
    content=[
        InlineContent(
            type="text",
            text="Chapter Title"
        )
    ]
)
```

### Styled Text Block

```python
styled_block = Block(
    id="styled-1",
    type="paragraph",
    content=[
        InlineContent(type="text", text="This text is "),
        InlineContent(
            type="text", 
            text="bold and red", 
            styles={
                "bold": True,
                "textColor": "#ff0000"
            }
        ),
        InlineContent(type="text", text=" while this is normal.")
    ]
)
```

## Working with Lists

### Bullet Lists

```python
bullet_items = [
    Block(
        id="bullet-1",
        type="bulletListItem",
        content=[InlineContent(type="text", text="First item")]
    ),
    Block(
        id="bullet-2",
        type="bulletListItem",
        content=[InlineContent(type="text", text="Second item")]
    )
]
```

### Numbered Lists

```python
numbered_items = [
    Block(
        id="num-1",
        type="numberedListItem",
        content=[InlineContent(type="text", text="First step")]
    ),
    Block(
        id="num-2",
        type="numberedListItem",
        content=[InlineContent(type="text", text="Second step")]
    )
]
```

### Nested Lists

```python
nested_list = Block(
    id="parent-item",
    type="bulletListItem",
    content=[InlineContent(type="text", text="Parent item")],
    children=[
        Block(
            id="child-1",
            type="paragraph",
            content=[InlineContent(type="text", text="Child item 1")]
        ),
        Block(
            id="child-2",
            type="paragraph",
            content=[InlineContent(type="text", text="Child item 2")]
        )
    ]
)
```

## Checklists

```python
checklist_items = [
    Block(
        id="check-1",
        type="checkListItem",
        props={"checked": True},
        content=[InlineContent(type="text", text="Completed task")]
    ),
    Block(
        id="check-2",
        type="checkListItem",
        props={"checked": False},
        content=[InlineContent(type="text", text="Pending task")]
    )
]
```

## Quotes

```python
quote_block = Block(
    id="quote-1",
    type="quote",
    content=[
        InlineContent(
            type="text",
            text="The only way to do great work is to love what you do."
        )
    ]
)
```

## Converting Between Formats

### To HTML

```python
from blocknote.converter import blocks_to_html

blocks = [heading_block, styled_block, quote_block]
html = blocks_to_html(blocks)
print(html)
```

### To Markdown

```python
from blocknote.converter import blocks_to_markdown

markdown = blocks_to_markdown(blocks)
print(markdown)
```

### To Dictionary

```python
from blocknote.converter import blocks_to_dict

block_dict = blocks_to_dict(blocks)
print(block_dict)
```

## Parsing External Content

### From HTML

```python
from blocknote.converter import html_to_blocks

html_content = """
<h1>My Document</h1>
<p>This is a <strong>paragraph</strong> with formatting.</p>
<blockquote>An important quote</blockquote>
"""

blocks = html_to_blocks(html_content)
```

### From Markdown

```python
from blocknote.converter import markdown_to_blocks

markdown_content = """
# My Document

This is a **paragraph** with formatting.

> An important quote
"""

blocks = markdown_to_blocks(markdown_content)
```

### From Dictionary

```python
from blocknote.converter import dict_to_blocks

dict_data = [
    {
        "id": "1",
        "type": "paragraph",
        "props": {},
        "content": [
            {
                "type": "text",
                "text": "Hello from dictionary!",
                "styles": {}
            }
        ],
        "children": []
    }
]

blocks = dict_to_blocks(dict_data)
```

## Error Handling

Always wrap converter calls in try-catch blocks:

```python
from blocknote.converter import blocks_to_html
from pydantic import ValidationError

try:
    html = blocks_to_html(blocks)
except TypeError as e:
    print(f"Invalid input type: {e}")
except ValueError as e:
    print(f"Invalid block structure: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Best Practices

### 1. Use Unique IDs

Always provide unique IDs for your blocks:

```python
import uuid

block = Block(
    id=str(uuid.uuid4()),  # Generate unique ID
    type="paragraph",
    content=[InlineContent(type="text", text="Content")]
)
```

### 2. Validate Input Data

Use Pydantic's validation features:

```python
from pydantic import ValidationError

try:
    block = Block(
        id="test",
        type="paragraph",
        content="This should be a list"  # Will cause validation error
    )
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### 3. Handle Empty Content

Check for empty content before processing:

```python
def safe_convert_to_html(blocks):
    if not blocks:
        return ""
    
    # Filter out blocks with no content
    valid_blocks = [
        block for block in blocks 
        if block.content or block.children
    ]
    
    return blocks_to_html(valid_blocks)
```

### 4. Preserve Formatting

When converting between formats, be aware of what formatting is preserved:

```python
# HTML preserves all formatting
html = blocks_to_html(blocks)

# Markdown preserves basic formatting only
markdown = blocks_to_markdown(blocks)  # Colors will be lost

# Dictionary preserves everything
dict_data = blocks_to_dict(blocks)
```

## Common Patterns

### Building a Document

```python
def create_document(title, sections):
    blocks = []
    
    # Add title
    blocks.append(Block(
        id="title",
        type="heading",
        props={"level": 1},
        content=[InlineContent(type="text", text=title)]
    ))
    
    # Add sections
    for i, (section_title, content) in enumerate(sections):
        # Section heading
        blocks.append(Block(
            id=f"section-{i}",
            type="heading",
            props={"level": 2},
            content=[InlineContent(type="text", text=section_title)]
        ))
        
        # Section content
        blocks.append(Block(
            id=f"content-{i}",
            type="paragraph",
            content=[InlineContent(type="text", text=content)]
        ))
    
    return blocks

# Usage
document = create_document(
    "My Report",
    [
        ("Introduction", "This is the introduction."),
        ("Methodology", "This describes our methods."),
        ("Results", "Here are the results.")
    ]
)

html = blocks_to_html(document)
```

### Processing User Input

```python
def process_user_content(user_html):
    try:
        # Parse HTML from user
        blocks = html_to_blocks(user_html)
        
        # Process blocks (e.g., sanitize, validate)
        processed_blocks = []
        for block in blocks:
            if block.type in ["paragraph", "heading", "quote"]:
                processed_blocks.append(block)
        
        # Convert back to clean HTML
        return blocks_to_html(processed_blocks)
        
    except Exception as e:
        print(f"Error processing content: {e}")
        return "<p>Invalid content</p>"
```

## Next Steps

- Explore [Converter Documentation](../converters/overview.md) for detailed converter information
- Check out [Examples](../examples/basic.md) for real-world use cases
- Review [API Reference](../api/schema.md) for complete API documentation
