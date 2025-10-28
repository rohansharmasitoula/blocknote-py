import uuid
from html.parser import HTMLParser
from typing import Any, Dict, List

from blocknote.schema import Block, InlineContent


def html_to_blocks(html: str) -> List[Block]:
    """
    Converts an HTML string to a list of Block objects.

    Args:
        html: The HTML string to convert

    Returns:
        List of validated Block objects

    Raises:
        ValueError: If HTML parsing fails or produces invalid blocks
        TypeError: If input is not a string
    """
    if not isinstance(html, str):
        raise TypeError("Input must be a string")

    if not html.strip():
        return []

    try:
        parser = BlockNoteHTMLParser()
        parser.feed(html)
        return parser.get_blocks()
    except Exception as e:
        raise ValueError(f"Failed to parse HTML: {e}")


class BlockNoteHTMLParser(HTMLParser):
    """Custom HTML parser for converting HTML to BlockNote blocks."""

    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current_block = None
        self.content_stack = []
        self.style_stack = []
        self.tag_stack = []

    def get_blocks(self) -> List[Block]:
        """Get the parsed blocks."""
        return self.blocks

    def handle_starttag(self, tag: str, attrs: List[tuple]):
        """Handle opening HTML tags."""
        self.tag_stack.append(tag)

        if tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            level = int(tag[1])
            self.current_block = {
                "type": "heading",
                "props": {"level": level},
                "content": [],
                "styles": {},
            }
        elif tag == "p":
            self.current_block = {
                "type": "paragraph",
                "props": {},
                "content": [],
                "styles": {},
            }
        elif tag == "blockquote":
            self.current_block = {
                "type": "quote",
                "props": {},
                "content": [],
                "styles": {},
            }
        elif tag == "ul":
            pass
        elif tag == "ol":
            pass
        elif tag == "li":
            parent_tag = self._get_parent_list_tag()
            if parent_tag == "ul":
                block_type = "bulletListItem"
            elif parent_tag == "ol":
                block_type = "numberedListItem"
            else:
                block_type = "bulletListItem"

            self.current_block = {
                "type": block_type,
                "props": {},
                "content": [],
                "styles": {},
            }
        elif tag == "div":
            class_attr = self._get_attr_value(attrs, "class")
            if class_attr and class_attr.startswith("blocknote-"):
                block_type = class_attr.replace("blocknote-", "")
                if block_type in [
                    "paragraph",
                    "heading",
                    "bulletListItem",
                    "numberedListItem",
                    "checkListItem",
                    "toggleListItem",
                    "quote",
                    "table",
                ]:
                    self.current_block = {
                        "type": block_type,
                        "props": {},
                        "content": [],
                        "styles": {},
                    }
                else:
                    self.current_block = {
                        "type": "paragraph",
                        "props": {},
                        "content": [],
                        "styles": {},
                    }
            else:
                self.current_block = {
                    "type": "paragraph",
                    "props": {},
                    "content": [],
                    "styles": {},
                }
        elif tag == "input":
            if self._get_attr_value(attrs, "type") == "checkbox":
                checked = "checked" in [attr[0] for attr in attrs]
                if self.current_block:
                    self.current_block["type"] = "checkListItem"
                    self.current_block["props"]["checked"] = checked
                else:
                    self.current_block = {
                        "type": "checkListItem",
                        "props": {"checked": checked},
                        "content": [],
                        "styles": {},
                    }
        elif tag in ["strong", "b"]:
            self.style_stack.append({"bold": True})
        elif tag in ["em", "i"]:
            self.style_stack.append({"italic": True})
        elif tag == "u":
            self.style_stack.append({"underline": True})
        elif tag == "s":
            self.style_stack.append({"strike": True})
        elif tag == "code":
            self.style_stack.append({"code": True})
        elif tag == "span":
            style_attr = self._get_attr_value(attrs, "style")
            styles = self._parse_style_attr(style_attr) if style_attr else {}
            if styles:
                self.style_stack.append(styles)

    def handle_endtag(self, tag: str):
        """Handle closing HTML tags."""
        if self.tag_stack:
            self.tag_stack.pop()

        if tag in [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "blockquote",
            "li",
            "div",
        ]:
            if self.current_block:
                if not self.current_block["content"]:
                    self.current_block["content"] = []

                block = Block(
                    id=str(uuid.uuid4()),
                    type=self.current_block["type"],
                    props=self.current_block["props"],
                    content=self.current_block["content"],
                    children=[],
                )
                self.blocks.append(block)
                self.current_block = None
        elif tag in ["strong", "b", "em", "i", "u", "s", "code", "span"]:
            if self.style_stack:
                self.style_stack.pop()

    def handle_data(self, data: str):
        """Handle text data between HTML tags."""
        if self.current_block is not None and data:
            combined_styles = {}
            for style_dict in self.style_stack:
                combined_styles.update(style_dict)

            inline_content = InlineContent(
                type="text", text=data, styles=combined_styles
            )
            self.current_block["content"].append(inline_content)

    def _get_parent_list_tag(self) -> str:
        """Get the parent list tag (ul or ol) from the tag stack."""
        for tag in reversed(self.tag_stack):
            if tag in ["ul", "ol"]:
                return tag
        return "ul"

    def _get_attr_value(self, attrs: List[tuple], attr_name: str) -> str:
        """Get the value of a specific attribute."""
        for name, value in attrs:
            if name == attr_name:
                return value
        return ""

    def _parse_style_attr(self, style_attr: str) -> Dict[str, Any]:
        """Parse CSS style attribute into a dictionary."""
        styles = {}
        if not style_attr:
            return styles

        for style_rule in style_attr.split(";"):
            if ":" in style_rule:
                prop, value = style_rule.split(":", 1)
                prop = prop.strip()
                value = value.strip()

                if prop == "color":
                    styles["textColor"] = value
                elif prop == "background-color":
                    styles["backgroundColor"] = value

        return styles


def _unescape_html(text: str) -> str:
    """
    Unescape HTML entities in text.

    Args:
        text: The text to unescape

    Returns:
        Unescaped text
    """
    if not isinstance(text, str):
        text = str(text)

    return (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#x27;", "'")
    )
