import time

import psycopg2
import pytest

from src.api.base_client import BaseAPIClient
from src.config.settings import settings
from src.exceptions.exceptions import DatabaseClientError
from src.models.db_client import PostgresDBClient
from src.models.kafka_client import KafkaClient


@pytest.fixture(scope="session")
def db_client():
    client = PostgresDBClient(
        host = settings.DB_HOST,
        db_name = settings.DB_NAME,
        user = settings.DB_USER,
        password = settings.DB_PASSWORD,
        port = 5432
    )
    connection = False
    for attempt in range(10):
        try:
            client.connect()
            connection = True
            break
        except psycopg2.OperationalError as e:
            print(f"[WARNING] Lỗi kết nối DB lần {attempt + 1}: {e}")
            time.sleep(2)
    if not connection:
        raise DatabaseClientError("[FAILED] Kết nối DB thất bại!")
    try:
        yield client
    finally:
        client.disconnect()

@pytest.fixture(scope="function")
def cleanup_user_test(db_client):
    user_ids = []
    yield user_ids
    if user_ids:
        ids_str = ",".join(map(str, user_ids))
        db_client.execute_query(f"DELETE FROM nguoi_dung where id in ({ids_str})")

@pytest.fixture(scope="function")
def cleanup_favorite_post_test(db_client):
    favorite_post_ids = []
    yield favorite_post_ids
    if favorite_post_ids:
        ids_str = ",".join(map(str, favorite_post_ids))
        db_client.execute_query(f"DELETE FROM tin_yeu_thich where id in ({ids_str})")

@pytest.fixture(scope="function")
def setup_loai_bat_dong_san(db_client):
    loai_bds_id = 9999
    try:
        db_client.execute_query(
            f"""
            INSERT INTO loai_bat_dong_san
(id, ten, mo_ta, trang_thai)
VALUES({loai_bds_id}, 'Phòng trọ test', 'Phòng cho thuê trong nhà trọ, khép kín hoặc chung chủ', 'HOAT_DONG');"""
        )
    except psycopg2.Error as e:
        print(f"Lỗi khi setup data loai_bat_dong_san: {e}")

    yield loai_bds_id

    try:
        db_client.execute_query(f"DELETE FROM loai_bat_dong_san WHERE id = {loai_bds_id}")
    except psycopg2.Error:
        pass

@pytest.fixture(scope="function")
def setup_quan_huyen_and_tinh_thanh(db_client):
    quan_huyen_id = 9999
    tinh_thanh_id =9998
    try:
        db_client.execute_query(
            f"INSERT INTO tinh_thanh(id, ten)VALUES({tinh_thanh_id}, 'Thành phố Test') ON CONFLICT (id) DO NOTHING"
        )
        db_client.execute_query(
            f"INSERT INTO quan_huyen(id, ten, tinh_thanh_id)VALUES({quan_huyen_id}, 'Quận Ba Đình Test', {tinh_thanh_id}) ON CONFLICT (id) DO NOTHING"
        )
    except psycopg2.Error as e:
        print(f"Lỗi khi setup data quan_huyen: {e}")

    yield quan_huyen_id

    try:
        db_client.execute_query(f"DELETE FROM quan_huyen WHERE id = {quan_huyen_id}")
    except psycopg2.Error:
        pass

@pytest.fixture(scope="function")
def setup_phuong_xa(db_client, setup_quan_huyen_and_tinh_thanh):
    phuong_xa_id = 9999
    quan_huyen_id = setup_quan_huyen_and_tinh_thanh
    try:
        db_client.execute_query(
            f"INSERT INTO phuong_xa(id, ten, quan_huyen_id, ma_hanh_chinh)VALUES({phuong_xa_id}, 'Phường Phúc Xá Test', {quan_huyen_id}, '9990');"
        )
    except psycopg2.Error as e:
        print(f"Lỗi khi setup data phuong_xa: {e}")

    yield phuong_xa_id

    try:
        db_client.execute_query(f"DELETE FROM phuong_xa WHERE id = {phuong_xa_id}")
    except psycopg2.Error:
        pass
