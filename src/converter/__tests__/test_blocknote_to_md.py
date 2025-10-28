import pytest
from blocknote.converter.blocknote_to_md import blocks_to_markdown
from blocknote.schema import Block, InlineContent


@pytest.fixture
def sample_blocks():
    """Fixture providing sample blocks for testing."""
    return [
        Block(
            id="1",
            type="heading",
            props={"level": 1},
            content=[InlineContent(type="text", text="Main Title")],
            children=[],
        ),
        Block(
            id="2",
            type="paragraph",
            content=[InlineContent(type="text", text="This is a paragraph.")],
            children=[],
        ),
    ]


@pytest.fixture
def list_blocks():
    """Fixture providing list blocks for testing."""
    return [
        Block(
            id="1",
            type="bulletListItem",
            children=[
                Block(
                    id="1.1",
                    type="paragraph",
                    content=[InlineContent(type="text", text="First item")],
                    children=[],
                ),
                Block(
                    id="1.2",
                    type="paragraph",
                    content=[InlineContent(type="text", text="Second item")],
                    children=[],
                ),
            ],
        ),
        Block(
            id="2",
            type="numberedListItem",
            children=[
                Block(
                    id="2.1",
                    type="paragraph",
                    content=[
                        InlineContent(type="text", text="First numbered")
                    ],
                    children=[],
                ),
                Block(
                    id="2.2",
                    type="paragraph",
                    content=[
                        InlineContent(type="text", text="Second numbered")
                    ],
                    children=[],
                ),
            ],
        ),
    ]


def test_blocks_to_markdown_basic(sample_blocks):
    """Test basic blocks to markdown conversion."""
    markdown = blocks_to_markdown(sample_blocks)
    expected = "# Main Title\n\nThis is a paragraph."
    assert markdown == expected


def test_blocks_to_markdown_empty_list():
    """Test conversion of empty block list."""
    markdown = blocks_to_markdown([])
    assert markdown == ""


def test_blocks_to_markdown_lists(list_blocks):
    """Test conversion of list blocks."""
    markdown = blocks_to_markdown(list_blocks)
    expected = (
        "* First item\n* Second item\n\n1. First numbered\n2. Second numbered"
    )
    assert markdown == expected


def test_blocks_to_markdown_string_content():
    """Test conversion with string content instead of InlineContent list."""
    blocks = [
        Block(
            id="1",
            type="paragraph",
            content="Simple text content",
            children=[],
        )
    ]
    markdown = blocks_to_markdown(blocks)
    assert markdown == "Simple text content"


def test_blocks_to_markdown_heading_levels():
    """Test different heading levels."""
    blocks = [
        Block(
            id="1",
            type="heading",
            props={"level": 1},
            content=[InlineContent(type="text", text="H1")],
            children=[],
        ),
        Block(
            id="2",
            type="heading",
            props={"level": 2},
            content=[InlineContent(type="text", text="H2")],
            children=[],
        ),
        Block(
            id="3",
            type="heading",
            props={"level": 6},
            content=[InlineContent(type="text", text="H6")],
            children=[],
        ),
    ]
    markdown = blocks_to_markdown(blocks)
    expected = "# H1\n\n## H2\n\n###### H6"
    assert markdown == expected


def test_blocks_to_markdown_invalid_heading_level():
    """Test handling of invalid heading levels."""
    blocks = [
        Block(
            id="1",
            type="heading",
            props={"level": 0},
            content=[InlineContent(type="text", text="Title")],
            children=[],
        ),
        Block(
            id="2",
            type="heading",
            props={"level": 10},
            content=[InlineContent(type="text", text="Title")],
            children=[],
        ),
    ]
    markdown = blocks_to_markdown(blocks)
    expected = "# Title\n\n# Title"
    assert markdown == expected


@pytest.mark.parametrize(
    "invalid_input,expected_error",
    [
        ("not a list", "Input must be a list"),
        ([{"not": "a block"}], "must be a Block object"),
    ],
)
def test_blocks_to_markdown_validation_errors(invalid_input, expected_error):
    """Test that invalid inputs raise appropriate errors."""
    with pytest.raises((TypeError, ValueError), match=expected_error):
        blocks_to_markdown(invalid_input)
