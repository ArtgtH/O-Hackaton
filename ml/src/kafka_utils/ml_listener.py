import pandas as pd

from app.models.preprocessing import preprocess
from app.models.prediction import predict


def get_from_kafka_and_return(data: pd.DataFrame) -> pd.DataFrame():
    res_encoded = preprocess(data)
    result_df = predict(res_encoded)
    return result_df
