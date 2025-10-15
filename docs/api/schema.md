# Schema API Reference

The schema module defines the core data structures used throughout BlockNote-py.

## Classes

::: blocknote.schema.Block

::: blocknote.schema.InlineContent

## Enums

::: blocknote.schema.BlockType

::: blocknote.schema.InlineContentType


## Usage Examples

### Creating Blocks

```python
from blocknote.schema import Block, InlineContent, BlockType, InlineContentType

# Simple paragraph
paragraph = Block(
    id="para-1",
    type=BlockType.PARAGRAPH,
    content=[
        InlineContent(
            type=InlineContentType.TEXT,
            text="Hello, World!",
            styles={}
        )
    ]
)

# Heading with styling
heading = Block(
    id="heading-1",
    type=BlockType.HEADING,
    props={"level": 1},
    content=[
        InlineContent(
            type=InlineContentType.TEXT,
            text="Document Title",
            styles={"bold": True}
        )
    ]
)

# List with children
list_item = Block(
    id="list-1",
    type=BlockType.BULLET_LIST_ITEM,
    content=[
        InlineContent(
            type=InlineContentType.TEXT,
            text="Parent item"
        )
    ],
    children=[
        Block(
            id="list-1-1",
            type=BlockType.PARAGRAPH,
            content=[
                InlineContent(
                    type=InlineContentType.TEXT,
                    text="Child item"
                )
            ]
        )
    ]
)
```

### Working with Styles

```python
# Text with multiple styles
styled_content = InlineContent(
    type=InlineContentType.TEXT,
    text="Styled text",
    styles={
        "bold": True,
        "italic": True,
        "textColor": "#ff0000",
        "backgroundColor": "#ffff00"
    }
)

# Block with styled content
styled_block = Block(
    id="styled-1",
    type=BlockType.PARAGRAPH,
    content=[styled_content]
)
```

### Validation

All schema classes use Pydantic for validation:

```python
from pydantic import ValidationError

try:
    # This will raise a validation error
    invalid_block = Block(
        id="invalid",
        type="invalid_type",  # Not a valid BlockType
        content=[]
    )
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Type Definitions

### Block Properties

Different block types support different properties:

| Block Type | Supported Props | Example |
|------------|-----------------|---------|
| `heading` | `level` (1-6) | `{"level": 2}` |
| `checkListItem` | `checked` (bool) | `{"checked": True}` |
| `paragraph` | `textAlignment` | `{"textAlignment": "center"}` |

### Style Properties

Inline content supports various styling options:

| Style Property | Type | Description | Example |
|----------------|------|-------------|---------|
| `bold` | `bool` | Bold text | `{"bold": True}` |
| `italic` | `bool` | Italic text | `{"italic": True}` |
| `underline` | `bool` | Underlined text | `{"underline": True}` |
| `strike` | `bool` | Strikethrough text | `{"strike": True}` |
| `code` | `bool` | Inline code formatting | `{"code": True}` |
| `textColor` | `str` | Text color (CSS color) | `{"textColor": "#ff0000"}` |
| `backgroundColor` | `str` | Background color | `{"backgroundColor": "#ffff00"}` |
