import time
import spacy
import logging
from typing import List, Tuple
import random
from case_context.config import SPACY_MODEL
import warnings

# Suppress spaCy W108 rule-based lemmatizer warnings
warnings.filterwarnings("ignore", category=UserWarning, message=r"\[W108\].*")

# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


def generate_sample_texts(n: int = 100) -> List[str]:
    """Generate sample business texts for benchmarking."""
    business_terms = [
        "network effects",
        "value chain",
        "competitive advantage",
        "market share",
        "barriers to entry",
        "economies of scale",
        "first mover advantage",
        "switching costs",
        "brand loyalty",
        "supply chain",
        "distribution network",
        "customer acquisition",
    ]
    return [
        f"This case study examines {random.choice(business_terms)} in the context of {random.choice(business_terms)}."
        for _ in range(n)
    ]


def get_optimized_nlp() -> spacy.language.Language:
    """
    Load the configured spaCy model and prune its pipeline to only 'tok2vec'
    for fast semantic matching. Uses `nlp.select_pipes(disable=...)` to disable
    all other components, minimizing computation and avoiding deprecation
    warnings from `disable_pipes()`. This ensures only vector-based similarity
    checks are performed.
    """

    nlp = spacy.load(SPACY_MODEL)
    # Disable all pipes except tok2vec
    pipes_to_disable = [pipe for pipe in nlp.pipe_names if pipe != "tok2vec"]
    nlp.select_pipes(disable=pipes_to_disable)
    return nlp


def benchmark_pipeline(nlp, texts: List[str]) -> Tuple[float, float]:
    """
    Benchmark spaCy pipeline performance.

    Args:
        nlp: Loaded spaCy model
        texts: List of texts to process

    Returns:
        Tuple of (total_time, avg_time_per_doc)
    """
    start_time = time.time()
    for text in texts:
        doc = nlp(text)
        # Force computation of similarity
        if len(doc) > 0:
            doc[0].similarity(doc[-1])
    total_time = time.time() - start_time
    avg_time = total_time / len(texts)
    return total_time, avg_time


def main():
    """Run benchmark comparison of full vs optimized pipeline."""
    print("Generating sample texts...")
    texts = generate_sample_texts()

    print("\nBenchmarking full pipeline...")
    nlp_full = spacy.load(SPACY_MODEL)
    full_total, full_avg = benchmark_pipeline(nlp_full, texts)

    print("\nBenchmarking optimized pipeline...")
    nlp_opt = get_optimized_nlp()
    opt_total, opt_avg = benchmark_pipeline(nlp_opt, texts)

    print("\nResults:")
    print(f"Full pipeline: {full_avg:.4f}s per doc (total: {full_total:.2f}s)")
    print(f"Optimized pipeline: {opt_avg:.4f}s per doc (total: {opt_total:.2f}s)")
    print(f"Speedup: {full_avg/opt_avg:.2f}x")


if __name__ == "__main__":
    main()
