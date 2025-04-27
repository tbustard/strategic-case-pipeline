"""End-to-end tests for the assemble module using real template files."""

import pytest
from pathlib import Path
from case_context.assemble import (
    build_concept_sentences,
    select_templates,
    assemble_answer,
)


def test_end_to_end_assemble():
    """Test the complete assembly pipeline using real template files."""
    # Define test concepts
    mapped_concepts = {
        "Business_Concept": [{"concept": "network effects", "theory": None}],
        "Strategic_Theory": [{"concept": "transaction cost", "theory": "TCE"}],
    }

    # Load real templates
    templates = select_templates(["RBV"])

    # Generate answer with normal word limit
    answer = assemble_answer(templates, mapped_concepts)

    # Verify answer structure
    assert "The Resource-Based View (RBV)" in answer
    assert "network effects" in answer.lower()
    assert "transaction cost" in answer.lower()


def test_end_to_end_assemble_tce():
    """Test assembly pipeline with TCE theory."""
    mapped_concepts = {
        "Strategic_Theory": [{"concept": "transaction cost", "theory": "TCE"}]
    }
    templates = select_templates(["TCE"])
    answer = assemble_answer(templates, mapped_concepts)

    # Verify TCE-specific content and structure
    assert "Transaction Cost Economics (TCE)" in answer
    assert "transaction cost" in answer.lower()


def test_end_to_end_assemble_platform():
    """Test assembly pipeline with Platform theory."""
    mapped_concepts = {
        "Business_Concept": [{"concept": "network effects", "theory": None}]
    }
    templates = select_templates(["Platform"])
    answer = assemble_answer(templates, mapped_concepts)

    # Verify Platform-specific content and structure
    assert "Platform theory" in answer
    assert "network effects" in answer.lower()


def test_end_to_end_assemble_multiple_theories():
    """Test assembly pipeline with multiple theories."""
    mapped_concepts = {
        "Strategic_Theory": [{"concept": "transaction cost", "theory": "TCE"}],
        "Business_Concept": [{"concept": "network effects", "theory": None}],
    }
    templates = select_templates(["TCE", "Platform"])
    answer = assemble_answer(templates, mapped_concepts)

    # Verify both theories are present
    assert "Transaction Cost Economics (TCE)" in answer
    assert "Platform theory" in answer
    assert "network effects" in answer.lower()
    assert "transaction cost" in answer.lower()


def test_end_to_end_empty_theory():
    """Test assembly pipeline with an empty theory folder."""
    mapped_concepts = {
        "Business_Concept": [{"concept": "test concept", "theory": None}]
    }
    templates = select_templates(["EmptyTheory"])
    answer = assemble_answer(templates, mapped_concepts)

    # Verify empty or concept-only output
    assert answer == "" or "test concept" in answer
    assert "{{CONCEPT_SENTENCES}}" not in answer


def test_end_to_end_multiple_three_theories():
    """Test assembly pipeline with three theories."""
    mapped_concepts = {
        "Strategic_Theory": [{"concept": "transaction cost", "theory": "TCE"}],
        "Business_Concept": [{"concept": "network effects", "theory": None}],
        "Industry_Context": [{"concept": "market share", "theory": None}],
    }
    templates = select_templates(["TCE", "RBV", "Platform"])
    answer = assemble_answer(templates, mapped_concepts)

    # Check all three intros in order
    intros = [
        "Transaction Cost Economics (TCE)",
        "The Resource-Based View",
        "Platform theory",
    ]
    idxs = [answer.index(i) for i in intros]
    assert all(i < j for i, j in zip(idxs, idxs[1:]))  # Verify order

    # Ensure concept sentences include all three concepts
    for c in ["transaction cost (TCE)", "network effects", "market share"]:
        assert c in answer

    # Ensure three conclusions appear
    for concl in [
        "In conclusion, TCE",
        "In conclusion, RBV",
        "In conclusion, platform",
    ]:
        assert concl in answer
