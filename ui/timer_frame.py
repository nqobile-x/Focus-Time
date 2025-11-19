import customtkinter as ctk
from controllers.timer_controller import TimerController
import tkinter.messagebox

class TimerFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        
        self.controller = TimerController(self.update_timer_display, self.on_timer_finish)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(self, text="Pomodoro Timer", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=20)

        # Timer Display
        self.timer_label = ctk.CTkLabel(self, text="25:00", font=ctk.CTkFont(size=80, weight="bold"))
        self.timer_label.grid(row=1, column=0, padx=20, pady=20)
        
        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.grid(row=2, column=0, padx=20, pady=20)
        self.progress_bar.set(1.0)

        # Controls
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, padx=20, pady=20)

        self.start_button = ctk.CTkButton(self.button_frame, text="Start", command=self.start_timer, width=100)
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = ctk.CTkButton(self.button_frame, text="Pause", command=self.pause_timer, width=100, state="disabled")
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", command=self.reset_timer, width=100, fg_color="firebrick")
        self.reset_button.grid(row=0, column=2, padx=10)
        
        # Mode Selection
        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.grid(row=4, column=0, padx=20, pady=20)
        
        self.mode_var = ctk.StringVar(value="Pomodoro")
        self.pomodoro_radio = ctk.CTkRadioButton(self.mode_frame, text="Pomodoro", variable=self.mode_var, value="Pomodoro", command=self.change_mode)
        self.pomodoro_radio.grid(row=0, column=0, padx=10)
        
        self.short_break_radio = ctk.CTkRadioButton(self.mode_frame, text="Short Break", variable=self.mode_var, value="Short Break", command=self.change_mode)
        self.short_break_radio.grid(row=0, column=1, padx=10)
        
        self.long_break_radio = ctk.CTkRadioButton(self.mode_frame, text="Long Break", variable=self.mode_var, value="Long Break", command=self.change_mode)
        self.long_break_radio.grid(row=0, column=2, padx=10)

        self.current_duration = 25 # Default

    def start_timer(self):
        self.controller.start_timer(self.current_duration)
        self.start_button.configure(state="disabled")
        self.pause_button.configure(state="normal")
        
    def pause_timer(self):
        self.controller.pause_timer()
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled")
        
    def reset_timer(self):
        self.controller.reset_timer()
        self.update_timer_display(0, 0) # Reset display
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled")
        self.change_mode() # Reset to current mode default

    def update_timer_display(self, remaining, total):
        minutes = remaining // 60
        seconds = remaining % 60
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
        
        if total > 0:
            progress = remaining / total
            self.progress_bar.set(progress)
        else:
            self.progress_bar.set(1.0)

    def on_timer_finish(self):
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled")
        self.progress_bar.set(0.0)
        
        # Save Session & Gamification
        from models.session import Session
        from models.gamification import Gamification
        
        if self.mode_var.get() == "Pomodoro":
             # 1. Save Session
             Session.add_session(self.current_duration, "Pomodoro")
             
             # 2. Calculate XP (Before update)
             previous_xp = Gamification.get_total_xp() - (self.current_duration * Gamification.XP_PER_MINUTE)
             # Note: get_total_xp reads from DB, so it already includes the session we just added. 
             # Actually, let's just get the previous total by subtracting.
             # Wait, get_total_xp queries the DB. We just added the session. So get_total_xp NOW includes the new points.
             # To check level up, we need the OLD total. 
             # So: Old Total = Current Total - (Duration * 10)
             
             current_xp = Gamification.get_total_xp()
             xp_gained = self.current_duration * Gamification.XP_PER_MINUTE
             old_xp = current_xp - xp_gained
             
             leveled_up, new_level = Gamification.check_level_up(old_xp)
             
             # 3. Update UI
             if hasattr(self.master, "update_profile"):
                 self.master.update_profile()
             
             # 4. Notifications
             msg = f"{self.mode_var.get()} finished!\n+{xp_gained} XP"
             if leveled_up:
                 msg += f"\n\n🎉 LEVEL UP! 🎉\nYou are now Level {new_level}!"
                 # Play special sound? (Optional)
        else:
             msg = f"{self.mode_var.get()} finished!"
        
        # Play sound
        from utils.sound_manager import SoundManager
        SoundManager.play_finish_sound()
        
        # Bring window to front
        self.master.deiconify()
        self.master.lift()
        self.master.focus_force()
        
        tkinter.messagebox.showinfo("Timer Finished", msg)

    def change_mode(self):
        mode = self.mode_var.get()
        if mode == "Pomodoro":
            self.current_duration = 25
        elif mode == "Short Break":
            self.current_duration = 5
        else:
            self.current_duration = 15
            
        self.timer_label.configure(text=f"{self.current_duration}:00")
        self.progress_bar.set(1.0)
        self.controller.reset_timer()
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled")
