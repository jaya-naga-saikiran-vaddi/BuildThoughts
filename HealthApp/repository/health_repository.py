from datetime import datetime

import MySQLdb

from config.logger_config import setup_logger
from db import mysql

logger = setup_logger("MainRunner")


class HealthRepository:

    def validateDate(self, log_date):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM health_logs WHERE log_date = %s", (log_date,))
        return cursor.fetchone()

    def saveHealthInfo(self, data):
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO health_logs (log_date, water_liters, sleep_hours, steps_walked, calories, mood)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['log_date'], data['water_liters'], data['sleep_hours'],
              data['steps_walked'], data['calories'], data['mood']))
        mysql.connection.commit()
        cur.close()

    def fetch_all_health_info(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM health_logs")
        rows = cur.fetchall()
        cur.close()
        return [{
            'id': row[0], 'log_date': str(row[1]), 'water_liters': row[2],
            'sleep_hours': row[3], 'steps_walked': row[4],
            'calories': row[5], 'mood': row[6]
        } for row in rows]

    def fetch_health_info_by_date(self, date):
        # Validate date format (assuming 'YYYY-MM-DD')
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            # Invalid date format, return None or handle error as you like
            return None

        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM health_logs WHERE log_date=%s", (date,))
            row = cur.fetchone()
        finally:
            cur.close()

        if row:
            return {
                'id': row[0],
                'log_date': str(row[1]),
                'water_liters': row[2],
                'sleep_hours': row[3],
                'steps_walked': row[4],
                'calories': row[5],
                'mood': row[6]
            }
        return None

    def update_health_info(self, date, data):
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE health_logs 
            SET water_liters=%s, sleep_hours=%s, steps_walked=%s, calories=%s, mood=%s 
            WHERE log_date=%s
        """, (data['water_liters'], data['sleep_hours'], data['steps_walked'],
              data['calories'], data['mood'], date))
        mysql.connection.commit()
        cur.close()

    def delete_health_info(self, date):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM health_logs WHERE log_date=%s", (date,))
        mysql.connection.commit()
        cur.close()

    def fetchLast5DaysSummary(self):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT log_date,AVG(water_liters) AS avg_water,AVG(sleep_hours) AS avg_sleep,AVG(steps_walked) AS avg_steps,
                AVG(calories) AS avg_calories FROM health_logs GROUP BY log_date ORDER BY log_date DESC LIMIT 5
        """)
        result = cursor.fetchall()
        cursor.close()

        return result[::-1]
