"""Concept mapping and knowledge base integration module."""

import logging
from typing import TypedDict, List, Dict, Optional, Tuple
from case_context.extract import load_nlp_model
from case_context.knowledge_base import KNOWLEDGE_BASE

from case_context.config import FUZZY_THRESHOLD, SEMANTIC_THRESHOLD

logger = logging.getLogger(__name__)

try:
    from rapidfuzz import process, fuzz
except ImportError:
    logger.error("Missing dependency: rapidfuzz. Please run `pip install rapidfuzz>=2.13.7`.")
    raise


class MappedConcept(TypedDict):
    """Structure for mapped business concepts."""
    concept: str
    category: str
    theory: Optional[str]
    confidence: float

def fuzzy_match_term(term: str, choices: List[str]) -> Tuple[str, float]:
    """
    Return best KB key match and score (0–100) using token_sort_ratio.
    
    Args:
        term: Term to match
        choices: List of possible matches
        
    Returns:
        Tuple of (best match, confidence score)
    """
    # Clean term: strip whitespace and lowercase for matching
    term_clean = term.strip().lower()
    match, score, _ = process.extractOne(
        term_clean, choices, scorer=fuzz.token_sort_ratio
    )
    return match, score

def semantic_match_term(term: str, choices: List[str], nlp) -> Tuple[str, float]:
    """
    Return best KB key match and spaCy similarity score (0–1).
    
    Args:
        term: Term to match
        choices: List of possible matches
        nlp: Loaded spaCy model
        
    Returns:
        Tuple of (best match, similarity score)
    """
    # Handle empty choices
    if not choices:
        return "", 0.0
        
    # Clean term: strip surrounding whitespace and lowercase
    term_clean = term.strip().lower()
    
    # Handle exact matches first
    for choice in choices:
        if term_clean == choice.lower():
            return choice, 1.0
            
    # Try fuzzy matching first
    best_fuzzy_score = 0
    best_fuzzy_match = None
    for choice in choices:
        score = fuzz.ratio(term_clean, choice.lower()) / 100.0
        if score > best_fuzzy_score:
            best_fuzzy_score = score
            best_fuzzy_match = choice
            
    # If fuzzy match is good enough, use it
    if best_fuzzy_score >= 0.8:
        return best_fuzzy_match, best_fuzzy_score
    
    # Try semantic matching
    doc = nlp(term_clean)
    similarities = [
        (choice, doc.similarity(nlp(choice.lower())))
        for choice in choices
    ]
    best_key, best_sim = max(similarities, key=lambda kv: kv[1])
    
    # For unrelated terms, both fuzzy and semantic scores should be low
    if best_fuzzy_score < 0.3 and best_sim < 0.7:
        return best_key, min(best_fuzzy_score, best_sim)
    
    # Return the best match overall
    if best_fuzzy_score > best_sim:
        return best_fuzzy_match, best_fuzzy_score
    return best_key, best_sim

def map_to_knowledge_base(extracted_terms: List[str]) -> List[MappedConcept]:
    """
    Map extracted terms to the knowledge base using exact, fuzzy, and semantic matching.
    
    Args:
        extracted_terms: List of terms to map
        
    Returns:
        List of mapped concepts with confidence scores
    """
    mapped_concepts: List[MappedConcept] = []
    kb_choices = list(KNOWLEDGE_BASE.keys())
    nlp = None  # Lazy load spaCy model only if needed
    
    for term in extracted_terms:
        term_lower = term.lower()
        
        # Try exact match first
        if term_lower in KNOWLEDGE_BASE:
            concept = KNOWLEDGE_BASE[term_lower]
            mapped_concepts.append({
                "concept": term,
                "category": concept["category"],
                "theory": concept["theory"],
                "confidence": 1.0
            })
            continue
            
        # Try fuzzy matching
        fuzzy_match, fuzzy_score = fuzzy_match_term(term_lower, kb_choices)
        if fuzzy_score >= FUZZY_THRESHOLD:
            concept = KNOWLEDGE_BASE[fuzzy_match]
            mapped_concepts.append({
                "concept": term,
                "category": concept["category"],
                "theory": concept["theory"],
                "confidence": fuzzy_score / 100.0
            })
            continue
            
        # Try semantic matching
        if nlp is None:
            nlp = load_nlp_model()
        semantic_match, semantic_score = semantic_match_term(term_lower, kb_choices, nlp)
        if semantic_score >= SEMANTIC_THRESHOLD:
            concept = KNOWLEDGE_BASE[semantic_match]
            mapped_concepts.append({
                "concept": term,
                "category": concept["category"],
                "theory": concept["theory"],
                "confidence": semantic_score
            })
            continue
            
        # No match found
        mapped_concepts.append({
            "concept": term,
            "category": "Unmapped",
            "theory": None,
            "confidence": 0.0
        })
    
    return mapped_concepts

def identify_relevant_theories(mapped_concepts: List[MappedConcept]) -> List[str]:
    """
    Identify strategic theories relevant to the case.
    
    Args:
        mapped_concepts: List of mapped concepts
        
    Returns:
        List of relevant theory names
    """
    theories = set()
    for concept in mapped_concepts:
        if concept["theory"]:
            theories.add(concept["theory"])
    return sorted(list(theories))

def analyze_case_context(
    case_facts: Dict[str, List[str]],
    question_facts: Dict[str, List[str]]
) -> Dict[str, List[MappedConcept]]:
    """
    Analyze the case and question context to identify relevant concepts.
    
    Args:
        case_facts: Extracted facts from case text
        question_facts: Extracted facts from question text
        
    Returns:
        Dictionary of mapped concepts by category
    """
    logger.info("Analyzing case context")
    
    # Combine all extracted terms
    all_terms = (
        case_facts["named_entities"] +
        case_facts["noun_chunks"] +
        case_facts["business_verbs"] +
        question_facts["named_entities"] +
        question_facts["noun_chunks"] +
        question_facts["business_verbs"]
    )
    
    # Map terms to knowledge base
    mapped_concepts = map_to_knowledge_base(all_terms)
    
    # Group by category
    categorized_concepts: Dict[str, List[MappedConcept]] = {}
    for concept in mapped_concepts:
        category = concept["category"]
        if category not in categorized_concepts:
            categorized_concepts[category] = []
        categorized_concepts[category].append(concept)
    
    return categorized_concepts 