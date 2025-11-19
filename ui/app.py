import customtkinter as ctk
from ui.timer_frame import TimerFrame
from ui.task_frame import TaskFrame
from ui.stats_frame import StatsFrame

class TimeManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Focus Timer")
        self.geometry("900x600")
        
        # Configure grid layout (1x2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create Navigation Frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="Focus App",
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # User Profile (Gamification)
        self.profile_frame = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        self.profile_frame.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="ew")
        
        self.level_label = ctk.CTkLabel(self.profile_frame, text="Level 1", font=ctk.CTkFont(size=12, weight="bold"))
        self.level_label.pack(anchor="w", padx=10)
        
        self.xp_bar = ctk.CTkProgressBar(self.profile_frame, height=8)
        self.xp_bar.pack(fill="x", padx=10, pady=5)
        self.xp_bar.set(0)
        
        self.xp_label = ctk.CTkLabel(self.profile_frame, text="0 / 500 XP", font=ctk.CTkFont(size=10))
        self.xp_label.pack(anchor="e", padx=10)
        
        self.update_profile()

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Timer",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=2, column=0, sticky="ew")

        self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Tasks",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=3, column=0, sticky="ew")
        
        self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Stats",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=4, column=0, sticky="ew")

        # Create Main Frames
        self.timer_frame = TimerFrame(self)
        self.task_frame = TaskFrame(self)
        self.stats_frame = StatsFrame(self)
        
        # Select default frame
        self.select_frame_by_name("home")

    def update_profile(self):
        from models.gamification import Gamification
        level, current_xp, next_level_xp, progress = Gamification.get_level_info()
        
        self.level_label.configure(text=f"Level {level}")
        self.xp_bar.set(progress)
        self.xp_label.configure(text=f"{current_xp} / {next_level_xp} XP")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.timer_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.timer_frame.grid_forget()
        
        if name == "frame_2":
            self.task_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.task_frame.grid_forget()
            
        if name == "frame_3":
            self.stats_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.stats_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")
        
    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
