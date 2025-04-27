"""Tests for pipeline components."""

import pytest
from pathlib import Path
from case_context.extract import load_nlp_model
from case_context.map import map_concepts
from case_context.assemble import assemble_answer


def test_load_nlp_model():
    """Test that the spaCy model loads correctly."""
    nlp = load_nlp_model()
    assert nlp is not None
    assert "ner" in nlp.pipe_names


def test_map_concepts_basic():
    """Test basic concept mapping functionality."""
    case_text = "The company leverages network effects in their platform."
    matches = map_concepts(facts={"case_text": case_text})
    assert len(matches) > 0
    assert any(m.concept == "Network Effects" for m in matches)


def test_assemble_answer_basic():
    """Test basic answer assembly."""
    case = "Company X uses network effects."
    question = "How do they create value?"
    answer = assemble_answer(
        case_text=case,
        question_text=question,
        instructions_text="Analyze the platform strategy.",
        user_inputs_text="Consider network effects.",
        style_instructions="Be analytical.",
    )
    assert len(answer) > 0
    assert isinstance(answer, str)
