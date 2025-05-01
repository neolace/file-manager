import setuptools

setup(
    name="file-manager",
    version="1.0.0",
    author="Tertius Geldenhuys",
    author_email="tertius.geldenhuys@outlook.com",
    description="A Python utility for efficient file management, cleaning, and organization.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/neolace/file-manager",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "dev": ["pytest", "pylint", "black"],
    },
    entry_points={
        "console_scripts": [
            "file-manager=file_manager.main:main",
        ],
    },
    package_data={
        "file_manager": ["config/*.json", "templates/*.html"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
