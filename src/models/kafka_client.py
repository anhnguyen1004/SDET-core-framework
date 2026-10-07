import logging
import json
import uuid
from dataclasses import dataclass
from src.models.data_models import User
from src.config.settings import settings
from confluent_kafka import Consumer, KafkaException, Producer

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class KafkaClient:
    def __init__(self, bootstrap_servers="localhost:9092", group_id="sdet_qa_group"):
        self.conf = {
            'auto.offset.reset': 'earliest',
            'bootstrap.servers': bootstrap_servers,
            'group.id': f'{group_id}-{uuid.uuid4()}'
        }
        self.producer = Producer(self.conf)
        self.consumer = Consumer(self.conf)
        
    def consume(self, topic: str, timeout: float = 10.0):
        self.consumer.subscribe([topic])
        logging.info(f"Listening to topic {topic}")

        message = self.consumer.poll(timeout=timeout)
        if message is None:
            logging.warning("[Kafka] Timeout! Không có message.")
            return None
        if message.error():
            raise KafkaException(f"Loi consume msg {message.error()}")
        logging.info(f"Raw message: {message.value()}")
        raw_response = message.value().decode('utf-8')
        return json.loads(raw_response)

    def close(self):
        self.consumer.close()
        self.producer.close()

    def produce(self, topic:str, data:dict):
        logging.info(f"Sending message to topic {topic}")
        payload_bytes = json.dumps(data).encode('utf-8')
        self.producer.produce(topic, value=payload_bytes)
        self.producer.flush()
        logging.info(f"Message is sent to topic {topic}")
