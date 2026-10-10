from unittest.mock import patch

import pytest

from src.services.user_register import UserRegister

pytestmark = pytest.mark.component

def test_user_register_return_error_when_db_failure(requests_mock, db_client, cleanup_user_test):
    payload = {
        "ho_ten": "User Test",
        "email": "test@example.com",
        "mat_khau": "123",
        "so_dien_thoai": "0912345678",
        "vai_tro": "NGUOI_DUNG",
        "trang_thai": "HOAT_DONG"
    }
    headers = {"Content-Type" : "application/json"}

    err = Exception("Database connection failed")
    with patch.object(db_client, "execute_query", side_effect=err):
        user_client = UserRegister(db_client=db_client)
        with pytest.raises(ValueError) as ex:
            user_client.register(payload, headers)
    assert "Error while registering user" in str(ex.value)


    
    