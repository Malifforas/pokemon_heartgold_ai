from tkinter import Image

import cv2
import numpy as np
import pyautogui
import requests
import time
import win32gui
import win32ui
import win32con

import cv2
import numpy as np
import pyautogui
import requests
import time
import win32gui
import win32ui
import win32con


class Screen:
    def __init__(self, name, matcher=None, region=None):
        self.name = name
        self.matcher = matcher
        self.region = region

    def capture_screenshot(self):
        screenshot = pyautogui.screenshot()
        if screenshot is not None:
            self._screenshot = np.array(screenshot)

    def get_player_position(self):
        if self._screenshot is None:
            return None

        # Load up the sprite for the player
        player_image_url = 'https://www.spriters-resource.com/resources/sheets/24/26777.png?updated=1460955691'
        response = requests.get(player_image_url)
        player_image = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)

        # Template matching
        res = cv2.matchTemplate(self._screenshot, player_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        if len(loc[0]) > 0:
            center_x = int(loc[1][0] + player_image.shape[1] / 2)
            center_y = int(loc[0][0] + player_image.shape[0] / 2)
            return center_x, center_y

        return None

    def wait_until_loaded(self):
        while not self.is_loaded():
            time.sleep(1)

    def is_loaded(self):
        if self.matcher is None:
            return True

        return self.matcher.exists(self.region)

def find_game_window():
    window_name = "Game Window"  # change this to match your game window title
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        return None

    # Get the dimensions of the game window
    rect = win32gui.GetWindowRect(hwnd)
    x, y, w, h = rect
    w = w - x
    h = h - y

    # Get the device context for the game window
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    # Create a bitmap object for the game window
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    # Copy the game window to the bitmap object
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)

    # Convert the bitmap to a numpy array
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(bmpstr, dtype='uint8')
    img.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)

    # Clean up
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return img


def capture_screen():
    screenshot = pyautogui.screenshot()
    if screenshot is not None:
        return np.array(screenshot)
    return None

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Threshold to binary
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Find contours
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # Get largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Get bounding rectangle of largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Crop image to bounding rectangle
    cropped_image = image[y:y+h, x:x+w]

    # Resize image
    resized_image = cv2.resize(cropped_image, (80, 80))

    return resized_image


class Screen:
    def __init__(self):
        self._screenshot = None

    def capture_screenshot(self):
        screenshot = pyautogui.screenshot()
        if screenshot is not None:
            self._screenshot = np.array(screenshot)

    def get_player_position(self):


     def is_loaded(self):
        return self.get_player_position() is not None

    def wait_until_loaded(self):
        while not self.is_loaded():
            self.capture_screenshot()
            time.sleep(1)

    def get_game_state(self):
        if self._screenshot is None:
            return None

        # preprocess the screenshot
        preprocessed_image = preprocess_image(self._screenshot)

        # create dictionary with game state information
        game_state = {
            "player_position": self.get_player_position(),
            "preprocessed_image": preprocessed_image
        }

        return game_state