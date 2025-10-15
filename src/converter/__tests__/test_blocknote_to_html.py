import pytest
from blocknote.converter.blocknote_to_html import blocks_to_html
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
                    content=[InlineContent(type="text", text="First numbered")],
                    children=[],
                ),
                Block(
                    id="2.2",
                    type="paragraph",
                    content=[InlineContent(type="text", text="Second numbered")],
                    children=[],
                ),
            ],
        ),
    ]


@pytest.fixture
def styled_blocks():
    """Fixture providing blocks with styled content."""
    return [
        Block(
            id="1",
            type="paragraph",
            content=[
                InlineContent(type="text", text="Bold text", styles={"bold": True}),
                InlineContent(type="text", text=" and "),
                InlineContent(type="text", text="italic text", styles={"italic": True}),
            ],
            children=[],
        ),
        Block(
            id="2",
            type="paragraph",
            content=[
                InlineContent(
                    type="text",
                    text="Colored text",
                    styles={"textColor": "red", "backgroundColor": "yellow"},
                )
            ],
            children=[],
        ),
    ]


def test_blocks_to_html_basic(sample_blocks):
    """Test basic blocks to HTML conversion."""
    html = blocks_to_html(sample_blocks)
    expected = "<h1>Main Title</h1>\n<p>This is a paragraph.</p>"
    assert html == expected


def test_blocks_to_html_empty_list():
    """Test conversion of empty block list."""
    html = blocks_to_html([])
    assert html == ""


def test_blocks_to_html_lists(list_blocks):
    """Test conversion of list blocks."""
    html = blocks_to_html(list_blocks)
    expected = "<ul><li>First item</li><li>Second item</li></ul>\n<ol><li>First numbered</li><li>Second numbered</li></ol>"
    assert html == expected


def test_blocks_to_html_string_content():
    """Test conversion with string content instead of InlineContent list."""
    blocks = [Block(id="1", type="paragraph", content="Simple text content", children=[])]
    html = blocks_to_html(blocks)
    assert html == "<p>Simple text content</p>"


def test_blocks_to_html_heading_levels():
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
    html = blocks_to_html(blocks)
    expected = "<h1>H1</h1>\n<h2>H2</h2>\n<h6>H6</h6>"
    assert html == expected


def test_blocks_to_html_invalid_heading_level():
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
    html = blocks_to_html(blocks)
    expected = "<h1>Title</h1>\n<h1>Title</h1>"
    assert html == expected


def test_blocks_to_html_styled_content(styled_blocks):
    """Test conversion of blocks with styled content."""
    html = blocks_to_html(styled_blocks)
    expected = '<p><strong>Bold text</strong> and <em>italic text</em></p>\n<p><span style="color: red"><span style="background-color: yellow">Colored text</span></span></p>'
    assert html == expected


def test_blocks_to_html_quote():
    """Test quote block conversion."""
    blocks = [
        Block(
            id="1",
            type="quote",
            content=[InlineContent(type="text", text="This is a quote")],
            children=[],
        )
    ]
    html = blocks_to_html(blocks)
    expected = "<blockquote>This is a quote</blockquote>"
    assert html == expected


def test_blocks_to_html_checklist():
    """Test checklist item conversion."""
    blocks = [
        Block(
            id="1",
            type="checkListItem",
            props={"checked": True},
            content=[InlineContent(type="text", text="Completed task")],
            children=[],
        ),
        Block(
            id="2",
            type="checkListItem",
            props={"checked": False},
            content=[InlineContent(type="text", text="Incomplete task")],
            children=[],
        ),
    ]
    html = blocks_to_html(blocks)
    expected = '<div><input type="checkbox" checked disabled> Completed task</div>\n<div><input type="checkbox"  disabled> Incomplete task</div>'
    assert html == expected


def test_blocks_to_html_html_escaping():
    """Test that HTML special characters are properly escaped."""
    blocks = [
        Block(
            id="1",
            type="paragraph",
            content=[InlineContent(type="text", text="<script>alert('xss')</script>")],
            children=[],
        )
    ]
    html = blocks_to_html(blocks)
    expected = "<p>&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;</p>"
    assert html == expected


def test_blocks_to_html_table_block_type():
    """Test handling of table block types."""
    blocks = [
        Block(
            id="1",
            type="table",
            content=[InlineContent(type="text", text="Table content")],
            children=[],
        )
    ]
    html = blocks_to_html(blocks)
    expected = "<div class='table-placeholder'>Table content</div>"
    assert html == expected


@pytest.mark.parametrize(
    "invalid_input,expected_error",
    [
        ("not a list", "Input must be a list"),
        ([{"not": "a block"}], "must be a Block object"),
    ],
)
def test_blocks_to_html_validation_errors(invalid_input, expected_error):
    """Test that invalid inputs raise appropriate errors."""
    with pytest.raises((TypeError, ValueError), match=expected_error):
        blocks_to_html(invalid_input)
