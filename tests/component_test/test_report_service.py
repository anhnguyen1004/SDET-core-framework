import uuid
from datetime import datetime
from unittest.mock import patch

import pytest

from src.config.settings import settings
from src.services.report_service import ReportService

pytestmark = pytest.mark.unit
# topic = f"sdet.bao-cao.created.{uuid.uuid4()}"
# DLQ_TOPIC = f"{settings.DLQ_TOPIC}.{uuid.uuid4()}"
topic = "sdet.bao-cao.created"
DLQ_TOPIC = settings.DLQ_TOPIC

def test_consume_report_notification(kafka_client, create_topic):
    test_topic = create_topic(topic)

    payload = {
        "nguoi_bao_cao_id": 99991,
        "tin_dang_id": 88881,
        "ly_do": "spam",
        "mo_ta": "Spam",
        "ngay_bao_cao": str(datetime.now()),
        "trang_thai": "chưa xử lý"
    }
    kafka_client.produce(topic=test_topic, data=payload)
    report_notification, _key = kafka_client.consume(topic=test_topic)
    assert report_notification is not None
    assert report_notification.get("nguoi_bao_cao_id") == payload.get("nguoi_bao_cao_id")

def test_consume_duplicate_report(kafka_client, db_client, create_topic, setup_user_and_post_test, caplog):
    test_topic = create_topic(topic)

    _report_service = ReportService(db_client, kafka_client)
    nguoi_bao_cao_id= setup_user_and_post_test["user_id"]
    tin_dang_id = setup_user_and_post_test["post_id"]
    key = str(uuid.uuid4())
    
    # First event
    payload = {
        "nguoi_bao_cao_id": nguoi_bao_cao_id,
        "tin_dang_id": tin_dang_id,
        "ly_do": "spam",
        "mo_ta": "Spam",
        "ngay_bao_cao": str(datetime.now()),
        "trang_thai": "chưa xử lý",
        "nguoi_xu_ly_id": nguoi_bao_cao_id,
        "ngay_xu_ly": str(datetime.now()),
        "ghi_chu_xu_ly": "Ghi chú"
    }
    _result1, key1 = kafka_client.produce(topic=test_topic, data=payload, key=key)
    _report_service.save_report(topic=test_topic)
    rpt = _report_service.get_report(tin_dang_id=tin_dang_id, nguoi_bao_cao_id=nguoi_bao_cao_id)

    assert key1 == key
    assert len(rpt) == 1 
    assert rpt[0]["ly_do"] == payload["ly_do"]

    kafka_client.produce(topic=test_topic, data=payload, key=key)
    duplicate_rpt = _report_service.save_report(topic=test_topic)

    assert duplicate_rpt is None
    assert "Duplicate report" in caplog.text

def test_produce_dql_when_poison_msg(db_client, kafka_client, create_topic, setup_user_and_post_test, purge_topic):
    test_topic = create_topic(topic)
    purge_topic(DLQ_TOPIC)

    _report_service = ReportService(db_client, kafka_client)
    nguoi_bao_cao_id= setup_user_and_post_test["user_id"]
    tin_dang_id = setup_user_and_post_test["post_id"]
    key = str(uuid.uuid4())
    
    payload = {
        "nguoi_bao_cao_id": nguoi_bao_cao_id,
        "tin_dang_id": tin_dang_id,
    }

    kafka_client.produce(topic=test_topic, data=payload, key=key)
    err = Exception("DB execution error")

    with patch.object(db_client, "execute_query", side_effect=err):
        _report_service.save_report(topic=test_topic)

    msg, dlq_key = kafka_client.consume(topic=DLQ_TOPIC)
    assert msg is not None
    assert dlq_key == key
