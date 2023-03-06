import sys
import os

sys.path.append(os.path.abspath('pokeapi'))
from emulator.desmu import Emulator
from pokeapi.api import PokemonAPI
from screen import Screen


def main():
    # Initialize objects
    emulator = Emulator()
    api = PokemonAPI()
    screen = Screen()

    # Load up the game on the emulator
    emulator.press_start()

    # Select continue game
    emulator.press_a()
    emulator.press_a()

    # Wait for game to load
    screen.wait_until_loaded()

    # Get the player's current position
    player_position = screen.get_player_position()

    # Get the nearby pokemon
    nearby_pokemon = screen.get_nearby_pokemon()

    # Get information on the nearby pokemon from the API
    for pokemon in nearby_pokemon:
        pokemon_data = api.get_pokemon_info(pokemon)
        print(pokemon_data)

    # Move the player to a new position
    new_position = (player_position[0], player_position[1] + 1)
    screen.move_player_to(new_position)
    emulator.press_a()

if __name__ == '__main__':
    main()
