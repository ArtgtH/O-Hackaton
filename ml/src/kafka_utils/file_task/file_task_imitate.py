import base64
import json
from io import BytesIO
from typing import Dict

import pandas as pd

from kafka_utils.config import TaskFile, logger
from kafka_utils.ml_listener import get_from_kafka_and_return


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


async def file_task_imitate_ML(value: Dict):
	raw_data = value["data"]
	decoded_bytes = base64.b64decode(raw_data)
	byte_stream = BytesIO(decoded_bytes)
	df_in = pd.read_csv(byte_stream)
	df_out = get_from_kafka_and_return(df_in)

	csv_str = df_out.to_csv(index=False)
	csv_base64 = base64.b64encode(csv_str.encode()).decode()

	result = dataframe_to_json(df_out)

	json_base64 = base64.b64encode(result.encode()).decode()

	new_task = TaskFile(
		task_id=value["task_id"],
		data=value["data"],
		result=json_base64,
		result_csv=csv_base64,
	)

	return new_task
