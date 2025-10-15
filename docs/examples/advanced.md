# Advanced Examples

This page provides advanced usage examples and patterns for BlockNote-py.

## Custom Block Processing Pipeline

Create a processing pipeline that validates, transforms, and converts blocks:

```python
from typing import List, Callable
from blocknote.schema import Block, InlineContent
from blocknote.converter import blocks_to_html, html_to_blocks

class BlockProcessor:
    def __init__(self):
        self.processors: List[Callable[[List[Block]], List[Block]]] = []
    
    def add_processor(self, processor: Callable[[List[Block]], List[Block]]):
        """Add a processing function to the pipeline."""
        self.processors.append(processor)
        return self
    
    def process(self, blocks: List[Block]) -> List[Block]:
        """Run all processors in sequence."""
        result = blocks
        for processor in self.processors:
            result = processor(result)
        return result

# Example processors
def remove_empty_blocks(blocks: List[Block]) -> List[Block]:
    """Remove blocks with no content."""
    return [block for block in blocks if block.content]

def sanitize_content(blocks: List[Block]) -> List[Block]:
    """Remove potentially unsafe content."""
    safe_blocks = []
    for block in blocks:
        if block.type in ['paragraph', 'heading', 'quote']:
            safe_blocks.append(block)
    return safe_blocks

def add_ids_if_missing(blocks: List[Block]) -> List[Block]:
    """Add UUIDs to blocks that don't have IDs."""
    import uuid
    for block in blocks:
        if not block.id:
            block.id = str(uuid.uuid4())
    return blocks

# Usage
processor = BlockProcessor()
processor.add_processor(remove_empty_blocks)
processor.add_processor(sanitize_content)
processor.add_processor(add_ids_if_missing)

# Process blocks
processed_blocks = processor.process(original_blocks)
```

## Multi-Format Document Converter

Convert documents between multiple formats with format detection:

```python
import re
from pathlib import Path
from typing import Union, List
from blocknote.converter import *
from blocknote.schema import Block

class DocumentConverter:
    def __init__(self):
        self.format_detectors = {
            'html': self._is_html,
            'markdown': self._is_markdown,
            'json': self._is_json
        }
    
    def _is_html(self, content: str) -> bool:
        return bool(re.search(r'<[^>]+>', content))
    
    def _is_markdown(self, content: str) -> bool:
        return bool(re.search(r'^#{1,6}\s|^\*\s|^\d+\.\s|^\>', content, re.MULTILINE))
    
    def _is_json(self, content: str) -> bool:
        return content.strip().startswith('[') and content.strip().endswith(']')
    
    def detect_format(self, content: str) -> str:
        """Auto-detect the format of input content."""
        for format_name, detector in self.format_detectors.items():
            if detector(content):
                return format_name
        return 'text'
    
    def to_blocks(self, content: str, source_format: str = None) -> List[Block]:
        """Convert content to BlockNote blocks."""
        if source_format is None:
            source_format = self.detect_format(content)
        
        if source_format == 'html':
            return html_to_blocks(content)
        elif source_format == 'markdown':
            return markdown_to_blocks(content)
        elif source_format == 'json':
            import json
            return dict_to_blocks(json.loads(content))
        else:
            # Treat as plain text
            return [Block(
                id="text-1",
                type="paragraph",
                content=[InlineContent(type="text", text=content)]
            )]
    
    def convert(self, content: str, target_format: str, source_format: str = None) -> str:
        """Convert content from one format to another."""
        blocks = self.to_blocks(content, source_format)
        
        if target_format == 'html':
            return blocks_to_html(blocks)
        elif target_format == 'markdown':
            return blocks_to_markdown(blocks)
        elif target_format == 'json':
            import json
            return json.dumps(blocks_to_dict(blocks), indent=2)
        else:
            raise ValueError(f"Unsupported target format: {target_format}")
    
    def convert_file(self, input_path: Union[str, Path], output_path: Union[str, Path], 
                    target_format: str = None):
        """Convert a file from one format to another."""
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        # Auto-detect target format from extension if not provided
        if target_format is None:
            ext_map = {'.html': 'html', '.md': 'markdown', '.json': 'json'}
            target_format = ext_map.get(output_path.suffix, 'html')
        
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert
        converted = self.convert(content, target_format)
        
        # Write output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(converted)

# Usage
converter = DocumentConverter()

# Auto-detect and convert
html_content = "<h1>Title</h1><p>Content</p>"
markdown = converter.convert(html_content, 'markdown')
print(markdown)

# Convert files
converter.convert_file('document.html', 'document.md')
```

