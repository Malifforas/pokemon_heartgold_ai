import numpy as np
import random

class QLearning:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay_rate=0.99):
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay_rate = exploration_decay_rate
        self.q_table = {}

    def get_q_value(self, state, action):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))
        return self.q_table[state][action]

    def update_q_value(self, state, action, reward, next_state):
        current_q = self.get_q_value(state, action)
        next_q = max([self.get_q_value(next_state, a) for a in self.actions])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_q - current_q)
        self.q_table[state][action] = new_q

    def choose_action(self, state, explore=True):
        if explore and random.random() < self.exploration_rate:
            return random.choice(self.actions)
        else:
            return np.argmax(self.q_table[state])

    def decay_exploration_rate(self):
        self.exploration_rate *= self.exploration_decay_rate