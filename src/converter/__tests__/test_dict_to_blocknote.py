import pytest
from blocknote.converter.dict_to_blocknote import dict_to_blocks
from blocknote.schema import Block, InlineContent


@pytest.fixture
def sample_block_data():
    """Fixture providing sample block data for testing."""
    return [
        {
            "id": "1",
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Hello, "},
                {"type": "text", "text": "world!", "styles": {"bold": True}},
            ],
        }
    ]


@pytest.fixture
def sample_block_data_with_string_content():
    """Fixture providing block data with string content."""
    return [
        {
            "id": "2",
            "type": "paragraph",
            "content": "Simple paragraph text",
        }
    ]


def test_dict_to_blocks_basic(sample_block_data):
    """Test basic dict to blocks conversion."""
    blocks = dict_to_blocks(sample_block_data)
    assert len(blocks) == 1
    assert isinstance(blocks[0], Block)
    assert blocks[0].id == "1"
    assert blocks[0].type == "paragraph"
    assert len(blocks[0].content) == 2
    assert isinstance(blocks[0].content[0], InlineContent)
    assert blocks[0].content[0].text == "Hello, "
    assert blocks[0].content[1].text == "world!"
    assert blocks[0].content[1].styles == {"bold": True}


def test_dict_to_blocks_string_content(sample_block_data_with_string_content):
    """Test conversion with string content."""
    blocks = dict_to_blocks(sample_block_data_with_string_content)
    assert len(blocks) == 1
    assert blocks[0].id == "2"
    assert blocks[0].type == "paragraph"
    assert len(blocks[0].content) == 1
    assert isinstance(blocks[0].content[0], InlineContent)
    assert blocks[0].content[0].text == "Simple paragraph text"


def test_dict_to_blocks_multiple_blocks():
    """Test conversion of multiple blocks."""
    data = [
        {"id": "1", "type": "paragraph", "content": "First paragraph"},
        {
            "id": "2",
            "type": "heading",
            "props": {"level": 1},
            "content": "Heading",
        },
    ]
    blocks = dict_to_blocks(data)
    assert len(blocks) == 2
    assert blocks[0].id == "1"
    assert blocks[1].id == "2"
    assert blocks[1].props["level"] == 1


@pytest.mark.parametrize(
    "invalid_data,expected_error",
    [
        ([{"type": "paragraph"}], "Block dict must contain 'id'"),
        ([{"id": "1"}], "Block dict must contain 'type'"),
        ([{"id": "1", "type": "invalid"}], "Invalid block type"),
        (
            [{"id": "1", "type": "paragraph", "content": 123}],
            "Invalid content type",
        ),
    ],
)
def test_dict_to_blocks_validation_errors(invalid_data, expected_error):
    """Test that invalid data raises appropriate errors."""
    with pytest.raises(ValueError, match=expected_error):
        dict_to_blocks(invalid_data)


def test_dict_to_blocks_empty_list():
    """Test conversion of empty list."""
    blocks = dict_to_blocks([])
    assert blocks == []


@pytest.mark.parametrize(
    "block_type,content,expected_valid",
    [
        ("paragraph", [{"type": "text", "text": "Test"}], True),
        ("heading", [{"type": "text", "text": "Title"}], True),
        ("bulletListItem", [{"type": "text", "text": "Item"}], True),
        ("numberedListItem", [{"type": "text", "text": "Item"}], True),
    ],
)
def test_dict_to_blocks_new_block_types(block_type, content, expected_valid):
    """Test conversion of supported block types."""
    data = [{"id": "1", "type": block_type, "content": content}]
    if expected_valid:
        blocks = dict_to_blocks(data)
        assert len(blocks) == 1
        assert blocks[0].type == block_type
    else:
        with pytest.raises(ValueError):
            dict_to_blocks(data)
