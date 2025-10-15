# Converters API Reference

Complete API reference for all BlockNote-py converters.

## HTML Converters

::: blocknote.converter.blocks_to_html

::: blocknote.converter.html_to_blocks

## Markdown Converters

::: blocknote.converter.blocks_to_markdown

::: blocknote.converter.markdown_to_blocks

## Dictionary Converters

::: blocknote.converter.blocks_to_dict

::: blocknote.converter.dict_to_blocks

## Usage Examples

### HTML Conversion

```python
from blocknote.converter import blocks_to_html, html_to_blocks
from blocknote.schema import Block, InlineContent

# Create a block
block = Block(
    id="example",
    type="paragraph",
    content=[
        InlineContent(
            type="text",
            text="Hello, World!",
            styles={"bold": True}
        )
    ]
)

# Convert to HTML
html = blocks_to_html([block])
print(html)  # <p><strong>Hello, World!</strong></p>

# Convert back to blocks
blocks = html_to_blocks(html)
print(blocks[0].content[0].text)  # Hello, World!
```

### Markdown Conversion

```python
from blocknote.converter import blocks_to_markdown, markdown_to_blocks

# Convert blocks to Markdown
markdown = blocks_to_markdown([block])
print(markdown)  # **Hello, World!**

# Convert Markdown to blocks
md_text = "# Heading\n\nThis is **bold** text."
blocks = markdown_to_blocks(md_text)
```

### Dictionary Conversion

```python
from blocknote.converter import blocks_to_dict, dict_to_blocks

# Convert to dictionary
block_dict = blocks_to_dict([block])
print(block_dict)

# Convert back to blocks
blocks = dict_to_blocks(block_dict)
```

## Error Handling

All converters raise appropriate exceptions for invalid input:

```python
from blocknote.converter import blocks_to_html
from pydantic import ValidationError

try:
    html = blocks_to_html("invalid input")
except TypeError as e:
    print(f"Type error: {e}")

try:
    html = blocks_to_html([{"invalid": "block"}])
except TypeError as e:
    print(f"Invalid block: {e}")
```

## Type Definitions

### Function Signatures

```python
def blocks_to_html(blocks: List[Block]) -> str: ...
def html_to_blocks(html: str) -> List[Block]: ...
def blocks_to_markdown(blocks: List[Block]) -> str: ...
def markdown_to_blocks(markdown: str) -> List[Block]: ...
def blocks_to_dict(blocks: List[Block]) -> List[Dict[str, Any]]: ...
def dict_to_blocks(data: List[Dict[str, Any]]) -> List[Block]: ...
```

### Common Exceptions

- **TypeError**: Invalid input type
- **ValueError**: Invalid data structure or content
- **ValidationError**: Pydantic validation failure

## Performance Considerations

### Memory Usage

- Large documents may consume significant memory
- Consider processing in batches for very large datasets

### Processing Time

- Complex nested structures take longer to process
- HTML parsing is generally slower than dictionary conversion
- Markdown parsing requires additional dependencies

### Optimization Tips

1. **Batch Processing**: Process multiple blocks at once
2. **Caching**: Cache converted results when possible
3. **Validation**: Pre-validate input data to avoid processing errors
4. **Memory Management**: Use generators for large datasets

## Best Practices

### Input Validation

```python
def safe_convert(blocks):
    if not isinstance(blocks, list):
        raise TypeError("Input must be a list")
    
    if not all(isinstance(b, Block) for b in blocks):
        raise TypeError("All items must be Block objects")
    
    return blocks_to_html(blocks)
```

### Error Recovery

```python
def robust_html_conversion(blocks):
    try:
        return blocks_to_html(blocks)
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return "<p>Content unavailable</p>"
```

### Performance Monitoring

```python
import time
from functools import wraps

def time_conversion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@time_conversion
def convert_large_document(blocks):
    return blocks_to_html(blocks)
```
