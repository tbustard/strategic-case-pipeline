"""Concept mapping module for matching extracted facts to knowledge base concepts.

This module provides functionality to map extracted business facts to predefined
concepts in the knowledge base using both fuzzy string matching and semantic
similarity.
"""

from dataclasses import dataclass
from typing import List, Optional, Union, Dict
import numpy as np
from fuzzywuzzy import fuzz
from spacy.language import Language

from case_context.extract import ExtractedFacts, load_nlp_model, extract_facts
from case_context.knowledge_base import KNOWLEDGE_BASE, Concept, CONCEPTS
from case_context.config import FUZZY_THRESHOLD, SEMANTIC_THRESHOLD


@dataclass
class ExtractedFact:
    """Represents a single extracted fact from text."""
    text: str
    source: str
    type: str


@dataclass
class ConceptMatch:
    """Represents a match between text and a concept."""

    concept: str
    score: float
    definition: str
    source: str
    matched_text: Optional[str] = None


def get_concept_by_name(name: str) -> Optional[Concept]:
    """Get a concept from the knowledge base by name.
    
    Args:
        name: Name of the concept to get
        
    Returns:
        Concept object if found, None otherwise
    """
    return KNOWLEDGE_BASE.get(name)


def normalize_similarity(similarity: float) -> float:
    """Normalize similarity score to 0-100 range."""
    # Cosine similarity is between -1 and 1, so we:
    # 1. Add 1 to make it 0-2
    # 2. Divide by 2 to make it 0-1
    # 3. Multiply by 100 to make it 0-100
    return ((similarity + 1) / 2) * 100


def _semantic_match(text: str, concept_text: str, nlp: Language) -> float:
    """Calculate semantic similarity between two texts using spaCy.

    Args:
        text: Source text to match against
        concept_text: Concept text to match
        nlp: Loaded spaCy model

    Returns:
        Similarity score between 0-100
    """
    # Handle common synonyms
    synonyms = {
        "network externalities": "network effects",
        "network externality": "network effects",
        "externalities": "network effects",
    }
    
    text_lower = text.lower()
    if text_lower in synonyms:
        text_lower = synonyms[text_lower]
        
    doc1 = nlp(text_lower)
    doc2 = nlp(concept_text.lower())
    return doc1.similarity(doc2) * 100  # Convert to 0-100 scale


def _get_matches(
    text: str, concepts: Dict[str, str], nlp: Language
) -> List[ConceptMatch]:
    """Find matching concepts for a given text using fuzzy and semantic matching.

    Args:
        text: Text to find matches for
        concepts: Dictionary of concepts to match against
        nlp: Loaded spaCy model

    Returns:
        List of ConceptMatch objects sorted by score
    """
    matches = []
    for concept_name, _ in concepts.items():
        # Try different fuzzy matching ratios
        fuzzy_scores = [
            fuzz.ratio(text.lower(), concept_name.lower()),  # Simple ratio
            fuzz.partial_ratio(text.lower(), concept_name.lower()),  # Partial string matching
            fuzz.token_sort_ratio(text.lower(), concept_name.lower()),  # Order-independent matching
            fuzz.token_set_ratio(text.lower(), concept_name.lower()),  # Set-based matching
        ]
        fuzzy_score = max(fuzzy_scores)
        
        semantic_score = _semantic_match(text, concept_name, nlp)
        
        # Use the higher of the two scores
        score = max(fuzzy_score, semantic_score)
        
        # Accept if either threshold is met
        if score >= FUZZY_THRESHOLD or score >= SEMANTIC_THRESHOLD:
            concept = get_concept_by_name(concept_name)
            if concept:
                matches.append(
                    ConceptMatch(
                        concept=concept_name,
                        score=float(score),
                        definition=concept.definition,
                        source=getattr(concept, "source", "case"),
                        matched_text=text
                    )
                )

    return sorted(matches, key=lambda m: m.score, reverse=True)


