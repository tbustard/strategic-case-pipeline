"""Tests for fact extraction functionality."""

import pytest
from spacy.language import Language

from case_context.extract import extract_business_facts, process_case_text, load_nlp_model

@pytest.fixture
def nlp() -> Language:
    """Create spaCy model for testing."""
    return load_nlp_model()

def test_extract_business_facts(nlp):
    """Test basic fact extraction."""
    text = "Apple Inc. competes in the smartphone market with innovative products."
    facts = extract_business_facts(text, nlp)
    
    assert len(facts.noun_chunks) > 0
    assert any("smartphone market" in chunk.text.lower() for chunk in facts.noun_chunks)
    assert any("competes" in verb.text.lower() for verb in facts.business_verbs)

def test_process_case_text(nlp):
    """Test case and question processing."""
    case_text = "Tesla Motors is disrupting the automotive industry."
    question_text = "How does Tesla's strategy create competitive advantage?"
    
    case_facts = extract_business_facts(case_text, nlp)
    question_facts = extract_business_facts(question_text, nlp)
    
    assert len(case_facts.noun_chunks) > 0
    assert len(question_facts.noun_chunks) > 0
    assert any("automotive industry" in chunk.text.lower() for chunk in case_facts.noun_chunks)
    assert any("competitive advantage" in chunk.text.lower() for chunk in question_facts.noun_chunks) 