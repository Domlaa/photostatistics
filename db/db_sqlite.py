import sqlite3

db_file = "photo_db.sqlite"
table = "photo_exif"


def save_to_sqlite(data, init):
    print(f"解析到 {len(data)} 张照片，正在保存到数据库...")
    conn = sqlite3.connect(db_file)
    if init or not check_table(conn):
        drop_table(conn)
        create_table(conn)
    insert_to_sqlite(conn, data)
    conn.commit()
    conn.close()


def drop_table(conn):
    cursor = conn.cursor()
    sql = f"DROP TABLE IF EXISTS {table};"
    cursor.execute(sql)
    cursor.close()


def create_table(conn):
    cursor = conn.cursor()
    # SQLite 没有 AUTO_INCREMENT，用 INTEGER PRIMARY KEY AUTOINCREMENT
    sql = f"""
    CREATE TABLE IF NOT EXISTS {table} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        md5 CHAR(32) UNIQUE,
        filename TEXT,
        model TEXT,
        datetime REAL,
        aperture REAL,
        shutter TEXT,
        iso INTEGER,
        lens TEXT,
        focal_length REAL,
        filepath TEXT
    );
    """
    cursor.execute(sql)
    cursor.close()


def check_table(conn):
    cursor = conn.cursor()
    query = """
        SELECT count(*)
        FROM sqlite_master
        WHERE type='table' AND name=?
    """
    cursor.execute(query, (table,))
    exist = cursor.fetchone()[0] > 0
    cursor.close()
    return exist


def insert_to_sqlite(conn, data):
    cursor = conn.cursor()
    fail_count = 0
    sql = f"""
        INSERT INTO {table}
        (md5, filename, model, datetime, aperture, shutter, iso, lens, focal_length, filepath)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    for row in data:
        md5 = row.get("md5")
        filename = row.get("filename")
        filepath = row.get("filepath")
        try:
            cursor.execute(sql, (
                md5,
                filename,
                row.get("model"),
                row.get("datetime"),
                row.get("aperture"),
                row.get("shutter"),
                row.get("iso"),
                row.get("lens"),
                row.get("focal_length"),
                filepath,
            ))
        except sqlite3.IntegrityError as e:
            print(f"插入失败: - {e}, md5: {md5}, name: {filepath}")
            fail_count = fail_count + 1
    cursor.close()
    print(f"fail to insert {fail_count}")