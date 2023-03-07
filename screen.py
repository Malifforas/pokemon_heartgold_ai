import pyautogui
import time
import numpy as np
import cv2
import requests
from io import BytesIO

class Screen:
    def __init__(self):
        self._screenshot = None

    def capture_screenshot(self):
        self._screenshot = np.array(pyautogui.screenshot())

    def get_player_position(self):
        player_image_url = 'https://www.spriters-resource.com/resources/sheets/24/26777.png?updated=1460955691'
        response = requests.get(player_image_url)
        player_image = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)

        screenshot_gray = cv2.cvtColor(self._screenshot, cv2.COLOR_BGR2GRAY)
        player_gray = cv2.cvtColor(player_image, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(screenshot_gray, player_gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(result >= threshold)
        if len(loc[0]) > 0 and len(loc[1]) > 0:
            center_x = int(loc[1][0] + player_gray.shape[1] / 2)
            center_y = int(loc[0][0] + player_gray.shape[0] / 2)
            return center_x, center_y
        return None

    def is_loaded(self):
        if self._screenshot is None:
            return False

        player_position = self.get_player_position()
        return player_position is not None

    def wait_until_loaded(self):
        while not self.is_loaded():
            self.capture_screenshot()
            time.sleep(1)

def main():
    screen = Screen()

    while True:
        screen.wait_until_loaded()

        player_position = screen.get_player_position()
        if player_position:
            print("Player position:", player_position)

if __name__ == "__main__":
    main()