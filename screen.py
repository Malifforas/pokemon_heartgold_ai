import numpy as np
import cv2
import pyautogui
import requests
import time

class Screen:
    def __init__(self):
        self._screenshot = None

    def capture_screenshot(self):
        screenshot = pyautogui.screenshot()
        if screenshot is not None:
            self._screenshot = np.array(screenshot)

    def get_player_position(self):
        player_image_url = 'https://www.spriters-resource.com/resources/sheets/24/26777.png?updated=1460955691'
        response = requests.get(player_image_url)
        player_image = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)

        if self._screenshot is None:
            return None

        # Template matching
        res = cv2.matchTemplate(self._screenshot, player_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        if len(loc[0]) > 0:
            center_x = int(loc[1][0] + player_image.shape[1] / 2)
            center_y = int(loc[0][0] + player_image.shape[0] / 2)
            return center_x, center_y

        return None

    def is_loaded(self):
        return self.get_player_position() is not None

    def wait_until_loaded(self):
        while not self.is_loaded():
            self.capture_screenshot()
            time.sleep(1)