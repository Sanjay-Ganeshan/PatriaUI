from json import JSONDecodeError
import sys

sys.dont_write_bytecode = True

import kivy
from kivy.config import Config

Config.set("input", "mouse", "mouse,multitouch_on_demand")


import os

from kivy.resources import resource_add_path, resource_find

mydir = os.path.dirname(os.path.abspath(__file__))
resource_add_path(os.path.join(mydir, "images"))
resource_add_path(os.path.join(mydir, "fonts"))
resource_add_path(os.path.join(mydir, "sfx"))

FONT = resource_find("Montserrat-SemiBold.ttf")

import typing as T
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.font_definitions import theme_font_styles

from .new_models.events.view_events import (LoadFinished)
from .new_models.specific.galina import GalinaNovikova
from .new_models.specific.lumina import LuminaGale
from .new_models.specific.silvia import SilviaFerreyra
from .new_models.state.state_manager import StateManager
from .new_models.state.view_state import Views
from .views.home import Home
from .save.file_io import path_for
from .save.powerful_json import loads, dumps

# Replace these with character's current info

class PatriaApp(MDApp):
    def __init__(self, state_manager: StateManager, **kwargs):
        super().__init__(**kwargs)

        self.state_manager = state_manager

    def build(self):
        for each_style in theme_font_styles:
            self.theme_cls.font_styles[each_style][0] = FONT 
        
        self.home = Home()
        self.home.state_manager = self.state_manager

        # Everything's wired up to respond to events, so just send
        # a no-op event down the pipeline so everything refreshes.
        self.home.state_manager.push_event(LoadFinished())
        return self.home


def main():
    Window.size = (1200, 800)
    Window.left = 100
    Window.top = 100

    SAVE_PATH = path_for("STATE")

    init_with_default: bool = True

    if os.path.isfile(SAVE_PATH):
        with open(SAVE_PATH, "r") as f:
            save_contents = f.read()
        try:
            state_manager = loads(save_contents)
        except (JSONDecodeError, ValueError) as err:
            print("SAVE FILE CORRUPTED. STARTING FRESH.")
        else:
            init_with_default = False
    
    if init_with_default:
        state_manager = StateManager()
        state_manager.game_state.characters["lumina"] = LuminaGale()
        state_manager.game_state.characters["galina"] = GalinaNovikova()
        state_manager.game_state.characters["silvia"] = SilviaFerreyra()
        state_manager.view_state.focused_character = "lumina"

    app = PatriaApp(state_manager)
    app.run()

    with open(SAVE_PATH, "w") as f:
        f.write(dumps(state_manager, indent=2))
    
