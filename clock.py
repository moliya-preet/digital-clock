import tkinter as tk
from time import strftime, time
from tkinter import messagebox, ttk

# ---------- Main Window ----------
root = tk.Tk()
root.title("Digital Clock + Stopwatch")
root.geometry("650x550")
root.configure(bg="white")
root.resizable(False, False)

# ---------- Global Variables ----------
alarm_times = []
stopwatch_running = False
stopwatch_start_time = 0
stopwatch_elapsed = 0
stopwatch_history = []

colors = ["black"]
color_index = 0

# ---------- Clock Function ----------
def update_clock():
    global color_index
    time_now = strftime("%I:%M:%S %p")
    date_now = strftime("%A, %d %B %Y")
    time_label.config(text=time_now, fg=colors[color_index])
    date_label.config(text=date_now, fg="black")
    color_index = (color_index + 1) % len(colors)

    # Check alarms
    current_time_24h = strftime("%H:%M:%S")
    for alarm_time in alarm_times:
        if alarm_time == current_time_24h:
            messagebox.showinfo("Alarm", f"⏰ Alarm Time Reached! ({alarm_time})")
    
    root.after(1000, update_clock)

# ---------- Stopwatch Functions ----------
def start_stopwatch():
    global stopwatch_running, stopwatch_start_time
    if not stopwatch_running:
        stopwatch_running = True
        stopwatch_start_time = time() - stopwatch_elapsed
        update_stopwatch()

def stop_stopwatch():
    global stopwatch_running, stopwatch_elapsed
    if stopwatch_running:
        stopwatch_running = False
        stopwatch_elapsed = time() - stopwatch_start_time
        stopwatch_history.append(stopwatch_elapsed)

def reset_stopwatch():
    global stopwatch_running, stopwatch_elapsed, stopwatch_history
    stopwatch_running = False
    stopwatch_elapsed = 0
    stopwatch_label.config(text="00:00:00")
    stopwatch_history.clear()

def update_stopwatch():
    global stopwatch_elapsed
    if stopwatch_running:
        stopwatch_elapsed = time() - stopwatch_start_time
        mins, secs = divmod(stopwatch_elapsed, 60)
        hrs, mins = divmod(mins, 60)
        stopwatch_label.config(text=f"{int(hrs):02d}:{int(mins):02d}:{int(secs):02d}")
        root.after(100, update_stopwatch)

# ---------- Combined History Window ----------
def open_history_page():
    history_win = tk.Toplevel(root)
    history_win.title("History")
    history_win.geometry("400x400")
    history_win.configure(bg="white")

    tab_control = ttk.Notebook(history_win)
    tab_control.pack(expand=1, fill='both')

    # Alarm history tab
    alarm_tab = tk.Frame(tab_control, bg="white")
    tab_control.add(alarm_tab, text="Alarm History")
    tk.Label(alarm_tab, text="Alarm History", font=("Arial", 14, "bold"), bg="white").pack(pady=5)
    alarm_listbox = tk.Listbox(alarm_tab, bg="white", fg="black", font=("Arial", 12))
    alarm_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    for alarm in alarm_times:
        alarm_listbox.insert(tk.END, alarm)
    # Reset button
    tk.Button(alarm_tab, text="Reset Alarm History", command=lambda: reset_alarm_history(alarm_listbox), bg="#f87171").pack(pady=5)

    # Stopwatch history tab
    stopwatch_tab = tk.Frame(tab_control, bg="white")
    tab_control.add(stopwatch_tab, text="Stopwatch History")
    tk.Label(stopwatch_tab, text="Stopwatch History", font=("Arial", 14, "bold"), bg="white").pack(pady=5)
    stopwatch_listbox = tk.Listbox(stopwatch_tab, bg="white", fg="black", font=("Arial", 12))
    stopwatch_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    for elapsed in stopwatch_history:
        mins, secs = divmod(elapsed, 60)
        hrs, mins = divmod(mins, 60)
        stopwatch_listbox.insert(tk.END, f"{int(hrs):02d}:{int(mins):02d}:{int(secs):02d}")
    # Reset button
    tk.Button(stopwatch_tab, text="Reset Stopwatch History", command=lambda: reset_stopwatch_history(stopwatch_listbox), bg="#f87171").pack(pady=5)

def reset_alarm_history(listbox):
    global alarm_times
    alarm_times.clear()
    listbox.delete(0, tk.END)

