#!/usr/bin/env python3
import signal
import subprocess
import time
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Pango, Gdk
import os
import fcntl
import sys

# Try to lock a file, exit if the lock is held
lock_file = os.path.expanduser("~/.lock_file")
try:
    file_handle = open(lock_file, 'w')
    fcntl.lockf(file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    sys.exit(0)


class MainWindow(Gtk.Window):
    def __init__(self, timer):
        super().__init__(title="Computer closing soon")
        self.timer = timer
        self.set_size_request(800, 100)
        self.set_border_width(10)
        self.set_resizable(False)
        self.set_keep_above(True)
        self.move(1920, 1080)
        self.connect("destroy", Gtk.main_quit)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.label = Gtk.Label()
        self.label.set_halign(Gtk.Align.CENTER)
        self.label.set_valign(Gtk.Align.CENTER)
        self.label.set_name("my-label")
        self.label.set_size_request(-1, -1)
        self.label.set_ellipsize(Pango.EllipsizeMode.END)
        self.box.pack_start(self.label, True, True, 0)

        self.progress = Gtk.ProgressBar(show_text=True)
        self.box.pack_start(self.progress, True, True, 0)

        self.css_provider = Gtk.CssProvider()
        css = b"""
        #my-label {
            font-size: 36pt;
        }
        #my-small-label {
            font-size: 14pt;
        }
        """
        self.css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.small_label = Gtk.Label()
        self.small_label.set_halign(Gtk.Align.CENTER)
        self.small_label.set_valign(Gtk.Align.CENTER)
        self.small_label.set_name("my-small-label")
        self.small_label.set_size_request(-1, -1)
        self.small_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.box.pack_start(self.small_label, True, True, 0)

        self.startseconds = -1
        self.update_timer()

    def update_timer(self):
        self.next_event = subprocess.check_output(
            ['systemctl', 'show', '--property=NextElapseUSecRealtime', self.timer]).decode('utf-8').split('=')[1].strip()
        if self.startseconds < 0:
            self.startseconds = int(time.mktime(time.strptime(
                self.next_event, "%a %Y-%m-%d %H:%M:%S %Z"))) - int(time.time())
        self.seconds = int(time.mktime(time.strptime(
            self.next_event, "%a %Y-%m-%d %H:%M:%S %Z"))) - int(time.time())
        self.update_label(self.seconds)
        return True

    def update_label(self, countdown):
        if countdown > 0:
            remaining_time = time.strftime('%-M:%S', time.gmtime(countdown))
            self.label.set_text(
                "Computer closing in: {}".format(remaining_time))
            self.progress.set_fraction(self.seconds/self.startseconds)
            progress_percentage = int(self.seconds / self.startseconds * 100)
            self.progress.set_text("{}%".format(progress_percentage))
            self.small_label.set_markup(
                "(Staff <b>cannot</b> stop this process)")
            return True
        else:
            self.label.set_text("Event triggered!")
            return False


def graceful_quit(signum, frame):
    Gtk.main_quit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 timer.py <timer_name>")
        sys.exit(1)

    timer_name = sys.argv[1]
    win = MainWindow(timer_name)
    win.show_all()
    GLib.timeout_add(1000, win.update_timer)
    signal.signal(signal.SIGINT, graceful_quit)
    Gtk.main()
