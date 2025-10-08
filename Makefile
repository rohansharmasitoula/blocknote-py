.PHONY: help test lint format type-check check-all fix-all clean install setup-dev

help:
	@echo "Available commands:"
	@echo "  make test          - Run tests with pytest"
	@echo "  make test-cov      - Run tests with coverage report"
	@echo "  make lint          - Run flake8 linter"
	@echo "  make format        - Format code with black and isort"
	@echo "  make type-check    - Run mypy type checker"
	@echo "  make check-all     - Run all checks (lint + format check + type check)"
	@echo "  make fix-all       - Auto-fix formatting and import issues"
	@echo "  make clean         - Remove build artifacts and cache files"
	@echo "  make install       - Install package in development mode"
	@echo "  make setup-dev     - Complete development setup"

test:
	PYTHONPATH=src uv run python -m pytest -v

test-cov:
	PYTHONPATH=src uv run python -m pytest -v --cov=src --cov-report=html --cov-report=term

lint:
	uv run flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
	uv run flake8 src --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics

format:
	uv run black src
	uv run isort src

format-check:
	uv run black --check src
	uv run isort --check-only src

type-check:
	uv run mypy src --ignore-missing-imports

check-all: lint format-check type-check
	@echo "All checks passed!"

fix-all: format
	@echo "Code formatting fixed!"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

install:
	uv pip install -e .

setup-dev:
	uv sync --dev
	uv run pre-commit install
	@echo "Development environment setup complete!"

build:
	uv build

publish-test:
	uv build
	uv run twine upload --repository testpypi dist/*

publish:
	uv build
	uv run twine upload dist/*
