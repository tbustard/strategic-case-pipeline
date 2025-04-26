"""Tests for spaCy pipeline optimization."""

import pytest
import logging
from extract import load_nlp_model

def test_only_tok2vec_in_pipeline(caplog):
    """Test that only tok2vec remains in the optimized pipeline."""
    # Capture INFO logs
    caplog.set_level(logging.INFO)
    
    # Load model
    nlp = load_nlp_model()
    
    # Assert only tok2vec is active
    assert nlp.pipe_names == ["tok2vec"]
    
    # Also assert logs contain our INFO message
    msgs = [rec.message for rec in caplog.records]
    assert any("Loaded optimized spaCy pipeline" in m for m in msgs) 