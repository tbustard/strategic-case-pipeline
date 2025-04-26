"""Tests for the concept mapping module."""

import pytest
from spacy.tokens import Doc, Span
from spacy.language import Language

from case_context.map import map_concepts, ConceptMatch, FUZZY_THRESHOLD, SEMANTIC_THRESHOLD
from case_context.extract import ExtractedFacts, load_nlp_model
from case_context.knowledge_base import Concept, KNOWLEDGE_BASE

# Create a small test knowledge base
TEST_KNOWLEDGE_BASE = [
    Concept(name="Resource-Based View", category="Strategy", theory="RBV"),
    Concept(name="Transaction Cost Economics", category="Economics", theory="TCE"),
    Concept(name="Market Power", category="Economics", theory="TCE"),
    Concept(name="Competitive Advantage", category="Strategy", theory="RBV"),
]

@pytest.fixture
def nlp() -> Language:
    """Create spaCy model for testing."""
    model = load_nlp_model()
    # Check if model has vectors by trying to get a vector
    test_token = model("test")[0]
    assert test_token.has_vector, "spaCy model must have word vectors for semantic similarity"
    return model

@pytest.fixture
def sample_facts(nlp):
    """Create sample extracted facts for testing."""
    # Create docs with word vectors
    text = "resource-based view and transaction cost economics"
    doc = nlp(text)
    
    # Create spans that match exactly with the knowledge base concepts
    noun_chunks = [
        Span(doc, 0, 3),  # "resource-based view"
        Span(doc, 4, 7)   # "transaction cost economics"
    ]
    
    # Create business verbs
    verb_doc = nlp("compete and dominate")
    business_verbs = [
        Span(verb_doc, 0, 1),  # "compete"
        Span(verb_doc, 2, 3)   # "dominate"
    ]
    
    return ExtractedFacts(
        noun_chunks=noun_chunks,
        business_verbs=business_verbs,
        named_entities=[]  # Not used in these tests
    )

def test_fuzzy_matching(sample_facts, monkeypatch):
    """Test that fuzzy matching works with high similarity terms."""
    # Patch the knowledge base for testing
    monkeypatch.setattr("case_context.map.KNOWLEDGE_BASE", TEST_KNOWLEDGE_BASE)
    
    matches = map_concepts(sample_facts)
    
    # Should find exact matches for both noun chunks
    assert len(matches) >= 2
    assert any(m.concept.name == "Resource-Based View" and m.method == "fuzzy" for m in matches)
    assert any(m.concept.name == "Transaction Cost Economics" and m.method == "fuzzy" for m in matches)
    
    # Verify scores are above threshold
    assert all(m.score >= FUZZY_THRESHOLD for m in matches if m.method == "fuzzy")

def test_semantic_matching(nlp, monkeypatch):
    """Test that semantic matching works with related terms."""
    # Patch the knowledge base for testing
    monkeypatch.setattr("case_context.map.KNOWLEDGE_BASE", TEST_KNOWLEDGE_BASE)
    
    # Create facts with semantically similar terms
    text = "strategic resources and competitive capabilities"
    doc = nlp(text)
    
    # Create spans that should semantically match with RBV
    noun_chunks = [
        Span(doc, 0, 2),  # "strategic resources"
        Span(doc, 3, 5)   # "competitive capabilities"
    ]
    
    facts = ExtractedFacts(
        noun_chunks=noun_chunks,
        business_verbs=[],
        named_entities=[]
    )
    
    matches = map_concepts(facts)
    
    # Should find semantic matches
    assert len(matches) >= 1
    assert any(m.concept.name == "Resource-Based View" and m.method == "semantic" for m in matches)
    
    # Verify scores are above threshold
    assert all(m.score >= SEMANTIC_THRESHOLD * 100 for m in matches if m.method == "semantic")

def test_no_matches_below_threshold(nlp, monkeypatch):
    """Test that terms below threshold are not matched."""
    # Patch the knowledge base for testing
    monkeypatch.setattr("case_context.map.KNOWLEDGE_BASE", TEST_KNOWLEDGE_BASE)
    
    # Create facts with unrelated terms
    text = "apple banana orange"
    doc = nlp(text)
    
    # Create spans that should not match any concepts
    noun_chunks = [
        Span(doc, 0, 1),  # "apple"
        Span(doc, 1, 2),  # "banana"
        Span(doc, 2, 3)   # "orange"
    ]
    
    facts = ExtractedFacts(
        noun_chunks=noun_chunks,
        business_verbs=[],
        named_entities=[]
    )
    
    matches = map_concepts(facts)
    
    # Should find no matches
    assert len(matches) == 0

def test_matches_sorted_by_score(sample_facts, monkeypatch):
    """Test that matches are sorted by score in descending order."""
    # Patch the knowledge base for testing
    monkeypatch.setattr("case_context.map.KNOWLEDGE_BASE", TEST_KNOWLEDGE_BASE)
    
    matches = map_concepts(sample_facts)
    
    # Verify scores are in descending order
    scores = [m.score for m in matches]
    assert scores == sorted(scores, reverse=True)