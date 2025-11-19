import unittest
import sys
import os
import sqlite3

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.task import Task
from database import DB_NAME

class TestTaskModel(unittest.TestCase):
    def setUp(self):
        # Use a test database or ensure we clean up
        # For simplicity, we'll use the main DB but clean up created tasks
        self.created_ids = []

    def tearDown(self):
        for task_id in self.created_ids:
            Task.delete_task(task_id)

    def test_add_and_get_task(self):
        Task.add_task("Test Task", "General", "High", 2)
        tasks = Task.get_all_tasks()
        
        # Find our task
        found = False
        for task in tasks:
            if task.title == "Test Task":
                found = True
                self.created_ids.append(task.id)
                self.assertEqual(task.priority, "High")
                break
        
        self.assertTrue(found)

    def test_toggle_complete(self):
        Task.add_task("Task to Complete")
        tasks = Task.get_all_tasks()
        task = next(t for t in tasks if t.title == "Task to Complete")
        self.created_ids.append(task.id)
        
        self.assertFalse(task.completed)
        
        new_status = Task.toggle_complete(task.id, task.completed)
        self.assertTrue(new_status)
        
        # Verify in DB
        tasks = Task.get_all_tasks()
        task = next(t for t in tasks if t.id == task.id)
        self.assertTrue(task.completed)

if __name__ == '__main__':
    unittest.main()
