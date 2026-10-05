import pytest
import logging
import json
import requests
from src.services.user_register import UserRegister

pytestmark = pytest.mark.backend

def test_verify_user_in_db(db_client):
    logging.info("Đang chạy test_verify_user_in_db")
    result = db_client.execute_query("SELECT id, email, trang_thai FROM nguoi_dung where id = 4")
    assert result is not None, "User not found!"

def test_verify_post_in_db(db_client):
    logging.info("Đang chạy test_verify_post_in_db")
    result = db_client.execute_query("SELECT * FROM tin_dang LIMIT 5")
    assert len(result) >0, "Post not found!"

def test_user_register(db_client, cleanup_user_test):
    payload = {
        "ho_ten": "User Test",
        "email": "test@example.com",
        "mat_khau": "123",
        "so_dien_thoai": "0912345678",
        "vai_tro": "NGUOI_DUNG",
        "trang_thai": "HOAT_DONG"
    }
    headers = {"Content-Type" : "application/json"}
 
    user_client = UserRegister()
    user_client.register(payload, headers)
    result = user_client.search_user(payload["ho_ten"])
    cleanup_user_test.append(result[0]["id"])
    assert result is not None
    assert result[0]["email"] == payload["email"]
