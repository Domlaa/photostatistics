import mysql.connector

host = "localhost"
user = "root"
password = "123456"
database = "photo_db"
table = "exif"


def get_conn():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    # return conn.cursor(dictionary=True)

# 10mm一组，最喜欢用的焦段
def focal_seq_10(cursor, time_range):
    cursor.execute("""
    SELECT
        FLOOR(focal_length/10)*10 AS focal_start,
        COUNT(*) AS usage_count
    FROM exif
    GROUP BY focal_start
    ORDER BY focal_start DESC;
    """)
    rows = cursor.fetchall()
    # cursor.close()
    return rows


if __name__ == '__main__':
    with get_conn()  as conn:
        cursor = conn.cursor(dictionary=True)
        focal_seq_10_data = focal_seq_10(cursor, None)
        print(f"find data {focal_seq_10_data}")



