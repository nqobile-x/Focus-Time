import math
from models.session import Session
from database import get_db_connection

class Gamification:
    XP_PER_MINUTE = 10
    XP_PER_LEVEL = 500

    @staticmethod
    def get_total_xp():
        """Calculates total XP based on total focus time."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT sum(duration) FROM sessions WHERE session_type = 'Pomodoro'")
        row = cursor.fetchone()
        total_minutes = row[0] if row[0] else 0
        conn.close()
        
        return total_minutes * Gamification.XP_PER_MINUTE

    @staticmethod
    def get_level_info():
        """Returns (current_level, current_xp, xp_for_next_level, progress_percent)"""
        total_xp = Gamification.get_total_xp()
        
        # Level Formula: 1 + (Total XP // 500)
        level = 1 + (total_xp // Gamification.XP_PER_LEVEL)
        
        # XP Progress within current level
        current_level_xp = total_xp % Gamification.XP_PER_LEVEL
        
        progress = current_level_xp / Gamification.XP_PER_LEVEL
        
        return level, current_level_xp, Gamification.XP_PER_LEVEL, progress

    @staticmethod
    def check_level_up(previous_xp):
        """Checks if the new XP total has crossed a level threshold."""
        current_xp = Gamification.get_total_xp()
        
        old_level = 1 + (previous_xp // Gamification.XP_PER_LEVEL)
        new_level = 1 + (current_xp // Gamification.XP_PER_LEVEL)
        
        return new_level > old_level, new_level
