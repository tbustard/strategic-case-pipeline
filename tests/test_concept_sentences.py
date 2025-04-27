"""Tests for concept sentence building and formatting."""

import pytest
from case_context.assemble import build_concept_sentences


def test_concept_sentence_formatting():
    """Test concept sentence formatting with special characters and theory tags."""
    mapped_concepts = {
        "CategoryA": [
            {"concept": "ÜberAnalyse", "theory": "TCE"},
            {"concept": "StandardWidget", "theory": None},
        ]
    }

    expected = "In this case, the categorya concepts include: ÜberAnalyse (TCE), StandardWidget."
    result = build_concept_sentences(mapped_concepts)

    assert result == expected

    # Verify Unicode is preserved
    assert "Über" in result

    # Verify theory parentheses formatting
    assert "(TCE)" in result
    assert "StandardWidget)" not in result  # No parentheses for None theory

    # Verify category name handling
    assert "categorya concepts" in result.lower()
