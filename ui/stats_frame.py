import customtkinter as ctk
from models.session import Session
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class StatsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(self, text="Statistics", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Summary Cards
        self.summary_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.summary_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.summary_frame.grid_columnconfigure((0, 1), weight=1)

        self.today_card = self.create_card(self.summary_frame, "Today's Focus", "0 min")
        self.today_card.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        self.count_card = self.create_card(self.summary_frame, "Sessions Completed", "0")
        self.count_card.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # Chart Area
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        # Refresh Button
        self.refresh_button = ctk.CTkButton(self, text="Refresh Stats", command=self.load_stats)
        self.refresh_button.grid(row=3, column=0, padx=20, pady=20)

        self.load_stats()

    def create_card(self, parent, title, value):
        frame = ctk.CTkFrame(parent)
        
        title_label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14))
        title_label.pack(padx=10, pady=(10, 0))
        
        value_label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=24, weight="bold"))
        value_label.pack(padx=10, pady=(0, 10))
        
        # Store reference to update later
        frame.value_label = value_label
        return frame

    def load_stats(self):
        # Get data
        count, total_minutes = Session.get_today_stats()
        
        # Update cards
        self.today_card.value_label.configure(text=f"{total_minutes} min")
        self.count_card.value_label.configure(text=str(count))
        
        # Update Chart
        self.update_chart()

    def update_chart(self):
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        stats = Session.get_weekly_stats()
        dates = list(stats.keys())
        minutes = list(stats.values())
        
        if not dates:
            label = ctk.CTkLabel(self.chart_frame, text="No data for this week yet.")
            label.pack(expand=True)
            return

        # Create Figure
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot
        ax.bar(dates, minutes, color="#3B8ED0")
        ax.set_title("Last 7 Days Focus Time")
        ax.set_ylabel("Minutes")
        ax.tick_params(axis='x', rotation=45)
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