@pytest.fixture(scope="function")
def setup_user_test(db_client):
    test_user_id = 99991
    hash_password = hash("12345")
    try:
        query_insert_user = f"""
            INSERT INTO nguoi_dung (id, ho_ten, email, mat_khau_hash, so_dien_thoai, vai_tro, trang_thai) 
            VALUES ({test_user_id}, 'SDET Test User', 'sdet_{test_user_id}@abc.com', '{hash_password}', '0912345678', 'NGUOI_DUNG', 'HOAT_DONG')
        """
        db_client.execute_query(query_insert_user)
        yield test_user_id
    finally:
        db_client.execute_query(f"DELETE FROM nguoi_dung where id = {test_user_id}")

@pytest.fixture(scope="function")   
def setup_user_and_post_test(db_client, setup_loai_bat_dong_san, setup_phuong_xa):
    test_user_id = 99991
    test_tin_dang_id = 88881
    hash_password = hash("12345")
    test_loai_bds_id = setup_loai_bat_dong_san
    test_phuong_xa_id = setup_phuong_xa
    try:
        query_insert_user = f"""
            INSERT INTO nguoi_dung (id, ho_ten, email, mat_khau_hash, so_dien_thoai, vai_tro, trang_thai) 
            VALUES ({test_user_id}, 'SDET Test User', 'sdet_{test_user_id}@abc.com', '{hash_password}', '0912345678', 'NGUOI_DUNG', 'HOAT_DONG')
        """
        query_insert_tin_dang = f"""
            INSERT INTO public.tin_dang
            (id, tieu_de, mo_ta, gia_thue, dien_tich, dia_chi_chi_tiet, loai_bat_dong_san_id, phuong_xa_id, nguoi_dang_id, ten_nguoi_lien_he, so_dien_thoai_lien_he, phuong_thuc_lien_he_uu_tien, trang_thai, ly_do_khoa, luot_xem, ngay_dang, ngay_cap_nhat, phong_ngu, phong_tam, is_blocked, is_deleted, deleted_at)
            VALUES({test_tin_dang_id}, 'Căn hộ cho thuê tại Phường 10 #7', 'Căn hộ rộng 39m², vị trí Phường 10, gần chợ và trường học, thích hợp cho người đi làm hoặc sinh viên.', 13700000.00, 39.00, 'Số 156 đường Phường 10', {test_loai_bds_id}, {test_phuong_xa_id}, {test_user_id}, 'Nguyễn Minh Anh', '0912345673', 'GOI_DIEN', 'DA_DUYET', NULL, 2, '2026-09-09 22:48:09.668', '2026-09-09 22:50:00.959', 0, 0, false, false, NULL);"""
        db_client.execute_query(query_insert_user)
        db_client.execute_query(query_insert_tin_dang)

        yield {
            "user_id": test_user_id,
            "post_id": test_tin_dang_id
        }
    
    finally:
        db_client.execute_query(f"DELETE FROM tin_dang where id = {test_tin_dang_id}")
        db_client.execute_query(f"DELETE FROM nguoi_dung where id = {test_user_id}")

@pytest.fixture(scope="function")
def cleanup_report(db_client, setup_user_and_post_test):
    nguoi_bao_cao_id = setup_user_and_post_test["user_id"]
    tin_dang_id = setup_user_and_post_test["post_id"]
    yield
    db_client.execute_query(f"DELETE FROM public.bao_cao WHERE nguoi_bao_cao_id={nguoi_bao_cao_id} AND tin_dang_id={tin_dang_id};")

@pytest.fixture(scope="function")
def purge_topic(kafka_client):
    def _purge(topic: str):
        kafka_client.consumer.subscribe([topic])
        # Drain all existing messages until no more arrive within 2s
        while kafka_client.consumer.poll(timeout=2.0) is not None:
            pass
    return _purge

@pytest.fixture(scope="session")
def api_client():
    api_client = BaseAPIClient(base_url="https://jsonplaceholder.typicode.com")
    return api_client

@pytest.fixture(scope="session")
def kafka_client():
    kafka_client = KafkaClient()
    yield kafka_client
    kafka_client.close()