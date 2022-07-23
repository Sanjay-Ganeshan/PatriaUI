import dataclasses
import typing as T
import importlib

from .roll_status import RollStatus
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
        self.app = None

        self.load_character("lumina:LuminaGale")
        self.change_character(self.load_character("galina:GalinaNovikova"))

    def set_app_instance(self, app):
        self.app = app
    
    def _update_app(self):
        if self.app is not None:
            self.app.character_sheet.constants = self.character_list[self.current_character]

    def get_current_character(self) -> Constants:
        return self.character_list[self.current_character]
    
    def change_character(self, new_char_id: int) -> Constants:
        assert new_char_id >= 0 and new_char_id < len(self.character_list), f"Bad ID: {new_char_id}"
        self.current_character = new_char_id
        self._update_app()

    def _load_save_data(save_data: str) -> T.Dict[str, T.Any]:
        raise NotImplementedError("Save data does not work yet")

    def load_character(self, character_type: str, save_data: T.Optional[str] = None) -> int:
        """
        character_type is a module:classname in character_info
        save_data can point to a save to load state from
        """
        # Get the module
        modname, classname = character_type.split(":")
        mod = importlib.import_module(
            f".character_info.{modname}", __package__
        )
        clazz = getattr(mod, classname)
        
        if save_data is not None:
            kwargs = self._load_save_data(save_data)
        else:
            kwargs = {}
        
        inst = clazz(**kwargs)
        self.character_list.append(inst)
        return len(self.character_list)-1

    def adjust_current_character(self, **replacements) -> None:
        self.character_list[self.current_character] = dataclasses.replace(
            self.character_list[self.current_character], **replacements
        )
        self._update_app()

    def change_roll_status(self, new_role_status: RollStatus):
        self.adjust_current_character(
            NEXT_ROLL_STATUS = new_role_status,
        )


THE_GAME = GameState()