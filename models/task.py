import sqlite3
from database import get_db_connection

class Task:
    def __init__(self, id, title, description, category, priority, estimated_pomodoros, completed, due_date, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.estimated_pomodoros = estimated_pomodoros
        self.completed = completed
        self.due_date = due_date
        self.created_at = created_at

    @staticmethod
    def get_all_tasks():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [Task(**dict(row)) for row in rows]

    @staticmethod
    def add_task(title, category="General", priority="Medium", estimated_pomodoros=1):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, category, priority, estimated_pomodoros)
            VALUES (?, ?, ?, ?)
        ''', (title, category, priority, estimated_pomodoros))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_task(task_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def toggle_complete(task_id, current_status):
        conn = get_db_connection()
        cursor = conn.cursor()
        new_status = not current_status
        cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (new_status, task_id))
        conn.commit()
        conn.close()
        return new_status
