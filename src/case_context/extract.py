"""Text extraction and NLP processing module."""

import logging
from typing import TypedDict, List, Optional, Tuple, NamedTuple
import spacy
from spacy.tokens import Doc, Span
from spacy.language import Language
from dataclasses import dataclass
from spacy.cli import download

from case_context.config import SPACY_MODEL, REQUIRED_COMPONENTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_nlp: Optional[Language] = None


class ExtractedFacts(NamedTuple):
    """Container for extracted facts."""

    noun_chunks: List[Span]
    business_verbs: List[Span]
    named_entities: List[Span]
    source: str


def load_nlp_model() -> Language:
    """Load spaCy model with required components.

    Returns:
        Loaded spaCy model with all required components
    """
    global _nlp
    if _nlp is not None:
        return _nlp

    try:
        nlp = spacy.load(SPACY_MODEL)
        logger.info(f"Loaded spaCy model {SPACY_MODEL}")
    except OSError:
        # Download model if not available
        logger.info(f"Downloading spaCy model {SPACY_MODEL}")
        download(SPACY_MODEL)
        nlp = spacy.load(SPACY_MODEL)

    # Ensure all required components are loaded
    for component in REQUIRED_COMPONENTS:
        if component not in nlp.pipe_names:
            logger.info(f"Adding {component} to pipeline")
            try:
                if component == "ner":
                    nlp.add_pipe("ner", last=True)
                else:
                    nlp.add_pipe(component, last=True)
            except Exception as e:
                logger.warning(f"Failed to add {component} to pipeline: {str(e)}")
                continue

    # Initialize the model with a simple sentence
    try:
        logger.info("Initializing spaCy model")
        nlp("This is a test sentence to initialize the model.")
    except Exception as e:
        logger.error(f"Failed to initialize spaCy model: {str(e)}")
        raise

    _nlp = nlp
    
    # Verify pipeline components
    logger.info(f"Active pipeline components: {nlp.pipe_names}")
    return nlp


def extract_business_verbs(doc: Doc) -> List[Span]:
    """Extract business-related verbs from text.

    Args:
        doc: spaCy Doc object

    Returns:
        List of verb spans
    """
    business_verbs = []
    for token in doc:
        if token.pos_ == "VERB":
            # Check if verb is business-related
            if token.lemma_.lower() in {
                "compete",
                "market",
                "sell",
                "buy",
                "invest",
                "acquire",
                "merge",
                "expand",
                "grow",
                "develop",
                "innovate",
                "disrupt",
                "transform",
                "optimize",
                "leverage",
                "monetize",
                "scale",
                "partner",
                "create",
                "creates",
                "created",
                "creating",
            }:
                business_verbs.append(doc[token.i : token.i + 1])
    return business_verbs


def extract_facts(text: str, source: str = "case") -> ExtractedFacts:
    """Extract facts from text.

    Args:
        text: Text to extract facts from
        source: Source of the text (case/question/user_inputs)

    Returns:
        ExtractedFacts object containing noun chunks, business verbs, and named entities
    """
    nlp = load_nlp_model()
    doc = nlp(text)

    # Extract noun chunks
    noun_chunks = list(doc.noun_chunks)

    # Extract business verbs (verbs that might indicate strategic actions)
    business_verbs = extract_business_verbs(doc)

    # Extract named entities
    named_entities = list(doc.ents)

    return ExtractedFacts(
        noun_chunks=noun_chunks,
        business_verbs=business_verbs,
        named_entities=named_entities,
        source=source,
    )


def process_case_text(
    case_text: str, question_text: str, user_inputs_text: str = ""
) -> List[ExtractedFacts]:
    """Process case and question text to extract facts.

    Args:
        case_text: Text from the case
        question_text: Text from the question
        user_inputs_text: Optional user inputs

    Returns:
        List of ExtractedFacts objects
    """
    facts = []

    # Extract facts from case text
    if case_text:
        facts.append(extract_facts(case_text, source="case"))

    # Extract facts from question text
    if question_text:
        facts.append(extract_facts(question_text, source="question"))

    # Extract facts from user inputs
    if user_inputs_text:
        facts.append(extract_facts(user_inputs_text, source="user_inputs"))

    return facts
