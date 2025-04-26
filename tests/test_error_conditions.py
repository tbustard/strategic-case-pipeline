"""Tests for semantic matching and mapping functionality."""

import pytest
from spacy.tokens import Doc, Span
from spacy.language import Language

from case_context.map import map_concepts, ConceptMatch
from case_context.extract import ExtractedFacts, load_nlp_model
from case_context.knowledge_base import Concept

@pytest.fixture
def nlp() -> Language:
    """Create spaCy model for testing."""
    model = load_nlp_model()
    # Check if model has vectors by trying to get a vector
    test_token = model("test")[0]
    assert test_token.has_vector, "spaCy model must have word vectors for semantic similarity"
    return model

def test_semantic_match_term(nlp, monkeypatch):
    """Test that semantic matching works with similar terms."""
    # Create a test knowledge base
    test_concepts = [
        Concept(name="Network Effects", category="Economics", theory="Platform"),
        Concept(name="Value Chain", category="Strategy", theory="RBV")
    ]
    
    # Create test facts
    doc = nlp("network effect")
    noun_chunks = [Span(doc, 0, 2)]  # "network effect"
    facts = ExtractedFacts(
        noun_chunks=noun_chunks,
        business_verbs=[],
        named_entities=[]
    )
    
    # Patch the knowledge base
    monkeypatch.setattr("case_context.map.KNOWLEDGE_BASE", test_concepts)
    matches = map_concepts(facts)
    
    # Should find a match for "network effect"
    assert len(matches) > 0
    assert any(m.concept.name == "Network Effects" for m in matches)
    assert any(m.score > 70 for m in matches)  # Score scaled to 0-100

def test_semantic_match_term_no_match(nlp, monkeypatch):
    """Test that unrelated terms get low similarity scores."""
    # Create a test knowledge base
    test_concepts = [
        Concept(name="Network Effects", category="Economics", theory="Platform"),
        Concept(name="Value Chain", category="Strategy", theory="RBV")
    ]
    
    # Create test facts with completely unrelated terms
    doc = nlp("purple elephant dancing")
    noun_chunks = [Span(doc, 0, 3)]  # "purple elephant dancing"
    facts = ExtractedFacts(
        noun_chunks=noun_chunks,
        business_verbs=[],
        named_entities=[]
    )
    
    # Patch the knowledge base
    monkeypatch.setattr("case_context.map.KNOWLEDGE_BASE", test_concepts)
    matches = map_concepts(facts)
    
    # Should find no matches at all
    assert len(matches) == 0