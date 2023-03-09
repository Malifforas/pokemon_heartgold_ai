import random
import time

from gamestate import GameState
from nuzlock import Nuzlock
from api import PokemonAPI
from screen import Screen

import numpy as np


class AI:
    def __init__(self, api):
        self.api = api
        self.state = GameState()
        self.nuzlock = Nuzlock(api)

    def run(self):
        print("Starting AI")
        while True:
            self.state.update()
            screen = Screen(self.state)
            if screen.is_battle_menu():
                self.handle_battle(screen)
            elif screen.is_dialogue():
                self.handle_dialogue(screen)
            elif screen.is_map():
                self.handle_map(screen)
            elif screen.is_main_menu():
                self.handle_main_menu(screen)

    def handle_battle(self, screen):
        if screen.is_text_box():
            screen.press_button()
        elif screen.is_select_move():
            if self.should_switch_pokemon(screen):
                screen.press_button(2)
            else:
                screen.press_button(random.randint(1, 4))
        elif screen.is_select_pokemon():
            screen.press_button(random.randint(1, 6))
        elif screen.is_switch_pokemon():
            screen.press_button(random.randint(1, 6))
        elif screen.is_run_menu():
            screen.press_button(1)

    def handle_dialogue(self, screen):
        if screen.is_text_box():
            screen.press_button()

    def handle_map(self, screen):
        if self.nuzlock.is_in_battle():
            self.handle_battle(screen)
        elif screen.is_text_box():
            screen.press_button()
        else:
            self.move_randomly(screen)

    def handle_main_menu(self, screen):
        screen.press_button(random.randint(1, 5))

    def should_switch_pokemon(self, screen):
        # We always switch to the first available Pokemon that is not fainted.
        for i in range(1, 6):
            if screen.get_pokemon_health(i) > 0:
                return i != screen.get_active_pokemon()
        return False

    def move_randomly(self, screen):
        # Move randomly in a random direction for a random amount of time
        move_time = random.randint(1, 10)
        moves = [Screen.KEY_UP, Screen.KEY_DOWN, Screen.KEY_LEFT, Screen.KEY_RIGHT]
        start_time = time.time()
        while time.time() - start_time < move_time:
            screen.press_button(random.choice(moves))
            time.sleep(0.1)

    def q_learning(self, api):
        state_space = 10 # replace with actual state space size
        action_space = 10 # replace with actual action space size
        q_table = np.zeros((state_space, action_space))

        alpha = 0.1  # Learning rate
        gamma = 0.6  # Discount factor
        epsilon = 0.1  # Exploration rate

        state = api.get_state()  # Replace with actual function to get state
        for i in range(1000): # Replace with number of episodes
            done = False
            score = 0
            while not done:
                if random.uniform(0, 1) < epsilon:
                    action = random.randint(0, action_space - 1)
                else:
                    action = np.argmax(q_table[state, :])
                next_state, reward, done, info = api.step(action)
                old_value = q_table[state, action]
                next_max = np.max(q_table[next_state, :])
                new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
                q_table[state, action] = new_value
                state = next_state
                score += reward
                time.sleep(0.01)  # Add a small delay to avoid emulator lag

            print(f"Episode {i} - Score: {score}")

        return q_table

    def play(self, q_table, api):
        state = api.get_state()  # Replace with actual function to get state
        done = False
        while not done:
            action = np.argmax(q_table[state, :])
            next_state, _, done, _ = api.step(action)
            state = next_state
            time.sleep(0.01)  # Add a small delay to avoid emulator lag