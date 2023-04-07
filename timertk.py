#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import time
import subprocess
import fcntl
import sys
import os

# Check if the timer argument is provided
if len(sys.argv) < 2:
    print("Please provide the timer name as an argument.")
    sys.exit(1)

timer = sys.argv[1]

# Check if the timer exists and is started
try:
    output = subprocess.check_output(['systemctl', 'show', '--property=ActiveState', timer]).decode('utf-8').strip()
except subprocess.CalledProcessError:
    print(f"Timer '{timer}' doesn't exist.")
    sys.exit(1)

if output.split('=')[1] != 'active':
    print(f"Timer '{timer}' is not started.")
    sys.exit(1)

# Try to lock a file, exit if the lock is held
lock_file = os.path.expanduser("~/.lock_file")
try:
    file_handle = open(lock_file, 'w')
    fcntl.lockf(file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    sys.exit(0)

# create the main window
root = tk.Tk()
root.title("Computer closing soon")
root.attributes('-type', 'utility')
root.geometry("800x150+{}+{}".format(int(root.winfo_screenwidth()), int(root.winfo_screenheight())))

# create a label for the countdown
label = tk.Label(root, font=("Helvetica", 36), pady=10)
label.pack()

# create a progress bar
progress = tk.ttk.Progressbar(root, orient="horizontal", length=600, mode="determinate")
progress.pack(pady=(10))

# create a label to exonerate staff
staff_text = "(Staff cannot stop this process)"
staffLabel = tk.Label(root, text=staff_text, font=("Helvetica", 16), pady=10)
staffLabel.pack()

# function to update the label and progress bar with the remaining time
def update_label(countdown):
    if countdown > 0:
        # format the remaining time as M:SS
        remaining_time = time.strftime('%-M:%S', time.gmtime(countdown))
        label.config(text="Computer closing in {}".format(remaining_time))
        # update the progress bar
        progress["value"] = (countdown / seconds) * 100
    else:
        label.config(text="Event triggered!")
        return
    root.after(1000, update_label, countdown-1)

# get the next systemd timer event
next_event = subprocess.check_output(['systemctl', 'show', '--property=NextElapseUSecRealtime', timer]).decode('utf-8').split('=')[1].strip()

# calculate the number of seconds until the next event
seconds = int(time.mktime(time.strptime(next_event, "%a %Y-%m-%d %H:%M:%S %Z"))) - int(time.time())

# start the countdown
update_label(seconds)

root.resizable(False, False)

try:
    # start the GUI loop
    root.mainloop()
except KeyboardInterrupt:
    # handle CTRL+C gracefully
    sys.exit(0)
