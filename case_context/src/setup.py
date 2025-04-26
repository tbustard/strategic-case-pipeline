from setuptools import setup, find_packages

setup(
    name="case_context",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.7.2",
        "en-core-web-sm==3.7.1",
        "python-docx>=1.1.0",
        "pytest>=8.0.0",
        "python-dotenv>=1.1.0",
        "rapidfuzz>=2.13.7",
    ],
    python_requires=">=3.9",
) 