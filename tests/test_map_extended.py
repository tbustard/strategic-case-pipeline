"""Extended tests for concept mapping functionality."""

import pytest
from pathlib import Path
from case_context.map import map_concepts, ConceptMatch


@pytest.fixture
def sample_case_text():
    """Return sample case text for testing."""
    return """
    The company's competitive advantage stems from its unique resources and capabilities.
    Their strong brand and customer relationships create barriers to entry.
    The network effects in their platform business model drive increasing returns to scale.
    """


@pytest.fixture
def sample_question_text():
    """Return sample question text for testing."""
    return """
    How does the company's resource-based view explain their competitive advantage?
    What role do transaction costs play in their business model?
    """


@pytest.fixture
def sample_user_inputs():
    """Return sample user inputs for testing."""
    return """
    Consider the impact of digital transformation.
    Analyze the role of platform economics.
    """


def test_map_concepts_full_flow(
    sample_case_text, sample_question_text, sample_user_inputs
):
    """Test the complete mapping flow with all inputs."""
    matches = map_concepts(
        facts={
            "case_text": sample_case_text,
            "question_text": sample_question_text,
            "user_inputs_text": sample_user_inputs,
        }
    )

    # Check that matches are returned
    assert len(matches) > 0

    # Check that matches have expected structure
    for match in matches:
        assert isinstance(match, ConceptMatch)
        assert match.concept
        assert match.score
        assert match.source in ["case", "question", "user_inputs"]


def test_map_concepts_partial_inputs(sample_case_text):
    """Test mapping with only case text provided."""
    matches = map_concepts(facts={"case_text": sample_case_text})

    # Should still return matches
    assert len(matches) > 0

    # All matches should be from case
    assert all(m.source == "case" for m in matches)


def test_map_concepts_no_inputs():
    """Test mapping with no inputs provided."""
    matches = map_concepts(facts={})

    # Should return empty list
    assert len(matches) == 0


def test_concept_match_ordering():
    """Test that matches are ordered by score."""
    matches = [
        ConceptMatch("A", 50.0, "Def1", "case"),
        ConceptMatch("B", 90.0, "Def2", "case"),
        ConceptMatch("C", 70.0, "Def3", "case"),
    ]

    # Sort matches
    sorted_matches = sorted(matches, key=lambda x: x.score, reverse=True)

    # Check order
    assert sorted_matches[0].concept == "B"
    assert sorted_matches[1].concept == "C"
    assert sorted_matches[2].concept == "A"
