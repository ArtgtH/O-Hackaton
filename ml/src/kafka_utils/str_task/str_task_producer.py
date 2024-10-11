import json
from dataclasses import asdict

from aiokafka import AIOKafkaProducer


from kafka_utils.config import settings, logger


class StrTaskProducer:
    def __init__(self, task):
        self.task = task

    async def produce(self):
        producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BROKERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await producer.start()
        try:
            message = asdict(self.task)
            await producer.send_and_wait("finished-str-tasks", value=message)
            logger.info(f"Producer sent {message}")
        finally:
            await producer.stop()
