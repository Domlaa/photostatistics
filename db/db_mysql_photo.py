import mysql.connector

host = "localhost"
user = "root"
password = "123456"
database = "photo_db"
table = "photo_exif"


def get_cursor():
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn.cursor()

def focal_seq_10(cursor, time_range):
    cursor.execute("""
    SELECT FLOOR(focal_length / 10) * 10 AS focal_group, COUNT(*) AS freq
    FROM photos
    GROUP BY focal_group
    ORDER BY focal_group;
    """)
    rows = cursor.fetchall()