def reset_stopwatch_history(listbox):
    global stopwatch_history
    stopwatch_history.clear()
    listbox.delete(0, tk.END)

# ---------- MAIN TABS ----------
main_tabs = ttk.Notebook(root)
main_tabs.pack(expand=1, fill="both")

# ----- Clock & Alarm Tab -----
clock_tab = tk.Frame(main_tabs, bg="white")
main_tabs.add(clock_tab, text="Clock")

# History button (first row, right)
history_frame = tk.Frame(clock_tab, bg="white")
history_frame.pack(fill=tk.X, pady=5, padx=10)
history_button = tk.Button(history_frame, text="📜 History", command=open_history_page, bg="white", font=("Arial", 12))
history_button.pack(side=tk.RIGHT)

# Digital Clock (second row, centered)
time_label = tk.Label(clock_tab, font=("Digital-7", 64), bg="white")
time_label.pack(pady=20)

# Date label
date_label = tk.Label(clock_tab, font=("Arial", 16), bg="white")
date_label.pack(pady=5)

# Alarm section
alarm_frame = tk.Frame(clock_tab, bg="white")
alarm_frame.pack(pady=10)

tk.Label(alarm_frame, text="Alarm (HH:MM:SS)", font=("Arial", 12), bg="white", fg="black").grid(row=0, column=0, padx=5)

# Alarm Entry (numeric only)
alarm_entry = tk.Entry(alarm_frame, font=("Arial", 12), width=8)
alarm_entry.grid(row=0, column=1, padx=5)

def format_alarm(event):
    # Keep only digits
    value = ''.join(filter(str.isdigit, alarm_entry.get()))
    if len(value) > 2:
        value = value[:2] + ':' + value[2:]
    if len(value) > 5:
        value = value[:5] + ':' + value[5:7]
    alarm_entry.delete(0, tk.END)
    alarm_entry.insert(0, value[:8])  # limit to HH:MM:SS

alarm_entry.bind("<KeyRelease>", format_alarm)

# AM/PM Choice
am_pm_var = tk.StringVar(value="AM")
am_pm_menu = tk.OptionMenu(alarm_frame, am_pm_var, "AM", "PM")
am_pm_menu.config(font=("Arial", 12))
am_pm_menu.grid(row=0, column=2, padx=5)

# Set Alarm Button
def set_alarm():
    time_text = alarm_entry.get()
    if len(time_text) == 8 and am_pm_var.get() in ["AM", "PM"]:
        hh, mm, ss = map(int, time_text.split(":")) 
        # Convert to 24-hour format
        if am_pm_var.get() == "PM" and hh != 12:
            hh += 12
        if am_pm_var.get() == "AM" and hh == 12:
            hh = 0
        alarm_time_24 = f"{hh:02d}:{mm:02d}:{ss:02d}"
        if alarm_time_24 not in alarm_times:
            alarm_times.append(alarm_time_24)
            messagebox.showinfo("Alarm Set", f"Alarm set for {time_text} {am_pm_var.get()}")
        alarm_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Invalid Alarm", "Please enter a valid time (HH:MM:SS) and select AM/PM")
    
tk.Button(alarm_frame, text="Set Alarm", command=set_alarm, bg="#22d3ee", font=("Arial", 11)).grid(row=0, column=3, padx=5)

# ----- Stopwatch Tab -----
stopwatch_tab = tk.Frame(main_tabs, bg="white")
main_tabs.add(stopwatch_tab, text="Stopwatch")

stopwatch_label = tk.Label(stopwatch_tab, text="00:00:00", font=("Digital-7", 50), bg="white", fg="black")
stopwatch_label.pack(pady=50)

sw_button_frame = tk.Frame(stopwatch_tab, bg="white")
sw_button_frame.pack(pady=10)
tk.Button(sw_button_frame, text="Start", command=start_stopwatch, bg="#22d3ee", font=("Arial", 12)).grid(row=0, column=0, padx=5)
tk.Button(sw_button_frame, text="Stop", command=stop_stopwatch, bg="#f87171", font=("Arial", 12)).grid(row=0, column=1, padx=5)
tk.Button(sw_button_frame, text="Reset", command=reset_stopwatch, bg="#34d399", font=("Arial", 12)).grid(row=0, column=2, padx=5)

# ---------- Start Clock ----------
update_clock()
root.mainloop()
