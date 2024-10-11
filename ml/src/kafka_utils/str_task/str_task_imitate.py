import base64
from io import BytesIO
from typing import Dict
import json
import pandas as pd

from kafka_utils.config import TaskStr, logger
from kafka_utils.ml_listener import get_from_kafka_and_return

FILE_JSON_PATH = "src/kafka_utils/str_task/test.json"


def dataframe_to_json(df):
    # Преобразуем DataFrame в список словарей
    data = df.to_dict(orient='records')

    # Форматируем данные в нужный JSON формат
    json_result = {
        "names": data
    }

    # Преобразуем словарь в JSON строку
    json_str = json.dumps(json_result, indent=4)

    return json_str


async def str_task_imitate_ML(value: Dict):

    data = {"rate_name": [value["data"]]}

    df_in = pd.DataFrame(data)

    df_out = get_from_kafka_and_return(df_in)

    result = dataframe_to_json(df_out)

    json_base64 = base64.b64encode(result.encode()).decode()

    with open(FILE_JSON_PATH, "rb") as file:
        json_file_bytes = file.read()

    base64_encoded_json = base64.b64encode(json_file_bytes).decode('utf-8')

    # TODO сделать чтобы работала accuracy

    csv_str = df_out.to_csv(index=False)
    csv_base64 = base64.b64encode(csv_str.encode()).decode()

    new_task = TaskStr(
        task_id=value["task_id"],
        data=value["data"],
        result=json_base64,
        accuracy=base64_encoded_json,
        result_csv=csv_base64
    )

    return new_task
