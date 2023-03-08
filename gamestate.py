from screen import Screen

class GameState:
    def __init__(self, emulator):
        self.emulator = emulator
        self.screen = Screen('gameplay', matcher=self.emulator.battle_menu_matcher)

    def is_in_battle(self):
        return self.screen.is_loaded()