# Quick Start

This guide will get you up and running with BlockNote-py in just a few minutes.

## Basic Conversion Example

Let's start with a simple example that demonstrates the core functionality:

```python
from blocknote.converter import blocks_to_html, html_to_blocks
from blocknote.schema import Block, InlineContent

# Create a BlockNote block
block = Block(
    id="example-1",
    type="heading",
    props={"level": 1},
    content=[
        InlineContent(
            type="text",
            text="Welcome to BlockNote-py!",
            styles={}
        )
    ]
)

# Convert to HTML
html = blocks_to_html([block])
print(html)
# Output: <h1>Welcome to BlockNote-py!</h1>

# Convert back to BlockNote blocks
blocks = html_to_blocks(html)
print(blocks[0].type)  # heading
print(blocks[0].props["level"])  # 1
print(blocks[0].content[0].text)  # Welcome to BlockNote-py!
```

## Working with Different Block Types

### Paragraphs with Styling

```python
from blocknote.converter import blocks_to_html
from blocknote.schema import Block, InlineContent

# Create a paragraph with mixed styling
block = Block(
    id="styled-paragraph",
    type="paragraph",
    content=[
        InlineContent(type="text", text="This is "),
        InlineContent(type="text", text="bold", styles={"bold": True}),
        InlineContent(type="text", text=" and this is "),
        InlineContent(type="text", text="italic", styles={"italic": True}),
        InlineContent(type="text", text=" text.")
    ]
)

html = blocks_to_html([block])
print(html)
# Output: <p>This is <strong>bold</strong> and this is <em>italic</em> text.</p>
```

### Lists

```python
# Bullet list
bullet_list = Block(
    id="bullet-1",
    type="bulletListItem",
    content=[InlineContent(type="text", text="First item")],
    children=[
        Block(
            id="bullet-1-1",
            type="paragraph",
            content=[InlineContent(type="text", text="Nested item")]
        )
    ]
)

# Numbered list
numbered_list = Block(
    id="numbered-1",
    type="numberedListItem",
    content=[InlineContent(type="text", text="First numbered item")]
)

html = blocks_to_html([bullet_list, numbered_list])
print(html)
```

### Quotes

```python
quote_block = Block(
    id="quote-1",
    type="quote",
    content=[
        InlineContent(
            type="text",
            text="The best way to predict the future is to invent it."
        )
    ]
)

html = blocks_to_html([quote_block])
print(html)
# Output: <blockquote>The best way to predict the future is to invent it.</blockquote>
```

## Converting from HTML

BlockNote-py can parse HTML and convert it back to BlockNote blocks:

```python
from blocknote.converter import html_to_blocks

html = """
<h1>Document Title</h1>
<p>This is a <strong>paragraph</strong> with <em>formatting</em>.</p>
<ul>
    <li>First bullet point</li>
    <li>Second bullet point</li>
</ul>
<blockquote>An inspiring quote</blockquote>
"""

blocks = html_to_blocks(html)

for block in blocks:
    print(f"Block type: {block.type}")
    if block.content:
        print(f"Content: {block.content[0].text}")
    print("---")
```

## Working with Markdown

Convert between BlockNote and Markdown:

```python
from blocknote.converter import blocks_to_markdown, markdown_to_blocks

# Create blocks
blocks = [
    Block(
        id="md-heading",
        type="heading",
        props={"level": 2},
        content=[InlineContent(type="text", text="Markdown Example")]
    ),
    Block(
        id="md-paragraph",
        type="paragraph",
        content=[
            InlineContent(type="text", text="This will be converted to "),
            InlineContent(type="text", text="Markdown", styles={"bold": True})
        ]
    )
]

# Convert to Markdown
markdown = blocks_to_markdown(blocks)
print(markdown)
# Output:
# ## Markdown Example
# 
# This will be converted to **Markdown**

# Convert back to blocks
converted_blocks = markdown_to_blocks(markdown)
```

## Working with Dictionaries

For integration with APIs or databases, you can convert blocks to/from dictionaries:

```python
from blocknote.converter import blocks_to_dict, dict_to_blocks

# Convert blocks to dictionary format
block_dict = blocks_to_dict([block])
print(block_dict)

# Convert back to blocks
blocks_from_dict = dict_to_blocks(block_dict)
```

## Next Steps

Now that you've seen the basics, explore more advanced features:

- [Basic Usage Guide](basic-usage.md) - More detailed examples
- [Converter Documentation](../converters/overview.md) - Deep dive into each converter
- [API Reference](../api/schema.md) - Complete API documentation
- [Examples](../examples/basic.md) - Real-world use cases
