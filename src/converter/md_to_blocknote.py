import uuid
from typing import List, Tuple

from blocknote.schema import Block, InlineContent
from markdown_it import MarkdownIt


def markdown_to_blocks(markdown: str) -> List[Block]:
    """
    Converts a Markdown string to a list of Block objects.

    Args:
        markdown: The markdown string to convert

    Returns:
        List of validated Block objects

    Raises:
        ValueError: If markdown parsing fails or produces invalid blocks
        TypeError: If input is not a string
    """
    if not isinstance(markdown, str):
        raise TypeError("Input must be a string")

    if not markdown.strip():
        return []

    try:
        md = MarkdownIt()
        tokens = md.parse(markdown)
        blocks = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            try:
                if token.type == "heading_open":
                    block = _parse_heading(tokens, i)
                    blocks.append(block)
                    i += 3
                elif token.type == "paragraph_open":
                    block = _parse_paragraph(tokens, i)
                    blocks.append(block)
                    i += 3
                elif (
                    token.type == "bullet_list_open"
                    or token.type == "ordered_list_open"
                ):
                    block, skip_count = _parse_list(tokens, i)
                    blocks.append(block)
                    i += skip_count
                elif token.type == "blockquote_open":
                    block = _parse_quote(tokens, i)
                    blocks.append(block)
                    i += 3
                else:
                    i += 1
            except Exception as e:
                raise ValueError(
                    f"Failed to parse markdown token at position {i}: {e}"
                )

        return blocks

    except Exception as e:
        raise ValueError(f"Failed to parse markdown: {e}")


def _parse_heading(tokens: List, start_idx: int) -> Block:
    """Parse a heading token sequence into a Block."""
    token = tokens[start_idx]
    level = int(token.tag[1])
    content_token = tokens[start_idx + 1]

    if (
        content_token.type == "inline"
        and hasattr(content_token, "children")
        and content_token.children
    ):
        content = _parse_inline_content(content_token.children)
    else:
        content = []

    return Block(
        id=str(uuid.uuid4()),
        type="heading",
        props={"level": level},
        content=content,
        children=[],
    )


def _parse_paragraph(tokens: List, start_idx: int) -> Block:
    """Parse a paragraph token sequence into a Block."""
    content_token = tokens[start_idx + 1]
    if (
        content_token.type == "inline"
        and hasattr(content_token, "children")
        and content_token.children
    ):
        content = _parse_inline_content(content_token.children)
    else:
        content = []

    return Block(
        id=str(uuid.uuid4()), type="paragraph", content=content, children=[]
    )


def _parse_list(tokens: List, start_idx: int) -> Tuple[Block, int]:
    """
    Parse a list token sequence into a Block.

    Returns:
        Tuple of (Block, number of tokens to skip)
    """
    list_type = (
        "bulletListItem"
        if tokens[start_idx].type == "bullet_list_open"
        else "numberedListItem"
    )
    return (
        Block(id=str(uuid.uuid4()), type=list_type, content=[], children=[]),
        3,
    )


def _parse_quote(tokens: List, start_idx: int) -> Block:
    """Parse a blockquote token sequence into a Block."""
    paragraph_token = tokens[start_idx + 1]
    if paragraph_token.type == "paragraph_open":
        content_token = tokens[start_idx + 2]
        if (
            content_token.type == "inline"
            and hasattr(content_token, "children")
            and content_token.children
        ):
            content = _parse_inline_content(content_token.children)
        else:
            content = []
    else:
        content = []

    return Block(
        id=str(uuid.uuid4()), type="quote", content=content, children=[]
    )


def _parse_inline_content(children: List) -> List[InlineContent]:
    """
    Parse markdown-it inline content tokens into InlineContent objects.

    Args:
        children: List of inline tokens from markdown-it

    Returns:
        List of InlineContent objects
    """
    content = []
    i = 0
    while i < len(children):
        child = children[i]

        if hasattr(child, "type"):
            if child.type == "text":
                content.append(InlineContent(type="text", text=child.content))
                i += 1
            elif child.type == "strong_open":
                if i + 1 < len(children) and hasattr(
                    children[i + 1], "content"
                ):
                    text = children[i + 1].content
                    content.append(
                        InlineContent(
                            type="text", text=text, styles={"bold": True}
                        )
                    )
                    i += 3  # Skip strong_open, text, strong_close
                else:
                    i += 1
            elif child.type == "em_open":
                if i + 1 < len(children) and hasattr(
                    children[i + 1], "content"
                ):
                    text = children[i + 1].content
                    content.append(
                        InlineContent(
                            type="text", text=text, styles={"italic": True}
                        )
                    )
                    i += 3  # Skip em_open, text, em_close
                else:
                    i += 1
            else:
                if hasattr(child, "content") and child.content:
                    content.append(
                        InlineContent(type="text", text=child.content)
                    )
                i += 1
        else:
            i += 1

    return content
