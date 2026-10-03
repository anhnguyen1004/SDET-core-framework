import logging
from dataclasses import dataclass
from models.data_models import User
from config.settings import settings

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class KafkaClient:

    def __init__(self, broker_url:str = settings.KAFKA_BROKER):
        self.broker_url = broker_url

    def produce_message(self, topic:str, data:User):
        logging.info(f"Sending message '{data}' to topic '{topic}' using broker '{self.broker_url}'")
    
if __name__ == "__main__":
    user = User(
        id=1,
        email="email@gmail.com",
        username="John Doe",
        is_active=True
    )

    client = KafkaClient()
    client.produce_message("topic.name", user)
