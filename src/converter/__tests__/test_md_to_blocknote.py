import pytest
from blocknote.converter.md_to_blocknote import markdown_to_blocks
from blocknote.schema import Block, InlineContent


@pytest.fixture
def sample_markdown():
    """Fixture providing sample markdown for testing."""
    return "# Hello, world!\n\nThis is a paragraph."


@pytest.fixture
def complex_markdown():
    """Fixture providing complex markdown."""
    return """# Main Heading

This is the first paragraph.

## Sub Heading

This is the second paragraph.

- List item 1
- List item 2

1. Numbered item 1
2. Numbered item 2
"""


def test_markdown_to_blocks_basic(sample_markdown):
    """Test basic markdown to blocks conversion."""
    blocks = markdown_to_blocks(sample_markdown)
    assert len(blocks) == 2
    assert blocks[0].type == "heading"
    assert blocks[0].props["level"] == 1
    assert blocks[0].content[0].text == "Hello, world!"
    assert blocks[1].type == "paragraph"
    assert blocks[1].content[0].text == "This is a paragraph."


def test_markdown_to_blocks_complex(complex_markdown):
    """Test conversion of complex markdown."""
    blocks = markdown_to_blocks(complex_markdown)

    assert len(blocks) >= 4

    assert blocks[0].type == "heading"
    assert blocks[0].props["level"] == 1
    assert blocks[0].content[0].text == "Main Heading"


def test_markdown_to_blocks_empty():
    """Test conversion of empty markdown."""
    blocks = markdown_to_blocks("")
    assert blocks == []


def test_markdown_to_blocks_only_text():
    """Test conversion of plain text."""
    blocks = markdown_to_blocks("Just some plain text")
    assert len(blocks) == 1
    assert blocks[0].type == "paragraph"
    assert blocks[0].content[0].text == "Just some plain text"


@pytest.mark.parametrize(
    "markdown_input,expected_types",
    [
        ("# Heading", ["heading"]),
        ("Paragraph text", ["paragraph"]),
        ("# H1\n\n## H2", ["heading", "heading"]),
        ("- Item 1\n- Item 2", ["bulletListItem"]),
        ("1. Item 1\n2. Item 2", ["numberedListItem"]),
    ],
)
def test_markdown_to_blocks_types(markdown_input, expected_types):
    """Test that different markdown elements produce correct block types."""
    blocks = markdown_to_blocks(markdown_input)
    actual_types = [block.type for block in blocks]
    for expected_type in expected_types:
        assert expected_type in actual_types


@pytest.mark.parametrize(
    "markdown_input,expected_types",
    [
        ("```code```", ["paragraph"]),
        ("> Quote", ["quote"]),
        ("# H1\n\n> Quote\n\n**bold**", ["heading", "quote", "paragraph"]),
    ],
)
def test_markdown_to_blocks_new_types(markdown_input, expected_types):
    """Test that new markdown elements produce correct block types."""
    blocks = markdown_to_blocks(markdown_input)
    actual_types = [block.type for block in blocks]
    for expected_type in expected_types:
        assert expected_type in actual_types


def test_markdown_to_blocks_quote():
    """Test parsing blockquotes."""
    md = "> This is a wise quote"
    blocks = markdown_to_blocks(md)
    assert len(blocks) == 1
    assert blocks[0].type == "quote"
    assert len(blocks[0].content) > 0
    content_text = "".join([item.text for item in blocks[0].content if hasattr(item, "text")])
    assert "wise quote" in content_text


def test_markdown_to_blocks_unique_ids(sample_markdown):
    """Test that all blocks have unique IDs."""
    blocks = markdown_to_blocks(sample_markdown)
    ids = [block.id for block in blocks]
    assert len(ids) == len(set(ids))
