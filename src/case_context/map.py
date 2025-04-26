"""Concept mapping module for matching extracted facts to knowledge base concepts.

This module provides functionality to map extracted business facts to predefined
concepts in the knowledge base using both fuzzy string matching and semantic
similarity.
"""

from dataclasses import dataclass
from typing import List, Literal

from fuzzywuzzy import fuzz

from .extract import ExtractedFacts, load_nlp_model
from .knowledge_base import Concept, KNOWLEDGE_BASE
from .config import FUZZY_THRESHOLD, SEMANTIC_THRESHOLD

@dataclass
class ConceptMatch:
    """Represents a match between an extracted fact and a knowledge base concept."""
    concept: Concept
    score: float
    method: Literal["fuzzy", "semantic"]
    matched_text: str

def map_concepts(facts: ExtractedFacts) -> List[ConceptMatch]:
    """Map extracted facts to knowledge base concepts using fuzzy and semantic matching.
    
    Args:
        facts: The extracted facts from the text
        
    Returns:
        List of ConceptMatch objects sorted by score in descending order
    """
    nlp = load_nlp_model()
    matches: List[ConceptMatch] = []
    
    # Process noun chunks
    for chunk in facts.noun_chunks:
        chunk_text = chunk.text.lower()
        chunk_doc = nlp(chunk_text)
        
        for concept in KNOWLEDGE_BASE:
            concept_name = concept.name.lower()
            
            # Try fuzzy matching with different ratios
            fuzzy_scores = [
                fuzz.ratio(chunk_text, concept_name),  # Simple ratio
                fuzz.partial_ratio(chunk_text, concept_name),  # Partial string matching
                fuzz.token_sort_ratio(chunk_text, concept_name),  # Order-independent matching
                fuzz.token_set_ratio(chunk_text, concept_name)  # Set-based matching
            ]
            fuzzy_score = max(fuzzy_scores)
            
            if fuzzy_score >= FUZZY_THRESHOLD:
                matches.append(ConceptMatch(
                    concept=concept,
                    score=fuzzy_score,
                    method="fuzzy",
                    matched_text=chunk_text
                ))
                continue  # Skip semantic matching if fuzzy match is good
            
            # Try semantic matching
            concept_doc = nlp(concept_name)
            semantic_score = chunk_doc.similarity(concept_doc)
            if semantic_score >= SEMANTIC_THRESHOLD:
                matches.append(ConceptMatch(
                    concept=concept,
                    score=semantic_score * 100,  # Scale to 0-100 like fuzzy
                    method="semantic",
                    matched_text=chunk_text
                ))
    
    # Process business verbs
    for verb in facts.business_verbs:
        verb_text = verb.text.lower()
        verb_doc = nlp(verb_text)
        
        for concept in KNOWLEDGE_BASE:
            concept_name = concept.name.lower()
            
            # Try fuzzy matching with different ratios
            fuzzy_scores = [
                fuzz.ratio(verb_text, concept_name),
                fuzz.partial_ratio(verb_text, concept_name),
                fuzz.token_sort_ratio(verb_text, concept_name),
                fuzz.token_set_ratio(verb_text, concept_name)
            ]
            fuzzy_score = max(fuzzy_scores)
            
            if fuzzy_score >= FUZZY_THRESHOLD:
                matches.append(ConceptMatch(
                    concept=concept,
                    score=fuzzy_score,
                    method="fuzzy",
                    matched_text=verb_text
                ))
                continue
            
            # Try semantic matching
            concept_doc = nlp(concept_name)
            semantic_score = verb_doc.similarity(concept_doc)
            if semantic_score >= SEMANTIC_THRESHOLD:
                matches.append(ConceptMatch(
                    concept=concept,
                    score=semantic_score * 100,  # Scale to 0-100 like fuzzy
                    method="semantic",
                    matched_text=verb_text
                ))
    
    # Sort matches by score in descending order
    return sorted(matches, key=lambda x: x.score, reverse=True) 