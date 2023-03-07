class Nuzlock:
    def __init__(self):
        self.caught_pokemon = set()
        self.visited_areas = set()
        self.current_area = None
        self.first_encounter = True

    def set_current_area(self, area_name):
        self.current_area = area_name

    def is_first_encounter(self):
        return self.first_encounter

    def set_first_encounter(self, value):
        self.first_encounter = value

    def is_caught(self, pokemon_name):
        return pokemon_name in self.caught_pokemon

    def add_to_caught(self, pokemon_name):
        self.caught_pokemon.add(pokemon_name)

    def is_visited(self, area_name):
        return area_name in self.visited_areas

    def add_to_visited(self, area_name):
        self.visited_areas.add(area_name)

    def can_catch_pokemon(self):
        return self.first_encounter and not self.is_caught(self.current_area)

    def reset(self):
        self.caught_pokemon = set()
        self.visited_areas = set()
        self.current_area = None
        self.first_encounter = True
