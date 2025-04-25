.PHONY: install test lint clean build publish

# Variables
PYTHON := python
PIP := pip
PYTEST := pytest
PYLINT := pylint
SOURCE_DIR := file_manager

# Default target
all: install lint test

# Install dependencies
install:
	$(PIP) install -e .
	$(PIP) install pytest pylint requests numpy

# Run tests
test:
	$(PYTEST)

# Run linting
lint:
	$(PYLINT) $(SOURCE_DIR)

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build package
build: clean
	$(PYTHON) setup.py sdist bdist_wheel

# Publish to PyPI
publish: build
	$(PIP) install twine
	twine upload dist/*

# Run the application
run:
	$(PYTHON) main.py $(ARGS)

# Help command
help:
	@echo "Available targets:"
	@echo "  all        : Install dependencies, run linting and tests"
	@echo "  install    : Install package in development mode and testing tools"
	@echo "  test       : Run tests"
	@echo "  lint       : Run linting"
	@echo "  clean      : Remove build artifacts"
	@echo "  build      : Build distribution packages"
	@echo "  publish    : Publish package to PyPI"
	@echo "  run        : Run the application (use ARGS='arguments')"
	@echo "  help       : Show this help message"
