import logging

import psycopg2
from psycopg2.extras import RealDictCursor

from src.exceptions.exceptions import DatabaseClientError

logger = logging.getLogger(__name__)

class PostgresDBClient:
    def __init__(self, host, db_name, user, password, port = 5432):
        self.host = host
        self.db_name = db_name
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        if self.connection and not self.connection.closed:
            return
        logger.info(f"Dang ket noi database toi {self.db_name} tai {self.host}...")
        try:
            self.connection = psycopg2.connect(
                host = self.host,
                database = self.db_name,
                user = self.user,
                password = self.password,
                port = self.port,
                cursor_factory = RealDictCursor
            )     
            logger.info("Ket noi database thanh cong!")
        except psycopg2.Error as e:
            logger.error(f"Loi ket noi database: {e}")
            raise

    def disconnect(self):
        if self.connection:
            self.connection.close()
            logger.info("Da ngat ket noi database")

    def execute_query(self, query: str):
        if not self.connection:
            raise DatabaseClientError("Chua mo ket noi db")
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
                return result
            
            self.connection.commit()
            return None
        except psycopg2.Error as e:
            logger.error(f"Loi truy van database: {e}")
            self.connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()

        
        