# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of blocknote-py
- Core schema types: `Block` and `InlineContent` with Pydantic validation
- Converter functions:
  - `dict_to_blocks`: Convert dictionaries to Block objects
  - `blocks_to_dict`: Convert Block objects to dictionaries
  - `markdown_to_blocks`: Parse markdown into Block objects
  - `blocks_to_markdown`: Convert Block objects to markdown
- Support for block types:
  - Paragraph
  - Heading (H1-H6)
  - Bullet list items
  - Numbered list items
  - Check list items
  - Toggle list items
  - Quotes
  - Tables (basic support)
- Text formatting support:
  - Bold text
  - Italic text
- Comprehensive test suite with pytest
- Type safety with Pydantic models
- Full documentation and examples

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [0.1.0] - 2024-10-09

### Added
- Initial project setup
- Basic package structure
- MIT License
