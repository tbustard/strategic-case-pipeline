"""Tests for the assemble module."""

import pytest
from pathlib import Path
from case_context.assemble import (
    build_concept_sentences,
    assemble_answer,
    load_template,
)
from case_context.map import ConceptMatch


def test_build_concept_sentences():
    """Test building concept sentences from mapped concepts."""
    mapped_concepts = {
        "STRATEGIC_CONCEPTS": [
            {"concept": "Porter's Five Forces", "theory": "Porter"},
            {"concept": "Value Chain", "theory": "Porter"},
        ],
        "ORGANIZATIONAL_CONCEPTS": [
            {"concept": "Organizational Culture", "theory": None}
        ],
    }

    expected = (
        "In this case, the strategic concepts include: Porter's Five Forces (Porter), Value Chain (Porter). "
        "In this case, the organizational concepts include: Organizational Culture."
    )

    assert build_concept_sentences(mapped_concepts) == expected


def test_assemble_answer():
    """Test assembling answer from templates and concepts."""
    case_text = "The company uses Porter's Five Forces to analyze competition."
    question_text = "How does the company analyze its industry?"
    instructions_text = "Focus on strategic frameworks."
    user_inputs_text = "Consider competitive forces."
    style_instructions = "Write analytically."

    answer = assemble_answer(
        case_text=case_text,
        question_text=question_text,
        instructions_text=instructions_text,
        user_inputs_text=user_inputs_text,
        style_instructions=style_instructions,
    )

    # Check that concept sentences were inserted
    assert "Five Forces" in answer

    # Check that all sections are present
    assert "Strategic Concepts" in answer
    assert "Case-Specific Evidence" in answer

    # Check word limit enforcement
    short_answer = assemble_answer(
        case_text=case_text,
        question_text=question_text,
        instructions_text=instructions_text,
        user_inputs_text=user_inputs_text,
        style_instructions=style_instructions,
        top_n=1,  # Limit number of matches
    )
    assert len(short_answer.split()) < len(answer.split())


def test_assemble_simple_case():
    """Test that assemble_answer detects and returns known concepts."""
    # Sample case and question text
    case_text = (
        "Apple Inc. leverages its strong brand and ecosystem to create network effects."
    )
    question_text = "How does Apple create competitive advantage?"
    instructions_text = "Focus on platform strategy and network effects."
    user_inputs_text = "Consider ecosystem lock-in effects."
    style_instructions = "Write like an MBA student."

    # Get assembled answer
    answer = assemble_answer(
        case_text=case_text,
        question_text=question_text,
        instructions_text=instructions_text,
        user_inputs_text=user_inputs_text,
        style_instructions=style_instructions,
    )

    # Check that answer is non-empty and contains expected phrases
    assert len(answer) > 0
    assert isinstance(answer, str)
    assert "competitive advantage" in answer.lower()
    assert "network effects" in answer.lower()  # This is more relevant to the case text
    assert "platform" in answer.lower()  # This is mentioned in the instructions


def test_assemble_no_matches():
    """Test handling when no concepts are matched."""
    answer = assemble_answer(
        case_text="This is a simple text with no strategic concepts.",
        question_text="What is happening?",
        instructions_text="Analyze the situation.",
        user_inputs_text="Look for patterns.",
        style_instructions="Be concise.",
    )
    assert isinstance(answer, str)
    assert len(answer) > 0


def test_assemble_with_empty_inputs():
    """Test handling of empty input strings."""
    answer = assemble_answer(
        case_text="",
        question_text="",
        instructions_text="",
        user_inputs_text="",
        style_instructions="",
    )
    assert isinstance(answer, str)
    assert len(answer) > 0  # Should still return some default response
