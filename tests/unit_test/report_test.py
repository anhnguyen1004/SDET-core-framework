import pytest
from src.models.report import Report
from datetime import datetime

pytestmark = pytest.mark.unit

def test_consume_report_notification(kafka_client):
    payload = {
        "nguoi_bao_cao_id": 99991,
        "tin_dang_id": 88881,
        "ly_do": "spam",
        "mo_ta": "Spam",
        "ngay_bao_cao": str(datetime.now()),
        "trang_thai": "chưa xử lý"
    }

    kafka_client.produce(topic="sdet.bao-cao.created", data=payload)
    report_notification = kafka_client.consume(topic="sdet.bao-cao.created")
    assert report_notification is not None
    assert report_notification.get("nguoi_bao_cao_id") == payload.get("nguoi_bao_cao_id")