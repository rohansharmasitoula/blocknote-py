from typing import Any, Dict, List

from blocknote.schema import Block, InlineContent


def blocks_to_dict(blocks: List[Block]) -> List[Dict[str, Any]]:
    """
    Converts a list of Block objects to a list of dictionaries.

    Args:
        blocks: List of Block objects to convert

    Returns:
        List of dictionaries representing the blocks

    Raises:
        TypeError: If input is not a list or contains non-Block objects
    """
    if not isinstance(blocks, list):
        raise TypeError("Input must be a list of Block objects")

    result = []
    for i, block in enumerate(blocks):
        if not isinstance(block, Block):
            raise TypeError(f"Item at index {i} must be a Block object, got {type(block)}")

        result.append(_block_to_dict(block))

    return result


def _block_to_dict(block: Block) -> Dict[str, Any]:
    """
    Convert a single Block object to a dictionary.

    Args:
        block: The Block object to convert

    Returns:
        Dictionary representation of the block
    """
    block_dict = {
        "id": block.id,
        "type": block.type,
        "props": block.props if block.props else {},
        "content": _content_to_dict(block.content),
        "children": [_block_to_dict(child) for child in block.children] if block.children else [],
    }

    return block_dict


def _content_to_dict(content) -> List[Dict[str, Any]]:
    """
    Convert block content to dictionary format.

    Args:
        content: Either a string, list of InlineContent objects, or other content

    Returns:
        List of dictionaries representing the content
    """
    if isinstance(content, str):
        return [{"type": "text", "text": content, "styles": {}}]
    elif isinstance(content, list):
        result = []
        for item in content:
            if isinstance(item, InlineContent):
                content_dict = {
                    "type": item.type,
                    "text": item.text if hasattr(item, "text") else "",
                    "styles": item.styles if item.styles else {},
                }
                result.append(content_dict)
            elif isinstance(item, dict):
                result.append(item)
            else:
                result.append({"type": "text", "text": str(item), "styles": {}})
        return result
    else:
        return content if content else []
