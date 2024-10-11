
import yaml
import pickle
import torch
from pathlib import Path
from optimum.onnxruntime import ORTModelForSequenceClassification

from kafka_utils.config import logger

app_root = Path(__file__).parent.parent
config_path = app_root / "config.yml"

config = {}
with open(config_path, "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


class Loadable:
    """
    A class used to load machine learning models based on their type.
    Attributes
    ----------
    model : object
        The loaded machine learning model.
    Methods
    -------
    __init__(name: str)
        Initializes the Loadable instance and loads the model based on the provided name.
    load_model_pickle(model_path)
        Loads a model from a pickle file.
    load_model_onnx(model_path)
        Placeholder method for loading an ONNX model.
    load_model_transformers(model_path)
        Placeholder method for loading a Transformers model.
    """

    def __init__(self, name: str):
        type_ = config[name]["format"]
        self.type = type_

        model_path = app_root / config[name]["path"]
        logger.info(f"Loading model from {model_path}")
        if type_ == "pickle":
            self.model = self.load_model_pickle(model_path)
        elif type_ == "onnx":
            self.model = self.load_model_onnx(model_path)
            label_enc_str = ("storage/label_encoder/label_encoder_" + name + ".pkl")
            self.label_encoder = self.load_model_pickle(str(app_root / label_enc_str))
        else:
            raise ValueError(f"Unknown model type: {type_}")

    def load_model_pickle(self, model_path: str):
        with open(model_path, "rb") as model_file:
            return pickle.load(model_file)

    def load_model_onnx(self, model_path: str):
        return ORTModelForSequenceClassification.from_pretrained(model_path)


class Predictor(Loadable):
    """
    Predictor class for making predictions using a pre-loaded model.
    Attributes:
        name (str): The name of the predictor.
    Methods:
        __init__(name):
            Initializes the Predictor with a given name.
        predict(data: np.ndarray) -> np.ndarray:
            Makes a prediction based on the input data using the loaded model.
        predict_async(data: np.ndarray) -> np.ndarray:
            Asynchronously makes a prediction based on the input data using the loaded model.
    """

    def __init__(self, name):
        super().__init__(name)

    def predict(self, data):
        if self.type == "pickle":
            return self.model.predict(data)
        elif self.type == "onnx":
            predictions = []
            for i in range(0, len(data)):
                batch = data[i]
                with torch.no_grad():
                    preds = self.model(**batch).logits.argmax(-1).tolist()
                    predictions.extend(self.label_encoder.inverse_transform(preds))
            return predictions
        else:
            raise ValueError(f"Unknown model type: {self.type}")

    # TODO
    async def predict_async(self, data):
        return self.predict(data)


class Vectorizer(Loadable):
    """
    A class used to represent a Vectorizer that inherits from Loadable.
    Attributes
    ----------
    name : str
        The name of the vectorizer.
    Methods
    -------
    transform(data: np.ndarray) -> np.ndarray
        Transforms the input data using the vectorizer's model.
    """

    def __init__(self, name) -> None:
        super().__init__(name)

    def transform(self, data):
        return self.model.transform(data)