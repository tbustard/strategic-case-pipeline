"""Knowledge base of strategic management concepts and theories."""

from typing import TypedDict, Literal, Optional

Category = Literal["Strategic_Theory", "Business_Concept", "Industry_Context"]


class Concept(TypedDict):
    category: Category
    theory: Optional[str]
    description: str


# Sample knowledge base entries
KNOWLEDGE_BASE: dict[str, Concept] = {
    "transaction cost": {
        "category": "Strategic_Theory",
        "theory": "TCE",
        "description": "Transaction Cost Economics - analyzing costs of market transactions",
    },
    "resource based view": {
        "category": "Strategic_Theory",
        "theory": "RBV",
        "description": "Resource-Based View - competitive advantage from unique resources",
    },
    "platform": {
        "category": "Business_Concept",
        "theory": None,
        "description": "Digital platform business model",
    },
    "network effects": {
        "category": "Business_Concept",
        "theory": None,
        "description": "Value increases with more users",
    },
    "barriers to entry": {
        "category": "Business_Concept",
        "theory": None,
        "description": "Obstacles preventing new competitors",
    },
    "competitive advantage": {
        "category": "Business_Concept",
        "theory": None,
        "description": "Superior position in market",
    },
    "value chain": {
        "category": "Business_Concept",
        "theory": None,
        "description": "Sequence of activities creating value",
    },
    "market share": {
        "category": "Industry_Context",
        "theory": None,
        "description": "Percentage of total market sales",
    },
    "industry structure": {
        "category": "Industry_Context",
        "theory": None,
        "description": "Organization of market participants",
    },
    "regulatory environment": {
        "category": "Industry_Context",
        "theory": None,
        "description": "Government rules affecting industry",
    },
}
