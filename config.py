"""Application configuration and settings."""

import logging
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
SPACY_MODEL: Final[str] = "en_core_web_sm"

# Version of the spaCy model package to install
SPACY_MODEL_VERSION: Final[str] = "3.7.1"

# Matching thresholds for concept mapping
FUZZY_THRESHOLD: Final[float] = 70.0
SEMANTIC_THRESHOLD: Final[float] = 0.65

# Logging
LOG_LEVEL: Final[str] = "INFO"
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Ensure directories exist
for directory in [TEMPLATES_DIR, TESTS_DIR]:
    directory.mkdir(exist_ok=True)
