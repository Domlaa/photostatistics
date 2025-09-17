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


def save_to_mysql(data, init):
    with get_conn() as conn:
        if init or not check_table(conn):
            drop_table(conn)
            create_table(conn)
        insert_to_mysql(conn, data)
        conn.commit()
        conn.close()


def drop_table(conn):
    cursor = conn.cursor()
    sql = """
    DROP TABLE IF EXISTS %s;
    """
    cursor.execute(sql, table)
    cursor.close()


def create_table(conn):
    cursor = conn.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS %s (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    datetime_original DATETIME NULL,
    aperture FLOAT NULL,
    shutter VARCHAR(50) NULL,
    iso INT NULL,
    lens VARCHAR(255) NULL,
    focal_length INT NULL,
    filepath TEXT
    );
    """
    cursor.execute(sql, table)
    cursor.close()


def check_table(conn):
    cursor = conn.cursor()
    query = """
              SELECT COUNT(*)
              FROM information_schema.tables
              WHERE table_schema = %s AND table_name = %s
          """
    cursor.execute(query, (database, table))
    exist = cursor.fetchone()[0] > 0
    cursor.close()
    return exist


def insert_to_mysql(conn, data):
    cursor = conn.cursor()

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

    conn.commit()
    cursor.close()
    conn.close()
