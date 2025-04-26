"""
Case‑anchored knowledge base for the Strategic Case Pipeline.

Structure
---------
knowledge_base = {
    "StrategicTheory": {  # canonical framework buckets
        "<FrameworkName>": {
            "<canonical term>": [<accepted paraphrases>]
        },
        ...
    },
    "BusinessConcept": {  # flat for now
        "<concept>": [<optional paraphrases>]
    },
    "IndustryContext": {  # proper nouns / products / site names, etc.
        "<case term>": []
    },
    "Ambiguous": {        # held out until categorised
        "<unclear term>": []
    }
}
"""

knowledge_base: dict[str, dict] = {
    "StrategicTheory": {
        "TCE": {
            "asset specificity": [
                "custom fabrication causing lock-in",
                "specialized inputs",
                "bespoke parts causing dependency",
                "tailored components with no resale value"
            ],
            "opportunism": [
                "supplier hold-up",
                "renegotiation threat"
            ],
            "coordination costs": [
                "frequent delays from fragmented subcontractors"
            ],
            "transaction costs": [
                "market exchange frictions",
                "negotiation overhead"
            ],
            "supplier fragmentation": [
                "many small subcontractors",
                "over 400,000 specialized subcontractors"
            ],
            "holdup risk": [
                "risk of delays from suppliers",
                "projects get held up"
            ]
        },
        "RBV": {
            "learning curve effects": [
                "move down cost curve as volumes rise"
            ],
            "proprietary manufacturing": [
                "in‑house production of clt panels",
                "owning specialized factories"
            ],
            "firm‑specific capabilities": [
                "architectural expertise",
                "integrated design software"
            ],
            "unique knowledge assets": ["proprietary design library"],
            "hard‑to‑imitate capabilities": ["firm‑specific know‑how"],
            "causal ambiguity": [],
            "social complexity": [],
            "path dependence": [],
            "dynamic capabilities": ["orchestrating resources"],
        },
        "PlatformStrategy": {
            "network effects": [
                "virtuous cycle of adoption"
            ],
            "standards and interfaces": [
                "interoperable specifications",
                "common language for parts"
            ],
            "multi‑sided network": [
                "ecosystem participation",
                "marketplace of suppliers and architects"
            ],
            "two‑sided platform": ["multi‑sided marketplace"],
            "critical mass": [],
            "network lock‑in": ["participant lock‑in"],
            "entry barriers": ["platform switching costs"],
        },
        "ResidualControlRights": {
            "residual control rights": [],
            "property rights theory": [],
            "decision rights": ["control of complementary assets"],
        },
        # Other frameworks left intentionally empty for now
        "ValueBasedStrategy": {
            "added value analysis": [],
            "value stick analysis": ["expand total value"]
        },
        "ValueStick": {
            "willingness to pay": [],
            "willingness to sell": [],
            "added value": [],
            "consumer surplus": [],
            "supplier surplus": [],
            "total value creation": [],
        },
        "Coopetition": {
            "value net": [],
            "co‑opetition": [],
            "mutual value creation": [],
        },
        "DemandSideDisruption": {
            "low‑end disruption": [],
            "over‑served customers": [],
            "simpler cheaper alternative": [],
            "underserved segment": [],
            "simple reliable alternative": [],
        },
        "ArchitecturalDisruption": {
            "reconfigured value chain": [],
            "new system architecture": [],
            "system reconfiguration": [],
            "interface innovation": [],
        },
        "PropertyRights": {
            "incomplete contracts": [],
            "asset ownership": [],
            "ownership structure": [],
        },
        "DynamicCapabilities": {
            "sensing": ["opportunity identification"],
            "seizing": ["resource mobilization"],
            "reconfiguring": ["asset re‑allocation"],
            "continuous learning": []
        },
    },

    "BusinessConcept": {
        # ---- 1. BUSINESS CONCEPT RESTRUCTURE (partial key migration) ----
        "CostStructure": {
            "cost-plus contracts": [],
            "fixed cost absorption": ["under-utilised factories"],
            "negative profit margin": ["unprofitable projects"],
            "economies of scale": ["running factories at capacity", "scale economies"],
            "economies of scope": ["shared resources across products"],
            "economies of density": [],
            "economies of adjacency": [],
            "learning economies": ["cumulative learning effects", "economies of learning"],
            "fixed cost leverage": [],
            "unit economics": [],
            "cost leadership": [],
            "capital intensity": [],
            "sunk cost": [],
            "overcapacity": [],
            "inventory holding cost": [],
        },
        "MarketStrategy": {
            "differentiation": [],
            "first mover advantage": [],
            "underpricing strategy": ["lose money on first projects"],
            "go-to-market strategy": [],
            "market acceptance": [],
            "customer adoption barriers": [],
            "barriers to adoption": [],
            "value capture": [],
            "asset-light model": [],
            "adjacent market expansion": [],
            "two-sided market": [],
            "network externalities": ["positive feedback loops"],
            "virtuous cycle": [],
            "positive feedback loop": [],
            "demand aggregation": [],
            "supplier switching costs": [],
            "switching costs": [],
            "standardization": ["menu of modular components"],
            "customization": ["unique building designs"],
            "modular construction": ["modular building systems"],
            "modular design": [],
            "value network": [],
            "stickiness": [],
            "customer lock‑in": [],
            "platform governance": [],
            "ecosystem governance": [],
            "blue ocean strategy": [],
            "value innovation": [],
        },
        "Operations": {
            "factory utilization": [],
            "shipping distance limit": ["within 500 miles of factory"],
            "shipping logistics": [],
            "supply uncertainty": [],
            "supply chain resilience": [],
            "risk mitigation": [],
            "component interoperability": [],
            "standard interfaces": [],
            "project pipeline": [],
            "holdup mitigation": [],
            "incentive alignment": [],
            "governance mechanisms": [],
            "stakeholder alignment": [],
            "learning curve": ["progress ratio", "experience curve"],
            "quality control": [],
            "process automation": [],
        },
        "Organization": {
            "organizational learning": [],
            "organizational complexity": [],
            "bureaucratic costs": [],
            "fragmentation": ["decentralized supply chain"],
            "local adaptation": [],
            "capability building": [],
            "knowledge sharing": [],
            "cross‑functional teams": [],
        },
        "Regulation": {
            "regulatory heterogeneity": [],
            "local code compliance": [],
            "building code approval": [],
            "permitting delays": [],
            "compliance cost": [],
        },
        "Misc": {
            # empty for now
        },
    },

    "IndustryContext": {
        # ---- 2. INDUSTRY CONTEXT RESTRUCTURE (partial migration) ----
        "Facilities": {
            "phoenix factory": [],
            "spokane clt plant": [],
            "clt panels factory": ["phoenix clt panels"],
        },
        "ProductsAndSystems": {
            "prefabricated panels": ["wall panels", "pre-installed conduits"],
            "floor cassettes": [],
            "bathroom pods": [],
            "prefab bathroom kit": [],
            "prefab kitchen kit": [],
            "clt panels": [],
            "clt wall system": [],
            "clt floor system": [],
            "clt facade": ["clt facade system"],
            "fast foundation": ["fast foundation system"],
            "k-crete": ["low‑carbon k‑crete", "k‑crete low carbon", "low‑carbon concrete", "k‑crete low-carbon concrete"],
            "kes energy storage": ["energy storage system"],
            "ktac air conditioning": ["ktac"],
            "mass timber": [],
            "cross laminated timber": ["clt"],
            "conference room partition system": [],
            "raised office floor": ["raised office floor clt"],
            "construction robotics demo": [],
        },
        "Projects": {
            "garden apartments": [],
            "garden apartment k3": ["k3 garden apartment"],
            "corridor multifamily": [],
            "corridor apartment project": [],
            "k4 workforce housing": ["k4 workforce housing building"],
            "k10 high rise": ["k10 multifamily high-rise"],
            "10-story india multifamily": [],
            "midrise timber office": [],
            "mrop midrise office": [],
            "mtop mass timber office": [],
            "industrial clt building": ["industrial building clt walls"],
            "single family prefab": [],
            "precast saudi home": ["precast home"],
            "mass timber office building": [],
        },
        "FocalCompany": {
            "terra": [],
        },
        "CompaniesAndSoftware": {
            "mga architects": [],
            "fields construction": [],
            "equilibrium engineers": [],
            "kroc construction office": [],
            "kroc office product": ["kroc"],
            "apollo software": [],
            "apollo construction suite": [],
            "katerra": [],
        },
        "DigitalTools": {
            "apollo cms": ["tenant management platform"],
            "apollo tenant app": ["tenant management app"],
            "katerra design library": [],
            "automated building design": [],
            "apollo project tracker": [],
            "terra bidding platform": [],
        },
        "Misc": {
        },
    },

    "Ambiguous": {
        # new phrases go here until reviewed
    }
}