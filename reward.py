import cv2
import numpy as np
import pokeapi
from typing import Optional

from api import PokemonAPI
from controller import Controller

ALPHA = 0.1
GAMMA = 0.9

class RewardSystem:
    def __init__(self, q_table: np.ndarray):
        self.last_state = None
        self.last_action = None
        self.last_reward = None
        self.q_table = q_table
        self.pokemon_api = pokeapi.V2Client()

    def get_reward(self, state: int, action: int, next_state: int, pokeheartgold: PokemonAPI) -> float:
        # Calculate current and next state values
        current_player_pokemon = pokeheartgold.get_active_pokemon()
        current_opponent_pokemon = pokeheartgold.get_opponent_active_pokemon()
        current_player_hp = int(current_player_pokemon.current_hp / current_player_pokemon.stats.hp * 100 // 20)
        current_opponent_hp = int(current_opponent_pokemon.current_hp / current_opponent_pokemon.stats.hp * 100 // 20)
        current_level_diff = current_player_pokemon.level - current_opponent_pokemon.level

        next_player_pokemon = pokeheartgold.get_active_pokemon()
        next_opponent_pokemon = pokeheartgold.get_opponent_active_pokemon()
        next_player_hp = int(next_player_pokemon.current_hp / next_player_pokemon.stats.hp * 100 // 20)
        next_opponent_hp = int(
            next_opponent_pokemon.current_hp / next_opponent_pokemon.stats.hp * 100 // 20)
        next_level_diff = next_player_pokemon.level - next_opponent_pokemon.level

        # Get current and next state
        current_state = current_player_hp * 15 + current_opponent_hp * 3 + current_level_diff + 37
        next_state = next_player_hp * 15 + next_opponent_hp * 3 + next_level_diff + 37

        # Calculate reward
        reward = 0.0
        if next_player_pokemon.current_hp == 0:
            reward = -1.0
        elif next_opponent_pokemon.current_hp == 0:
            reward = 1.0

        # Update Q-Table
        current_q = self.q_table[current_state][action]
        next_max_q = np.max(self.q_table[next_state])
        new_q = current_q + ALPHA * (reward + GAMMA * next_max_q - current_q)
        self.q_table[current_state][action] = new_q

        return reward