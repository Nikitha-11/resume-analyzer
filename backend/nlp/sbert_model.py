from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute similarity using TF-IDF + cosine similarity.
    """
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    sim = cosine_similarity(tfidf[0], tfidf[1])
    return float(sim[0][0])
