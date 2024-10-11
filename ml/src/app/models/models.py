import numpy as np
import pandas as pd
import asyncio
import yaml
import pickle
from pathlib import Path
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

from .model_classes import Predictor, Vectorizer


app_root = Path(__file__).parent.parent

class ClassPredictor(Predictor):
    def __init__(self):
        super().__init__("class")


class QualityPredictor(Predictor):
    def __init__(self):
        super().__init__("quality")


class BathroomPredictor(Predictor):
    def __init__(self):
        super().__init__("bathroom")


class BeddingPredictor(Predictor):
    def __init__(self):
        super().__init__("bedding")


class ViewPredictor(Predictor):
    def __init__(self):
        super().__init__("view")


class CapacityPredictor(Predictor):
    def __init__(self):
        super().__init__("capacity")


class ClubPredictor(Predictor):
    def __init__(self):
        super().__init__("club")


class TfidfVectorizer(Vectorizer):
    def __init__(self):
        super().__init__("tfidf")


class CountVectorizer(Vectorizer):
    def __init__(self):
        super().__init__("count")


class Tokenizer:
    def __init__(self, batch_size=1024):
        self.tokenizer = self.load_tokenizer()
        self.batch_size = batch_size

    def load_tokenizer(self):
        return AutoTokenizer.from_pretrained(app_root / 'storage' / 'bedding')

    def transform(self, sequences):
        tokenized_batches = []
        for i in range(0, len(sequences), self.batch_size):
            batch = sequences[i:i + self.batch_size]
            tokenized_batch = self.tokenizer(batch, padding=True, truncation=True, return_tensors="pt")
            tokenized_batches.append(tokenized_batch)
        return tokenized_batches