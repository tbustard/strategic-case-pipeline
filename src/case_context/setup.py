"""Setup configuration for the case_context package."""

import sys

# Remove any pytest flags before calling setup()
if len(sys.argv) > 1:
    sys.argv = [a for a in sys.argv if not a.startswith("-") and not a.startswith("not")]
if len(sys.argv) == 1:
    sys.argv.append("build")

from setuptools import setup, find_packages

setup(
    name="case_context",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.0.0",
        "fuzzywuzzy>=0.18.0",
        "python-Levenshtein>=0.12.0",
        "jinja2>=3.0.0",
        "python-docx>=0.8.11",
    ],
    python_requires=">=3.9",
)
