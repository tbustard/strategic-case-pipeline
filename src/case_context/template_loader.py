"""Template loading and management."""
from pathlib import Path
from typing import Dict, List, Optional
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

# Constants
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"

# Default template content
DEFAULT_TEMPLATES = {
    "RBV": {
        "intro": "The Resource-Based View (RBV) framework analyzes how firms can achieve sustainable competitive advantage through their unique resources and capabilities.",
        "analysis": "From an RBV perspective, the key resources and capabilities identified in this case include: {{ concepts|join(', ') }}.",
        "conclusion": "These resources and capabilities contribute to the firm's competitive position by being valuable, rare, inimitable, and non-substitutable (VRIN)."
    },
    "TCE": {
        "intro": "Transaction Cost Economics (TCE) examines how firms can minimize transaction costs through governance choices and organizational structures.",
        "analysis": "From a TCE perspective, the key transaction cost considerations include: {{ concepts|join(', ') }}.",
        "conclusion": "These transaction cost factors influence the firm's make-or-buy decisions and governance structures."
    },
    "Platform": {
        "intro": "Platform theory analyzes how firms can create value through network effects and ecosystem management.",
        "analysis": "From a platform perspective, the key platform dynamics include: {{ concepts|join(', ') }}.",
        "conclusion": "These platform elements shape how the firm creates and captures value in its ecosystem."
    }
}

def load_answer_template() -> Template:
    """Load the main answer template.

    Returns:
        The loaded Jinja2 template
    """
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(['html', 'xml'])
    )
    return env.get_template("answer.j2")

def load_theory_template(theory: str, section: str) -> str:
    """Load a theory-specific template section.

    Args:
        theory: The theory name (e.g., 'RBV', 'TCE')
        section: The template section ('intro', 'analysis', 'conclusion')

    Returns:
        The template content as a string
    """
    theory_path = TEMPLATES_DIR / theory.lower()
    section_file = theory_path / f"{section}.j2"

    if section_file.exists():
        with open(section_file) as f:
            return f.read()
    elif theory in DEFAULT_TEMPLATES and section in DEFAULT_TEMPLATES[theory]:
        return DEFAULT_TEMPLATES[theory][section]
    else:
        return ""

def create_default_templates() -> None:
    """Create default templates if they don't exist."""
    # Create templates directory if it doesn't exist
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    # Create main answer template
    answer_template = TEMPLATES_DIR / "answer.j2"
    if not answer_template.exists():
        with open(answer_template, "w") as f:
            f.write("""{% if matches %}
## Strategic Concepts

{% for match in matches %}
{{ match.concept }} ({{ match.score|round }}% match): {{ match.definition }}
{% endfor %}

## Case-Specific Evidence

{% for match in matches %}
{{ match.matched_text }}
{% endfor %}

## Additional Context

{{ instructions }}

{{ user_inputs }}
{% else %}
No strategic concepts were detected. Please broaden your question or lower matching thresholds.
{% endif %}""")

    # Create theory templates
    for theory, sections in DEFAULT_TEMPLATES.items():
        theory_dir = TEMPLATES_DIR / theory.lower()
        theory_dir.mkdir(exist_ok=True)
        for section, content in sections.items():
            section_file = theory_dir / f"{section}.j2"
            if not section_file.exists():
                with open(section_file, "w") as f:
                    f.write(content)

# Create templates on module import
create_default_templates() 