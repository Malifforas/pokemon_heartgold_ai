import requests


class PokemonAPI:
    def __init__(self):
        self.base_url = 'https://pokeapi.co/api/v2/'

    def get_pokemon_info(self, pokemon_name):
        url = f'{self.base_url}pokemon/{pokemon_name}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pokemon_info = {
                'name': data['name'],
                'type': data['types'][0]['type']['name'],
                'moves': [move['move']['name'] for move in data['moves']]
            }
            return pokemon_info
        else:
            raise Exception(f"Error: {response.status_code}")

    def get_move_info(self, move_name):
        url = f'{self.base_url}move/{move_name}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            move_info = {
                'name': data['name'],
                'type': data['type']['name'],
                'power': data['power'],
                'accuracy': data['accuracy']
            }
            return move_info
        else:
            raise Exception(f"Error: {response.status_code}")