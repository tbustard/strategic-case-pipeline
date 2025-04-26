"""Knowledge base module containing strategic management concepts."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Concept:
    """A strategic management concept."""
    name: str
    category: str
    theory: Optional[str] = None

# Initial knowledge base with core strategic management concepts
KNOWLEDGE_BASE = [
    # Transaction Cost Economics concepts
    Concept("Transaction Cost Economics", "Economics", "TCE"),
    Concept("Asset Specificity", "Economics", "TCE"),
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
    Concept("Network Effects", "Strategy", "PlatformStrategy"),
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