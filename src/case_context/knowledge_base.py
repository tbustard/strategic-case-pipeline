"""Knowledge base definitions and data structures."""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Concept:
    """A business concept with its definition and theory."""

    name: str
    definition: str
    theory: Optional[str] = None


KNOWLEDGE_BASE: Dict[str, Concept] = {
    "Network Effects": Concept(
        name="Network Effects",
        definition="The phenomenon where a product or service becomes more valuable as more people use it.",
        theory="PlatformStrategy",
    ),
    "First Mover Advantage": Concept(
        name="First Mover Advantage",
        definition="The competitive edge gained by entering a market or developing a technology before rivals.",
        theory="CompetitiveDynamics",
    ),
    "Asset Specificity": Concept(
        name="Asset Specificity",
        definition="The degree to which investments are specific to a particular transaction and have little value outside that relationship.",
        theory="TCE",
    ),
    "Five Forces": Concept(
        name="Five Forces",
        definition="Porter's framework for analyzing industry competition through five key forces: supplier power, buyer power, competitive rivalry, threat of substitution, and threat of new entry.",
        theory="CompetitiveDynamics",
    ),
    "Platform Strategy": Concept(
        name="Platform Strategy",
        definition="A business model that creates value by facilitating exchanges between two or more interdependent groups, usually consumers and producers.",
        theory="PlatformStrategy",
    ),
    # ... existing concepts ...
}

# Expose concepts as a simple dictionary for mapping
CONCEPTS: Dict[str, str] = {
    concept.name: concept.definition for concept in KNOWLEDGE_BASE.values()
}

# Initial knowledge base with core strategic management concepts
KNOWLEDGE_BASE_LIST = [
    # Transaction Cost Economics concepts
    Concept("Transaction Cost Economics", "Economics", "TCE"),
    Concept("Opportunism", "Economics", "TCE"),
    Concept("Governance Structure", "Economics", "TCE"),
    Concept("Make or Buy Decision", "Economics", "TCE"),
    # Resource Based View concepts
    Concept("Resource-Based View", "Strategy", "RBV"),
    Concept("Core Competency", "Strategy", "RBV"),
    Concept("Competitive Advantage", "Strategy", "RBV"),
    Concept("VRIO Framework", "Strategy", "RBV"),
    Concept("Dynamic Capabilities", "Strategy", "RBV"),
    # Platform Strategy concepts
    Concept("Platform Strategy", "Strategy", "PlatformStrategy"),
    Concept("Multi-sided Platform", "Strategy", "PlatformStrategy"),
    Concept("Platform Ecosystem", "Strategy", "PlatformStrategy"),
    # Disruption concepts
    Concept("Disruptive Innovation", "Strategy", "DemandSideDisruption"),
    Concept("Low-end Disruption", "Strategy", "DemandSideDisruption"),
    Concept("New-market Disruption", "Strategy", "DemandSideDisruption"),
    Concept("Architectural Innovation", "Strategy", "ArchitecturalDisruption"),
    Concept("Modular Innovation", "Strategy", "ArchitecturalDisruption"),
    # General business concepts
    Concept("Market Entry", "BusinessConcept"),
    Concept("Market Share", "BusinessConcept"),
    Concept("Value Chain", "BusinessConcept"),
    Concept("Industry Structure", "BusinessConcept"),
    Concept("Barriers to Entry", "BusinessConcept"),
]
