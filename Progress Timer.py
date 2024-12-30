import tkinter as tk
from tkinter import messagebox
import time
import threading
import winsound
from datetime import datetime

class TimerClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer and Clock")
        self.running_timer = None
        self.remaining_time = 0
        self.timer_paused = False
        self.start_time = None  # Track when the timer starts
        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        self.display_label = tk.Label(self.root, font=("Helvetica", 24), fg="blue")
        self.display_label.pack(pady=20)

        self.timer_entry = tk.Entry(self.root, font=("Helvetica", 24), justify='center')
        self.timer_entry.pack(pady=5)
        self.timer_entry.insert(0, "Enter minutes")

        self.start_timer_btn = tk.Button(self.root, text="Start Timer", font=("Helvetica", 16), command=self.start_timer)
        self.start_timer_btn.pack(pady=5)

        self.pause_resume_btn = tk.Button(self.root, text="Pause Timer", font=("Helvetica", 16), command=self.pause_resume_timer)
        self.pause_resume_btn.pack(pady=5)
        self.pause_resume_btn.config(state=tk.DISABLED)

        self.stop_timer_btn = tk.Button(self.root, text="Stop Timer", font=("Helvetica", 16), command=self.stop_timer)
        self.stop_timer_btn.pack(pady=5)
        self.stop_timer_btn.config(state=tk.DISABLED)

    def update_clock(self):
        if self.running_timer is None:
            current_time = time.strftime("%H:%M:%S")
            self.display_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def start_timer(self):
        try:
            minutes = int(self.timer_entry.get())
            self.remaining_time = minutes * 60
            if self.running_timer:
                self.root.after_cancel(self.running_timer)
            self.start_time = datetime.now()  # Track when the timer starts
            self.timer_paused = False
            self.pause_resume_btn.config(text="Pause Timer", state=tk.NORMAL)
            self.stop_timer_btn.config(state=tk.NORMAL)
            self.countdown(self.remaining_time)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def countdown(self, remaining_time):
        if remaining_time > 0:
            self.remaining_time = remaining_time
            hours, remainder = divmod(remaining_time, 3600)  # Get hours and remaining seconds
            mins, secs = divmod(remainder, 60)  # Get minutes and seconds from the remainder
            time_format = f"{hours:02}:{mins:02}:{secs:02}"
            self.display_label.config(text=time_format)

            if not self.timer_paused:
                self.running_timer = self.root.after(1000, self.countdown, remaining_time - 1)
        else:
            self.timer_finished()

    def timer_finished(self):
        self.display_label.config(text="Time's up!")
        self.stop_timer_btn.config(state=tk.DISABLED)
        self.pause_resume_btn.config(state=tk.DISABLED)
        self.log_time()
        threading.Thread(target=self.play_alarm).start()

    def pause_resume_timer(self):
        if self.timer_paused:
            self.timer_paused = False
            self.pause_resume_btn.config(text="Pause Timer")
            self.countdown(self.remaining_time)
        else:
            self.timer_paused = True
            self.pause_resume_btn.config(text="Resume Timer")

    def stop_timer(self):
        if self.running_timer:
            self.root.after_cancel(self.running_timer)
            self.timer_paused = False
            self.timer_finished()

    def play_alarm(self):
        duration = 1000
        freq = 440
        for _ in range(5):
            winsound.Beep(freq, duration)
            time.sleep(0.2)

    def log_time(self):
        if self.start_time:
            elapsed_time = datetime.now() - self.start_time
            elapsed_minutes = divmod(elapsed_time.total_seconds(), 60)[0]
            log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Time Spent: {int(elapsed_minutes)} minutes\n"
            with open("time_log.txt", "a") as file:
                file.write(log_message)
            self.start_time = None

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerClockApp(root)
    root.mainloop()
