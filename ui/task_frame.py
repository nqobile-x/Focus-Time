import customtkinter as ctk
from controllers.task_controller import TaskController

class TaskFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        
        self.controller = TaskController()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # List area expands

        # Header
        self.header_label = ctk.CTkLabel(self, text="Tasks", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Add Task Area
        self.add_task_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.add_task_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.add_task_frame.grid_columnconfigure(0, weight=1)

        self.task_entry = ctk.CTkEntry(self.add_task_frame, placeholder_text="New Task Title")
        self.task_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        self.add_button = ctk.CTkButton(self.add_task_frame, text="Add", width=60, command=self.add_task)
        self.add_button.grid(row=0, column=1)

        # Task List Area (Scrollable)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Your Tasks")
        self.scrollable_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.load_tasks()

    def load_tasks(self):
        # Clear existing
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tasks = self.controller.get_tasks()
        
        for i, task in enumerate(tasks):
            self.create_task_item(task, i)

    def create_task_item(self, task, index):
        item_frame = ctk.CTkFrame(self.scrollable_frame)
        item_frame.grid(row=index, column=0, padx=5, pady=5, sticky="ew")
        item_frame.grid_columnconfigure(1, weight=1)

        # Checkbox (Completion)
        check_var = ctk.BooleanVar(value=task.completed)
        checkbox = ctk.CTkCheckBox(item_frame, text="", variable=check_var, width=24,
                                   command=lambda t=task: self.toggle_task(t))
        checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Title
        title_label = ctk.CTkLabel(item_frame, text=task.title, anchor="w")
        title_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        if task.completed:
            title_label.configure(text_color="gray")

        # Delete Button
        delete_btn = ctk.CTkButton(item_frame, text="X", width=30, fg_color="firebrick",
                                   command=lambda t=task: self.delete_task(t))
        delete_btn.grid(row=0, column=2, padx=10, pady=10)

    def add_task(self):
        title = self.task_entry.get()
        if title:
            self.controller.add_task(title, "General", "Medium", 1)
            self.task_entry.delete(0, "end")
            self.load_tasks()

    def toggle_task(self, task):
        self.controller.toggle_task_completion(task.id, task.completed)
        self.load_tasks()

    def delete_task(self, task):
        self.controller.delete_task(task.id)
        self.load_tasks()
