"""Pipeline helper for docx integration."""

from pathlib import Path
from docx import Document
from case_context.assemble import assemble_answer


def _docx_to_text(p: str) -> str:
    """Convert docx file to text.

    Args:
        p: Path to docx file

    Returns:
        Extracted text content
    """
    doc = Document(p)
    return "\n".join(par.text for par in doc.paragraphs)


def run_pipeline(
    case_path: str, question_path: str, instructions_path: str, style_path: str = ""
) -> str:
    """Run the complete pipeline from docx files to answer.

    Args:
        case_path: Path to case docx
        question_path: Path to question docx
        instructions_path: Path to instructions docx
        style_path: Optional path to style guidelines docx

    Returns:
        Generated answer text
    """
    return assemble_answer(
        case_text=_docx_to_text(case_path),
        question_text=_docx_to_text(question_path),
        instructions_text=_docx_to_text(instructions_path),
        user_inputs_text="",
        style_instructions=_docx_to_text(style_path) if style_path else "",
    )
