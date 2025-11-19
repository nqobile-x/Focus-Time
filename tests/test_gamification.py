import unittest
import sys
import os
import sqlite3

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.gamification import Gamification
from models.session import Session
from database import get_db_connection

class TestGamification(unittest.TestCase):
    def setUp(self):
        # Clean up sessions
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions')
        conn.commit()
        conn.close()

    def test_xp_calculation(self):
        # 0 XP initially
        self.assertEqual(Gamification.get_total_xp(), 0)
        
        # Add 25 min session -> 250 XP
        Session.add_session(25, "Pomodoro")
        self.assertEqual(Gamification.get_total_xp(), 250)
        
        # Add another -> 500 XP
        Session.add_session(25, "Pomodoro")
        self.assertEqual(Gamification.get_total_xp(), 500)

    def test_level_calculation(self):
        # Level 1: 0 XP
        level, _, _, _ = Gamification.get_level_info()
        self.assertEqual(level, 1)
        
        # Level 1: 250 XP
        Session.add_session(25, "Pomodoro")
        level, _, _, _ = Gamification.get_level_info()
        self.assertEqual(level, 1)
        
        # Level 2: 500 XP
        Session.add_session(25, "Pomodoro")
        level, _, _, _ = Gamification.get_level_info()
        self.assertEqual(level, 2)
        
        # Level 3: 1000 XP
        Session.add_session(50, "Pomodoro") # Total 500 + 500 = 1000
        level, _, _, _ = Gamification.get_level_info()
        self.assertEqual(level, 3)

    def test_check_level_up(self):
        # 0 -> 250 XP (No Level Up)
        leveled_up, new_level = Gamification.check_level_up(0) # Checking if 250 triggers level up from 0? 
        # Wait, check_level_up takes "previous_xp". 
        # If we have 0 XP in DB, and we pass 0, it calculates current (0) vs old (0).
        
        # Let's simulate the flow:
        # 1. User has 490 XP (Level 1)
        # 2. User finishes 1 min session (+10 XP) -> Total 500 XP (Level 2)
        
        # Mock DB state for "Current"
        Session.add_session(50, "Pomodoro") # 500 XP
        
        # Check if going from 490 to 500 triggers level up
        leveled_up, new_level = Gamification.check_level_up(490)
        self.assertTrue(leveled_up)
        self.assertEqual(new_level, 2)
        
        # Check if going from 250 to 500 triggers level up
        leveled_up, new_level = Gamification.check_level_up(250)
        self.assertTrue(leveled_up)
        
        # Check if going from 500 to 510 triggers level up (No)
        Session.add_session(1, "Pomodoro") # 510 XP
        leveled_up, new_level = Gamification.check_level_up(500)
        self.assertFalse(leveled_up)

if __name__ == '__main__':
    unittest.main()
