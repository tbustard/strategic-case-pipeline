"""End-to-end tests for the assemble module using real template files."""

import pytest
from pathlib import Path
from case_context.assemble import build_concept_sentences, select_templates, generate_answer

def test_end_to_end_assemble():
    """Test the complete assembly pipeline using real template files."""
    # Define test concepts
    mapped_concepts = {
        "Business_Concept": [
            {"concept": "network effects", "theory": None}
        ],
        "Strategic_Theory": [
            {"concept": "transaction cost", "theory": "TCE"}
        ]
    }
    
    # Load real templates
    templates = select_templates(["RBV"])
    
    # Generate answer with normal word limit
    answer = generate_answer(templates, mapped_concepts)
    
    # Verify answer structure
    assert answer.startswith("The Resource-Based View (RBV) of the firm focuses on")
    assert "Analysis:" in answer
    assert "In conclusion" in answer
    assert "{{CONCEPT_SENTENCES}}" not in answer
    assert "network effects" in answer
    assert "transaction cost (TCE)" in answer
    
    # Test word limit truncation
    short_answer = generate_answer(templates, mapped_concepts, word_limit=10)
    words = short_answer.split()
    assert len(words) <= 10
    assert short_answer.endswith("...")

def test_end_to_end_assemble_tce():
    """Test assembly pipeline with TCE theory."""
    mapped_concepts = {
        "Strategic_Theory": [{"concept": "transaction cost", "theory": "TCE"}]
    }
    templates = select_templates(["TCE"])
    answer = generate_answer(templates, mapped_concepts)
    
    # Verify TCE-specific content and structure
    assert answer.startswith("Transaction Cost Economics (TCE)")
    assert "Analysis:" in answer
    assert "In conclusion" in answer
    assert "{{CONCEPT_SENTENCES}}" not in answer
    assert "transaction cost (TCE)" in answer
    assert answer.endswith("...") is False  # full output

def test_end_to_end_assemble_platform():
    """Test assembly pipeline with Platform theory."""
    mapped_concepts = {
        "Business_Concept": [{"concept": "network effects", "theory": None}]
    }
    templates = select_templates(["Platform"])
    answer = generate_answer(templates, mapped_concepts)
    
    # Verify Platform-specific content and structure
    assert answer.startswith("Platform theory examines")
    assert "Analysis:" in answer
    assert "In conclusion" in answer
    assert "{{CONCEPT_SENTENCES}}" not in answer
    assert "network effects" in answer
    assert answer.endswith("...") is False

def test_end_to_end_assemble_multiple_theories():
    """Test assembly pipeline with multiple theories."""
    mapped_concepts = {
        "Strategic_Theory": [{"concept": "transaction cost", "theory": "TCE"}],
        "Business_Concept": [{"concept": "network effects", "theory": None}]
    }
    templates = select_templates(["TCE", "Platform"])
    answer = generate_answer(templates, mapped_concepts)
    
    # Verify both theories are present
    assert "Transaction Cost Economics (TCE)" in answer
    assert "Platform theory examines" in answer
    
    # Verify concept sentences
    assert "{{CONCEPT_SENTENCES}}" not in answer
    assert "transaction cost (TCE)" in answer
    assert "network effects" in answer
    
    # Verify section structure
    assert "Analysis:" in answer
    assert "In conclusion, TCE" in answer
    assert "In conclusion, platform theory" in answer
    
    # Verify section order
    tce_intro_pos = answer.find("Transaction Cost Economics (TCE)")
    platform_intro_pos = answer.find("Platform theory examines")
    tce_conclusion_pos = answer.find("In conclusion, TCE")
    platform_conclusion_pos = answer.find("In conclusion, platform theory")
    
    assert tce_intro_pos < platform_intro_pos
    assert platform_intro_pos < tce_conclusion_pos
    assert tce_conclusion_pos < platform_conclusion_pos

def test_end_to_end_empty_theory():
    """Test assembly pipeline with an empty theory folder."""
    mapped_concepts = {
        "Business_Concept": [{"concept": "test concept", "theory": None}]
    }
    templates = select_templates(["EmptyTheory"])
    answer = generate_answer(templates, mapped_concepts)
    
    # Verify empty or concept-only output
    assert answer == "" or "test concept" in answer
    assert "{{CONCEPT_SENTENCES}}" not in answer

def test_end_to_end_multiple_three_theories():
    """Test assembly pipeline with three theories."""
    mapped_concepts = {
        "Strategic_Theory": [{"concept": "transaction cost", "theory": "TCE"}],
        "Business_Concept": [{"concept": "network effects", "theory": None}],
        "Industry_Context": [{"concept": "market share", "theory": None}]
    }
    templates = select_templates(["TCE", "RBV", "Platform"])
    answer = generate_answer(templates, mapped_concepts)
    
    # Check all three intros in order
    intros = [
        "Transaction Cost Economics (TCE)",
        "The Resource-Based View",
        "Platform theory examines"
    ]
    idxs = [answer.index(i) for i in intros]
    assert idxs == sorted(idxs)
    
    # Ensure concept sentences include all three concepts
    for c in ["transaction cost (TCE)", "network effects", "market share"]:
        assert c in answer
    
    # Ensure three conclusions appear
    for concl in ["In conclusion, TCE", "In conclusion, RBV", "In conclusion, platform"]:
        assert concl in answer 