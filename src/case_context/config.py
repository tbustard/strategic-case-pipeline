"""Configuration settings for case context analysis."""

from pathlib import Path
from typing import Final, List

# Base paths
ROOT_DIR: Final[Path] = Path(__file__).parent.parent.parent
DATA_DIR: Final[Path] = ROOT_DIR / "data"
TEMPLATES_DIR: Final[Path] = ROOT_DIR / "templates"

# Application settings
MAX_OUTPUT_WORDS: Final[int] = 500
DEFAULT_THEME: Final[str] = "light"

# NLP settings
SPACY_MODEL: Final[str] = "en_core_web_lg"  # Use large model for better semantic matching
SPACY_MODEL_VERSION: Final[str] = "3.7.2"
FUZZY_THRESHOLD: Final[float] = 60.0  # Minimum fuzzy match score
SEMANTIC_THRESHOLD: Final[float] = 50.0  # Minimum semantic similarity score
REQUIRED_COMPONENTS: Final[List[str]] = ["tagger", "parser", "ner"]

# Logging
LOG_LEVEL: Final[str] = "INFO"
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Template settings
DEFAULT_WORD_LIMIT: Final[int] = 500
MAX_WORD_LIMIT: Final[int] = 550

# Export settings
DEFAULT_HEADING: Final[str] = "Case Analysis"
DEFAULT_FONT_SIZE: Final[int] = 12  # in points

# Create directories if they don't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
