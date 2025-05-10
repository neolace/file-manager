.PHONY: install test lint clean build publish venv coverage typecheck

# Variables
PYTHON := python
PIP := pip
PYTEST := pytest
PYLINT := pylint
MYPY := mypy
SOURCE_DIR := file_manager
VERSION := 1.0.0

# Default target
all: install lint typecheck test

venv:
	$(PYTHON) -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  source venv/bin/activate (Linux/Mac)"
	@echo "  venv\\Scripts\\activate (Windows)"

install:
	$(PIP) install -e .
	$(PIP) install pytest pylint mypy pytest-cov requests numpy

test:
	$(PYTEST)

coverage:
	$(PYTEST) --cov=$(SOURCE_DIR) --cov-report=term-missing

typecheck:
	$(MYPY) $(SOURCE_DIR)

lint:
	$(PYLINT) $(SOURCE_DIR)

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

build: clean
	$(PYTHON) setup.py sdist bdist_wheel

publish: build
	$(PIP) install twine
	twine upload dist/*

run:
	$(PYTHON) main.py $(ARGS)

help:
	@echo "Available targets:"
	@echo "  all        : Install dependencies, run linting, type checking and tests"
	@echo "  install    : Install package in development mode and testing tools"
	@echo "  test       : Run tests"
	@echo "  coverage   : Run tests with coverage report"
	@echo "  typecheck  : Run type checking with mypy"
	@echo "  lint       : Run linting"
	@echo "  clean      : Remove build artifacts"
	@echo "  build      : Build distribution packages"
	@echo "  publish    : Publish package to PyPI"
	@echo "  run        : Run the application (use ARGS='arguments')"
	@echo "  venv       : Create a virtual environment"
	@echo "  help       : Show this help message"