import asyncio
import json

from aiokafka import AIOKafkaConsumer

from kafka_utils.config import settings, logger

from kafka_utils.file_task.file_task_imitate import file_task_imitate_ML
from kafka_utils.file_task.file_task_producer import FileTaskProducer

from kafka_utils.str_task.str_task_producer import StrTaskProducer
from kafka_utils.str_task.str_task_imitate import str_task_imitate_ML


async def consume():
	logger.info("Starting consumer")
	consumer = AIOKafkaConsumer(
		"ml-input",
		bootstrap_servers=settings.KAFKA_BROKERS,
		auto_offset_reset="earliest",
		enable_auto_commit=True,
		group_id="my-group",
		value_deserializer=lambda x: json.loads(x.decode("utf-8")),
	)

	await consumer.start()

	try:
		async for message in consumer:
			logger.info(f"Received message: {message.value} from {message.topic}")

			if message.value["type"] == "file":
				result = await file_task_imitate_ML(message.value)

				await FileTaskProducer(result).produce()

			elif message.value["type"] == "string":
				result = await str_task_imitate_ML(message.value)

				await StrTaskProducer(result).produce()

	finally:
		logger.info("Shutting down consumer")
		await consumer.stop()


if __name__ == "__main__":
	asyncio.run(consume())
