import json
import logging
import uuid
from dataclasses import dataclass

from confluent_kafka import Consumer, KafkaException, Producer

logger = logging.getLogger(__name__)

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
        logger.info(f"Listening to topic {topic}")

        message = self.consumer.poll(timeout=timeout)
        if message is None:
            logger.warning("[Kafka] Timeout! Không có message.")
            return None
        if message.error():
            raise KafkaException(f"Loi consume msg {message.error()}")
        logger.info(f"Raw message: {message.value()}")
        raw_response = message.value().decode('utf-8')
        message_key = message.key().decode('utf-8') if message.key() is not None else None
        logger.info(f"Start processing message with key {message_key}")
        return [json.loads(raw_response), message_key]

    def close(self):
        self.consumer.close()
        self.producer.close()

    def produce(self, topic:str, data:dict):
        key = str(uuid.uuid4())
        logger.info(f"Sending message to topic {topic} with key {key}")
        payload_bytes = json.dumps(data).encode('utf-8')
        self.producer.produce(topic, key = key, value=payload_bytes)
        self.producer.flush()
        logger.info(f"Message is sent to topic {topic}")
