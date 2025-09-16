from common import const
from process.processor.data_processor import DataProcessor
import mysql.connector


class MysqlDataProcessor(DataProcessor):

    def __init__(self):
        self.conn = self.get_conn()

    def get_conn(self):
        return mysql.connector.connect(
            host=const.host,
            user=const.user,
            password=const.password,
            database=const.database
        )

    def save_to_db(self, data, init):
        with self.conn as conn:
            if init or not self.check_table():
                self.drop_table()
                self.create_table()
            self.insert_to_db(data)
            conn.commit()

    def drop_table(self):
        with self.conn.cursor() as cursor:
            sql = """
               DROP TABLE IF EXISTS %s;
               """
            cursor.execute(sql, const.table)

    def create_table(self):
        with self.conn.cursor() as cursor:
            sql = """
               CREATE TABLE IF NOT EXISTS %s (
               id INT AUTO_INCREMENT PRIMARY KEY,
               filename VARCHAR(255),
               datetime_original DATETIME NULL,
               aperture FLOAT NULL,
               shutter VARCHAR(50) NULL,
               iso INT NULL,
               lens VARCHAR(255) NULL,
               focal_length FLOAT NULL,
               filepath TEXT
               );
               """
            cursor.execute(sql, const.table)
            cursor.close()

    def check_table(self):
        with self.conn.cursor() as cursor:
            query = """
                        SELECT COUNT(*)
                        FROM information_schema.tables
                        WHERE table_schema = %s AND table_name = %s
                    """
            cursor.execute(query, (const.database, const.table))
            exist = cursor.fetchone()[0] > 0
            return exist

    def insert_to_db(self, data):
        with self.conn.cursor() as cursor:
            sql = """
                INSERT INTO %s
                (filename, datetime_original, aperture, shutter, iso, lens, focal_length, filepath)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            for row in data:
                cursor.execute(sql, (
                    const.table,
                    row["filename"],
                    row["datetime_original"],
                    row["aperture"],
                    row["shutter"],
                    row["iso"],
                    row["lens"],
                    row["focal_length"],
                    row["filepath"],
                ))
