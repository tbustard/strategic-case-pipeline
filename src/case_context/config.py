"""Configuration settings for the Strategic-Case Auto-Writer."""

import os
from pathlib import Path
from typing import Final

# Paths
ROOT_DIR: Final[Path] = Path(__file__).parent
TEMPLATES_DIR: Final[Path] = ROOT_DIR / "templates"
TESTS_DIR: Final[Path] = ROOT_DIR / "tests"

# Application settings
MAX_OUTPUT_WORDS: Final[int] = 500
DEFAULT_THEME: Final[str] = "light"

# NLP settings
SPACY_MODEL: Final[str] = "en_core_web_md"
SPACY_MODEL_VERSION: Final[str] = "3.7.2"
FUZZY_THRESHOLD: Final[float] = 80.0  # Minimum fuzzy match score (0-100)
SEMANTIC_THRESHOLD: Final[float] = 0.5  # Minimum semantic similarity score (0-1)

# Logging
LOG_LEVEL: Final[str] = "INFO"
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Ensure directories exist
for directory in [TEMPLATES_DIR, TESTS_DIR]:
    directory.mkdir(exist_ok=True) 