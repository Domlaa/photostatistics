from typing import List, Tuple, Union

from db import db_mysql
from process.data_processor import DataProcessor


class MysqlDataProcessor(DataProcessor):

    def __init__(self):
        self.conn = db_mysql.get_conn()

    def focal_seq_10(self, time_range) -> {}:
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT
            FLOOR(focal_length/10)*10 AS focal_start,
            COUNT(*) AS usage_count
        FROM exif
        GROUP BY focal_start
        ORDER BY focal_start DESC;
        """)
        rows = cursor.fetchall()
        cursor.close()

        focal_seq_10_map = {}
        for row in rows:
            f_start = int(row['focal_start'])
            key = f"{f_start}-{f_start + 9} mm"
            focal_seq_10_map[key] = row['usage_count']
        return focal_seq_10_map

    def focal_top10(self, time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT 
                focal_length, COUNT(*) as usage_count
                from exif
            WHERE datetime_original BETWEEN %s AND %s
            GROUP BY focal_length
            ORDER BY usage_count DESC
            LIMIT 10;
            """, time_range)
            # 二维数组
            rows = cursor.fetchall()
            map = {row[0]: row[1] for row in rows}
            return map

    def total_shot(self, time_range) -> int:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM exif;")
            (total,) = cursor.fetchone()
            return total

    def shot_calendar(self, time_range) -> List[List[Union[str, int]]]:
        # start_date = time_range[0]
        # end_date = time_range[1]
        # print(f"{start_date} - {end_date}")
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT 
                DATE(datetime_original) as day,
                COUNT(*) as cnt
            FROM exif
            WHERE datetime_original BETWEEN %s AND %s
            GROUP BY DATE(datetime_original)
            ORDER BY cnt
            """, time_range)
            rows = cursor.fetchall()
            return [[str(day), int(cnt)] for day, cnt in rows]

    def lens_use_rate(self, time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    lens, 
                    COUNT(*) AS usage_count
                FROM exif
                WHERE datetime_original BETWEEN %s AND %s
                GROUP BY lens;
                  """, time_range)
            rows = cursor.fetchall()
            return [(str(name), int(cnt)) for name, cnt in rows]

    def iso_use_rate(self, time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    iso, 
                    COUNT(*) AS usage_count
                FROM exif
                WHERE datetime_original BETWEEN %s AND %s
                GROUP BY iso
                ORDER BY iso;
                """, time_range)
            rows = cursor.fetchall()
            return [(str(name), int(cnt)) for name, cnt in rows]

    def shutter_use_rate(self, time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    shutter, 
                    COUNT(*) AS usage_count
                FROM exif
                WHERE datetime_original BETWEEN %s AND %s
                GROUP BY shutter
                ORDER BY usage_count;
                """, time_range)
            rows = cursor.fetchall()
            return [(str(name), int(cnt)) for name, cnt in rows]

    def aperture_use_rate(self, time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    aperture, 
                    COUNT(*) AS usage_count
                FROM exif
                WHERE datetime_original BETWEEN %s AND %s
                GROUP BY aperture
                ORDER BY aperture;
                """, time_range)
            rows = cursor.fetchall()
            return [(str(name), int(cnt)) for name, cnt in rows]

    def shot_hour(self, time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT
                HOUR(datetime_original) AS hour,
                COUNT(*) AS usage_count
            FROM exif
            WHERE datetime_original BETWEEN %s AND %s
            GROUP BY HOUR(datetime_original)
            ORDER BY hour;
            """, time_range)
            rows = cursor.fetchall()
            map = {row[0]: row[1] for row in rows}
            return map

    def monthly_shot_times(self, time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT
                DATE_FORMAT(datetime_original, '%Y-%m') AS month,
                COUNT(*) AS photos
            FROM exif
            WHERE datetime_original BETWEEN %s AND %s
            GROUP BY DATE_FORMAT(datetime_original, '%Y-%m')
            ORDER BY month;
            """, time_range)
            rows = cursor.fetchall()
            map = {row[0]: row[1] for row in rows}
            return map


if __name__ == '__main__':
    processor = MysqlDataProcessor()
    time_range = ['2024-01-01 00:00:00', '2024-12-31 23:59:59']

    focal_seq_10_map = processor.focal_seq_10(time_range)
    shot_calendar_data = processor.shot_calendar(time_range)
    lens_use_data = processor.lens_use_rate(time_range)
    iso_use_data = processor.iso_use_rate(time_range)
    shutter_use_data = processor.shutter_use_rate(time_range)
    aperture_use_data = processor.aperture_use_rate(time_range)
    hour_data = processor.shot_hour(time_range)
    monthly_shot_times = processor.monthly_shot_times(time_range)
    focal_top10_data = processor.focal_top10(time_range)


    print()

    # statistics_data = {
    #     'days_with_photos': days_with_photos,
    #     'total_photos': total_shot,
    #     'most_active_month': most_active_month,
    #     'photos_in_most_active_month': photos_in_most_active_month,
    #     'favorite_time': favorite_time,
    #     'most_productive_date': most_productive_date,
    #     'photos_on_most_productive_day': photos_on_most_productive_day,
    #     'fav_focal_range': fav_focal_range,
    #     'most_used_focal_length': most_used_focal_length,
    #     'fav_lens': fav_lens,
    #     'photos_with_fav_lens': photos_with_fav_lens,
    #     'fav_iso': fav_iso,
    #     'fav_shutter': fav_shutter,
    #     'fav_aperture': fav_aperture,
    # }
    # print(statistics_data)
