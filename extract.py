"""Text extraction and NLP processing module."""

import logging
from typing import TypedDict, List, Optional
import spacy
from spacy.tokens import Doc
from spacy.language import Language

from case_context.config import SPACY_MODEL
from bench_speed import get_optimized_nlp

# Configure logging with more explicit format
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)

# Cache for spaCy NLP model
_nlp: Optional[spacy.language.Language] = None


class ExtractedFacts(TypedDict):
    """Structure for extracted business-relevant information."""

    named_entities: List[str]
    noun_chunks: List[str]
    business_verbs: List[str]


def load_nlp_model() -> spacy.language.Language:
    """
    Load and return the spaCy NLP model (caching so it loads only once).

    Note: uses the model name defined in config.SPACY_MODEL.
    """
    global _nlp
    if _nlp is None:
        try:
            logger.info("Loading spaCy model: %s", SPACY_MODEL)
            _nlp = get_optimized_nlp()
            logger.info("Loaded optimized spaCy pipeline: %s", _nlp.pipe_names)
        except OSError:
            logger.error(
                f"Model {SPACY_MODEL} not found. Please run: python -m spacy download {SPACY_MODEL}"
            )
            raise
    return _nlp


def extract_business_facts(text: str) -> ExtractedFacts:
    """
    Extract business-relevant information from text using NLP.

    Args:
        text: Input text to analyze

    Returns:
        ExtractedFacts containing named entities, noun chunks, and business verbs
    """
    nlp = load_nlp_model()
    doc = nlp(text)

    # TODO: Refine business verb list based on strategic management context
    business_verbs = {
        "acquire",
        "compete",
        "differentiate",
        "diversify",
        "enter",
        "exit",
        "expand",
        "innovate",
        "integrate",
        "merge",
        "outsource",
        "partner",
        "position",
        "scale",
        "segment",
        "specialize",
        "standardize",
    }

    return ExtractedFacts(
        named_entities=[ent.text for ent in doc.ents],
        noun_chunks=[chunk.text for chunk in doc.noun_chunks],
        business_verbs=[
            token.text for token in doc if token.text.lower() in business_verbs
        ],
    )


def process_case_text(
    case_text: str, question_text: str
) -> tuple[ExtractedFacts, ExtractedFacts]:
    """
    Process both case text and question text to extract relevant information.

    Args:
        case_text: The main case study text
        question_text: The question(s) to be answered

    Returns:
        Tuple of ExtractedFacts for case and question
    """
    logger.info("Processing case and question text")
    case_facts = extract_business_facts(case_text)
    question_facts = extract_business_facts(question_text)
    return case_facts, question_facts
