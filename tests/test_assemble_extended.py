"""Extended tests for answer assembly functionality."""

import pytest
from spacy.language import Language
from unittest.mock import patch

from case_context.map import ConceptMatch
from case_context.assemble import assemble_answer
from case_context.extract import ExtractedFacts


@pytest.fixture
def mock_concept_matches():
    """Return a list of mock concept matches for testing."""
    return [
        ConceptMatch(
            concept="Network Effects",
            score=90.0,
            definition="The phenomenon where a product or service becomes more valuable as more people use it",
            matched_text="network effects",
            source="case"
        ),
        ConceptMatch(
            concept="First Mover Advantage",
            score=85.0,
            definition="The competitive edge gained by entering a market or developing a technology before rivals",
            matched_text="first mover",
            source="case"
        ),
        ConceptMatch(
            concept="Asset Specificity",
            score=80.0,
            definition="The degree to which investments are specific to a particular transaction",
            matched_text="specific assets",
            source="case"
        ),
    ]


def test_happy_path(mock_concept_matches):
    """Test assemble_answer with all inputs provided."""
    case_text = "The company leverages network effects in their platform."
    question_text = "What strategic concepts are relevant to this case?"
    instructions_text = "Please analyze the case and identify key strategic concepts."
    style_instructions = "Use clear, concise language."

    result = assemble_answer(
        case_text=case_text,
        question_text=question_text,
        instructions_text=instructions_text,
        style_instructions=style_instructions,
    )

    assert isinstance(result, str)
    assert len(result) > 0
    assert "Strategic Concepts" in result  # Section header
    assert "Network Effects" in result
    assert "First Mover Advantage" in result
    assert "Case-Specific Evidence" in result  # Section header


def test_only_question_matches(mock_concept_matches):
    """Test filtering matches when only_question=True."""
    case_text = "The company leverages network effects in their platform."
    question_text = "What strategic concepts are relevant to this case?"

    result = assemble_answer(
        case_text=case_text,
        question_text=question_text,
        only_question=True
    )

    assert isinstance(result, str)
    assert len(result) > 0
    assert "Strategic Concepts" in result
    assert "No strategic concepts" in result  # Should show no matches message
    assert "Case-Specific Evidence" in result


def test_top_n_parameter(mock_concept_matches):
    """Test limiting number of matches with top_n parameter."""
    case_text = "The company leverages network effects in their platform."
    question_text = "What strategic concepts are relevant to this case?"

    result = assemble_answer(
        case_text=case_text,
        question_text=question_text,
        top_n=1
    )

    assert isinstance(result, str)
    assert len(result) > 0
    assert "Strategic Concepts" in result
    assert result.count("Network Effects") == 1  # Only highest scoring match
    assert "First Mover Advantage" not in result
    assert "Case-Specific Evidence" in result


def test_no_matches_fallback():
    """Test behavior when no matches are found."""
    case_text = "The weather was nice today."
    question_text = "How was the weather?"

    result = assemble_answer(
        case_text=case_text,
        question_text=question_text
    )

    assert isinstance(result, str)
    assert len(result) > 0
    assert "Strategic Concepts" in result
    assert "No strategic concepts were identified" in result
    assert "Case-Specific Evidence" in result
    assert case_text in result
    assert question_text in result
 