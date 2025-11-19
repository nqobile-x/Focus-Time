import customtkinter as ctk
from ui.app import TimeManagementApp
from database import initialize_db

def main():
    # Initialize Database
    initialize_db()
    
    # Set up the main application window
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    
    app = TimeManagementApp()
    app.mainloop()

if __name__ == "__main__":
    main()
