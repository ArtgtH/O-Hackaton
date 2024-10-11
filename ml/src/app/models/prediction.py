import numpy as np
import pandas as pd
import asyncio
from app.models.models import (ClassPredictor,
                               QualityPredictor,
                               BathroomPredictor,
                               BeddingPredictor,
                               ViewPredictor,
                               CapacityPredictor,
                               ClubPredictor,
                               TfidfVectorizer,
                               CountVectorizer,
                               Tokenizer)

PREDICTORS = {
    "class": {
        "input": "count",
        "model": ClassPredictor(),
    },
    "quality": {
        "input": "tfidf",
        "model": QualityPredictor(),
    },
    "bathroom": {
        "input": "tfidf",
        "model": BathroomPredictor(),
    },
    "bedding": {
        "input": "tokenizer",
        "model": BeddingPredictor()
    },
    "view": {
        "input": "tokenizer",
        "model": ViewPredictor()
    },
    "capacity": {
        "input": "tokenizer",
        "model": CapacityPredictor()
    },
    "club": {
        "input": "tfidf",
        "model": ClubPredictor()
    },
}

TARGETS = list(PREDICTORS.keys())
DEFAULT = pd.DataFrame(columns=[name for name in TARGETS])


def predict(rate_names) -> pd.DataFrame:
    """
    Predicts outcomes using pre-trained models.
    Args:
        rate_names (dict): An dict of differently transformed rate_name for pred.
    Returns:
        pl.DataFrame: A DataFrame containing the predictions from each model.
    """
    if not rate_names:
        return DEFAULT

    predictions = [
        PREDICTORS[name]["model"].predict(rate_names[PREDICTORS[name]["input"]])
        for name in PREDICTORS
    ]

    return pd.DataFrame(
        {name: pred for name, pred in zip(TARGETS, predictions)}
    )