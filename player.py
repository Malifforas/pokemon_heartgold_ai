import cv2
import numpy as np
import time
import os

from screen import Screen
from controller import Controller
from reward import RewardSystem

class Player:
    def __init__(self):
        self.screen = Screen()
        self.controller = Controller()
        self.reward_system = RewardSystem()

        self.game_window_name = "Desmume 0.9.11 x64"

        self.movement_keys = {
            "up": 0,
            "down": 1,
            "left": 2,
            "right": 3
        }

    def start(self):
        self.screen.find_window(self.game_window_name)

        while True:
            # Capture screen
            screen_image = self.screen.capture()

            # Find player position
            player_position = self.screen.find_player(screen_image)

            # Calculate distance from center of the screen
            distance_from_center = abs(player_position[0] - self.screen.width / 2)

            # Give reward for being close to the center of the screen
            reward = 1 - (distance_from_center / (self.screen.width / 2))
            self.reward_system.give_reward(reward)

            # Choose random movement
            movement_key = np.random.choice(list(self.movement_keys.keys()))

            # Perform movement
            self.controller.press_key(self.movement_keys[movement_key])
            time.sleep(0.5)
            self.controller.release_key(self.movement_keys[movement_key])

            # Wait for game to load
            if self.screen.is_loading():
                self.screen.wait_until_loaded()

            # Check if game over
            if self.screen.is_game_over():
                break

        print(f"Game over! Final score: {self.reward_system.get_reward()}")

if __name__ == "__main__":
    player = Player()
    player.start()