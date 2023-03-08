from screen import Screen
from player import Player, RewardSystem
import numpy as np
class QLearning:
    def __init__(self, actions):
        self.q_table = np.zeros((624, len(actions)))
        self.actions = actions

    def choose_action(self, state, epsilon=0.05):
        if np.random.uniform() < epsilon:
            return np.random.choice(self.actions)
        else:
            state_idx = state[0] * 8 + state[1]
            return self.actions[np.argmax(self.q_table[state_idx])]

    def update_table(self, state, action, reward, next_state, alpha=0.1, gamma=0.99):
        state_idx = state[0] * 8 + state[1]
        next_state_idx = next_state[0] * 8 + next_state[1]
        self.q_table[state_idx, action] += alpha * (
            reward + gamma * np.max(self.q_table[next_state_idx]) - self.q_table[state_idx, action]
        )

class AI:
    def __init__(self):
        self.screen = Screen()
        self.player = Player()
        self.reward_system = RewardSystem()
        self.q_learning = QLearning([0, 1, 2, 3, 4])

    def run(self):
        while True:
            # Give a reward to the AI for being alive
            self.reward_system.give_reward(1)

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