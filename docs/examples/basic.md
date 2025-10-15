# Basic Examples

This page provides practical examples of using BlockNote-py in real-world scenarios.

## Example 1: Blog Post Converter

Convert a blog post from HTML to BlockNote and then to Markdown:

```python
from blocknote.converter import html_to_blocks, blocks_to_markdown

# Sample blog post HTML
blog_html = """
<h1>Getting Started with Python</h1>
<p>Python is a <strong>powerful</strong> and <em>versatile</em> programming language.</p>
<h2>Why Choose Python?</h2>
<ul>
    <li>Easy to learn</li>
    <li>Large community</li>
    <li>Extensive libraries</li>
</ul>
<blockquote>
    "Python is executable pseudocode." - Bruce Eckel
</blockquote>
<p>Ready to start your Python journey?</p>
"""

# Convert HTML to BlockNote blocks
blocks = html_to_blocks(blog_html)

# Convert to Markdown for documentation
markdown = blocks_to_markdown(blocks)
print(markdown)
```

**Output:**
```markdown
# Getting Started with Python

Python is a **powerful** and *versatile* programming language.

## Why Choose Python?

* Easy to learn
* Large community
* Extensive libraries

> "Python is executable pseudocode." - Bruce Eckel

Ready to start your Python journey?
```

## Example 2: Content Management System

Create a simple CMS that stores content as BlockNote blocks:

```python
import json
from typing import List
from blocknote.schema import Block, InlineContent
from blocknote.converter import blocks_to_dict, dict_to_blocks, blocks_to_html

class SimpleCMS:
    def __init__(self):
        self.content_store = {}
    
    def create_article(self, article_id: str, title: str, content_blocks: List[Block]):
        """Store an article as BlockNote blocks."""
        article_data = {
            "title": title,
            "blocks": blocks_to_dict(content_blocks),
            "created_at": "2024-01-01"  # In real app, use datetime
        }
        self.content_store[article_id] = article_data
    
    def get_article_html(self, article_id: str) -> str:
        """Retrieve article and convert to HTML."""
        if article_id not in self.content_store:
            return "<p>Article not found</p>"
        
        article = self.content_store[article_id]
        blocks = dict_to_blocks(article["blocks"])
        
        # Add title as H1
        title_block = Block(
            id="title",
            type="heading",
            props={"level": 1},
            content=[InlineContent(type="text", text=article["title"])]
        )
        
        all_blocks = [title_block] + blocks
        return blocks_to_html(all_blocks)
    
    def export_to_json(self, filename: str):
        """Export all content to JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.content_store, f, indent=2)

# Usage example
cms = SimpleCMS()

# Create article content
article_blocks = [
    Block(
        id="intro",
        type="paragraph",
        content=[
            InlineContent(type="text", text="Welcome to our "),
            InlineContent(type="text", text="amazing", styles={"bold": True}),
            InlineContent(type="text", text=" content management system!")
        ]
    ),
    Block(
        id="features",
        type="heading",
        props={"level": 2},
        content=[InlineContent(type="text", text="Features")]
    ),
    Block(
        id="feature-1",
        type="bulletListItem",
        content=[InlineContent(type="text", text="Easy content creation")]
    ),
    Block(
        id="feature-2",
        type="bulletListItem",
        content=[InlineContent(type="text", text="Multiple export formats")]
    )
]

# Store the article
cms.create_article("welcome-post", "Welcome to Our CMS", article_blocks)

# Retrieve as HTML
html_output = cms.get_article_html("welcome-post")
print(html_output)
```

## Example 3: Documentation Generator

Generate documentation from structured data:

