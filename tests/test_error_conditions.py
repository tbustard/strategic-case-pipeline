"""Tests for semantic matching and mapping functionality."""

import pytest
from case_context.map import semantic_match_term
from case_context.extract import load_nlp_model

def test_semantic_match_term():
    term = "network effect"
    nlp = load_nlp_model()
    match, score = semantic_match_term(term, ["network effects", "value chain"], nlp)
    assert match in ["network effects", "value chain"]
    assert score > 0.7

def test_semantic_match_term_no_match():
    term = "completelyUnknownTerm"
    nlp = load_nlp_model()
    match, score = semantic_match_term(term, ["network effects", "value chain"], nlp)
    assert score < 0.5  # Low confidence score for unrelated terms