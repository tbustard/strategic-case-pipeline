"""Concept mapping and knowledge base integration module."""

import logging
from typing import TypedDict, List, Dict, Optional, Tuple
from case_context.extract import load_nlp_model
from case_context.knowledge_base import KNOWLEDGE_BASE, Concept
from case_context.config import FUZZY_THRESHOLD, SEMANTIC_THRESHOLD 