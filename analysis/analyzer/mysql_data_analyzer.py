from datetime import datetime
from typing import List, Union

import mysql.connector

from analysis.analyzer.data_analyzer import DataAnalyzer
from common import const


class MysqlDataAnalyzer(DataAnalyzer):

    def __init__(self):
        self.conn = self.get_conn()

    def get_conn(self):
        return mysql.connector.connect(
            host=const.host,
            user=const.user,
            password=const.password,
            database=const.database
        )

    def focal_seq_10(self, _time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
            SELECT
                FLOOR(focal_length/10)*10 AS focal_start,
                COUNT(*) AS usage_count
            FROM {const.table}
            WHERE datetime_original BETWEEN %s AND %s
            GROUP BY focal_start
            ORDER BY focal_start DESC;
            """, _time_range)
            rows = cursor.fetchall()
            _map = {}
            for row in rows:
                f_start = int(row[0])
                key = f"{f_start}-{f_start + 9} mm"
                _map[key] = row[1]
            return _map

    def focal_top10(self, _time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
            SELECT 
                focal_length, 
                COUNT(*) AS usage_count
            FROM {const.table}
            WHERE datetime_original BETWEEN %s AND %s
            GROUP BY focal_length
            ORDER BY usage_count DESC
            LIMIT 10;
            """, _time_range)
            # 二维数组
            rows = cursor.fetchall()
            _map = {row[0]: row[1] for row in rows}
            return _map

    def total_shot(self, _time_range) -> int:
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
            SELECT 
                COUNT(*) 
            FROM {const.table}
            WHERE datetime_original BETWEEN %s AND %s;
            """, _time_range)
            (total,) = cursor.fetchone()
            return total

    def shot_calendar(self, _time_range) -> List[List[Union[str, int]]]:
        # start_date = time_range[0]
        # end_date = time_range[1]
        # print(f"{start_date} - {end_date}")
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
            SELECT 
                DATE(datetime_original) as day,
                COUNT(*) as cnt
            FROM {const.table}
            WHERE datetime_original BETWEEN %s AND %s
            GROUP BY DATE(datetime_original)
            ORDER BY cnt
            """, _time_range)
            rows = cursor.fetchall()
            return [[str(day), int(cnt)] for day, cnt in rows]

    def lens_use_rate(self, _time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT 
                    lens, 
                    COUNT(*) AS usage_count
                FROM {const.table}
                WHERE datetime_original BETWEEN %s AND %s
                GROUP BY lens;
                  """, _time_range)
            rows = cursor.fetchall()
            return [(str(name), int(cnt)) for name, cnt in rows]

    def iso_use_rate(self, _time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT 
                    iso, 
                    COUNT(*) AS usage_count
                FROM {const.table}
                WHERE datetime_original BETWEEN %s AND %s
                GROUP BY iso
                ORDER BY iso;
                """, _time_range)
            rows = cursor.fetchall()
            return [(str(name), int(cnt)) for name, cnt in rows]

    def shutter_use_rate(self, _time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT 
                    shutter, 
                    COUNT(*) AS usage_count
                FROM {const.table}
                WHERE datetime_original BETWEEN %s AND %s
                GROUP BY shutter
                ORDER BY usage_count;
                """, _time_range)
            rows = cursor.fetchall()
            return [(str(name), int(cnt)) for name, cnt in rows]

    def aperture_use_rate(self, _time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT 
                    aperture, 
                    COUNT(*) AS usage_count
                FROM {const.table}
                WHERE datetime_original BETWEEN %s AND %s
                GROUP BY aperture
                ORDER BY aperture;
                """, _time_range)
            rows = cursor.fetchall()
            return [(str(name), int(cnt)) for name, cnt in rows]

    def shot_hour(self, _time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
            SELECT
                HOUR(datetime_original) AS hour,
                COUNT(*) AS usage_count
            FROM {const.table}
            WHERE datetime_original BETWEEN %s AND %s
            GROUP BY HOUR(datetime_original)
            ORDER BY hour;
            """, _time_range)
            rows = cursor.fetchall()
            _map = {row[0]: row[1] for row in rows}
            return _map

    def monthly_shot_times(self, _time_range) -> {}:
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
            SELECT
                DATE_FORMAT(datetime_original, '%Y-%m') AS month,
                COUNT(*) AS photos
            FROM {const.table}
            WHERE datetime_original BETWEEN %s AND %s
            GROUP BY DATE_FORMAT(datetime_original, '%Y-%m')
            ORDER BY month;
            """, _time_range)
            rows = cursor.fetchall()
            _map = {row[0]: row[1] for row in rows}
            return _map


if __name__ == '__main__':
    analyzer = MysqlDataAnalyzer()

    time_range = ['2025-01-01 00:00:00', '2025-12-31 23:59:59']
    s_dt = datetime.strptime(time_range[0], "%Y-%m-%d %H:%M:%S")
    e_dt = datetime.strptime(time_range[1], "%Y-%m-%d %H:%M:%S")
    start_year = s_dt.year
    end_year = e_dt.year

    focal_seq_10_map = analyzer.focal_seq_10(time_range)
    shot_calendar_data = analyzer.shot_calendar(time_range)
    lens_use_data = analyzer.lens_use_rate(time_range)
    iso_use_data = analyzer.iso_use_rate(time_range)
    shutter_use_data = analyzer.shutter_use_rate(time_range)
    aperture_use_data = analyzer.aperture_use_rate(time_range)
    hour_data = analyzer.shot_hour(time_range)
    monthly_shot_times = analyzer.monthly_shot_times(time_range)
    focal_top10_data = analyzer.focal_top10(time_range)

    total_shot = analyzer.total_shot(time_range)
    # 找到 value 最大的那一项
    most_productive = max(shot_calendar_data, key=lambda x: x[1])
    fav_focal_range = max(focal_seq_10_map.items(), key=lambda x: x[1])
    # map 里的子项中，某个最大的key/value
    most_used_focal_length_t = max(focal_top10_data.items(), key=lambda x: x[1])
    fav_lens = max(lens_use_data, key=lambda x: x[1])
    fav_iso = max(iso_use_data, key=lambda x: x[1])
    fav_shutter = max(shutter_use_data, key=lambda x:x[1])
    fav_aperture = max(aperture_use_data, key=lambda x:x[1])

    statistics_data = {
        'days_with_photos': len(shot_calendar_data),
        'total_photos': total_shot,
        'most_active_month': max(monthly_shot_times, key=monthly_shot_times.get),
        'photos_in_most_active_month': max(monthly_shot_times.values()),
        'favorite_time': max(hour_data, key=hour_data.get),
        'most_productive_date': most_productive[0],
        'photos_on_most_productive_day': most_productive[1],
        'fav_focal_range': fav_focal_range[0],
        'most_used_focal_length': int(most_used_focal_length_t[0]),
        'fav_lens': fav_lens[0],
        'photos_with_fav_lens': fav_lens[1],
        'fav_iso': fav_iso[0],
        'fav_shutter': fav_shutter[0],
        'fav_aperture': fav_aperture[0],
    }
    print(focal_seq_10_map)
