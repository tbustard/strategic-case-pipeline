#!/usr/bin/env python3
"""Command-line interface for case analysis."""

import sys
import click
from pathlib import Path
from typing import Optional
from case_context.assemble import assemble_answer


def validate_inputs(
    case_file: Optional[str],
    question_file: Optional[str],
    case_text: Optional[str],
    question_text: Optional[str],
) -> None:
    """Validate input combinations and file existence.

    Args:
        case_file: Path to case file
        question_file: Path to question file
        case_text: Direct case text
        question_text: Direct question text

    Raises:
        click.UsageError: If input combination is invalid
    """
    # Check for mixed input modes
    if case_file and case_text:
        raise click.UsageError(
            "Please provide either a case file path or direct text input, but not both."
        )
    if question_file and question_text:
        raise click.UsageError(
            "Please provide either a question file path or direct text input, but not both."
        )

    # Check that we have at least one input mode for each
    if not (case_file or case_text):
        raise click.UsageError(
            "Please provide either a case file path or direct case text."
        )
    if not (question_file or question_text):
        raise click.UsageError(
            "Please provide either a question file path or direct question text."
        )

    # Check file existence
    if case_file and not Path(case_file).exists():
        raise click.UsageError(
            f"File not found: {case_file}\n"
            "Please provide a valid path to your case file "
            "(e.g. Data/Case.docx or cases/Case1.txt)."
        )
    if question_file and not Path(question_file).exists():
        raise click.UsageError(
            f"File not found: {question_file}\n"
            "Please provide a valid path to your question file "
            "(e.g. Data/Question_1.txt)."
        )


@click.command(
    help="""
Analyze a business case and generate a structured answer.

Two modes of operation:
1. File-based input:   Provide paths to case and question files
2. Direct text input:  Paste case and question text directly using --case-text/--question-text

Example (file-based):
    python -m case_context.app Data/Case.docx Data/Question_1.txt

Example (direct input):
    python -m case_context.app --case-text "..." --question-text "..."
"""
)
@click.argument("case_file", type=str, required=False)
@click.argument("question_file", type=str, required=False)
@click.option(
    "--case-text", help="Paste the case text directly instead of supplying a file"
)
@click.option(
    "--question-text",
    help="Paste the question text directly instead of supplying a file",
)
@click.option(
    "--instructions",
    help="Professor's guiding instructions for format and content",
    required=False,
    default=None,
)
@click.option(
    "--user-inputs",
    help="Any extra context or parameters",
    required=False,
    default=None,
)
@click.option(
    "--style-instructions",
    help="Tone/style adjustments (e.g., 'student-like, less robotic')",
    required=False,
    default=None,
)
def main(
    case_file: Optional[str],
    question_file: Optional[str],
    case_text: Optional[str],
    question_text: Optional[str],
    instructions: Optional[str],
    user_inputs: Optional[str],
    style_instructions: Optional[str],
) -> None:
    """Analyze a case and answer a question about it."""
    # Validate inputs
    validate_inputs(case_file, question_file, case_text, question_text)

    # Prompt for missing inputs
    if instructions is None:
        instructions = click.prompt("Answer instructions")
    if user_inputs is None:
        user_inputs = click.prompt("Additional user inputs")
    if style_instructions is None:
        style_instructions = click.prompt("Rewrite instructions")

    # Get input texts
    if case_text:
        case_content = case_text
    else:
        case_content = Path(case_file).read_text()

    if question_text:
        question_content = question_text
    else:
        question_content = Path(question_file).read_text()

    # Get assembled answer
    answer = assemble_answer(
        case_text=case_content,
        question_text=question_content,
        instructions_text=instructions,
        user_inputs_text=user_inputs,
        style_instructions=style_instructions,
    )

    # Print results
    click.echo("\nAnalysis Results:")
    click.echo("----------------")
    click.echo(answer)


if __name__ == "__main__":
    main()
