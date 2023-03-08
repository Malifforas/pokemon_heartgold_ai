from screen import Screen
from player import Player
from reward import RewardSystem
from q_learning import QLearning

class AI:
    def __init__(self):
        self.screen = Screen()
        self.player = Player()
        self.reward_system = RewardSystem()
        self.q_learning = QLearning([0, 1, 2, 3, 4])

    def run(self):
        while True:
            # Capture the current screen and get the current state
            self.screen.capture()
            state = self.screen.process_screen()

            # Choose an action based on the current state
            action = self.q_learning.choose_action(state)

            # Take the chosen action and get the resulting screen and state
            if action == 0:
                self.player.move_up()
            elif action == 1:
                self.player.move_down()
            elif action == 2:
                self.player.move_left()
            elif action == 3:
                self.player.move_right()
            elif action == 4:
                self.player.press_a()
            self.screen.capture()
            next_state = self.screen.process_screen()

            # Get the reward for the action and update the Q-table
            reward = self.reward_system.get_reward(state, next_state)
            self.q_learning.update_table(state, action, reward, next_state)