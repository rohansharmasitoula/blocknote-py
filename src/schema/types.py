"""
Blocknote schema types and models.

This module defines the core Pydantic models for Blocknote blocks and
inline content. All models include validation and type safety for
working with Blocknote data structures.
"""

from enum import Enum
from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field, validator


class TextAlignment(str, Enum):
    """Text alignment options."""

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


class InlineContentType(str, Enum):
    """Enumeration of supported inline content types."""

    TEXT = "text"


class BlockType(str, Enum):
    """Enumeration of supported block types in Blocknote."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    BULLET_LIST_ITEM = "bulletListItem"
    NUMBERED_LIST_ITEM = "numberedListItem"
    CHECK_LIST_ITEM = "checkListItem"
    TOGGLE_LIST_ITEM = "toggleListItem"
    QUOTE = "quote"
    TABLE = "table"


class InlineContent(BaseModel):
    """
    Represents inline content within a block.

    Inline content is the text and styling information that makes up the
    content of a block. Currently only supports text content with optional
    styling.

    Attributes:
        type: The type of inline content (currently only "text")
        text: The actual text content
        styles: Dictionary of styling properties (e.g., {"bold": True})
    """

    type: InlineContentType = Field(
        ..., description="The type of inline content"
    )
    text: str = Field(..., description="The text content")
    styles: Dict[str, Any] = Field(
        default_factory=dict, description="Styling properties"
    )

    class Config:
        use_enum_values = True


class Block(BaseModel):
    """
    Represents a Blocknote block with content and children.

    A Block is the fundamental unit of content in Blocknote. Blocks can contain
    inline content and can have child blocks, allowing for nested structures
    like lists and complex documents.

    Attributes:
        id: Unique identifier for the block
        type: The type of block (paragraph, heading, list items, etc.)
        props: Block-specific properties including default styling
        content: The content of the block (text or list of InlineContent)
        children: List of child blocks
    """

    id: str = Field(..., description="Unique identifier for the block")
    type: BlockType = Field(..., description="The type of block")
    props: Dict[str, Any] = Field(
        default_factory=dict,
        description="Block-specific and styling properties",
    )
    content: Union[str, List[InlineContent]] = Field(
        default_factory=list, description="The content of the block"
    )
    children: List["Block"] = Field(
        default_factory=list, description="Child blocks"
    )

    @validator("content")
    def validate_content(cls, v, values):
        """Validate that content format matches the block type."""
        if "type" in values:
            block_type = values["type"]
            text_block_types = [
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.BULLET_LIST_ITEM,
                BlockType.NUMBERED_LIST_ITEM,
                BlockType.CHECK_LIST_ITEM,
                BlockType.TOGGLE_LIST_ITEM,
                BlockType.QUOTE,
            ]
            if block_type in text_block_types:
                if isinstance(v, str):
                    return [
                        InlineContent(type=InlineContentType.TEXT, text=v)
                    ]
                elif not isinstance(v, list):
                    message = (
                        f"Content for {block_type} must be a string or "
                        "list of InlineContent"
                    )
                    raise ValueError(message)
            elif block_type == BlockType.TABLE:
                # Table content is returned as provided
                pass
        return v

    class Config:
        use_enum_values = True


Block.model_rebuild()
