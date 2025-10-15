# BlockNote to Markdown Converter

The `blocks_to_markdown()` function converts BlockNote blocks into Markdown format.

## Function Signature

```python
def blocks_to_markdown(blocks: List[Block]) -> str
```

## Parameters

- **blocks** (`List[Block]`): A list of BlockNote Block objects to convert

## Returns

- **str**: Markdown string representation of the blocks

## Basic Usage

```python
from blocknote.converter import blocks_to_markdown
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
        content=[
            InlineContent(type="text", text="This is "),
            InlineContent(type="text", text="bold", styles={"bold": True}),
            InlineContent(type="text", text=" text.")
        ]
    )
]

markdown = blocks_to_markdown(blocks)
print(markdown)
```

**Output:**
```markdown
# My Document

This is **bold** text.
```

## Supported Block Types

- **Headings**: Converted to `#` syntax (H1-H6)
- **Paragraphs**: Plain text paragraphs
- **Bullet Lists**: Converted to `*` list items
- **Numbered Lists**: Converted to `1.` list items
- **Quotes**: Converted to `>` blockquotes

## Supported Styling

- **Bold**: `**text**`
- **Italic**: `*text*`

## See Also

- [Markdown to BlockNote Converter](markdown-to-blocknote.md)
- [API Reference](../api/converters.md)
