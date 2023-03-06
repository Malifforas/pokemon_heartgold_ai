import time
import pyautogui


class Emulator:
    def __init__(self):
        # Set up keybindings for emulator
        self.keybindings = {
            'a': 'z',
            'b': 'x',
            'start': 'enter',
            'select': 'backspace',
            'up': 'up',
            'down': 'down',
            'left': 'left',
            'right': 'right'
        }

    def press_key(self, key):
        pyautogui.press(self.keybindings[key])
        time.sleep(0.5)

    def move(self, direction):
        self.press_key(direction)

    def press_a(self):
        self.press_key('a')

    def press_b(self):
        self.press_key('b')

    def press_start(self):
        self.press_key('start')

    def press_select(self):
        self.press_key('select')