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

        roi = (250, 130, 300, 250)
        location = pyautogui.locateOnScreen(image=player_image, grayscale=True, region=roi)
        if location:
            center_x = location[0] + location[2] // 2
            center_y = location[1] + location[3] // 2
            return center_x, center_y
        return None

    def is_loaded(self):
        if self._screenshot is None:
            return False

        player_position = self.get_player_position()
        return player_position is not None

    def wait_until_loaded(self):
        while not self.is_loaded():
            time.sleep(1)

def main():
    screen = Screen()

    while True:
        screen.capture_screenshot()
        screen.wait_until_loaded()

        player_position = screen.get_player_position()
        if player_position:
            print("Player position:", player_position)

if __name__ == "__main__":
    main()