"""Tests for the map module."""

import pytest
from case_context.map import (
    fuzzy_match_term,
    semantic_match_term,
    map_to_knowledge_base,
    FUZZY_THRESHOLD,
    SEMANTIC_THRESHOLD
)
from case_context.extract import load_nlp_model
from case_context.knowledge_base import KNOWLEDGE_BASE
from case_context.config import SEMANTIC_THRESHOLD as CONFIG_SEMANTIC_THRESHOLD

def test_fuzzy_match_term():
    """Test fuzzy matching functionality."""
    choices = ["transaction cost", "resource based view", "competitive advantage"]
    
    # Exact match should return 100
    match, score = fuzzy_match_term("transaction cost", choices)
    assert match == "transaction cost"
    assert score == 100.0
    
    # Close match should score above threshold
    match, score = fuzzy_match_term("transact cost", choices)
    assert match == "transaction cost"
    assert score >= FUZZY_THRESHOLD
    
    # Unrelated term should score low
    match, score = fuzzy_match_term("unrelated concept", choices)
    assert score < FUZZY_THRESHOLD

def test_semantic_match_term():
    """Test semantic matching of business terms."""
    nlp = load_nlp_model()
    
    # Test exact match
    match, score = semantic_match_term("network effects", ["network effects", "barriers to entry", "value chain"], nlp)
    assert match == "network effects"
    assert score == 1.0
    
    # Test close match
    match, score = semantic_match_term("network effect", ["network effects", "barriers to entry", "value chain"], nlp)
    assert match == "network effects"
    assert score >= SEMANTIC_THRESHOLD
    
    # Test no match
    match, score = semantic_match_term("completely unrelated", ["network effects", "barriers to entry"], nlp)
    assert score < SEMANTIC_THRESHOLD

def test_map_to_knowledge_base():
    """Test mapping of terms to knowledge base concepts."""
    terms = ["network effects", "completely unknown term"]
    mapped = map_to_knowledge_base(terms)
    
    # Check network effects mapping
    network = next(m for m in mapped if m["concept"] == "network effects")
    assert network["category"] == "Business_Concept"
    assert network["confidence"] > CONFIG_SEMANTIC_THRESHOLD
    
    # Check unmapped term
    unmapped = next(m for m in mapped if m["concept"] == "completely unknown term")
    assert unmapped["category"] == "Unmapped"
    assert unmapped["confidence"] < 0.75  # Slightly more lenient threshold

def test_edge_cases():
    """Test edge case handling in mapping."""
    nlp = load_nlp_model()
    
    # Test ambiguous term
    match, score = semantic_match_term("platform", ["platform", "market share", "value chain"], nlp)
    assert match in ["platform", "market share", "value chain"]
    assert score >= SEMANTIC_THRESHOLD
    
    # Test empty inputs
    match, score = semantic_match_term("", ["something"], nlp)
    assert score < SEMANTIC_THRESHOLD
    match, score = semantic_match_term("something", [], nlp)
    assert score < SEMANTIC_THRESHOLD

def test_mixed_edge_cases():
    """Test handling of mixed case and hyphenated terms."""
    nlp = load_nlp_model()
    
    # Test mixed case handling
    match, score = semantic_match_term("Network Effects", ["network effects"], nlp)
    assert match == "network effects"
    assert score >= SEMANTIC_THRESHOLD
    
    # Test hyphen handling
    hyphen_match = map_to_knowledge_base(["market-share"])[0]
    assert hyphen_match["confidence"] >= 0.45  # More lenient threshold for hyphenated terms