import time
from datetime import datetime

import pytest

from src.services.report_service import ReportService

pytestmark = pytest.mark.unit
topic = "sdet.bao-cao.created"

def test_consume_report_notification(kafka_client):
    payload = {
        "nguoi_bao_cao_id": 99991,
        "tin_dang_id": 88881,
        "ly_do": "spam",
        "mo_ta": "Spam",
        "ngay_bao_cao": str(datetime.now()),
        "trang_thai": "chưa xử lý"
    }

    kafka_client.produce(topic=topic, data=payload)
    report_notification, _key = kafka_client.consume(topic=topic)
    assert report_notification is not None
    assert report_notification.get("nguoi_bao_cao_id") == payload.get("nguoi_bao_cao_id")

def test_consume_duplicate_report(kafka_client, db_client, purge_topic, setup_user_and_post_test, cleanup_report):
    purge_topic(topic=topic)
    _report_service = ReportService(db_client, kafka_client)
    nguoi_bao_cao_id= setup_user_and_post_test["user_id"]
    tin_dang_id = setup_user_and_post_test["post_id"]

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

    payload_duplicate = {
        "nguoi_bao_cao_id": nguoi_bao_cao_id,
        "tin_dang_id": tin_dang_id,
        "ly_do": "spam1",
        "mo_ta": "Spam1",
        "ngay_bao_cao": str(datetime.now()),
        "trang_thai": "chưa xử lý",
        "nguoi_xu_ly_id": nguoi_bao_cao_id,
        "ngay_xu_ly": str(datetime.now()),
        "ghi_chu_xu_ly": "Ghi chú"
    }

    kafka_client.produce(topic=topic, data=payload)

    time.sleep(2)

    kafka_client.produce(topic=topic, data=payload_duplicate)

    _result1, key1 = kafka_client.consume(topic=topic)
    _result2, key2 = kafka_client.consume(topic=topic)
    
    assert key1 != key2