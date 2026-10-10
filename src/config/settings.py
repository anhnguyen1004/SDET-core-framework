import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    ENV = os.getenv("ENV_NAME")
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")


settings = Config()