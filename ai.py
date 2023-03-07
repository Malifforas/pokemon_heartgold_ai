import threading

import debug
from screen import Screen
from player import Player
from player import RewardSystem


class AI:
    def __init__(self):
        self.screen = Screen()
        self.player = Player()
        self.reward_system = RewardSystem()

    def run(self):
        while True:
            self.reward_system.give_reward(1)  # Example usage of reward system
            self.screen.capture()
            # Add logic to process captured screen and determine actions for player
            self.player.move_up()  # Example action
# Start logging keypresses
threading.Thread(target=debug.check_keypresses).start()