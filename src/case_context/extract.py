"""Text extraction and NLP processing module."""

import logging
from typing import TypedDict, List, Optional
import spacy
from spacy.tokens import Doc, Span
from spacy.language import Language
from dataclasses import dataclass

from case_context.config import SPACY_MODEL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_nlp: Optional[Language] = None

@dataclass
class ExtractedFacts:
    """Container for extracted business facts from text."""
    noun_chunks: List[Span]
    business_verbs: List[Span]
    named_entities: List[Span]

def load_nlp_model() -> Language:
    """Load and cache the spaCy model with required pipeline components."""
    global _nlp
    if _nlp is None:
        try:
            logger.info(f"Loading spaCy model: {SPACY_MODEL}")
            _nlp = spacy.load(SPACY_MODEL)
            # Ensure we have the dependency parser for noun chunks
            if "parser" not in _nlp.pipe_names:
                _nlp.add_pipe("parser")
            logger.info("Loaded spaCy pipeline with components: %s", _nlp.pipe_names)
        except OSError:
            logger.error(
                f"Model {SPACY_MODEL} not found. Please run: python -m spacy download {SPACY_MODEL}"
            )
            raise
    return _nlp

def extract_business_facts(text: str, nlp: spacy.Language) -> ExtractedFacts:
    """Extract business-related facts from text.
    
    Args:
        text: The text to analyze
        nlp: A loaded spaCy language model
        
    Returns:
        ExtractedFacts containing noun chunks, business verbs, and named entities
    """
    doc = nlp(text)
    
    # Extract noun chunks
    noun_chunks = list(doc.noun_chunks)
    
    # Extract business verbs (verbs that might indicate business actions)
    business_verbs = [token for token in doc if token.pos_ == "VERB"]
    
    # Extract named entities
    named_entities = [ent for ent in doc.ents if ent.label_ in {"ORG", "PRODUCT", "GPE"}]
    
    return ExtractedFacts(
        noun_chunks=noun_chunks,
        business_verbs=business_verbs,
        named_entities=named_entities
    )

def process_case_text(case_text: str, question_text: str) -> tuple[ExtractedFacts, ExtractedFacts]:
    """
    Process both case text and question text to extract relevant information.
    
    Args:
        case_text: The main case study text
        question_text: The question(s) to be answered
        
    Returns:
        Tuple of ExtractedFacts for case and question
    """
    logger.info("Processing case and question text")
    nlp = load_nlp_model()  # Load model once and reuse
    case_facts = extract_business_facts(case_text, nlp)
    question_facts = extract_business_facts(question_text, nlp)
    return case_facts, question_facts 