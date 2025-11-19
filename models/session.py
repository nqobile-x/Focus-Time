import sqlite3
from database import get_db_connection
from datetime import datetime, timedelta

class Session:
    def __init__(self, id, task_id, duration, session_type, completed_at):
        self.id = id
        self.task_id = task_id
        self.duration = duration # in minutes
        self.session_type = session_type
        self.completed_at = completed_at

    @staticmethod
    def add_session(duration, session_type="Pomodoro", task_id=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Use local time explicitly to match query logic
        now = datetime.now()
        cursor.execute('''
            INSERT INTO sessions (task_id, duration, session_type, completed_at)
            VALUES (?, ?, ?, ?)
        ''', (task_id, duration, session_type, now))
        conn.commit()
        conn.close()

    @staticmethod
    def get_today_stats():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get start of today
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        cursor.execute('''
            SELECT count(*), sum(duration) 
            FROM sessions 
            WHERE completed_at >= ? AND session_type = 'Pomodoro'
        ''', (today_start,))
        
        row = cursor.fetchone()
        count = row[0] if row[0] else 0
        total_minutes = row[1] if row[1] else 0
        
        conn.close()
        return count, total_minutes

    @staticmethod
    def get_weekly_stats():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get start of 7 days ago
        week_start = datetime.now() - timedelta(days=6)
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        
        cursor.execute('''
            SELECT date(completed_at), sum(duration)
            FROM sessions
            WHERE completed_at >= ? AND session_type = 'Pomodoro'
            GROUP BY date(completed_at)
            ORDER BY date(completed_at)
        ''', (week_start,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Format for chart: {date_str: minutes}
        stats = {row[0]: row[1] for row in rows}
        return stats
