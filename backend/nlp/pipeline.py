from backend.nlp.extract_text import extract_resume
from backend.nlp.preprocess import preprocess
from backend.nlp.sbert_model import compute_similarity

def analyse_resume(resume_path: str, job_description: str) -> float:
    """
    Full pipeline: extract, preprocess, embed, and compute similarity.
    """
    # Step 1: Extract text
    raw_text = extract_resume(resume_path)

    # Step 2: Preprocess text
    clean_text = preprocess(raw_text)

    # Step 3: Compute similarity with job description
    score = compute_similarity(clean_text, job_description)

    return score
