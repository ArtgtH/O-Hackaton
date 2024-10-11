import logging
from dataclasses import dataclass
from typing import Any, Dict

from pydantic_settings import BaseSettings
import dotenv

dotenv.load_dotenv()


class Settings(BaseSettings):
    KAFKA_BROKERS: str

    class Config:
        env_file_encoding = "utf-8"


settings = Settings()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


@dataclass
class TaskFile:
    task_id: str
    data: str
    result: str
    result_csv: str


@dataclass
class TaskStr:
    task_id: str
    data: str
    result: str
    result_csv: str
    accuracy: str
