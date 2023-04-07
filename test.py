#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import time
import subprocess
import fcntl
import sys
import os

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
root.wm_attributes("-topmost", 1)
root.geometry("800x100+{}+{}".format(int(root.winfo_screenwidth()), int(root.winfo_screenheight())))

# create a label for the countdown
label = tk.Label(root, font=("Helvetica", 36))
label.pack()

# create a progress bar
progress = tk.ttk.Progressbar(root, orient="horizontal", length=600, mode="determinate")
progress.pack()

# function to update the label and progress bar with the remaining time
def update_label(countdown):
    if countdown > 0:
        # format the remaining time as M:SS
        remaining_time = time.strftime('%-M:%S', time.gmtime(countdown))
        label.config(text="Computer closing in: {}".format(remaining_time))
        # update the progress bar
        progress["value"] = (countdown / seconds) * 100
    else:
        label.config(text="Event triggered!")
        return
    root.after(1000, update_label, countdown-1)

# get the next systemd timer event
next_event = subprocess.check_output(['systemctl', 'show', '--property=NextElapseUSecRealtime', 'logrotate.timer']).decode('utf-8').split('=')[1].strip()

# calculate the number of seconds until the next event
seconds = int(time.mktime(time.strptime(next_event, "%a %Y-%m-%d %H:%M:%S %Z"))) - int(time.time())

# start the countdown
update_label(seconds)

# start the GUI loop
root.mainloop()
