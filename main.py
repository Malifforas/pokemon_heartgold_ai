from random import randint
from time import sleep

import config
from api import PokemonAPI
from desmu import Emulator
from nuzlock import Nuzlock
from screen import Screen

screen = Screen()
screen.capture_screenshot()
game_state = screen.get_game_state()

def main():
    # Initialize objects
    emulator = Emulator()
    api = PokemonAPI()
    screen = Screen()
    nuzlock = Nuzlock(api)

    # Load up the game on the emulator
    emulator.press_start()
    emulator.press_a()
    emulator.press_a()

    # Wait for game to load
    screen.wait_until_loaded()

    while True:
        # Check for nuzlocke rules
        nuzlock.check_rules(screen, emulator)

        # Get the player's current position
        player_position = screen.get_player_position()

        # Get the nearby pokemon
        nearby_pokemon = screen.get_nearby_pokemon()

        # Get information on the nearby pokemon from the API
        for pokemon in nearby_pokemon:
            pokemon_data = api.get_pokemon_info(pokemon)
            print(pokemon_data)

        # Move the player to a new position
        direction = ['up', 'down', 'left', 'right'][randint(0, 3)]
        new_position = screen.get_new_position(player_position, direction)
        screen.move_player_to(new_position)
        emulator.move(direction)
        sleep(1)

# Use the configuration settings
print(config.SCREEN_WIDTH)
print(config.BUTTON_A)

if __name__ == '__main__':
    main()