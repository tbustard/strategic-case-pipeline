"""Test configuration and fixtures."""
import pytest
from spacy.language import Language

from case_context.extract import load_nlp_model
from case_context.config import SPACY_MODEL

@pytest.fixture(scope="session")
def nlp_model() -> Language:
    """Initialize spaCy model once for all tests.
    
    Returns:
        Loaded spaCy model with all required components
    """
    return load_nlp_model()

@pytest.fixture(autouse=True)
def setup_nlp(nlp_model: Language) -> None:
    """Ensure NLP model is loaded before each test.
    
    Args:
        nlp_model: The loaded spaCy model
        
    Raises:
        AssertionError: If model is not properly initialized
    """
    assert nlp_model.pipe_names, "NLP model pipeline components not loaded"
    assert "ner" in nlp_model.pipe_names, "NER component not loaded" 