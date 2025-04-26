from case_context.setuptools import setup, find_packages

setup(
    name="case-context",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.32.0",
        "spacy==3.7.2",
        "python-docx==1.1.0",
        "pytest==8.0.0",
        "python-dotenv==1.0.1",
        "rapidfuzz>=2.13.7",
    ],
) 