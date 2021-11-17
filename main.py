import os
import sys
import datetime
import syslog
from pynput import keyboard
from threading import Timer

class Keylogger:
    def __init__(self):
        self.email = ''
        self.password = ''
        self.count = 0

    def handle_key_press(self, key):
        self.count += 1

    def report(self):
        msg = f'Keystrokes: {self.count}'
        syslog.syslog(msg)
        self.count = 0
        now = datetime.datetime.now()
#        seconds_left = (24 * 60 - (now.hour * 60 + now.minute)) * 60
        seconds_left = 60
        timer = Timer(interval=seconds_left, function=self.report)
        print(f'Sleeping for {seconds_left} seconds.', flush=True)
        timer.daemon = True
        timer.start()

    def start(self):
        self.report()
        with keyboard.Listener(on_release=self.handle_key_press) as listener:
            listener.join()

if __name__ == '__main__':
    keylogger = Keylogger()
    keylogger.start()

