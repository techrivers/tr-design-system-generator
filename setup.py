"""Setup script for Design System Generator."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="tr-design-system-generator",
    version="1.0.0",
    description="Autonomous AI-powered design system creation from product ideas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Technology Rivers",
    author_email="info@technologyrivers.com",
    url="https://github.com/anadeem93/tr-design-system-generator",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "jinja2>=3.1.0",
        "python-multipart>=0.0.6",
        "aiofiles>=23.2.1",
        "python-dotenv>=1.0.0",
        "colorama>=0.4.6",
        "rich>=13.7.0",
        "litellm>=1.15.0",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "tr-ds=cli.cli:main",
        ],
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Designers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
)
