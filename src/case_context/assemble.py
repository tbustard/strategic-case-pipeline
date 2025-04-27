"""Assemble answer from matched concepts and templates."""

from typing import List, Optional, Dict, Union
from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path
import json

from case_context.map import map_concepts, ConceptMatch
from case_context.extract import process_case_text
from case_context.template_loader import load_answer_template, load_theory_template
from case_context.config import TEMPLATES_DIR


def build_concept_sentences(mapped_concepts: Dict[str, List[Dict[str, str]]]) -> str:
    """Build sentences describing matched concepts.

    Args:
        mapped_concepts: Dictionary mapping concept categories to lists of concept dicts

    Returns:
        String containing formatted sentences about matched concepts
    """
    if not mapped_concepts:
        return "No strategic concepts were detected."
        
    sentences = []
    
    for category, concepts in mapped_concepts.items():
        if not concepts:
            continue
            
        # Format each concept with its theory if present
        formatted_concepts = []
        for concept in concepts:
            if concept.get("theory"):
                formatted_concepts.append(f"{concept['concept']} ({concept['theory']})")
            else:
                formatted_concepts.append(concept['concept'])
                
        # Convert category from UPPER_CASE to Title Case and then lowercase
        category_name = category.replace("_", " ").title().lower()
        
        # Build sentence
        sentence = f"In this case, the {category_name} include: {', '.join(formatted_concepts)}."
        sentences.append(sentence)
        
    return " ".join(sentences) if sentences else "No strategic concepts were detected."


def assemble_answer(
    templates: Optional[Dict[str, Dict[str, str]]] = None,
    mapped_concepts: Optional[Dict[str, List[Dict[str, Optional[str]]]]] = None,
    case_text: Optional[str] = None,
    question_text: Optional[str] = None,
    instructions_text: Optional[str] = None,
    user_inputs_text: Optional[str] = None,
    style_instructions: Optional[str] = None,
    only_question: bool = False,
    top_n: Optional[int] = None,
) -> str:
    """Assemble an answer from matched concepts and templates.

    Args:
        templates: Optional dictionary of theory templates
        mapped_concepts: Optional dictionary of mapped concepts by category
        case_text: Optional case text to analyze
        question_text: Optional question text to analyze  
        instructions_text: Optional instructions text
        user_inputs_text: Optional user inputs text
        style_instructions: Optional style instructions
        only_question: Whether to only use matches from question text
        top_n: Optional limit on number of matches to include

    Returns:
        Assembled answer text
    """
    # If templates and mapped_concepts provided, build answer from templates
    if templates and mapped_concepts:
        sections = []
        
        # Add style instructions if provided
        if style_instructions:
            sections.append(f"REVISED[{style_instructions}]:")

        # Add strategic concepts section
        sections.append("## Strategic Concepts\n")
        
        # Process each theory template
        for theory, template in templates.items():
            if "intro" in template:
                sections.append(template["intro"])
            if "analysis" in template:
                sections.append(template["analysis"])
                
        # Add case-specific evidence section
        sections.append("\n## Case-Specific Evidence\n")
        for category, concepts in mapped_concepts.items():
            concept_list = [c["concept"] for c in concepts]
            if concept_list:
                sections.append(", ".join(concept_list))
                
        # Add additional context section
        sections.append("\n## Additional Context\n")
        
        return "\n".join(sections)

    # Otherwise extract facts and map concepts
    facts = {
        "case_text": case_text or "",
        "question_text": question_text or "",
        "instructions_text": instructions_text or "",
        "user_inputs_text": user_inputs_text or "",
    }

    matches = map_concepts(facts=facts)
    
    if only_question:
        matches = [m for m in matches if m.source == "question"]
    if top_n:
        matches = matches[:top_n]

    # Load answer template
    template = load_answer_template()
    
    # Prepare context for template
    context = {
        "matches": matches,
        "style": style_instructions or "",
        "case_text": case_text or "",
        "question_text": question_text or "",
    }
    
    # Render template
    answer = template.render(**context)
    
    return answer


def revise_answer(answer: str, style_instructions: str) -> str:
    """Revise answer according to style instructions.

    Args:
        answer: Initial answer text
        style_instructions: Style guidelines to follow

    Returns:
        Revised answer text
    """
    if not style_instructions:
        return answer
        
    return f"REVISED[{style_instructions}]:\n{answer}"


def load_template():
    """Load the answer template.

    Returns:
        Loaded Jinja2 template
    """
    return load_answer_template()


def select_templates(theories: List[str]) -> Dict[str, str]:
    """Load and return templates for the given theories.

    Args:
        theories: List of theory names to load templates for (e.g., ["TCE", "RBV"])

    Returns:
        Dict mapping theory names to their template content
    """
    templates = {}
    
    for theory in theories:
        intro = load_theory_template(theory, "intro")
        analysis = load_theory_template(theory, "analysis") 
        conclusion = load_theory_template(theory, "conclusion")
        
        if all([intro, analysis, conclusion]):
            templates[theory] = {
                "intro": intro.strip(),
                "analysis": analysis.strip(),
                "conclusion": conclusion.strip()
            }
        else:
            # If any section is missing, use default content
            default_content = {
                "RBV": {
                    "intro": "The Resource-Based View (RBV) of the firm focuses on internal resources and capabilities as the primary source of competitive advantage.",
                    "analysis": "{{CONCEPT_SENTENCES}}\n\nThese resources and capabilities contribute to the firm's competitive position.",
                    "conclusion": "The RBV framework helps explain how the firm's unique resource bundle creates sustainable competitive advantage."
                },
                "TCE": {
                    "intro": "Transaction Cost Economics (TCE) examines how firms choose to organize their economic activities.",
                    "analysis": "{{CONCEPT_SENTENCES}}\n\nThese factors influence the firm's make-or-buy decisions and governance structures.",
                    "conclusion": "TCE provides insights into the optimal boundaries of the firm and its relationships with other market participants."
                },
                "Platform": {
                    "intro": "Platform theory examines how firms create and capture value through digital platforms and ecosystems.",
                    "analysis": "{{CONCEPT_SENTENCES}}\n\nThese platform dynamics shape the firm's competitive strategy and market position.",
                    "conclusion": "Platform strategy helps explain how firms leverage network effects and ecosystem complementarities."
                }
            }
            if theory in default_content:
                templates[theory] = default_content[theory]

    return templates


def generate_answer(*args, **kwargs) -> str:
    """Legacy wrapper for assemble_answer."""
    return assemble_answer(*args, **kwargs)


__all__ = [
    "assemble_answer",
    "generate_answer",
    "build_concept_sentences",
    "revise_answer",
]
