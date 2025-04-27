"""Tests for concept mapping functionality."""

import pytest
from spacy.tokens import Doc

from case_context.extract import ExtractedFacts
from case_context.knowledge_base import Concept
from case_context.map import map_concepts, ConceptMatch


@pytest.fixture
def mock_concepts():
    """Return a list of mock concepts for testing."""
    return [
        Concept(
            name="Resource-Based View",
            definition="A framework that sees resources as key to superior firm performance",
            theory="RBV",
        ),
        Concept(
            name="Network Effects",
            definition="The phenomenon where a product or service becomes more valuable as more people use it",
            theory="PlatformStrategy",
        ),
    ]


@pytest.fixture
def mock_facts():
    """Return mock extracted facts for testing."""
    return {
        "case_text": "The company leveraged its unique resources and network effects.",
        "question_text": "How did the resource-based view apply?",
        "user_inputs_text": "Consider network effects in the analysis.",
    }


def test_map_concepts_basic(mock_facts):
    """Test basic concept mapping functionality."""
    matches = map_concepts(facts=mock_facts)
    assert len(matches) > 0
    assert any(m.concept == "Network Effects" for m in matches)


def test_map_concepts_scoring(mock_facts):
    """Test that concept matches are properly scored."""
    matches = map_concepts(facts=mock_facts)
    assert all(0 <= m.score <= 100 for m in matches)


def test_map_concepts_empty_input():
    """Test handling of empty input."""
    empty_facts = {"case_text": "", "question_text": "", "user_inputs_text": ""}
    matches = map_concepts(facts=empty_facts)
    assert len(matches) == 0


def test_map_concepts_no_matches():
    """Test handling of input with no concept matches."""
    irrelevant_facts = {
        "case_text": "The weather was nice today.",
        "question_text": "How was the weather?",
        "user_inputs_text": "It was sunny.",
    }
    matches = map_concepts(facts=irrelevant_facts)
    assert len(matches) == 0
