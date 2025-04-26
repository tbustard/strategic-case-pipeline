"""Template selection and answer generation module."""

import logging
from pathlib import Path
from typing import Dict, List, Optional
from jinja2 import Environment, FileSystemLoader
from case_context.config import TEMPLATES_DIR, MAX_OUTPUT_WORDS
from case_context.extract import process_case_text, extract_business_facts
from case_context.map import map_concepts, ConceptMatch

# Set up template environment
TEMPLATE_DIR = Path(__file__).parent / "templates"
env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))

logger = logging.getLogger(__name__)

def build_concept_sentences(mapped_concepts: Dict[str, List[Dict]]) -> str:
    """
    Turn mapped_concepts into human-readable sentences.

    Args:
        mapped_concepts: Dictionary of concepts by category

    Returns:
        Formatted string of concept sentences
    """
    sentences = []
    for category, concepts in mapped_concepts.items():
        names = [
            c["concept"] + (f" ({c['theory']})" if c.get("theory") else "")
            for c in concepts
        ]
        if names:
            # Normalize category name and append "concepts" only if not already present
            cat_name = category.replace("_", " ").lower()
            if not cat_name.endswith("concepts"):
                cat_name += " concepts"
            sentences.append(
                f"In this case, the {cat_name} include: "
                + ", ".join(names)
                + "."
            )
    return " ".join(sentences)

def load_template(theory: str, section: str) -> Optional[str]:
    """
    Load a template for a specific theory and section.
    
    Args:
        theory: Name of the strategic theory
        section: Section type (intro, analysis, conclusion)
        
    Returns:
        Template text if found, None otherwise
    """
    template_path = TEMPLATES_DIR / theory / f"{section}.txt"
    try:
        return template_path.read_text()
    except FileNotFoundError:
        logger.warning(f"Template not found: {template_path}")
        return None

def select_templates(theories: List[str]) -> Dict[str, Dict[str, str]]:
    """
    Select appropriate templates for each theory.
    
    Args:
        theories: List of relevant strategic theories
        
    Returns:
        Dictionary of templates by theory and section
    """
    templates = {}
    for theory in theories:
        theory_templates = {}
        for section in ["intro", "analysis", "conclusion"]:
            template = load_template(theory, section)
            if template:
                theory_templates[section] = template
        if theory_templates:
            templates[theory] = theory_templates
    return templates

def generate_answer(
    templates: Dict[str, Dict[str, str]],
    mapped_concepts: Dict[str, List[Dict]],
    word_limit: int = MAX_OUTPUT_WORDS
) -> str:
    """
    Generate the final answer by combining templates and case-specific content.
    
    Args:
        templates: Selected templates by theory and section
        mapped_concepts: Mapped concepts by category
        word_limit: Maximum word count for the answer
        
    Returns:
        Generated answer text
    """
    answer_parts = []

    # Build concept sentences
    concept_sentences = build_concept_sentences(mapped_concepts)

    # Generate introduction
    for theory, theory_templates in templates.items():
        intro = theory_templates.get("intro")
        if intro:
            answer_parts.append(intro)

    # Generate analysis
    for theory, theory_templates in templates.items():
        analysis = theory_templates.get("analysis")
        if analysis:
            # Insert concept sentences into analysis
            filled = analysis.replace("{{CONCEPT_SENTENCES}}", concept_sentences)
            answer_parts.append(filled)

    # Generate conclusion
    for theory, theory_templates in templates.items():
        conclusion = theory_templates.get("conclusion")
        if conclusion:
            answer_parts.append(conclusion)

    # Combine parts and enforce word limit
    answer = " ".join(answer_parts)
    words = answer.split()
    if len(words) > word_limit:
        answer = " ".join(words[:word_limit]) + "..."

    return answer

def assemble_answer(case_text: str, question_text: str) -> str:
    """Assemble an answer by extracting and mapping concepts from case text.
    
    Args:
        case_text: The main case study text
        question_text: The question to be answered
        
    Returns:
        A structured string containing detected concepts and their definitions
    """
    # 1. Extract facts
    case_facts, question_facts = process_case_text(case_text, question_text)
    
    # 2. Map to concepts
    case_matches = map_concepts(case_facts)
    question_matches = map_concepts(question_facts)
    
    # 3. Combine and sort matches (question matches first)
    all_matches = question_matches + [m for m in case_matches if m not in question_matches]
    
    # 4. Load and render template
    template = env.get_template("answer.j2")
    
    return template.render(matches=all_matches[:5])  # Show top 5 matches