## Content Validation and Sanitization

Advanced content validation with custom rules:

```python
from typing import List, Dict, Any, Optional
from blocknote.schema import Block, InlineContent
from blocknote.converter import blocks_to_html

class ContentValidator:
    def __init__(self):
        self.allowed_block_types = {
            'paragraph', 'heading', 'bulletListItem', 
            'numberedListItem', 'quote'
        }
        self.allowed_styles = {
            'bold', 'italic', 'underline'
        }
        self.max_heading_level = 6
        self.max_content_length = 1000
    
    def validate_block(self, block: Block) -> Dict[str, Any]:
        """Validate a single block and return validation results."""
        issues = []
        
        # Check block type
        if block.type not in self.allowed_block_types:
            issues.append(f"Block type '{block.type}' not allowed")
        
        # Check heading level
        if block.type == 'heading':
            level = block.props.get('level', 1)
            if level > self.max_heading_level:
                issues.append(f"Heading level {level} exceeds maximum {self.max_heading_level}")
        
        # Check content length
        total_text = ''.join(
            item.text for item in block.content 
            if isinstance(item, InlineContent)
        )
        if len(total_text) > self.max_content_length:
            issues.append(f"Content length {len(total_text)} exceeds maximum {self.max_content_length}")
        
        # Check styles
        for item in block.content:
            if isinstance(item, InlineContent):
                invalid_styles = set(item.styles.keys()) - self.allowed_styles
                if invalid_styles:
                    issues.append(f"Invalid styles: {invalid_styles}")
        
        return {
            'block_id': block.id,
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def validate_blocks(self, blocks: List[Block]) -> Dict[str, Any]:
        """Validate a list of blocks."""
        results = []
        total_issues = 0
        
        for block in blocks:
            result = self.validate_block(block)
            results.append(result)
            if not result['valid']:
                total_issues += len(result['issues'])
        
        return {
            'valid': total_issues == 0,
            'total_blocks': len(blocks),
            'total_issues': total_issues,
            'results': results
        }
    
    def sanitize_blocks(self, blocks: List[Block]) -> List[Block]:
        """Sanitize blocks by removing invalid content."""
        sanitized = []
        
        for block in blocks:
            if block.type not in self.allowed_block_types:
                # Convert to paragraph
                block.type = 'paragraph'
            
            # Sanitize content
            clean_content = []
            for item in block.content:
                if isinstance(item, InlineContent):
                    # Filter styles
                    clean_styles = {
                        k: v for k, v in item.styles.items()
                        if k in self.allowed_styles
                    }
                    
                    # Truncate text if too long
                    text = item.text
                    if len(text) > self.max_content_length:
                        text = text[:self.max_content_length] + "..."
                    
                    clean_content.append(InlineContent(
                        type=item.type,
                        text=text,
                        styles=clean_styles
                    ))
            
            # Create sanitized block
            sanitized_block = Block(
                id=block.id,
                type=block.type,
                props=block.props,
                content=clean_content,
                children=[]  # Remove children for simplicity
            )
            sanitized.append(sanitized_block)
        
        return sanitized

# Usage
validator = ContentValidator()

# Validate blocks
validation_result = validator.validate_blocks(blocks)
if not validation_result['valid']:
    print(f"Found {validation_result['total_issues']} issues")
    for result in validation_result['results']:
        if not result['valid']:
            print(f"Block {result['block_id']}: {result['issues']}")

# Sanitize blocks
clean_blocks = validator.sanitize_blocks(blocks)
```

