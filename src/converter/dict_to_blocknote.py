from typing import Any, Dict, List

from blocknote.schema import Block, BlockType, InlineContent, InlineContentType


def dict_to_blocks(data: List[Dict[str, Any]]) -> List[Block]:
    """
    Converts a list of dictionaries to a list of Block objects.

    Args:
        data: List of dictionaries representing Blocknote blocks

    Returns:
        List of validated Block objects

    Raises:
        TypeError: If input is not a list
        ValueError: If any dictionary cannot be converted to a valid Block
    """
    if not isinstance(data, list):
        raise TypeError("Input must be a list of dictionaries")

    blocks = []
    for i, item in enumerate(data):
        try:
            if not isinstance(item, dict):
                raise TypeError(f"Item at index {i} must be a dictionary, got {type(item)}")

            block_dict = _normalize_block_dict(item)
            block = Block(**block_dict)
            blocks.append(block)
        except Exception as e:
            raise ValueError(f"Failed to convert dict at index {i} to Block: {e}. Dict: {item}")
    return blocks


def _normalize_block_dict(block_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a block dictionary to ensure it conforms to Blocknote schema.

    Args:
        block_dict: Dictionary representing a block

    Returns:
        Normalized dictionary
    """
    normalized = block_dict.copy()

    if "id" not in normalized:
        raise ValueError("Block dict must contain 'id'")
    if "type" not in normalized:
        raise ValueError("Block dict must contain 'type'")

    try:
        BlockType(normalized["type"])
    except ValueError:
        raise ValueError(f"Invalid block type: {normalized['type']}")

    if "content" in normalized:
        content = normalized["content"]
        block_type = normalized["type"]

        if block_type in [
            "paragraph",
            "heading",
            "bulletListItem",
            "numberedListItem",
            "checkListItem",
            "toggleListItem",
            "quote",
        ]:
            if isinstance(content, str):
                normalized["content"] = [InlineContent(type=InlineContentType.TEXT, text=content)]
            elif isinstance(content, list):
                normalized_content = []
                for item in content:
                    if isinstance(item, dict):
                        normalized_content.append(InlineContent(**item))
                    elif isinstance(item, InlineContent):
                        normalized_content.append(item)
                    else:
                        raise ValueError(f"Invalid content item: {item}")
                normalized["content"] = normalized_content
            else:
                raise ValueError(f"Invalid content type for {block_type}: {type(content)}")
        elif block_type == "table":
            normalized["content"] = content

    if "props" not in normalized:
        normalized["props"] = {}
    elif not isinstance(normalized["props"], dict):
        raise ValueError("props must be a dictionary")

    if "children" not in normalized:
        normalized["children"] = []
    elif not isinstance(normalized["children"], list):
        raise ValueError("children must be a list")

    return normalized
