"""Tests for the extract module."""

import pytest
from case_context.extract import extract_business_facts, process_case_text

def test_extract_business_facts():
    """Test basic fact extraction."""
    text = "Apple Inc. competes in the smartphone market with innovative products."
    facts = extract_business_facts(text)
    
    assert "Apple Inc." in facts["named_entities"]
    assert "the smartphone market" in facts["noun_chunks"]
    assert "competes" in facts["business_verbs"]
    assert "innovative products" in facts["noun_chunks"]

def test_process_case_text():
    """Test case and question processing."""
    case_text = "Tesla Motors is disrupting the automotive industry."
    question_text = "How does Tesla's strategy create competitive advantage?"
    
    case_facts, question_facts = process_case_text(case_text, question_text)
    
    assert "Tesla Motors" in case_facts["named_entities"]
    assert "competitive advantage" in question_facts["noun_chunks"] 