## Performance Optimization

Optimize processing for large documents:

```python
import time
from typing import List, Iterator
from blocknote.schema import Block
from blocknote.converter import blocks_to_html

class PerformantProcessor:
    def __init__(self, chunk_size: int = 100):
        self.chunk_size = chunk_size
    
    def chunk_blocks(self, blocks: List[Block]) -> Iterator[List[Block]]:
        """Split blocks into smaller chunks for processing."""
        for i in range(0, len(blocks), self.chunk_size):
            yield blocks[i:i + self.chunk_size]
    
    def process_large_document(self, blocks: List[Block]) -> str:
        """Process large documents in chunks."""
        html_parts = []
        
        for chunk in self.chunk_blocks(blocks):
            start_time = time.time()
            html_chunk = blocks_to_html(chunk)
            html_parts.append(html_chunk)
            
            processing_time = time.time() - start_time
            print(f"Processed {len(chunk)} blocks in {processing_time:.2f}s")
        
        return '\n'.join(html_parts)
    
    def benchmark_conversion(self, blocks: List[Block], iterations: int = 5):
        """Benchmark conversion performance."""
        times = []
        
        for i in range(iterations):
            start_time = time.time()
            blocks_to_html(blocks)
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = sum(times) / len(times)
        print(f"Average conversion time: {avg_time:.4f}s")
        print(f"Blocks per second: {len(blocks) / avg_time:.0f}")
        
        return {
            'average_time': avg_time,
            'blocks_per_second': len(blocks) / avg_time,
            'all_times': times
        }

# Usage
processor = PerformantProcessor(chunk_size=50)

# Process large document
large_blocks = [create_sample_block() for _ in range(1000)]
html_result = processor.process_large_document(large_blocks)

# Benchmark performance
benchmark_results = processor.benchmark_conversion(large_blocks)
```

## Integration with Web Frameworks

Example integration with FastAPI:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from blocknote.converter import *
from blocknote.schema import Block

app = FastAPI(title="BlockNote Converter API")

class ConversionRequest(BaseModel):
    content: str
    source_format: str
    target_format: str

class BlocksRequest(BaseModel):
    blocks: List[Dict[str, Any]]

@app.post("/convert")
async def convert_content(request: ConversionRequest):
    """Convert content between formats."""
    try:
        # Convert to blocks first
        if request.source_format == 'html':
            blocks = html_to_blocks(request.content)
        elif request.source_format == 'markdown':
            blocks = markdown_to_blocks(request.content)
        elif request.source_format == 'json':
            import json
            blocks = dict_to_blocks(json.loads(request.content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported source format")
        
        # Convert to target format
        if request.target_format == 'html':
            result = blocks_to_html(blocks)
        elif request.target_format == 'markdown':
            result = blocks_to_markdown(blocks)
        elif request.target_format == 'json':
            import json
            result = json.dumps(blocks_to_dict(blocks))
        else:
            raise HTTPException(status_code=400, detail="Unsupported target format")
        
        return {"result": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/blocks/to-html")
async def blocks_to_html_endpoint(request: BlocksRequest):
    """Convert blocks to HTML."""
    try:
        blocks = dict_to_blocks(request.blocks)
        html = blocks_to_html(blocks)
        return {"html": html}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/html/to-blocks")
async def html_to_blocks_endpoint(html: str):
    """Convert HTML to blocks."""
    try:
        blocks = html_to_blocks(html)
        return {"blocks": blocks_to_dict(blocks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

These advanced examples demonstrate sophisticated usage patterns that can be adapted for production applications.

## Next Steps

- Review [Basic Examples](basic.md) for simpler use cases
- Check [API Reference](../api/schema.md) for detailed documentation
- Explore [Contributing Guide](../contributing.md) to add your own examples
