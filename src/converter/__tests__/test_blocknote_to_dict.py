import pytest
from blocknote.converter.blocknote_to_dict import blocks_to_dict
from blocknote.schema import Block, InlineContent


@pytest.fixture
def sample_blocks():
    """Fixture providing sample blocks for testing."""
    return [
        Block(
            id="1",
            type="paragraph",
            content=[
                InlineContent(type="text", text="Hello, "),
                InlineContent(
                    type="text", text="world!", styles={"bold": True}
                ),
            ],
            children=[],
        )
    ]


@pytest.fixture
def nested_blocks():
    """Fixture providing nested blocks for testing."""
    return [
        Block(
            id="1",
            type="bulletListItem",
            content=[],
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
        )
    ]


def test_blocks_to_dict_basic(sample_blocks):
    """Test basic blocks to dict conversion."""
    result = blocks_to_dict(sample_blocks)

    assert len(result) == 1
    assert result[0]["id"] == "1"
    assert result[0]["type"] == "paragraph"
    assert len(result[0]["content"]) == 2
    assert result[0]["content"][0]["text"] == "Hello, "
    assert result[0]["content"][1]["text"] == "world!"
    assert result[0]["content"][1]["styles"] == {"bold": True}
    assert result[0]["children"] == []


def test_blocks_to_dict_nested(nested_blocks):
    """Test conversion of nested blocks."""
    result = blocks_to_dict(nested_blocks)

    assert len(result) == 1
    assert result[0]["id"] == "1"
    assert result[0]["type"] == "bulletListItem"
    assert len(result[0]["children"]) == 2
    assert result[0]["children"][0]["id"] == "1.1"
    assert result[0]["children"][0]["content"][0]["text"] == "First item"
    assert result[0]["children"][1]["id"] == "1.2"
    assert result[0]["children"][1]["content"][0]["text"] == "Second item"


def test_blocks_to_dict_empty_list():
    """Test conversion of empty block list."""
    result = blocks_to_dict([])
    assert result == []


def test_blocks_to_dict_string_content():
    """Test conversion with string content."""
    blocks = [
        Block(id="1", type="paragraph", content="Simple text", children=[])
    ]
    result = blocks_to_dict(blocks)

    assert len(result) == 1
    assert result[0]["content"][0]["text"] == "Simple text"
    assert result[0]["content"][0]["type"] == "text"


def test_blocks_to_dict_with_props():
    """Test conversion with block props."""
    blocks = [
        Block(
            id="1",
            type="heading",
            props={"level": 2, "textColor": "blue"},
            content=[InlineContent(type="text", text="Title")],
            children=[],
        )
    ]
    result = blocks_to_dict(blocks)

    assert result[0]["props"]["level"] == 2
    assert result[0]["props"]["textColor"] == "blue"


@pytest.mark.parametrize(
    "invalid_input,expected_error",
    [
        ("not a list", "Input must be a list"),
        ([{"not": "a block"}], "must be a Block object"),
    ],
)
def test_blocks_to_dict_validation_errors(invalid_input, expected_error):
    """Test that invalid inputs raise appropriate errors."""
    with pytest.raises(TypeError, match=expected_error):
        blocks_to_dict(invalid_input)


def test_blocks_to_dict_multiple_blocks():
    """Test conversion of multiple blocks."""
    blocks = [
        Block(id="1", type="paragraph", content="First", children=[]),
        Block(
            id="2",
            type="heading",
            props={"level": 1},
            content="Second",
            children=[],
        ),
        Block(id="3", type="paragraph", content="Third", children=[]),
    ]
    result = blocks_to_dict(blocks)

    assert len(result) == 3
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"
    assert result[2]["id"] == "3"
    assert result[1]["props"]["level"] == 1


def test_blocks_to_dict_roundtrip():
    """Test that dict -> blocks -> dict produces the same result."""
    from blocknote.converter.dict_to_blocknote import dict_to_blocks

    original_dict = [
        {
            "id": "1",
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Hello"},
                {"type": "text", "text": " world", "styles": {"italic": True}},
            ],
        }
    ]

    # Convert dict to blocks
    blocks = dict_to_blocks(original_dict)

    # Convert blocks back to dict
    result_dict = blocks_to_dict(blocks)

    # Compare (accounting for default values)
    assert result_dict[0]["id"] == original_dict[0]["id"]
    assert result_dict[0]["type"] == original_dict[0]["type"]
    assert len(result_dict[0]["content"]) == len(original_dict[0]["content"])
    assert (
        result_dict[0]["content"][0]["text"]
        == original_dict[0]["content"][0]["text"]
    )
    assert (
        result_dict[0]["content"][1]["text"]
        == original_dict[0]["content"][1]["text"]
    )
    assert (
        result_dict[0]["content"][1]["styles"]
        == original_dict[0]["content"][1]["styles"]
    )