def map_concepts(facts: Union[Dict[str, str], List[ExtractedFact]]) -> List[ConceptMatch]:
    """Map extracted facts to concepts in the knowledge base.
    
    Args:
        facts: Dictionary of text by source or list of ExtractedFact objects
        
    Returns:
        List of ConceptMatch objects sorted by score
    """
    nlp = load_nlp_model()
    
    # Convert dict input to ExtractedFact list
    if isinstance(facts, dict):
        extracted_facts = []
        for source, text in facts.items():
            if not isinstance(text, str):
                continue
            doc = nlp(text)
            # Extract noun chunks
            for chunk in doc.noun_chunks:
                extracted_facts.append(
                    ExtractedFact(
                        text=chunk.text,
                        source=source,
                        type="noun_chunk"
                    )
                )
            # Extract business verbs
            for token in doc:
                if token.pos_ == "VERB":
                    extracted_facts.append(
                        ExtractedFact(
                            text=token.text,
                            source=source,
                            type="verb"
                        )
                    )
    else:
        extracted_facts = facts

    # Get matches for each fact
    all_matches = []
    for fact in extracted_facts:
        matches = _get_matches(fact.text, CONCEPTS, nlp)
        all_matches.extend(matches)

    # Sort by score and remove duplicates
    all_matches.sort(key=lambda x: x.score, reverse=True)
    seen = set()
    unique_matches = []
    for match in all_matches:
        key = (match.concept, match.source)
        if key not in seen:
            seen.add(key)
            unique_matches.append(match)

    return unique_matches


def map_concepts_old(facts: ExtractedFacts) -> List[ConceptMatch]:
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

        for concept in CONCEPTS:
            concept_name = concept.name.lower()

            # Try fuzzy matching with different ratios
            fuzzy_scores = [
                fuzz.ratio(chunk_text, concept_name),  # Simple ratio
                fuzz.partial_ratio(chunk_text, concept_name),  # Partial string matching
                fuzz.token_sort_ratio(
                    chunk_text, concept_name
                ),  # Order-independent matching
                fuzz.token_set_ratio(chunk_text, concept_name),  # Set-based matching
            ]
            fuzzy_score = max(fuzzy_scores)

            if fuzzy_score >= FUZZY_THRESHOLD:
                matches.append(
                    ConceptMatch(
                        concept=concept_name,
                        score=fuzzy_score,
                        definition=concept.definition,
                    )
                )
                continue  # Skip semantic matching if fuzzy match is good

            # Try semantic matching
            concept_doc = nlp(concept_name)
            semantic_score = chunk_doc.similarity(concept_doc)
            if semantic_score >= SEMANTIC_THRESHOLD:
                matches.append(
                    ConceptMatch(
                        concept=concept_name,
                        score=semantic_score * 100,  # Scale to 0-100 like fuzzy
                        definition=concept.definition,
                    )
                )

    # Process business verbs
    for verb in facts.business_verbs:
        verb_text = verb.text.lower()
        verb_doc = nlp(verb_text)

        for concept in CONCEPTS:
            concept_name = concept.name.lower()

            # Try fuzzy matching with different ratios
            fuzzy_scores = [
                fuzz.ratio(verb_text, concept_name),
                fuzz.partial_ratio(verb_text, concept_name),
                fuzz.token_sort_ratio(verb_text, concept_name),
                fuzz.token_set_ratio(verb_text, concept_name),
            ]
            fuzzy_score = max(fuzzy_scores)

            if fuzzy_score >= FUZZY_THRESHOLD:
                matches.append(
                    ConceptMatch(
                        concept=concept_name,
                        score=fuzzy_score,
                        definition=concept.definition,
                    )
                )
                continue

            # Try semantic matching
            concept_doc = nlp(concept_name)
            semantic_score = verb_doc.similarity(concept_doc)
            if semantic_score >= SEMANTIC_THRESHOLD:
                matches.append(
                    ConceptMatch(
                        concept=concept_name,
                        score=semantic_score * 100,  # Scale to 0-100 like fuzzy
                        definition=concept.definition,
                    )
                )

    # Sort matches by score in descending order
    return sorted(matches, key=lambda x: x.score, reverse=True)
