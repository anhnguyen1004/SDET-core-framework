import pytest
import logging

pytestmark = pytest.mark.backend

def test_verify_user_in_db(db_client):
    logging.info("Đang chạy test_verify_user_in_db")
    result = db_client.execute_query("SELECT id, email, trang_thai FROM nguoi_dung where id = 4")
    assert result is not None, "User not found!"

def test_verify_post_in_db(db_client):
    logging.info("Đang chạy test_verify_post_in_db")
    result = db_client.execute_query("SELECT * FROM tin_dang LIMIT 5")
    assert len(result) >0, "Post not found!"
