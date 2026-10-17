import json
import uuid
from unittest.mock import patch

import pytest
from confluent_kafka import KafkaException

from src.config.settings import settings

pytestmark = pytest.mark.unit
# topic = f"sdet.bao-cao.created.{uuid.uuid4()}"
# DLQ_TOPIC = f"{settings.DLQ_TOPIC}.{uuid.uuid4()}"
topic = "sdet.bao-cao.created"
DLQ_TOPIC = settings.DLQ_TOPIC

def test_produce_dql_when_fail_to_parse_msg(kafka_client, purge_topic, unique_topic):
    purge_topic(topic=DLQ_TOPIC)
    payload = {
        "payload": {}
    }
    key = str(uuid.uuid4())
    kafka_client.produce(topic=unique_topic, data=payload, key=key)

    err = json.JSONDecodeError("Invalid JSON", "doc", 0)
    with patch.object(json, "loads", side_effect=err), pytest.raises(KafkaException):
        kafka_client.consume(topic=unique_topic)

    msg, dlq_key = kafka_client.consume(topic=DLQ_TOPIC)
    assert msg is not None
    assert dlq_key == key