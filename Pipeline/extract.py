"""
Extractor
=========

Convert raw case / question text into structured tags based on the
nested `knowledge_base` dictionary.

Tag schema
----------
Tag = tuple[top_level, sub_bucket | framework, canonical_term]

Examples
~~~~~~~~
('StrategicTheory', 'TCE', 'opportunism')
('BusinessConcept', 'CostStructure', 'economies of scale')
('IndustryContext', 'Facilities', 'phoenix factory')
('IndustryContext', 'FocalCompany', 'terra')
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from data.knowledge_base import knowledge_base

Tag = Tuple[str, str, str]  # (top_level, sub_or_framework, canonical_term)

# --------------------------------------------------------------------
# Build flat lookup indices for O(1) matching
# --------------------------------------------------------------------
_THEORY_IDX: Dict[str, Tuple[str, str]] = {}
_BIZ_IDX: Dict[str, Tuple[str, str]] = {}
_IC_IDX: Dict[str, Tuple[str, str]] = {}

_word_re = re.compile(r"\s+")


def _normalise(text: str) -> str:
    """Lower‑case, collapse whitespace, strip punctuation lightly."""
    return _word_re.sub(" ", text.lower())


def _build_indices() -> None:
    """Populate global lookup dictionaries from the nested KB."""
    # --- StrategicTheory -------------------------------------------------
    for framework, terms in knowledge_base["StrategicTheory"].items():
        for canon, synonyms in terms.items():
            _THEORY_IDX[canon] = (framework, canon)
            for s in synonyms:
                _THEORY_IDX[s] = (framework, canon)

    # --- BusinessConcept -------------------------------------------------
    for sub_bucket, terms in knowledge_base["BusinessConcept"].items():
        for canon, synonyms in terms.items():
            _BIZ_IDX[canon] = (sub_bucket, canon)
            for s in synonyms:
                _BIZ_IDX[s] = (sub_bucket, canon)

    # --- IndustryContext -------------------------------------------------
    for sub_bucket, terms in knowledge_base["IndustryContext"].items():
        for canon, synonyms in terms.items():
            _IC_IDX[canon] = (sub_bucket, canon)
            for s in synonyms:
                _IC_IDX[s] = (sub_bucket, canon)


# Build on import
_build_indices()


# --------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------
def extract_tags(text: str) -> List[Tag]:
    """
    Return a list of Tag tuples present in *text*.

    The function performs simple substring checks against pre‑normalised
    lookup tables. For exam‑length cases this is more than fast enough;
    optimise later if needed.
    """
    found: List[Tag] = []
    haystack = _normalise(text)

    # StrategicTheory
    for phrase, (fw, canon) in _THEORY_IDX.items():
        if phrase in haystack:
            found.append(("StrategicTheory", fw, canon))

    # BusinessConcept
    for phrase, (sub, canon) in _BIZ_IDX.items():
        if phrase in haystack:
            found.append(("BusinessConcept", sub, canon))

    # IndustryContext
    for phrase, (sub, canon) in _IC_IDX.items():
        if phrase in haystack:
            found.append(("IndustryContext", sub, canon))

    # de‑duplicate while preserving order
    seen = set()
    unique: List[Tag] = []
    for t in found:
        if t not in seen:
            unique.append(t)
            seen.add(t)
    return unique


# Simple CLI helper ---------------------------------------------------
if __name__ == "__main__":
    import sys

    sample_text = (
        " ".join(sys.argv[1:])
        or "Terra's Phoenix factory faces supplier hold‑up risks."
    )
    for tag in extract_tags(sample_text):
        print(tag)
