import requests
import logging
import json

from fastapi import APIRouter, status

from src.models.db_client import PostgresDBClient
from src.models.user import User
from src.config.settings import settings

router = APIRouter()

class UserRegister:
    def __init__(self, db_client:PostgresDBClient):
        self.db_client = db_client
    
    @router.post("/api/users/register", status_code=status.HTTP_201_CREATED)
    def register(self, payload:dict, headers:dict):
        if headers.get("Content-Type") != "application/json":
            logging.error("Headers is not valid")
        user = User(
            id = None,
            ho_ten = payload["ho_ten"],
            email = payload["email"],
            so_dien_thoai = payload["so_dien_thoai"],
            mat_khau = payload["mat_khau"],
            vai_tro = payload["vai_tro"],
            trang_thai = payload["trang_thai"]
        )
        try:
            query = f"INSERT INTO public.nguoi_dung(ho_ten, email, mat_khau_hash, so_dien_thoai, vai_tro, trang_thai) VALUES('{user.ho_ten}', '{user.email}', '$2b$12$QchccORt3LztJ2OdNVoHC.EQpGYfBNl008MZoOdP7YLIBg6ky9ePC', '{user.so_dien_thoai}', '{user.vai_tro}', 'HOAT_DONG');"
            self.db_client.connect()
            result = self.db_client.execute_query(query)
        except Exception as e:
            raise ValueError(f"Error while registering user: {str(e)}")
        finally:
            self.db_client.disconnect()
        return result
    
    def search_user(self, ho_ten: str):
        query = f"SELECT * FROM public.nguoi_dung WHERE ho_ten = '{ho_ten}'"
        self.db_client.connect()
        result = self.db_client.execute_query(query)
        self.db_client.disconnect()
        return result