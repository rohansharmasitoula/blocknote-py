import pytest
from blocknote.converter.html_to_blocknote import html_to_blocks


def test_html_to_blocks_basic():
    """Test basic HTML to blocks conversion."""
    html = "<h1>Main Title</h1><p>This is a paragraph.</p>"
    blocks = html_to_blocks(html)

    assert len(blocks) == 2

    assert blocks[0].type == "heading"
    assert blocks[0].props["level"] == 1
    assert len(blocks[0].content) == 1
    assert blocks[0].content[0].text == "Main Title"
    assert blocks[1].type == "paragraph"
    assert len(blocks[1].content) == 1
    assert blocks[1].content[0].text == "This is a paragraph."


def test_html_to_blocks_empty_string():
    """Test conversion of empty HTML string."""
    blocks = html_to_blocks("")
    assert blocks == []


def test_html_to_blocks_whitespace_only():
    """Test conversion of whitespace-only HTML."""
    blocks = html_to_blocks("   \n\t   ")
    assert blocks == []


def test_html_to_blocks_headings():
    """Test different heading levels."""
    html = "<h1>H1</h1><h2>H2</h2><h6>H6</h6>"
    blocks = html_to_blocks(html)

    assert len(blocks) == 3
    assert blocks[0].type == "heading"
    assert blocks[0].props["level"] == 1
    assert blocks[0].content[0].text == "H1"

    assert blocks[1].type == "heading"
    assert blocks[1].props["level"] == 2
    assert blocks[1].content[0].text == "H2"

    assert blocks[2].type == "heading"
    assert blocks[2].props["level"] == 6
    assert blocks[2].content[0].text == "H6"


def test_html_to_blocks_lists():
    """Test conversion of HTML lists."""
    html = (
        "<ul><li>First item</li><li>Second item</li></ul>"
        "<ol><li>First numbered</li><li>Second numbered</li></ol>"
    )
    blocks = html_to_blocks(html)

    assert len(blocks) == 4

    assert blocks[0].type == "bulletListItem"
    assert blocks[0].content[0].text == "First item"

    assert blocks[1].type == "bulletListItem"
    assert blocks[1].content[0].text == "Second item"

    assert blocks[2].type == "numberedListItem"
    assert blocks[2].content[0].text == "First numbered"

    assert blocks[3].type == "numberedListItem"
    assert blocks[3].content[0].text == "Second numbered"


def test_html_to_blocks_styled_content():
    """Test conversion of HTML with styled content."""
    html = (
        "<p><strong>Bold text</strong> and "
        "<em>italic text</em></p>"
    )
    blocks = html_to_blocks(html)

    assert len(blocks) == 1
    assert blocks[0].type == "paragraph"
    assert len(blocks[0].content) == 3

    assert blocks[0].content[0].text == "Bold text"
    assert blocks[0].content[0].styles.get("bold") is True

    assert blocks[0].content[1].text == " and "
    assert not blocks[0].content[1].styles

    assert blocks[0].content[2].text == "italic text"
    assert blocks[0].content[2].styles.get("italic") is True


def test_html_to_blocks_nested_styles():
    """Test conversion of nested HTML styles."""
    html = (
        "<p><strong><em>Bold and italic"
        "</em></strong></p>"
    )
    blocks = html_to_blocks(html)

    assert len(blocks) == 1
    assert blocks[0].type == "paragraph"
    assert len(blocks[0].content) == 1

    content = blocks[0].content[0]
    assert content.text == "Bold and italic"
    assert content.styles.get("bold") is True
    assert content.styles.get("italic") is True


def test_html_to_blocks_span_with_styles():
    """Test conversion of span elements with CSS styles."""
    html = (
        '<p><span style="color: red; background-color: yellow;">'
        "Colored text</span></p>"
    )
    blocks = html_to_blocks(html)

    assert len(blocks) == 1
    assert blocks[0].type == "paragraph"
    assert len(blocks[0].content) == 1

    content = blocks[0].content[0]
    assert content.text == "Colored text"
    assert content.styles.get("textColor") == "red"
    assert content.styles.get("backgroundColor") == "yellow"


