import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from plyer import notification
import threading
import time

# Timetable data (pre-filled based on your image)
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
periods = [
    ("08:55", "09:50"),
    ("09:50", "10:45"),
    ("10:50", "11:45"),
    ("11:45", "12:40"),
    ("12:40", "01:30"),
    ("01:30", "02:15"),
    ("02:15", "03:00"),
    ("03:05", "03:50"),
    ("03:50", "04:35")
]

preset_timetable = {
    # Monday
    ("Monday", 0): "OS",
    ("Monday", 1): "QA",
    ("Monday", 2): "JAVA",
    ("Monday", 3): "PDP",
    ("Monday", 5): "UHV",
    ("Monday", 6): "VA",
    ("Monday", 7): "MATH",
    ("Monday", 8): "TAFL",

    # Tuesday
    ("Tuesday", 0): "UHV",
    ("Tuesday", 1): "PDP",
    ("Tuesday", 2): "MATH",
    ("Tuesday", 3): "SPORT",
    ("Tuesday", 5): "CLUB",
    ("Tuesday", 6): "CLUB",
    ("Tuesday", 7): "CYBER W/S",
    ("Tuesday", 8): "CYBER W/S",

    # Wednesday
    ("Wednesday", 0): "OS",
    ("Wednesday", 1): "JAVA",
    ("Wednesday", 2): "MM",
    ("Wednesday", 3): "PYTHON",
    ("Wednesday", 5): "MATH",
    ("Wednesday", 6): "LIB",
    ("Wednesday", 7): "PDP",
    ("Wednesday", 8): "TAFL",

    # Thursday
    ("Thursday", 0): "JAVA",
    ("Thursday", 1): "QA",
    ("Thursday", 2): "OOPS LAB",
    ("Thursday", 3): "OOPS LAB",
    ("Thursday", 5): "CLUB",
    ("Thursday", 6): "CLUB",
    ("Thursday", 7): "VA",
    ("Thursday", 8): "OS",

    # Friday
    ("Friday", 0): "OS",
    ("Friday", 1): "JAVA",
    ("Friday", 2): "OS LAB",
    ("Friday", 3): "OS LAB",
    ("Friday", 5): "PYTHON",
    ("Friday", 6): "MATH",
    ("Friday", 7): "TAFL",
    ("Friday", 8): "TAFL",
}

entries = {}

# GUI creation
def create_timetable_grid(root):
    style = ttk.Style()
    style.configure("TEntry", padding=6, relief="flat", font=('Segoe UI', 10))
    style.configure("Header.TLabel", font=('Segoe UI', 10, 'bold'), background="#005f73", foreground="white", anchor="center", padding=6)
    style.configure("Day.TLabel", font=('Segoe UI', 10, 'bold'), background="#94d2bd", anchor="center", padding=6)

    # Header
    ttk.Label(root, text="Day / Time", style="Header.TLabel", width=15).grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
    for i, (start, end) in enumerate(periods):
        ttk.Label(root, text=f"{start}-{end}", style="Header.TLabel", width=15).grid(row=0, column=i+1, sticky="nsew", padx=1, pady=1)

    # Rows
    for row, day in enumerate(days):
        ttk.Label(root, text=day, style="Day.TLabel", width=15).grid(row=row+1, column=0, sticky="nsew", padx=1, pady=1)
        for col in range(len(periods)):
            # Use preset_timetable if available, else empty string
            entry_text = preset_timetable.get((day, col), "")
            entry = ttk.Entry(root, width=15, font=('Segoe UI', 10))
            entry.grid(row=row+1, column=col+1, sticky="nsew", padx=1, pady=1)
            entry.insert(0, entry_text)
            entries[(day, col)] = entry

def check_and_notify():
    while True:
        now = datetime.now()
        current_day = now.strftime("%A")
        current_time = now.strftime("%H:%M")

        if current_day in days:
            current_dt = datetime.now()
            for i, (start, _) in enumerate(periods):
                # Notify 5 minutes before class
                notify_dt = datetime.strptime(start, "%H:%M").replace(
                    year=current_dt.year, month=current_dt.month, day=current_dt.day
                ) - timedelta(minutes=5)
                if 0 <= (current_dt - notify_dt).total_seconds() < 60:
                    entry = entries.get((current_day, i))
                    if entry:
                        subject = entry.get()
                        if subject:
                            notification.notify(
                                title="Class Reminder",
                                message=f"{subject} class starts at {start}",
                                timeout=10
                            )
        time.sleep(60)

# GUI Start
root = tk.Tk()
root.title("College Timetable Reminder")

create_timetable_grid(root)

# Add Exit Button
exit_button = tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white", font=("Arial", 12, "bold"))
exit_button.grid(row=len(days)+2, column=0, columnspan=len(periods)+1, pady=10)

# Background thread for checking time
threading.Thread(target=check_and_notify, daemon=True).start()

root.mainloop()
