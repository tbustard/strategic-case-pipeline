"""Tests for the assemble module."""

import pytest
from pathlib import Path
from case_context.assemble import build_concept_sentences, generate_answer, load_template, assemble_answer

def test_build_concept_sentences():
    """Test building concept sentences from mapped concepts."""
    mapped_concepts = {
        "STRATEGIC_CONCEPTS": [
            {"concept": "Porter's Five Forces", "theory": "Porter"},
            {"concept": "Value Chain", "theory": "Porter"}
        ],
        "ORGANIZATIONAL_CONCEPTS": [
            {"concept": "Organizational Culture", "theory": None}
        ]
    }
    
    expected = (
        "In this case, the strategic concepts include: Porter's Five Forces (Porter), Value Chain (Porter). "
        "In this case, the organizational concepts include: Organizational Culture."
    )
    
    assert build_concept_sentences(mapped_concepts) == expected

def test_generate_answer():
    """Test generating answer from templates and concepts."""
    templates = {
        "Porter": {
            "intro": "This case analysis applies Porter's strategic framework.",
            "analysis": "The industry structure can be analyzed using {{CONCEPT_SENTENCES}}",
            "conclusion": "In conclusion, Porter's framework provides valuable insights."
        }
    }
    
    mapped_concepts = {
        "STRATEGIC_CONCEPTS": [
            {"concept": "Five Forces", "theory": "Porter"}
        ]
    }
    
    answer = generate_answer(templates, mapped_concepts)
    
    # Check that concept sentences were inserted
    assert "Five Forces (Porter)" in answer
    
    # Check that all sections are present
    assert "This case analysis applies" in answer
    assert "In conclusion" in answer
    
    # Check word limit enforcement
    long_answer = generate_answer(templates, mapped_concepts, word_limit=10)
    assert len(long_answer.split()) <= 10
    assert long_answer.endswith("...")

def test_assemble_simple_case():
    """Test that assemble_answer detects and returns known concepts."""
    # Sample case and question text
    case_text = "Apple Inc. leverages its strong brand and ecosystem to create network effects."
    question_text = "How does Apple create competitive advantage?"
    
    # Get assembled answer
    answer = assemble_answer(case_text, question_text)
    
    # Check that we got a non-empty string with expected format
    assert isinstance(answer, str)
    assert len(answer) > 0
    assert "The following strategic concepts are most relevant:" in answer
    
    # Check that we detected at least one known concept
    assert "Competitive Advantage" in answer
    
    # Check that the answer includes concept definitions
    assert "match" in answer.lower()
    
    # Check that question-oriented matches appear first
    assert answer.find("Competitive Advantage") < answer.find("Dynamic Capabilities") 