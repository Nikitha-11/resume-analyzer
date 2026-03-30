import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Make sure you download these once in your environment:
# nltk.download('stopwords')
# nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text: str) -> str:
    """
    Basic cleaning: lowercase, remove punctuation/numbers/symbols.
    """
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # keep only letters and spaces
    return text

def tokenize_text(text: str) -> list:
    """
    Tokenize, remove stopwords, and lemmatize.
    """
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens

def preprocess(text: str) -> str:
    """
    Full pipeline: clean + tokenize + rejoin.
    """
    cleaned = clean_text(text)
    tokens = tokenize_text(cleaned)
    return " ".join(tokens)
