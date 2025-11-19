import time
import threading

class TimerController:
    def __init__(self, update_callback, finish_callback):
        self.update_callback = update_callback
        self.finish_callback = finish_callback
        self.is_running = False
        self.remaining_time = 0
        self.total_time = 0
        self.timer_thread = None
        self.stop_event = threading.Event()

    def start_timer(self, duration_minutes):
        if not self.is_running:
            self.total_time = duration_minutes * 60
            self.remaining_time = self.total_time
            self.is_running = True
            self.stop_event.clear()
            self.timer_thread = threading.Thread(target=self._run_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()
        else:
            # Resume
            self.is_running = True
            self.stop_event.clear()
            self.timer_thread = threading.Thread(target=self._run_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()

    def pause_timer(self):
        self.is_running = False
        self.stop_event.set()

    def reset_timer(self):
        self.is_running = False
        self.stop_event.set()
        self.remaining_time = 0
        self.update_callback(0, 0)

    def _run_timer(self):
        while self.remaining_time > 0 and not self.stop_event.is_set():
            time.sleep(1)
            self.remaining_time -= 1
            self.update_callback(self.remaining_time, self.total_time)
        
        if self.remaining_time <= 0 and not self.stop_event.is_set():
            self.is_running = False
            self.finish_callback()
