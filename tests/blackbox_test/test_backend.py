import pytest
import logging
import json
import requests
from src.services.favorite_post_service import FavoritePostService
from src.services.user_register import UserRegister

pytestmark = pytest.mark.backend

def test_user_register(requests_mock, db_client, cleanup_user_test):
    payload = {
        "ho_ten": "User Test",
        "email": "test@example.com",
        "mat_khau": "123",
        "so_dien_thoai": "0912345678",
        "vai_tro": "NGUOI_DUNG",
        "trang_thai": "HOAT_DONG"
    }
    headers = {"Content-Type" : "application/json"}
    hash_password = hash(payload["mat_khau"])
    user_client = UserRegister(db_client)
    user_client.register(payload, headers)
    result = user_client.search_user(payload["ho_ten"])
    cleanup_user_test.append(result[0]["id"])
    assert result is not None
    assert result[0]["email"] == payload["email"]
    assert result[0]["mat_khau_hash"] == str(hash_password)
 
def test_logic_tin_yeu_thich_khi_tin_dang_soft_delete(api_client, db_client, setup_favorite_post_test, cleanup_user_test, cleanup_favorite_post_test):
    # Create User B
    user_b_id= 99999
    query = f"""
            INSERT INTO nguoi_dung (id, ho_ten, email, mat_khau_hash, so_dien_thoai, vai_tro, trang_thai) 
            VALUES ({user_b_id}, 'SDET Test User', 'sdet_{user_b_id}@abc.com', '{hash("12345")}', '0912345678', 'NGUOI_DUNG', 'HOAT_DONG')
        """
    db_client.execute_query(query)
    cleanup_user_test.append(user_b_id)

    # User B add favorite post (post is created by user A in setup)
    payload = {
        "nguoi_dung_id": user_b_id,
        "tin_dang_id": setup_favorite_post_test["post_id"]
    }
    favor_post_client = FavoritePostService(db_client)
    add_response = favor_post_client.add_favorite_post(payload)

    # User A soft delete post
    db_client.execute_query(f"UPDATE tin_dang SET is_deleted = True WHERE id = {setup_favorite_post_test['post_id']}")
    favorite_post = db_client.execute_query(f"SELECT * FROM tin_yeu_thich WHERE nguoi_dung_id = {user_b_id} AND tin_dang_id = {setup_favorite_post_test['post_id']}")
    cleanup_favorite_post_test.append(favorite_post[0]["id"])

    get_response = favor_post_client.get_favorite_post(user_b_id)
    assert add_response["status"] == "success"
    assert favorite_post is not None
    assert len(get_response) == 0
    