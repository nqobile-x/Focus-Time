import threading
import platform

class SoundManager:
    @staticmethod
    def play_finish_sound():
        """Plays a sound when the timer finishes."""
        threading.Thread(target=SoundManager._play_sound_thread, daemon=True).start()

    @staticmethod
    def _play_sound_thread():
        try:
            # Try using winsound on Windows
            if platform.system() == "Windows":
                import winsound
                # Play a sequence of beeps
                winsound.Beep(1000, 500)
                winsound.Beep(1500, 500)
                winsound.Beep(1000, 500)
            else:
                # Fallback for other OS or if winsound fails (not likely on Windows)
                print("Beep! Timer Finished!")
        except Exception as e:
            print(f"Error playing sound: {e}")
