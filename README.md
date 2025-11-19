# Time Management App

A desktop productivity tool built with Python and CustomTkinter.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

This application helps users maintain focus and track their efficiency. It combines a Pomodoro timer, a persistent task list, and gamification elements (XP and leveling) to create an engaging experience.

The project is built using a Model-View-Controller (MVC) architecture, ensuring clean separation between logic, data, and the user interface. It uses CustomTkinter for the UI and SQLite for local data storage.

## Features

- **Focus Timer**: A customizable Pomodoro timer with adjustable work and break intervals.
- **Task Management**: Create, track, and manage tasks.
- **Gamification**: Earn XP and level up by completing focus sessions.
- **Analytics**: View session history and productivity statistics.
- **Modern UI**: A dark-mode interface that is high-DPI aware.

## Technical Overview

This project demonstrates the following technical concepts:

<img width="900" height="627" alt="Screenshot 2025-11-20 015252" src="https://github.com/user-attachments/assets/845a2af1-40d6-4d7c-b783-410818aa2cdd" />

<img width="900" height="626" alt="Screenshot 2025-11-20 015354" src="https://github.com/user-attachments/assets/9ff13d4e-823c-4a66-8b72-66215f701992" />



- **MVC Architecture**: The codebase is organized into Models, Views, and Controllers to ensure modularity and maintainability.
- **Database Integration**: SQLite is used for reliable local storage of tasks and user progress.
- **Object-Oriented Design**: The application makes extensive use of classes and inheritance.
- **Type Hinting**: Python type hints are used throughout for code clarity and reliability.

## Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip

### Steps

1. Clone the repository or download the source code.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure

https://github.com/user-attachments/assets/375e319c-96e1-4988-894b-a94806d263c8



- `controllers/`: Application logic and event handling.
- `models/`: Database models and business entities.
- `ui/`: User interface components.
- `utils/`: Helper functions and constants.
- `database.py`: Database initialization.
- `main.py`: Application entry point.

## Future Improvements

- Cloud synchronization.
- Advanced data visualization.
- Export functionality for reports.

---
Built by Nqobile.
