import os
import sys
import smtplib
import datetime
from pynput import keyboard
from threading import Timer

class Keylogger:
    def __init__(self):
        self.email = ''
        self.password = ''
        self.count = 0

    def handle_key_press(self, key):
        self.count += 1

    def request_mail_credentials(self):
        try:
            self.email = os.environ["counter_email"]
        except KeyError:
            print("Must set counter_email enviroment variable.")
            sys.exit(1)
        try:
            self.password = os.environ["counter_password"]
        except KeyError:
            print("Must set counter_password enviroment variable.")
            sys.exit(1)
        print("Got environment variables", flush=True)

    def send_mail(self, email, password, msg):
        print("Getting ready to send email report.",flush=True)
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, msg)
        except Exception as e:
            print('An error occurred: ', e)
        finally:
            server.quit()
        print("Email report sent.",flush=True)

    def report(self):
        log_date = datetime.datetime.now()
        msg = f'Subject: Log info {log_date}\n\nKeystrokes: {self.count}\n'
        self.send_mail(self.email, self.password, msg)
        self.count = 0
        now = datetime.datetime.now()
        seconds_left = (24 * 60 - (now.hour * 60 + now.minute)) * 60
        timer = Timer(interval=seconds_left+1, function=self.report)
        print(f'Sleeping for {seconds_left} seconds.', flush=True)
        timer.daemon = True
        timer.start()

    def start(self):
        self.request_mail_credentials()
        self.report()
        with keyboard.Listener(on_release=self.handle_key_press) as listener:
            listener.join()

if __name__ == '__main__':
    keylogger = Keylogger()
    keylogger.start()

