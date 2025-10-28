from typing import List, Optional

from blocknote.schema import Block

from .blocknote_to_html import blocks_to_html

try:
    from weasyprint import CSS, HTML
    from weasyprint.text.fonts import FontConfiguration

    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False


def blocks_to_pdf(
    blocks: List[Block],
    output_path: Optional[str] = None,
    css_string: Optional[str] = None,
    font_config: Optional[object] = None,
    page_size: str = "A4",
    margin: str = "2cm",
) -> bytes:
    """Convert BlockNote blocks to PDF."""
    if not WEASYPRINT_AVAILABLE:
        raise ImportError(
            "WeasyPrint is required for PDF generation. "
            "Install it with: pip install 'blocknote-py[pdf]'"
        )

    if not isinstance(blocks, list):
        raise TypeError("Input must be a list of Block objects")

    if not blocks:
        html_content = (
            "<!DOCTYPE html><html><head><title>Empty Document</title>"
            "</head><body></body></html>"
        )
    else:
        try:
            html_body = blocks_to_html(blocks)
        except Exception as e:
            raise ValueError(f"Failed to convert blocks to HTML: {e}")

        html_content = _create_html_document(
            html_body, css_string, page_size, margin
        )

    try:
        if font_config is None:
            font_config = FontConfiguration()

        css_objects = []
        if css_string:
            css_objects.append(CSS(string=css_string))

        html_doc = HTML(string=html_content)

        if output_path:
            html_doc.write_pdf(
                output_path, stylesheets=css_objects, font_config=font_config
            )
            pdf_bytes = html_doc.write_pdf(
                stylesheets=css_objects, font_config=font_config
            )
            return pdf_bytes
        else:
            return html_doc.write_pdf(
                stylesheets=css_objects, font_config=font_config
            )

    except Exception as e:
        raise ValueError(f"Failed to generate PDF: {e}")


def _create_html_document(
    body_content: str,
    custom_css: Optional[str] = None,
    page_size: str = "A4",
    margin: str = "2cm",
) -> str:
    """Create complete HTML document with styling."""
    css_parts = [
        "@page {size: " + page_size + "; margin: " + margin + "; }",
        (
            "body { font-family: -apple-system, sans-serif; "
            "line-height: 1.6; color: #333; font-size: 12pt; }"
        ),
        (
            "h1,h2,h3,h4,h5,h6 { color: #2c3e50; margin-top: 1.5em; "
            "margin-bottom: 0.5em; page-break-after: avoid; }"
        ),
        "h1 { font-size: 24pt; }",
        "h2 { font-size: 20pt; }",
        "h3 { font-size: 16pt; }",
        "h4 { font-size: 14pt; }",
        "h5 { font-size: 12pt; }",
        "h6 { font-size: 11pt; }",
        "p { margin-bottom: 1em; orphans: 2; widows: 2; }",
        "ul,ol { margin-bottom: 1em; padding-left: 2em; }",
        "li { margin-bottom: 0.25em; }",
        (
            "blockquote { margin: 1em 0; padding: 0.5em 1em; "
            "border-left: 4px solid #3498db; background-color: #f8f9f9; "
            "font-style: italic; }"
        ),
        (
            "code { background-color: #f1f2f6; padding: 0.2em 0.4em; "
            "border-radius: 3px; font-family: Monaco, monospace; "
            "font-size: 0.9em; }"
        ),
        "strong { font-weight: 600; }",
        "em { font-style: italic; }",
        "u { text-decoration: underline; }",
        "s { text-decoration: line-through; }",
        (
            ".table-placeholder { border: 1px solid #ddd; padding: 1em; "
            "background-color: #f9f9f9; text-align: center; "
            "font-style: italic; }"
        ),
        "input[type='checkbox'] { margin-right: 0.5em; }",
        ".page-break { page-break-before: always; }",
        ".no-break { page-break-inside: avoid; }",
    ]

    default_css = "\n        ".join(css_parts)

    css_content = default_css
    if custom_css:
        css_content += "\n\n" + custom_css

    html_template = (
        f"<!DOCTYPE html><html lang='en'><head>"
        f"<meta charset='UTF-8'>"
        "<meta name='viewport' "
        "content='width=device-width, initial-scale=1.0'>"
        f"<title>BlockNote Document</title>"
        f"<style>{css_content}</style></head>"
        f"<body>{body_content}</body></html>"
    )

    return html_template


def blocks_to_pdf_with_template(
    blocks: List[Block],
    template_path: str,
    output_path: Optional[str] = None,
    template_variables: Optional[dict] = None,
) -> bytes:
    """Convert blocks to PDF using custom HTML template."""
    if not WEASYPRINT_AVAILABLE:
        raise ImportError(
            "WeasyPrint is required for PDF generation. "
            "Install it with: pip install 'blocknote-py[pdf]'"
        )

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")

    html_body = blocks_to_html(blocks)

    if template_variables:
        for key, value in template_variables.items():
            template_content = template_content.replace(
                f"{{{{{key}}}}}", str(value)
            )

    template_content = template_content.replace("{{content}}", html_body)

    try:
        html_doc = HTML(string=template_content)

        if output_path:
            html_doc.write_pdf(output_path)
            return html_doc.write_pdf()
        else:
            return html_doc.write_pdf()

    except Exception as e:
        raise ValueError(f"Failed to generate PDF from template: {e}")
