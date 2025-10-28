from typing import List

from blocknote.schema import Block


def blocks_to_html(blocks: List[Block]) -> str:
    """
    Converts a list of Block objects to an HTML string.

    Args:
        blocks: List of validated Block objects to convert

    Returns:
        An HTML string representation of the blocks

    Raises:
        TypeError: If input is not a list or contains non-Block objects

    Example:
        >>> blocks = [
        ...     Block(
        ...         id="1",
        ...         type="heading",
        ...         props={"level": 1},
        ...         content=[InlineContent(type="text", text="Title")],
        ...     )
        ... ]
        >>> blocks_to_html(blocks)
        '<h1>Title</h1>'
    """
    if not isinstance(blocks, list):
        raise TypeError("Input must be a list of Block objects")

    if not blocks:
        return ""

    html_elements = []

    for i, block in enumerate(blocks):
        try:
            if not isinstance(block, Block):
                raise TypeError(
                    f"Item at index {i} must be a Block object, "
                    f"got {type(block)}"
                )

            html_element = _convert_block_to_html(block)
            if html_element:
                html_elements.append(html_element)
        except Exception as e:
            raise ValueError(
                f"Failed to convert block at index {i} to HTML: {e}"
            )

    return "\n".join(html_elements)


def _convert_block_to_html(block: Block) -> str:
    """
    Convert a single Block to its HTML representation.

    Args:
        block: The Block object to convert

    Returns:
        HTML string for the block
    """
    block_type = block.type
    content = _extract_content_html(block.content)

    if block_type == "heading":
        level = block.props.get("level", 1)
        if not isinstance(level, int) or level < 1 or level > 6:
            level = 1
        return f"<h{level}>{content}</h{level}>"

    elif block_type == "paragraph":
        return f"<p>{content}</p>"

    elif block_type == "bulletListItem":
        if not block.children:
            return f"<ul><li>{content}</li></ul>"
        child_items = []
        for child in block.children:
            if child.type == "paragraph":
                child_content = _extract_content_html(child.content)
                child_items.append(f"<li>{child_content}</li>")
        return f"<ul>{''.join(child_items)}</ul>"

    elif block_type == "numberedListItem":
        if not block.children:
            return f"<ol><li>{content}</li></ol>"
        child_items = []
        for child in block.children:
            if child.type == "paragraph":
                child_content = _extract_content_html(child.content)
                child_items.append(f"<li>{child_content}</li>")
        return f"<ol>{''.join(child_items)}</ol>"

    elif block_type == "checkListItem":
        checked = block.props.get("checked", False)
        checkbox_state = "checked" if checked else ""
        return (
            "<div><input type=\"checkbox\" "
            f"{checkbox_state} disabled> {content}</div>"
        )

    elif block_type == "quote":
        return f"<blockquote>{content}</blockquote>"

    elif block_type == "table":
        return f"<div class='table-placeholder'>{content}</div>"

    else:
        return f'<div class="blocknote-{block_type}">{content}</div>'


def _extract_content_html(content) -> str:
    """
    Extract HTML content from Block content field, preserving styling.

    Args:
        content: Either a string or list of InlineContent objects

    Returns:
        HTML string with proper styling tags
    """
    if isinstance(content, str):
        return _escape_html(content)
    elif isinstance(content, list):
        result_parts = []
        for item in content:
            if hasattr(item, "type") and item.type == "text":
                text = _escape_html(item.text)
                if item.styles.get("bold"):
                    text = f"<strong>{text}</strong>"
                if item.styles.get("italic"):
                    text = f"<em>{text}</em>"
                if item.styles.get("underline"):
                    text = f"<u>{text}</u>"
                if item.styles.get("strike"):
                    text = f"<s>{text}</s>"
                if item.styles.get("code"):
                    text = f"<code>{text}</code>"

                if "backgroundColor" in item.styles:
                    bg_color = item.styles["backgroundColor"]
                    text = (
                        '<span style="background-color: {}">{}</span>'.format(
                            bg_color,
                            text,
                        )
                    )

                if "textColor" in item.styles:
                    color = item.styles["textColor"]
                    text = f'<span style="color: {color}">{text}</span>'

                result_parts.append(text)
            else:
                result_parts.append(_escape_html(str(item)))
        return "".join(result_parts)
    else:
        return _escape_html(str(content))


def _escape_html(text: str) -> str:
    """
    Escape HTML special characters in text.

    Args:
        text: The text to escape

    Returns:
        HTML-escaped text
    """
    if not isinstance(text, str):
        text = str(text)

    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )
