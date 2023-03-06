import requests


class Pokemon:
    def __init__(self, name):
        self.name = name
        self.url = f"https://pokeapi.co/api/v2/pokemon/{name}"

    def get_info(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            return {
                'name': data['name'],
                'id': data['id'],
                'types': [type['type']['name'] for type in data['types']],
                'moves': [move['move']['name'] for move in data['moves']]
            }
        else:
            return None
