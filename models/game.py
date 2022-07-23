import dataclasses
import typing as T
import importlib

from .weapon import Weapon
from .roll_status import RollStatus
from .character import Constants
from .. import save
import inspect

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
        self.weapon_lookup: T.Dict[str, Weapon] = {}
        self.game_log = GameLog()
        self.app = None
        self.restore_state()
        self._add_default_characters()

    def set_app_instance(self, app):
        self.app = app
        self.app.bind(on_stop=self.on_stop)
    
    def _update_app(self):
        if self.app is not None:
            self.app.character_sheet.constants = self.character_list[self.current_character]

    def register_weapon(self, wep: Weapon) -> str:
        while (s_id := str(wep.short_name)) in self.weapon_lookup:
            pass

        self.weapon_lookup[s_id] = wep

        return s_id

    def get_weapon(self, wep_id: str) -> Weapon:
        return self.weapon_lookup[wep_id]

    def get_current_character(self) -> Constants:
        return self.get_character()

    def get_character(self, which_id: T.Optional[int] = None) -> Constants:
        i = self.current_character if which_id is None else which_id
        return self.character_list[i]
    
    def change_character(self, new_char_id: T.Optional[int] = None) -> Constants:
        if new_char_id is None:
            new_char_id = (self.current_character + 1) % len(self.character_list)
        assert new_char_id >= 0 and new_char_id < len(self.character_list), f"Bad ID: {new_char_id}"
        self.current_character = new_char_id
        self._update_app()
    
    def get_character_id_with_name(self, name_prefix: str) -> T.List[int]:
        found = [ix for (ix, c) in enumerate(self.character_list) if c.CHARACTER_NAME.lower().startswith(name_prefix.lower())]
        return found

    def _add_default_characters(self) -> None:
        from .weapon_info.character_specific_weapons import LuminaDMR, LuminaPistol

        if not len(self.get_character_id_with_name("Lumina")) > 0:
            ch_id = self.create_character("lumina:LuminaGale")
            char = self.get_character(ch_id)
            self.equip(
                ch_id,
                self.register_weapon(LuminaDMR()),
            )
            self.equip(
                ch_id,
                self.register_weapon(LuminaPistol()),
            )
            
        
        if not self.get_character_id_with_name("Galina"):
            self.create_character("galina:GalinaNovikova")

    def on_stop(self, *args):
        #self._export_save_data()
        pass

    def export_obj(self, obj: T.Any, obj_id: str, obj_prefix: str) -> None:
        modname = ".".join(inspect.getmodule(obj).__name__.split(".")[-2])
        classname = type(obj).__name__
        d = obj.to_dict()
        d["modname"] = modname
        d["classname"] = classname
        save.save(d, f"{obj_prefix}_{obj_id}")

    def _export_save_data(self):
        for each_char in self.character_list:
            chid = each_char.CHARACTER_NAME.split()[0].lower()
            self.export_obj(each_char, chid, "ch")
            
        for wp_id in self.weapon_lookup:
            self.export_obj(self.weapon_lookup[wp_id], wp_id, "wp")
    
    def restore_state(self):
        for each_obj in save.query():
            if each_obj.startswith("ch"):
                self.character_list.append(self.import_obj(each_obj))
            
            if each_obj.startswith("wp"):
                self.weapon_lookup[each_obj[len("wp_"):]] = self.import_obj(each_obj)

    def import_obj(self, save_data: str, **overrides) -> int:
        d = save.load(save_data)
        modname = d.pop("modname")
        classname = d.pop("classname")
        final_overrides = {}
        final_overrides.update(d)
        final_overrides.update(overrides)
        return self.create_obj(f"{modname}:{classname}", **final_overrides)

    def create_character(self, char_type: str, **overrides) -> int:
        ch = self.create_obj(f"character_info.{char_type}", **overrides)
        self.character_list.append(ch)
        return len(self.character_list) - 1

    def create_obj(self, obj_type: str, **overrides) -> T.Any:
        """
        obj_type is a module:classname in models/
        save_data can point to a save to load state from
        """
        # Get the module
        modname, classname = obj_type.split(":")
        mod = importlib.import_module(
            f".{modname}", __package__
        )
        clazz = getattr(mod, classname)
        
        inst = clazz(**overrides)
        return inst

    def adjust_current_character(self, chr_id: T.Optional[int] = None, **replacements) -> None:
        if chr_id is None:
            chr_id = self.current_character
        
        self.character_list[self.current_character] = dataclasses.replace(
            self.character_list[self.current_character], **replacements
        )
    
        if chr_id == self.current_character:
            self._update_app()

    def change_roll_status(self, new_role_status: RollStatus):
        self.adjust_current_character(
            NEXT_ROLL_STATUS = new_role_status,
        )

    def equip(self, chr_id: int, wep_id: str) -> None:
        new_val = self.get_character(chr_id).WEAPONS + (wep_id,)
        print(new_val)
        self.adjust_current_character(
            chr_id,
            WEAPONS = new_val
        )


THE_GAME = GameState()