from process.processor.data_processor import DataProcessor
import mysql.connector

host = "localhost"
user = "root"
password = "123456"
database = "photo_db"
table = "exif"

class MysqlDataProcessor(DataProcessor):

    def __init__(self):
        self.conn = self.get_conn()

    def get_conn(self):
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
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
            cursor.execute(sql, table)

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
            cursor.execute(sql, table)
            cursor.close()

    def check_table(self):
        with self.conn.cursor() as cursor:
            query = """
                        SELECT COUNT(*)
                        FROM information_schema.tables
                        WHERE table_schema = %s AND table_name = %s
                    """
            cursor.execute(query, (database, table))
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
                    table,
                    row["filename"],
                    row["datetime_original"],
                    row["aperture"],
                    row["shutter"],
                    row["iso"],
                    row["lens"],
                    row["focal_length"],
                    row["filepath"],
                ))