```python
from blocknote.schema import Block, InlineContent
from blocknote.converter import blocks_to_html, blocks_to_markdown

def generate_api_docs(api_functions):
    """Generate documentation for API functions."""
    blocks = []
    
    # Title
    blocks.append(Block(
        id="title",
        type="heading",
        props={"level": 1},
        content=[InlineContent(type="text", text="API Documentation")]
    ))
    
    for func_name, func_info in api_functions.items():
        # Function name
        blocks.append(Block(
            id=f"func-{func_name}",
            type="heading",
            props={"level": 2},
            content=[
                InlineContent(type="text", text=func_name, styles={"code": True})
            ]
        ))
        
        # Description
        blocks.append(Block(
            id=f"desc-{func_name}",
            type="paragraph",
            content=[InlineContent(type="text", text=func_info["description"])]
        ))
        
        # Parameters
        if func_info.get("parameters"):
            blocks.append(Block(
                id=f"params-title-{func_name}",
                type="heading",
                props={"level": 3},
                content=[InlineContent(type="text", text="Parameters")]
            ))
            
            for param_name, param_info in func_info["parameters"].items():
                blocks.append(Block(
                    id=f"param-{func_name}-{param_name}",
                    type="bulletListItem",
                    content=[
                        InlineContent(type="text", text=param_name, styles={"bold": True}),
                        InlineContent(type="text", text=f" ({param_info['type']}): "),
                        InlineContent(type="text", text=param_info["description"])
                    ]
                ))
        
        # Example
        if func_info.get("example"):
            blocks.append(Block(
                id=f"example-title-{func_name}",
                type="heading",
                props={"level": 3},
                content=[InlineContent(type="text", text="Example")]
            ))
            
            blocks.append(Block(
                id=f"example-{func_name}",
                type="paragraph",
                content=[
                    InlineContent(
                        type="text", 
                        text=func_info["example"], 
                        styles={"code": True}
                    )
                ]
            ))
    
    return blocks

# Sample API data
api_data = {
    "blocks_to_html": {
        "description": "Converts BlockNote blocks to HTML format.",
        "parameters": {
            "blocks": {
                "type": "List[Block]",
                "description": "List of BlockNote blocks to convert"
            }
        },
        "example": "html = blocks_to_html([block1, block2])"
    },
    "html_to_blocks": {
        "description": "Parses HTML and converts to BlockNote blocks.",
        "parameters": {
            "html": {
                "type": "str",
                "description": "HTML string to parse"
            }
        },
        "example": "blocks = html_to_blocks('<p>Hello</p>')"
    }
}

# Generate documentation
doc_blocks = generate_api_docs(api_data)

# Output as HTML
html_docs = blocks_to_html(doc_blocks)
print("HTML Documentation:")
print(html_docs)

print("\n" + "="*50 + "\n")

# Output as Markdown
markdown_docs = blocks_to_markdown(doc_blocks)
print("Markdown Documentation:")
print(markdown_docs)
```

## Example 4: Rich Text Editor Backend

Handle rich text editor data on the backend:

```python
from flask import Flask, request, jsonify
from blocknote.converter import dict_to_blocks, blocks_to_html, html_to_blocks, blocks_to_dict

app = Flask(__name__)

# In-memory storage (use database in production)
documents = {}

@app.route('/api/documents', methods=['POST'])
def create_document():
    """Create a new document from BlockNote editor data."""
    try:
        data = request.json
        doc_id = data.get('id')
        blocks_data = data.get('blocks', [])
        
        # Convert to BlockNote blocks for validation
        blocks = dict_to_blocks(blocks_data)
        
        # Store as dictionary for easy serialization
        documents[doc_id] = {
            'blocks': blocks_to_dict(blocks),
            'html_cache': blocks_to_html(blocks)  # Cache HTML for quick retrieval
        }
        
        return jsonify({'success': True, 'id': doc_id})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/documents/<doc_id>/html', methods=['GET'])
def get_document_html(doc_id):
    """Get document as HTML."""
    if doc_id not in documents:
        return jsonify({'error': 'Document not found'}), 404
    
    return jsonify({'html': documents[doc_id]['html_cache']})

@app.route('/api/documents/<doc_id>/blocks', methods=['GET'])
def get_document_blocks(doc_id):
    """Get document as BlockNote blocks."""
    if doc_id not in documents:
        return jsonify({'error': 'Document not found'}), 404
    
    return jsonify({'blocks': documents[doc_id]['blocks']})

@app.route('/api/import/html', methods=['POST'])
def import_html():
    """Import HTML content and convert to BlockNote format."""
    try:
        html_content = request.json.get('html', '')
        blocks = html_to_blocks(html_content)
        blocks_data = blocks_to_dict(blocks)
        
        return jsonify({'blocks': blocks_data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

## Example 5: Content Migration Tool

Migrate content from one format to another:

```python
import os
import glob
from pathlib import Path
from blocknote.converter import html_to_blocks, blocks_to_markdown

