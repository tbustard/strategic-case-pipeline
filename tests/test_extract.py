"""Tests for fact extraction functionality."""

import pytest
from spacy.tokens import Doc, Span
from spacy.language import Language

from case_context.extract import extract_facts, process_case_text, load_nlp_model


@pytest.fixture
def nlp() -> Language:
    """Create spaCy model for testing."""
    model = load_nlp_model()
    # Check if model has vectors by trying to get a vector
    test_token = model("test")[0]
    assert (
        test_token.has_vector
    ), "spaCy model must have word vectors for semantic similarity"
    return model


def test_extract_facts_basic():
    """Test basic fact extraction."""
    text = "Apple Inc. leverages its strong brand to create network effects."
    facts = extract_facts(text)

    # Check noun chunks
    assert len(facts.noun_chunks) > 0
    assert any("Apple Inc" in chunk.text for chunk in facts.noun_chunks)
    assert any("brand" in chunk.text for chunk in facts.noun_chunks)

    # Check business verbs
    assert len(facts.business_verbs) > 0
    assert any("leverages" in verb.text for verb in facts.business_verbs)

    # Check named entities
    assert len(facts.named_entities) > 0
    assert any("Apple Inc" in ent.text for ent in facts.named_entities)


def test_extract_facts_empty():
    """Test fact extraction with empty text."""
    facts = extract_facts("")
    assert len(facts.noun_chunks) == 0
    assert len(facts.business_verbs) == 0
    assert len(facts.named_entities) == 0


def test_process_case_text():
    """Test processing both case and question text."""
    case_text = "The company leverages network effects."
    question_text = "How does the platform create value?"

    case_facts, question_facts = process_case_text(case_text, question_text)

    # Check case facts
    assert len(case_facts.noun_chunks) > 0
    assert any("company" in chunk.text for chunk in case_facts.noun_chunks)
    assert any("leverages" in verb.text for verb in case_facts.business_verbs)

    # Check question facts
    assert len(question_facts.noun_chunks) > 0
    assert any("platform" in chunk.text for chunk in question_facts.noun_chunks)
    assert any("creat" in verb.lemma_ for verb in question_facts.business_verbs)
