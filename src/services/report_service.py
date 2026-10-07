from src.models.db_client import PostgresDBClient
from src.models.kafka_client import KafkaClient

class ReportService:
    def __init__(self, db_client:PostgresDBClient, kafka_client:KafkaClient):
        self.db_client = db_client
        self.kafka_client = kafka_client
        