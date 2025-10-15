from typing import List

from blocknote.schema import Block, InlineContent


def blocks_to_markdown(blocks: List[Block]) -> str:
    """
    Converts a list of Block objects to a Markdown string.

    Args:
        blocks: List of validated Block objects to convert

    Returns:
        A markdown string representation of the blocks

    Raises:
        TypeError: If input is not a list or contains non-Block objects

    Example:
        >>> blocks = [Block(id="1", type="heading", props={"level": 1}, content=[InlineContent(type="text", text="Title")])]
        >>> blocks_to_markdown(blocks)
        '# Title'
    """
    if not isinstance(blocks, list):
        raise TypeError("Input must be a list of Block objects")

    if not blocks:
        return ""

    markdown_lines = []

    for i, block in enumerate(blocks):
        try:
            if not isinstance(block, Block):
                raise TypeError(f"Item at index {i} must be a Block object, got {type(block)}")

            markdown_line = _convert_block_to_markdown(block)
            if markdown_line:  # Only add non-empty lines
                markdown_lines.append(markdown_line)
        except Exception as e:
            raise ValueError(f"Failed to convert block at index {i} to markdown: {e}")

    return "\n\n".join(markdown_lines)


def _convert_block_to_markdown(block: Block) -> str:
    """
    Convert a single Block to its markdown representation.

    Args:
        block: The Block object to convert

    Returns:
        Markdown string for the block
    """
    block_type = block.type
    content = _extract_content_text(block.content)

    if block_type == "heading":
        level = block.props.get("level", 1)
        if not isinstance(level, int) or level < 1 or level > 6:
            level = 1  # Default to level 1 for invalid levels
        return f"{'#' * level} {content}"

    elif block_type == "paragraph":
        return content

    elif block_type == "bulletListItem":
        if not block.children:
            return f"* {content}"
        # Convert children to list items
        child_lines = []
        for child in block.children:
            if child.type == "paragraph":
                child_content = _extract_content_text(child.content)
                child_lines.append(f"* {child_content}")
        return "\n".join(child_lines)

    elif block_type == "numberedListItem":
        if not block.children:
            return f"1. {content}"
        # Convert children to numbered list items
        child_lines = []
        for i, child in enumerate(block.children, 1):
            if child.type == "paragraph":
                child_content = _extract_content_text(child.content)
                child_lines.append(f"{i}. {child_content}")
        return "\n".join(child_lines)

    else:
        # For unsupported block types, return empty string or could raise warning
        return ""


def _extract_content_text(content) -> str:
    """
    Extract text content from Block content field.

    Args:
        content: Either a string or list of InlineContent objects

    Returns:
        Plain text string
    """
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        result_parts = []
        for item in content:
            if hasattr(item, "type") and item.type == "text":
                text = item.text
                # Apply styling if present
                if item.styles.get("bold"):
                    text = f"**{text}**"
                if item.styles.get("italic"):
                    text = f"*{text}*"
                result_parts.append(text)
            else:
                result_parts.append(str(item))
        return "".join(result_parts)
    else:
        return str(content)
