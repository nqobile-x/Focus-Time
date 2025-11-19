import unittest
import sys
import os
import sqlite3
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.session import Session
from database import get_db_connection

class TestSessionModel(unittest.TestCase):
    def setUp(self):
        # Clean up sessions for testing
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions')
        conn.commit()
        conn.close()

    def test_add_and_get_stats(self):
        # Add a session
        Session.add_session(25, "Pomodoro")
        
        # Check today's stats
        count, minutes = Session.get_today_stats()
        self.assertEqual(count, 1)
        self.assertEqual(minutes, 25)
        
        # Add another
        Session.add_session(25, "Pomodoro")
        count, minutes = Session.get_today_stats()
        self.assertEqual(count, 2)
        self.assertEqual(minutes, 50)

    def test_weekly_stats(self):
        # Add a session for today
        Session.add_session(25, "Pomodoro")
        
        # Add a session for yesterday (manually to bypass current timestamp default)
        conn = get_db_connection()
        cursor = conn.cursor()
        yesterday = datetime.now() - timedelta(days=1)
        cursor.execute('''
            INSERT INTO sessions (duration, session_type, completed_at)
            VALUES (?, ?, ?)
        ''', (50, "Pomodoro", yesterday))
        conn.commit()
        conn.close()
        
        stats = Session.get_weekly_stats()
        self.assertEqual(len(stats), 2) # Today and Yesterday
        
        # Verify values (dates are keys, so just check values exist)
        self.assertIn(25, stats.values())
        self.assertIn(50, stats.values())

if __name__ == '__main__':
    unittest.main()
