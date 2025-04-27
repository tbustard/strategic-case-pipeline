"""Tests for error handling and edge cases."""

import pytest
from spacy.tokens import Doc, Span
from spacy.language import Language

from case_context.extract import load_nlp_model
from case_context.knowledge_base import Concept
from case_context.map import map_concepts


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


def test_semantic_match_term(nlp, monkeypatch):
    """Test that semantic matching works with similar terms."""
    # Create a test knowledge base
    test_concepts = [
        Concept(
            name="Network Effects",
            definition="Value increases with user base",
            theory="Platform",
        ),
        Concept(
            name="Value Chain",
            definition="Sequential activities that add value",
            theory="RBV",
        ),
    ]
    monkeypatch.setattr(
        "case_context.map.CONCEPTS", {c.name: c.definition for c in test_concepts}
    )

    # Test with semantically similar terms
    facts = {
        "case_text": "The platform exhibits strong network externalities.",
        "question_text": "",
        "user_inputs_text": "",
    }
    matches = map_concepts(facts=facts)
    assert len(matches) > 0
    assert any(m.concept == "Network Effects" for m in matches)


def test_semantic_match_term_no_match(nlp, monkeypatch):
    """Test that unrelated terms get low similarity scores."""
    # Create a test knowledge base
    test_concepts = [
        Concept(
            name="Network Effects",
            definition="Value increases with user base",
            theory="Platform",
        ),
        Concept(
            name="Value Chain",
            definition="Sequential activities that add value",
            theory="RBV",
        ),
    ]
    monkeypatch.setattr(
        "case_context.map.CONCEPTS", {c.name: c.definition for c in test_concepts}
    )

    # Test with unrelated terms
    facts = {
        "case_text": "The weather was nice today.",
        "question_text": "",
        "user_inputs_text": "",
    }
    matches = map_concepts(facts=facts)
    assert len(matches) == 0  # No matches above threshold
