import re
import pandas as pd
from typing import Optional
from app.models.models import TfidfVectorizer, CountVectorizer, Tokenizer
from app.models.utils.translation import TRANSLATION

TFIDF_VECTORIZER = TfidfVectorizer()
COUNT_VECTORIZER = CountVectorizer()
TOKENIZER = Tokenizer()


def preprocess_rate_name(text: str) -> str:
    """
    Preprocesses the given text by converting it to lowercase, stripping leading and trailing whitespace,
    translating characters based on a predefined translation table, and removing non-alphanumeric characters.
    Args:
        text (str): The input text to preprocess.
    Returns:
        Optional[str]: The cleaned text if it is not empty after preprocessing, otherwise the original text.
    """
    if not text:
        return ''

    text = text.lower().strip()
    text = text.translate(TRANSLATION)
    cleaned_text = re.sub(r"[^a-z0-9\s]+", " ", text)

    if cleaned_text != "":
        return cleaned_text
    # stupid
    return text


def preprocess(df: pd.DataFrame) -> Optional[dict]:
    """
    Preprocesses the input DataFrame by transforming the 'rate_name' column using various vectorizers and tokenizers.
    Args:
        df (pd.DataFrame): The input DataFrame containing a 'rate_name' column.
    Returns:
        Optional[dict]: A dictionary containing the transformed 'rate_name' data using TFIDF, Count Vectorizer, and Tokenizer.
                        Returns None if the DataFrame is empty or does not contain the 'rate_name' column.
    """
    
    if df.shape[0] == 0 or "rate_name" not in df.columns:
        return None

    rates = df["rate_name"].map(preprocess_rate_name)
    tfidf = TFIDF_VECTORIZER.transform(rates)
    count = COUNT_VECTORIZER.transform(rates)
    tokens = TOKENIZER.transform(rates.tolist())

    return {
        "rate_name": rates,
        "tfidf": tfidf,
        "count": count,
        "tokenizer": tokens
    }
