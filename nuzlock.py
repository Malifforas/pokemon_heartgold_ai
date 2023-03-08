from api import PokemonAPI

# Create an instance of the PokemonAPI class to access information about the game
api = PokemonAPI()

# Nuzlocke rules:

# list to keep track of caught pokemon
caught_pokemon = []

# dictionary to keep track of visited areas
visited_areas = {}

# function to check if a pokemon has already been caught
class Nuzlock:
    def __init__(self, api):
        self.api = api
        self.caught_pokemon = []
        self.visited_areas = {}
def is_pokemon_caught(pokemon_name):
    for pokemon in caught_pokemon:
        if pokemon["name"] == pokemon_name:
            return True
    return False

# function to catch a new pokemon
def catch_pokemon(pokemon_name):
    if not is_pokemon_caught(pokemon_name):
        caught_pokemon.append({"name": pokemon_name})
        print(f"Congratulations! You caught a {pokemon_name}.")
    else:
        print(f"You've already caught a {pokemon_name}.")

# function to check if player is allowed to catch a pokemon in a new area
def can_catch_pokemon(area_name):
    if area_name not in visited_areas:
        visited_areas[area_name] = True
        return True
    return False

# function to handle a wild pokemon encounter
def handle_encounter(pokemon_name, area_name, is_double_battle=False):
    if can_catch_pokemon(area_name):
        if is_double_battle:
            print(f"You encountered a double battle with {pokemon_name[0]} and {pokemon_name[1]}!")
            choice = input("Which Pokemon would you like to catch? Enter 1 or 2: ")
            if choice == "1":
                catch_pokemon(pokemon_name[0])
            elif choice == "2":
                catch_pokemon(pokemon_name[1])
            else:
                print("Invalid choice, no Pokemon were caught.")
        else:
            catch_pokemon(pokemon_name)
    else:
        print("You cannot catch any Pokemon in this area.")
# Pokemon death rules:
# Permanently remove any Pokemon that faints from the player's team.
# Prevent the player from using the Revival Blessing move to bring back dead Pokemon.

def remove_fainted_pokemon(party):
    """
    Removes any fainted Pokemon from the player's team.
    """
    for pokemon in party:
        if pokemon.current_hp == 0:
            print(f"{pokemon.name} has fainted and is permanently removed from your team.")
            party.remove(pokemon)

def prevent_revival_blessing(pokemon):
    """
    Prevents the player from using the Revival Blessing move to bring back dead Pokemon.
    """
    if pokemon.current_hp == 0:
        print(f"{pokemon.name} has fainted and cannot be revived with the Revival Blessing move.")
        return False
    return True


# Gameplay rules

# Prompt the player to give nicknames to all newly caught Pokemon
def nickname_pokemon(pokemon):
    nickname = input(f"What would you like to nickname your {pokemon['name']}? ")
    pokemon['nickname'] = nickname

# The player can only use Pokemon that they have caught themselves
def is_owned_pokemon(pokemon, owned_pokemon):
    return pokemon in owned_pokemon

# Fainted Pokemon can be put in the Pokemon Storage System permanently rather than releasing them
def store_fainted_pokemon(pokemon, storage_system):
    storage_system.append(pokemon)

# The player's starter Pokemon must be randomly chosen based on the last digit of the player's Trainer ID number or using the Trainer ID modulo 3
def choose_starter(trainer_id):
    starters = {
        0: {'name': 'Chikorita', 'type': 'Grass'},
        1: {'name': 'Cyndaquil', 'type': 'Fire'},
        2: {'name': 'Totodile', 'type': 'Water'}
    }
    last_digit = int(str(trainer_id)[-1])
    return starters[last_digit % 3]

# Prevent the player from over-leveling their Pokemon above the next gym leader's highest level Pokemon or the previous Elite Four member's highest level Pokemon

# Return the highest level Pokemon among the player's team
def get_highest_level_pokemon(owned_pokemon):
    levels = [pokemon['level'] for pokemon in owned_pokemon]
    if levels:
        return max(levels)
    else:
        return 0

# Return the highest level Pokemon among the next gym leader's or previous Elite Four member's team
def get_next_highest_level_pokemon(game_progress, gyms):
    next_gym_index = game_progress['current_gym']
    if next_gym_index < len(gyms):
        gym = gyms[next_gym_index]
        highest_level_pokemon = max(gym['pokemon'], key=lambda p: p['level'])
    else:
        highest_level_pokemon = max(game_progress['elite_four'], key=lambda p: p['level'])
    return highest_level_pokemon['level']

# Check if the player's owned Pokemon levels are within the allowed range
def check_owned_pokemon_levels(owned_pokemon, game_progress, gyms):
    highest_owned_level = get_highest_level_pokemon(owned_pokemon)
    highest_allowed_level = get_next_highest_level_pokemon(game_progress, gyms)
    return highest_owned_level <= highest_allowed_level