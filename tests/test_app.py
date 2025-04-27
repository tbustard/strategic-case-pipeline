"""Tests for the CLI interface."""

import pytest
from click.testing import CliRunner
from case_context.app import main


def run_cli_with(
    case: str,
    question: str,
    instructions: str,
    user_inputs: str,
    style_instructions: str,
) -> str:
    """Run the CLI with the given inputs.

    Args:
        case: Case text
        question: Question text
        instructions: Instructions text
        user_inputs: User inputs text
        style_instructions: Style instructions

    Returns:
        CLI output
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create input files
        with open("case.txt", "w") as f:
            f.write(case)
        with open("question.txt", "w") as f:
            f.write(question)
        with open("instructions.txt", "w") as f:
            f.write(instructions)
        with open("inputs.txt", "w") as f:
            f.write(user_inputs)

        # Run CLI
        result = runner.invoke(
            main,
            [
                "case.txt",
                "question.txt",
                "--instructions",
                "instructions.txt",
                "--user-inputs",
                "inputs.txt",
                "--style-instructions",
                style_instructions,
            ],
        )
        return result.output


def test_style_revision(monkeypatch):
    """Test that style instructions are applied to the output."""
    # Mock the revise_answer function to return a known string
    monkeypatch.setattr(
        "case_context.assemble.revise_answer",
        lambda initial, instr: f"REVISED[{instr}]: {initial}",
    )

    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create test files
        with open("case.txt", "w") as f:
            f.write("Test case text")
        with open("question.txt", "w") as f:
            f.write("Test question text")

        # Run the CLI with all inputs
        result = runner.invoke(
            main,
            [
                "case.txt",
                "question.txt",
                "--instructions",
                "Test instructions",
                "--user-inputs",
                "Test inputs",
                "--style-instructions",
                "Make it student-like",
            ],
        )

        # Check that the output includes our mock revision
        assert "REVISED[Make it student-like]:" in result.output


def test_file_not_found_error():
    """Test that non-existent file paths produce friendly error messages."""
    runner = CliRunner()
    result = runner.invoke(main, ["nonexistent.txt"])

    assert result.exit_code == 2  # Click's error exit code
    assert (
        "Please provide either a question file path or direct question text"
        in result.output
    )


def test_direct_text_input(monkeypatch):
    """Test that direct text input works without file path errors."""
    # Mock the revise_answer function
    monkeypatch.setattr(
        "case_context.assemble.revise_answer",
        lambda initial, instr: f"REVISED[{instr}]: {initial}",
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--case-text",
            "Direct case text",
            "--question-text",
            "Direct question",
            "--instructions",
            "Test instructions",
            "--user-inputs",
            "Test inputs",
            "--style-instructions",
            "Make it student-like",
        ],
    )

    assert result.exit_code == 0
    assert "REVISED[Make it student-like]:" in result.output


def test_mixed_input_error():
    """Test that mixing file and direct text input raises an error."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create test file
        with open("case.txt", "w") as f:
            f.write("Test case text")

        result = runner.invoke(main, ["case.txt", "--case-text", "Direct case text"])

        assert result.exit_code == 2  # Click's error exit code
        assert (
            "Please provide either a case file path or direct text input"
            in result.output
        )
