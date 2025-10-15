# Dictionary to BlockNote Converter

The `dict_to_blocks()` function converts Python dictionaries into BlockNote blocks.

## Function Signature

```python
def dict_to_blocks(data: List[Dict[str, Any]]) -> List[Block]
```

## Parameters

- **data** (`List[Dict[str, Any]]`): List of dictionaries representing blocks

## Returns

- **List[Block]**: List of validated BlockNote Block objects

## Basic Usage

```python
from blocknote.converter import dict_to_blocks

data = [
    {
        "id": "1",
        "type": "paragraph",
        "props": {},
        "content": [
            {
                "type": "text",
                "text": "Hello, World!",
                "styles": {}
            }
        ],
        "children": []
    }
]

blocks = dict_to_blocks(data)
print(blocks[0].content[0].text)  # "Hello, World!"
```

## Dictionary Format

Each dictionary must contain:

- **id**: Unique string identifier
- **type**: Block type (paragraph, heading, etc.)
- **props**: Block properties (optional)
- **content**: List of content objects or string
- **children**: List of child block dictionaries (optional)

## Validation

The converter validates:
- Required fields are present
- Block types are valid
- Content structure is correct
- Nested children are properly formatted

## Error Handling

```python
try:
    blocks = dict_to_blocks(data)
except ValueError as e:
    print(f"Validation failed: {e}")
```

## See Also

- [BlockNote to Dictionary Converter](blocknote-to-dict.md)
- [API Reference](../api/converters.md)
