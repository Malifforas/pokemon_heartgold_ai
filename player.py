import cv2
import numpy as np
import time
import os
import json
import random
import math

import win32api
import win32con

import pokeapi
import requests

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

import screen
from screen import Screen
from controller import Controller

from api import PokemonAPI
from reward import RewardSystem


class Player:
    def __init__(self):
        self.NUM_STATES = 75
        self.NUM_ACTIONS = 4  # attack, switch, bag, flee
        self.ALPHA = 0.1  # learning rate
        self.GAMMA = 0.9  # discount factor
        self.EPSILON = 0.1  # exploration rate
        self.q_table = np.zeros((self.NUM_STATES, self.NUM_ACTIONS))
        self.reward_system = RewardSystem()

        self.client = pokeapi.V2Client()
        self.game_window_name = "Desmume 0.9.11 x64"
        self.movement_keys = {
            "up": 0,
            "down": 1,
            "left": 2,
            "right": 3
        }

    def start(self):
        # find game window
        game_window = self.screen.find_game_window()

        # start game loop
        while True:
            # capture screen
            screen_image = self.screen.capture_screen(game_window)

            # preprocess screen image for Q-learning
            processed_image = self.preprocess_screen(screen_image)

            # get current game state
            game_state = self.get_game_state(processed_image)

            # choose next action using Q-learning algorithm
            next_action = self.q_learning(game_state)

            # map chosen action to game action
            game_action = self.map_action(next_action)

            # perform game action
            self.perform_action(game_window, game_action)

            # check if game over
            if self.screen.is_game_over():
                break

        # print final score
        print(f"Game over! Final score: {self.reward_system.last_reward}")

    def q_learning(self, state):
        # choose action based on exploration-exploitation tradeoff
        if np.random.uniform(0, 1) < self.EPSILON:
            action = np.random.choice(self.NUM_ACTIONS)
        else:
            action = np.argmax(self.q_table[state, :])

        # calculate reward for the chosen action
        next_state, reward = self.reward_system.get_reward(action)

        # update Q-table
        current_q = self.q_table[state, action]
        max_next_q = np.max(self.q_table[next_state, :])
        new_q = current_q + self.ALPHA * (reward + self.GAMMA * max_next_q - current_q)
        self.q_table[state, action] = new_q

        return action

    def map_action(self, action):
        # map action index to corresponding key
        if action == 0:
            return "a"
        elif action == 1:
            return "s"
        elif action == 2:
            return "b"
        elif action == 3:
            return self.movement_keys[np.random.choice(list(self.movement_keys.keys()))]

    def preprocess_screen(self, screen_image):
        # convert to grayscale
        processed_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2GRAY)

        # crop to relevant game area
        processed_image = processed_image[75:375, 25:295]

        # resize image to smaller size
        processed_image = cv2.resize(processed_image, (30, 30))

        # normalize pixel values to be between 0 and 1
        processed_image = processed_image / 255.0

        return processed_image

    def get_game_state(self, processed_image):
        # flatten image into 1D array
        state = processed_image.flatten()

        # add additional features to state
        player_info = self.screen.get_player_info()
        enemy_info = self.screen.get_enemy_info()
        state = np.concatenate((state, player_info, enemy_info))

        # convert state to integer index
        state_index = int("".join(str(int(i)) for i in state), 2)

        return state_index

    def perform_action(self, game_window, game_action):
        if game_action == "a":
            # press A key
            win32api.keybd_event(0x41, 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(0x41, 0, win32con.KEYEVENTF_KEYUP, 0)
        elif game_action == "s":
            # press S key
            win32api.keybd_event(0x53, 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(0x53, 0, win32con.KEYEVENTF_KEYUP, 0)
        elif game_action == "b":
            # press B key
            win32api.keybd_event(0x42, 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(0x42, 0, win32con.KEYEVENTF_KEYUP, 0)
        elif game_action in self.movement_keys:
            # move player in specified direction
            direction = self.movement_keys[game_action]
            win32api.keybd_event(direction, 0, 0, 0)
            time.sleep(0.2)
            win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)