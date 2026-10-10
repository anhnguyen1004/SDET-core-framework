from fastapi import APIRouter, status

from src.exceptions.exceptions import DatabaseClientError
from src.models.db_client import PostgresDBClient

router = APIRouter()

class FavoritePostService:
    def __init__(self, db_client:PostgresDBClient):
        self.db_client = db_client

    @router.post("/api/post/add-favorite-post", status_code=status.HTTP_201_CREATED)
    def add_favorite_post(self, payload: dict):
        if self.db_client is None:
            raise DatabaseClientError("Database client is not initialized")
        user_id = payload.get("nguoi_dung_id")
        post_id = payload.get("tin_dang_id")

        if user_id is None or post_id is None:
            raise ValueError("Invalid payload")
        
        existing_post = self.db_client.execute_query(f"SELECT * FROM tin_yeu_thich WHERE nguoi_dung_id = {user_id} AND tin_dang_id = {post_id}")
        if existing_post:
            raise ValueError("Bài viết đã tồn tại trong danh sách yêu thích")

        self.db_client.execute_query(f"INSERT INTO tin_yeu_thich (nguoi_dung_id, tin_dang_id) VALUES ({user_id}, {post_id})")

        return {
            "status": "success",
            "message": "Bài viết đã được thêm vào danh sách yêu thích"
        }
    
    @router.get("api/post/favorite-post/{user_id}", status_code=status.HTTP_200_OK)
    def get_favorite_post(self, user_id: int):
        query = f"SELECT * FROM tin_yeu_thich INNER JOIN tin_dang ON tin_yeu_thich.tin_dang_id = tin_dang.id WHERE nguoi_dung_id = {user_id} and tin_dang.is_deleted = false and tin_dang.is_blocked = false"
        return self.db_client.execute_query(query)
