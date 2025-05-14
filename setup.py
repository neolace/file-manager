from setuptools import setup, find_packages

# Project metadata
PROJECT_NAME = "file-manager"
VERSION = "1.0.0"
AUTHOR = "Tertius Geldenhuys"
AUTHOR_EMAIL = "tertius.geldenhuys@outlook.com"
GITHUB_URL = "https://github.com/neolace/file-manager"
MIN_PYTHON_VERSION = ">=3.6"
README_PATH = "README.md"


def read_long_description(file_path: str) -> str:
    """Read and return the content of the long description file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# Package configuration groups
package_metadata = {
    "name": PROJECT_NAME,
    "version": VERSION,
    "author": AUTHOR,
    "author_email": AUTHOR_EMAIL,
    "description": "A Python utility for efficient file management, cleaning, and organization.",
    "long_description": read_long_description(README_PATH),
    "long_description_content_type": "text/markdown",
    "url": GITHUB_URL,
}

dependencies = {
    "packages": find_packages(),
    "python_requires": MIN_PYTHON_VERSION,
    "install_requires": [],  # Add dependencies here, e.g., "requests>=2.25.1"
    "extras_require": {
        "dev": ["pytest", "pylint", "black"],
    },
}

project_files = {
    "package_data": {
        "file_manager": ["config/*.json", "templates/*.html"],
    },
}

entry_points = {
    "console_scripts": [
        "file-manager=file_manager.main:main",
    ],
}

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

# Setup configuration
setup(
    **package_metadata,
    **dependencies,
    **project_files,
    entry_points=entry_points,
    classifiers=classifiers,
)
