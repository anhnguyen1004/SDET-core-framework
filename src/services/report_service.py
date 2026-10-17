import logging

from confluent_kafka import KafkaException

from src.config.settings import settings
from src.models.db_client import PostgresDBClient
from src.models.kafka_client import KafkaClient

logger = logging.getLogger(__name__)
DLQ_TOPIC = settings.DLQ_TOPIC

class ReportService:
    def __init__(self, db_client:PostgresDBClient, kafka_client:KafkaClient):
        self.db_client = db_client
        self.kafka_client = kafka_client

    def save_report(self, topic: str):
        try:
            msg, key = self.kafka_client.consume(topic=topic)
            tin_dang_id = msg.get("tin_dang_id")
            nguoi_bao_cao_id = msg.get("nguoi_bao_cao_id")
            ly_do = msg.get("ly_do")
            mo_ta = msg.get("mo_ta")
            trang_thai = msg.get("trang_thai")
            nguoi_xu_ly_id = msg.get("nguoi_xu_ly_id")
            ngay_bao_cao = msg.get("ngay_bao_cao")
            ngay_xu_ly = msg.get("ngay_xu_ly")
            ghi_chu_xu_ly = msg.get("ghi_chu_xu_ly")

            existing_report = self.get_report(tin_dang_id=tin_dang_id, nguoi_bao_cao_id=nguoi_bao_cao_id)
            if existing_report:
                logger.warning(f"Duplicate report for post {tin_dang_id} and user {nguoi_bao_cao_id}") 
                return None

            query = f"""
                INSERT INTO public.bao_cao
                (tin_dang_id, nguoi_bao_cao_id, ly_do, mo_ta, trang_thai, nguoi_xu_ly_id, ngay_bao_cao, ngay_xu_ly, ghi_chu_xu_ly)
                VALUES({tin_dang_id}, {nguoi_bao_cao_id}, '{ly_do}', '{mo_ta}', '{trang_thai}', {nguoi_xu_ly_id}, '{ngay_bao_cao}', '{ngay_xu_ly}', '{ghi_chu_xu_ly}');
            """
            result = self.db_client.execute_query(query)
            return result
        except KafkaException as e:
            logger.error(f"Failed to parse message: {e}, sending to DLQ")
            self.kafka_client.produce(DLQ_TOPIC, data=msg, key=key)
            return None
        except Exception as e:  # noqa: BLE001
            logger.error(f"Failed to process report: {e}, sending to DLQ")
            self.kafka_client.produce(DLQ_TOPIC, data=msg, key=key)
            return None
    
    def get_report(self, tin_dang_id: int, nguoi_bao_cao_id: int):
        query = f"""
            SELECT *
            FROM public.bao_cao
            WHERE tin_dang_id={tin_dang_id} AND nguoi_bao_cao_id={nguoi_bao_cao_id};
        """
        result = self.db_client.execute_query(query)
        return result