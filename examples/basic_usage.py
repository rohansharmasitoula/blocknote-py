"""
Basic usage examples for blocknote-py.

This script demonstrates the core functionality of the blocknote-py library.
"""

from blocknote.converter import (
    blocks_to_dict,
    blocks_to_markdown,
    dict_to_blocks,
    markdown_to_blocks,
)
from blocknote.schema import Block, InlineContent


def example_dict_to_blocks():
    """Convert dictionaries to Block objects."""
    print("=" * 60)
    print("Example 1: Dictionary to Blocks")
    print("=" * 60)

    data = [
        {
            "id": "1",
            "type": "heading",
            "props": {"level": 1},
            "content": [{"type": "text", "text": "Welcome to Blocknote-py"}],
        },
        {
            "id": "2",
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "This is a "},
                {"type": "text", "text": "paragraph", "styles": {"bold": True}},
                {"type": "text", "text": " with "},
                {"type": "text", "text": "styled text", "styles": {"italic": True}},
                {"type": "text", "text": "."},
            ],
        },
    ]

    blocks = dict_to_blocks(data)

    print(f"\nConverted {len(blocks)} blocks:")
    for block in blocks:
        print(f"  - {block.type}: {block.id}")

    print("\nFirst block content:")
    for content in blocks[0].content:
        print(f"  - {content.text}")


def example_markdown_to_blocks():
    """Parse markdown into Block objects."""
    print("\n" + "=" * 60)
    print("Example 2: Markdown to Blocks")
    print("=" * 60)

    markdown = """# Hello World

This is a paragraph with **bold** and *italic* text.

## Features

- Easy to use
- Type-safe
- Well tested

### Getting Started

1. Install the package
2. Import the functions
3. Start converting!

> This is a quote block
"""

    blocks = markdown_to_blocks(markdown)

    print(f"\nParsed {len(blocks)} blocks from markdown:")
    for i, block in enumerate(blocks, 1):
        print(f"  {i}. {block.type}")


def example_blocks_to_markdown():
    """Convert Block objects to markdown."""
    print("\n" + "=" * 60)
    print("Example 3: Blocks to Markdown")
    print("=" * 60)

    blocks = [
        Block(
            id="1",
            type="heading",
            props={"level": 1},
            content=[InlineContent(type="text", text="My Document")],
            children=[],
        ),
        Block(
            id="2",
            type="paragraph",
            content=[
                InlineContent(type="text", text="This is "),
                InlineContent(type="text", text="important", styles={"bold": True}),
                InlineContent(type="text", text=" text."),
            ],
            children=[],
        ),
        Block(
            id="3",
            type="bulletListItem",
            content=[],
            children=[
                Block(
                    id="3.1",
                    type="paragraph",
                    content=[InlineContent(type="text", text="First item")],
                    children=[],
                ),
                Block(
                    id="3.2",
                    type="paragraph",
                    content=[InlineContent(type="text", text="Second item")],
                    children=[],
                ),
            ],
        ),
    ]

    markdown = blocks_to_markdown(blocks)

    print("\nGenerated markdown:")
    print("-" * 40)
    print(markdown)
    print("-" * 40)


def example_blocks_to_dict():
    """Convert Block objects to dictionaries."""
    print("\n" + "=" * 60)
    print("Example 4: Blocks to Dictionary")
    print("=" * 60)

    blocks = [
        Block(
            id="unique-1",
            type="paragraph",
            content="Simple text content",
            children=[],
        ),
        Block(
            id="unique-2",
            type="heading",
            props={"level": 2},
            content=[InlineContent(type="text", text="Section Title")],
            children=[],
        ),
    ]

    dict_data = blocks_to_dict(blocks)

    print("\nConverted blocks to dictionaries:")
    for item in dict_data:
        print(f"  - ID: {item['id']}, Type: {item['type']}")


def example_roundtrip():
    """Demonstrate roundtrip conversion."""
    print("\n" + "=" * 60)
    print("Example 5: Roundtrip Conversion")
    print("=" * 60)

    # Start with markdown
    original_markdown = """# Title

This is **bold** text."""

    print("Original markdown:")
    print(original_markdown)

    # Convert to blocks
    blocks = markdown_to_blocks(original_markdown)
    print(f"\nConverted to {len(blocks)} blocks")

    # Convert to dict
    dict_data = blocks_to_dict(blocks)
    print(f"Converted to {len(dict_data)} dictionaries")

    # Convert back to blocks
    blocks_again = dict_to_blocks(dict_data)
    print(f"Converted back to {len(blocks_again)} blocks")

    # Convert to markdown
    final_markdown = blocks_to_markdown(blocks_again)
    print("\nFinal markdown:")
    print(final_markdown)

    print("\nRoundtrip successful!" if final_markdown.strip() else "Roundtrip failed!")


def main():
    """Run all examples."""
    example_dict_to_blocks()
    example_markdown_to_blocks()
    example_blocks_to_markdown()
    example_blocks_to_dict()
    example_roundtrip()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