def test_html_to_blocks_blockquote():
    """Test blockquote conversion."""
    html = "<blockquote>This is a quote</blockquote>"
    blocks = html_to_blocks(html)

    assert len(blocks) == 1
    assert blocks[0].type == "quote"
    assert blocks[0].content[0].text == "This is a quote"


def test_html_to_blocks_checkbox_div():
    """Test conversion of checkbox divs."""
    html = (
        '<div><input type="checkbox" checked> Completed task</div>'
        '<div><input type="checkbox"> Incomplete task</div>'
    )
    blocks = html_to_blocks(html)

    assert len(blocks) == 2

    assert blocks[0].type == "checkListItem"
    assert blocks[0].props.get("checked") is True
    assert blocks[0].content[0].text == " Completed task"

    assert blocks[1].type == "checkListItem"
    assert blocks[1].props.get("checked") is False
    assert blocks[1].content[0].text == " Incomplete task"


def test_html_to_blocks_table_div_classes():
    """Test conversion of divs with table BlockNote classes."""
    html = '<div class="blocknote-table">Table content</div>'
    blocks = html_to_blocks(html)

    assert len(blocks) == 1
    assert blocks[0].type == "table"
    assert blocks[0].content[0].text == "Table content"


def test_html_to_blocks_underline_and_strikethrough():
    """Test conversion of underline and strikethrough styles."""
    html = "<p><u>Underlined text</u> and <s>strikethrough text</s></p>"
    blocks = html_to_blocks(html)

    assert len(blocks) == 1
    assert blocks[0].type == "paragraph"
    assert len(blocks[0].content) == 3

    assert blocks[0].content[0].text == "Underlined text"
    assert blocks[0].content[0].styles.get("underline") is True

    assert blocks[0].content[1].text == " and "

    assert blocks[0].content[2].text == "strikethrough text"
    assert blocks[0].content[2].styles.get("strike") is True
    assert blocks[0].content[2].text == "strikethrough text"
    assert blocks[0].content[2].styles.get("strike") is True


def test_html_to_blocks_code():
    """Test conversion of code elements."""
    html = "<p>This is <code>inline code</code> in a paragraph.</p>"
    blocks = html_to_blocks(html)

    assert len(blocks) == 1
    assert blocks[0].type == "paragraph"
    assert len(blocks[0].content) == 3

    assert blocks[0].content[1].text == "inline code"
    assert blocks[0].content[1].styles.get("code") is True


def test_html_to_blocks_mixed_content():
    """Test conversion of complex mixed HTML content."""
    html = """
    <h1>Document Title</h1>
    <p>This is a <strong>paragraph</strong> with <em>mixed</em> content.</p>
    <ul>
        <li>First bullet point</li>
        <li>Second bullet point</li>
    </ul>
    <blockquote>Important quote here</blockquote>
    """
    blocks = html_to_blocks(html)

    assert len(blocks) == 5

    assert blocks[0].type == "heading"
    assert blocks[0].content[0].text == "Document Title"

    assert blocks[1].type == "paragraph"
    assert len(blocks[1].content) == 5

    assert blocks[2].type == "bulletListItem"
    assert blocks[3].type == "bulletListItem"

    assert blocks[4].type == "quote"
    assert blocks[4].content[0].text == "Important quote here"


@pytest.mark.parametrize(
    "invalid_input,expected_error",
    [
        (123, "Input must be a string"),
        (None, "Input must be a string"),
        ([], "Input must be a string"),
    ],
)
def test_html_to_blocks_validation_errors(invalid_input, expected_error):
    """Test that invalid inputs raise appropriate errors."""
    with pytest.raises(TypeError, match=expected_error):
        html_to_blocks(invalid_input)


def test_html_to_blocks_malformed_html():
    """Test handling of malformed HTML."""
    html = "<p>Unclosed paragraph</p><h1>Title</h1>"
    blocks = html_to_blocks(html)

    assert len(blocks) >= 1
