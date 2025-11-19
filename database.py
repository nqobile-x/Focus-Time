import sqlite3
import os

DB_NAME = "timemanagement.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    if not os.path.exists(DB_NAME):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create Tasks Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                priority TEXT,
                estimated_pomodoros INTEGER DEFAULT 1,
                completed BOOLEAN DEFAULT 0,
                due_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Sessions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                duration INTEGER,
                session_type TEXT,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        ''')
        
        # Create Settings Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_duration INTEGER DEFAULT 25,
                short_break INTEGER DEFAULT 5,
                long_break INTEGER DEFAULT 15,
                theme TEXT DEFAULT 'System',
                sound_enabled BOOLEAN DEFAULT 1
            )
        ''')
        
        # Insert default settings if not exists
        cursor.execute('SELECT count(*) FROM settings')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO settings (work_duration, short_break, long_break) VALUES (25, 5, 15)')
            
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
