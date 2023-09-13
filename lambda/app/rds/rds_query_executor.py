import pymysql
from typing import Dict, Any
from config import RDSConfig

class RDSQueryExecutor:
    def __init__(self, config: RDSConfig):
        self.config = config

    def execute_query(self) -> Dict[str, Any]:
        connection = pymysql.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.username,
            password=self.config.password,
            db=self.config.database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(self.config.query)
                result = cursor.fetchall()
        finally:
            connection.close()
            
        return result