def migrate_html_to_markdown(input_dir: str, output_dir: str):
    """Migrate all HTML files in a directory to Markdown via BlockNote."""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    html_files = input_path.glob("*.html")
    
    for html_file in html_files:
        print(f"Processing {html_file.name}...")
        
        try:
            # Read HTML file
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Convert HTML -> BlockNote -> Markdown
            blocks = html_to_blocks(html_content)
            markdown_content = blocks_to_markdown(blocks)
            
            # Write Markdown file
            output_file = output_path / f"{html_file.stem}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"✓ Converted to {output_file.name}")
            
        except Exception as e:
            print(f"✗ Error processing {html_file.name}: {e}")

# Usage
if __name__ == "__main__":
    migrate_html_to_markdown("./html_docs", "./markdown_docs")
```

## Example 6: Content Validation

Validate and clean user-generated content:

```python
from typing import List
from blocknote.schema import Block, InlineContent
from blocknote.converter import html_to_blocks, blocks_to_html

def sanitize_content(html_input: str) -> str:
    """Sanitize HTML content by converting through BlockNote."""
    
    # Allowed block types
    ALLOWED_BLOCKS = {
        "paragraph", "heading", "bulletListItem", 
        "numberedListItem", "quote"
    }
    
    # Allowed styles
    ALLOWED_STYLES = {
        "bold", "italic", "underline"
    }
    
    try:
        # Parse HTML to blocks
        blocks = html_to_blocks(html_input)
        
        # Filter and sanitize blocks
        clean_blocks = []
        for block in blocks:
            if block.type in ALLOWED_BLOCKS:
                # Clean the content
                clean_content = []
                for content_item in block.content:
                    if isinstance(content_item, InlineContent):
                        # Filter styles
                        clean_styles = {
                            k: v for k, v in content_item.styles.items()
                            if k in ALLOWED_STYLES
                        }
                        
                        clean_content.append(InlineContent(
                            type=content_item.type,
                            text=content_item.text,
                            styles=clean_styles
                        ))
                
                # Create clean block
                clean_block = Block(
                    id=block.id,
                    type=block.type,
                    props=block.props,
                    content=clean_content,
                    children=[]  # Remove children for simplicity
                )
                clean_blocks.append(clean_block)
        
        # Convert back to HTML
        return blocks_to_html(clean_blocks)
    
    except Exception as e:
        # Return safe fallback
        return f"<p>Content could not be processed: {str(e)}</p>"

# Test the sanitizer
unsafe_html = """
<h1>Title</h1>
<p>This is <strong>bold</strong> and <script>alert('xss')</script> text.</p>
<div style="color: red;">This div will be converted to paragraph</div>
<p style="background: yellow;">Styled paragraph</p>
"""

safe_html = sanitize_content(unsafe_html)
print("Sanitized HTML:")
print(safe_html)
```

These examples demonstrate practical applications of BlockNote-py in various scenarios. Each example can be adapted and extended based on your specific needs.

## Next Steps

- Explore [Advanced Examples](advanced.md) for more complex use cases
- Check the [API Reference](../api/schema.md) for detailed documentation
- Review [Converter Documentation](../converters/overview.md) for specific converter features
