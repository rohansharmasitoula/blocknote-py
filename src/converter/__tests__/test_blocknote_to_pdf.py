import os
import tempfile

import pytest
from blocknote.schema import Block, BlockType, InlineContent, InlineContentType

try:
    from converter.blocknote_to_pdf import (
        WEASYPRINT_AVAILABLE,
        _create_html_document,
        blocks_to_pdf,
        blocks_to_pdf_with_template,
    )
except ImportError:
    WEASYPRINT_AVAILABLE = False


@pytest.mark.skipif(
    not WEASYPRINT_AVAILABLE, reason="WeasyPrint not available"
)
class TestBlocknoteToPdf:
    """Test cases for BlockNote to PDF conversion."""

    def test_empty_blocks_to_pdf(self):
        """Test converting empty blocks list to PDF."""
        blocks = []
        pdf_bytes = blocks_to_pdf(blocks)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b"%PDF-")

    def test_single_paragraph_to_pdf(self):
        """Test converting a single paragraph block to PDF."""
        blocks = [
            Block(
                id="1",
                type=BlockType.PARAGRAPH,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="Hello, World!"
                    )
                ],
            )
        ]

        pdf_bytes = blocks_to_pdf(blocks)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b"%PDF-")

    def test_heading_blocks_to_pdf(self):
        """Test converting heading blocks to PDF."""
        blocks = [
            Block(
                id="1",
                type=BlockType.HEADING,
                props={"level": 1},
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="Main Title"
                    )
                ],
            ),
            Block(
                id="2",
                type=BlockType.HEADING,
                props={"level": 2},
                content=[
                    InlineContent(type=InlineContentType.TEXT, text="Subtitle")
                ],
            ),
            Block(
                id="3",
                type=BlockType.PARAGRAPH,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="Some content under the subtitle.",
                    )
                ],
            ),
        ]

        pdf_bytes = blocks_to_pdf(blocks)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b"%PDF-")

    def test_styled_text_to_pdf(self):
        """Test converting blocks with styled text to PDF."""
        blocks = [
            Block(
                id="1",
                type=BlockType.PARAGRAPH,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="This is bold text",
                        styles={"bold": True},
                    )
                ],
            ),
            Block(
                id="2",
                type=BlockType.PARAGRAPH,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="This is italic text",
                        styles={"italic": True},
                    )
                ],
            ),
            Block(
                id="3",
                type=BlockType.PARAGRAPH,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="This is colored text",
                        styles={
                            "textColor": "red",
                            "backgroundColor": "yellow",
                        },
                    )
                ],
            ),
        ]

        pdf_bytes = blocks_to_pdf(blocks)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b"%PDF-")

    def test_list_blocks_to_pdf(self):
        """Test converting list blocks to PDF."""
        blocks = [
            Block(
                id="1",
                type=BlockType.BULLET_LIST_ITEM,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="First bullet point"
                    )
                ],
            ),
            Block(
                id="2",
                type=BlockType.BULLET_LIST_ITEM,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="Second bullet point"
                    )
                ],
            ),
            Block(
                id="3",
                type=BlockType.NUMBERED_LIST_ITEM,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="First numbered item"
                    )
                ],
            ),
            Block(
                id="4",
                type=BlockType.CHECK_LIST_ITEM,
                props={"checked": True},
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="Completed task"
                    )
                ],
            ),
        ]

        pdf_bytes = blocks_to_pdf(blocks)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b"%PDF-")

    def test_quote_block_to_pdf(self):
        """Test converting quote blocks to PDF."""
        blocks = [
            Block(
                id="1",
                type=BlockType.QUOTE,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="This is a quote block.",
                    )
                ],
            )
        ]

        pdf_bytes = blocks_to_pdf(blocks)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b"%PDF-")

    def test_save_pdf_to_file(self):
        """Test saving PDF to a file."""
        blocks = [
            Block(
                id="1",
                type=BlockType.PARAGRAPH,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="Test content for file output",
                    )
                ],
            )
        ]

        with tempfile.NamedTemporaryFile(
            suffix=".pdf", delete=False
        ) as tmp_file:
            tmp_path = tmp_file.name

        try:
            pdf_bytes = blocks_to_pdf(blocks, output_path=tmp_path)

            # Check that file was created
            assert os.path.exists(tmp_path)
            assert os.path.getsize(tmp_path) > 0

            # Check that bytes are still returned
            assert isinstance(pdf_bytes, bytes)
            assert len(pdf_bytes) > 0
            assert pdf_bytes.startswith(b"%PDF-")

            # Check file content
            with open(tmp_path, "rb") as f:
                file_content = f.read()
                assert file_content.startswith(b"%PDF-")

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_custom_css_styling(self):
        """Test PDF generation with custom CSS."""
        blocks = [
            Block(
                id="1",
                type=BlockType.HEADING,
                props={"level": 1},
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="Custom Styled Title"
                    )
                ],
            ),
            Block(
                id="2",
                type=BlockType.PARAGRAPH,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="This paragraph has custom styling.",
                    )
                ],
            ),
        ]

        custom_css = """
        h1 {
            color: #ff6b6b;
            text-align: center;
            border-bottom: 2px solid #4ecdc4;
        }
        p {
            font-size: 14pt;
            text-align: justify;
        }
        """

        pdf_bytes = blocks_to_pdf(blocks, css_string=custom_css)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b"%PDF-")

    def test_custom_page_settings(self):
        """Test PDF generation with custom page settings."""
        blocks = [
            Block(
                id="1",
                type=BlockType.PARAGRAPH,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="Content with custom page settings",
                    )
                ],
            )
        ]

        pdf_bytes = blocks_to_pdf(blocks, page_size="Letter", margin="1in")

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b"%PDF-")

    def test_template_based_pdf_generation(self):
        """Test PDF generation using a custom template."""
        blocks = [
            Block(
                id="1",
                type=BlockType.HEADING,
                props={"level": 1},
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="Template Test"
                    )
                ],
            ),
            Block(
                id="2",
                type=BlockType.PARAGRAPH,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="This content is inserted into a template.",
                    )
                ],
            ),
        ]

        # Create a temporary template file
        template_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2cm; }
        .header { text-align: center; color: #333; }
        .footer { text-align: center; font-size: 10pt; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{document_title}}</h1>
        <hr>
    </div>

    <div class="content">
        {{content}}
    </div>

    <div class="footer">
        <hr>
        <p>Generated by BlockNote-py</p>
    </div>
</body>
</html>"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False
        ) as tmp_template:
            tmp_template.write(template_content)
            template_path = tmp_template.name

        try:
            template_variables = {
                "title": "Test Document",
                "document_title": "My Custom Document",
            }

            pdf_bytes = blocks_to_pdf_with_template(
                blocks, template_path, template_variables=template_variables
            )

            assert isinstance(pdf_bytes, bytes)
            assert len(pdf_bytes) > 0
            assert pdf_bytes.startswith(b"%PDF-")

        finally:
            if os.path.exists(template_path):
                os.unlink(template_path)

    def test_invalid_input_types(self):
        """Test error handling for invalid input types."""
        with pytest.raises(
            TypeError, match="Input must be a list of Block objects"
        ):
            blocks_to_pdf("not a list")

        with pytest.raises((TypeError, ValueError)):
            blocks_to_pdf(["not", "block", "objects"])

    def test_create_html_document_function(self):
        """Test the _create_html_document helper function."""
        body_content = "<h1>Test</h1><p>Content</p>"
        custom_css = "h1 { color: red; }"

        html_doc = _create_html_document(
            body_content, custom_css=custom_css, page_size="A4", margin="1cm"
        )

        assert "<!DOCTYPE html>" in html_doc
        assert "<h1>Test</h1><p>Content</p>" in html_doc
        assert "h1 { color: red; }" in html_doc
        assert "size: A4;" in html_doc
        assert "margin: 1cm;" in html_doc

    def test_template_file_not_found(self):
        """Test error handling when template file is not found."""
        blocks = [
            Block(
                id="1",
                type=BlockType.PARAGRAPH,
                content=[
                    InlineContent(type=InlineContentType.TEXT, text="Test")
                ],
            )
        ]

        with pytest.raises(FileNotFoundError, match="Template file not found"):
            blocks_to_pdf_with_template(blocks, "/nonexistent/template.html")

    def test_complex_document_structure(self):
        """Test PDF generation with a complex document structure."""
        blocks = [
            Block(
                id="1",
                type=BlockType.HEADING,
                props={"level": 1},
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="Document Title"
                    )
                ],
            ),
            Block(
                id="2",
                type=BlockType.PARAGRAPH,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="This document contains ",
                    ),
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="bold",
                        styles={"bold": True},
                    ),
                    InlineContent(type=InlineContentType.TEXT, text=" and "),
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="italic",
                        styles={"italic": True},
                    ),
                    InlineContent(type=InlineContentType.TEXT, text=" text."),
                ],
            ),
            Block(
                id="3",
                type=BlockType.HEADING,
                props={"level": 2},
                content=[
                    InlineContent(type=InlineContentType.TEXT, text="Features")
                ],
            ),
            Block(
                id="4",
                type=BlockType.BULLET_LIST_ITEM,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="Bullet lists"
                    )
                ],
            ),
            Block(
                id="5",
                type=BlockType.BULLET_LIST_ITEM,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="Numbered lists"
                    )
                ],
            ),
            Block(
                id="6",
                type=BlockType.QUOTE,
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT,
                        text="Quotes are also supported",
                    )
                ],
            ),
            Block(
                id="7",
                type=BlockType.CHECK_LIST_ITEM,
                props={"checked": True},
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="Completed task"
                    )
                ],
            ),
            Block(
                id="8",
                type=BlockType.CHECK_LIST_ITEM,
                props={"checked": False},
                content=[
                    InlineContent(
                        type=InlineContentType.TEXT, text="Pending task"
                    )
                ],
            ),
        ]

        pdf_bytes = blocks_to_pdf(blocks)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b"%PDF-")


@pytest.mark.skipif(
    WEASYPRINT_AVAILABLE,
    reason="Testing ImportError when WeasyPrint is not available",
)
class TestBlocknoteToPdfWithoutWeasyPrint:
    """Test cases for when WeasyPrint is not available."""

    def test_import_error_without_weasyprint(self):
        """Test that an error is raised when WeasyPrint is unavailable."""
        pass
