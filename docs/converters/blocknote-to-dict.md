# BlockNote to Dictionary Converter

The `blocks_to_dict()` function converts BlockNote blocks into Python dictionary format.

## Function Signature

```python
def blocks_to_dict(blocks: List[Block]) -> List[Dict[str, Any]]
```

## Parameters

- **blocks** (`List[Block]`): A list of BlockNote Block objects to convert

## Returns

- **List[Dict[str, Any]]**: List of dictionaries representing the blocks

## Basic Usage

```python
from blocknote.converter import blocks_to_dict
from blocknote.schema import Block, InlineContent

block = Block(
    id="1",
    type="paragraph",
    content=[
        InlineContent(type="text", text="Hello, World!")
    ]
)

data = blocks_to_dict([block])
print(data)
```

**Output:**
```python
[
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
```

## Use Cases

- **API Integration**: Send BlockNote data to REST APIs
- **Database Storage**: Store structured block data
- **Serialization**: Convert blocks for JSON storage
- **Data Processing**: Manipulate block data programmatically

## See Also

- [Dictionary to BlockNote Converter](dict-to-blocknote.md)
- [API Reference](../api/converters.md)
