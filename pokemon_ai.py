import gym
import numpy as np
import random

import self as self
import tensorflow as tf
from collections import deque
from player import Player
from screen import Screen


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(24, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class PokemonAI:
    def __init__(self):
        self.screen = Screen()
        self.player = Player()
        self.agent = DQNAgent(state_size=4, action_size=5)

    def get_state(self):
        # Get player and enemy pokemon health
        player_hp = self.screen.get_player_hp()
        enemy_hp = self.screen.get_enemy_hp()

        # Get player and enemy pokemon status effect
        player_effect = self.screen.get_player_effect()
        enemy_effect = self.screen.get_enemy_effect()

        # Combine all information into a state
        state = [player_hp, enemy_hp, player_effect, enemy_effect]

        return np.reshape(state, [1, 4])

    def run(self, episodes):
        for e in range(episodes):
            # Reset the game
            self.player.reset()

            # Get initial state
            state = self.get_state()

            # Initialize variables for episode
            reward_total = 0
            done = False
            t = 0

            # Play the game until the player loses
            while not done:
                # Choose an action
                action = self.agent.act(state)

                # Take the action
                reward, done = self.player.take_action(action)

                # Update total reward
                reward_total += reward

                # Get next state
                next_state = self.get_state()

                # Remember the experience
                self.agent.remember(state, action, reward, next_state, done)

                # Update state
                state = next_state
# Import the necessary libraries
import time

# Define the number of episodes to run
episodes = 1000

# Define the maximum number of steps per episode
max_steps = 500

# Define the batch size for replay
batch_size = 32

# Define the target score to stop training
target_score = 100

# Define the number of episodes to evaluate the trained agent
evaluate_episodes = 10

# Initialize a list to store the scores
scores = []

# Train the agent
for e in range(episodes):
    # Reset the game
    self.player.reset()

    # Get initial state
    state = self.get_state()

    # Initialize variables for episode
    reward_total = 0
    done = False
    t = 0

    # Play the game until the player loses or max steps are reached
    while not done and t < max_steps:
        # Choose an action
        action = self.agent.act(state)

        # Take the action
        reward, done = self.player.take_action(action)

        # Update total reward
        reward_total += reward

        # Get next state
        next_state = self.get_state()

        # Remember the experience
        self.agent.remember(state, action, reward, next_state, done)

        # Update state
        state = next_state

        # Increment the step counter
        t += 1

    # Print the score for the episode
    print("Episode {}: Score = {}".format(e, reward_total))

    # Append the score to the scores list
    scores.append(reward_total)

    # Train the agent on a batch of experiences
    if len(self.agent.memory) > batch_size:
        self.agent.replay(batch_size)

    # Check if the target score has been reached
    if np.mean(scores[-100:]) >= target_score:
        print("Target score of {} reached after {} episodes".format(target_score, e+1))
        break

# Evaluate the trained agent
total_rewards = 0
for e in range(evaluate_episodes):
    # Reset the game
    self.player.reset()

    # Get initial state
    state = self.get_state()

    # Initialize variables for episode
    reward_total = 0
    done = False

    # Play the game until the player loses
    while not done:
        # Choose an action
        action = self.agent.act(state)

        # Take the action
        reward, done = self.player.take_action(action)

        # Update total reward
        reward_total += reward

        # Get next state
        next_state = self.get_state()

        # Update state
        state = next_state

    # Print the score for the episode
    print("Evaluation Episode {}: Score = {}".format(e, reward_total))

    # Add the reward to the total rewards
    total_rewards += reward_total

# Calculate the average reward
average_reward = total_rewards / evaluate_episodes

# Print the average reward
print("Average reward over {} evaluation episodes: {}".format(evaluate_episodes, average_reward))
