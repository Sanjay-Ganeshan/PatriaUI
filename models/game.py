import dataclasses
import typing as T
from .character import Constants

class CharacterList(list):
    pass


class GameLog:
    def __init__(self):
        self.logs = []
        self.callbacks = []

    def log(self, msg):
        self.logs.append(msg)
        print(msg)
        for each_callback in self.callbacks:
            each_callback(msg)

    def bind(self, callback):
        self.callbacks.append(callback)


class GameState:
    def __init__(self) -> None:
        self.current_character = 0
        self.character_list: T.List[Constants] = CharacterList()
        self.game_log = GameLog()

        self.character_list.append(Constants())
        self.app = None

    def set_app_instance(self, app):
        self.app = app
    
    def adjust_current_character(self, **replacements) -> None:
        self.character_list[self.current_character] = dataclasses.replace(
            self.character_list[self.current_character], **replacements
        )
        if self.app is not None:
            self.app.character_sheet.constants = self.character_list[self.current_character]



THE_GAME = GameState()