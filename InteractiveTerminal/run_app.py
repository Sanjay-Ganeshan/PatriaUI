import sys

sys.dont_write_bytecode = True

import kivy
from kivy.config import Config

Config.set("input", "mouse", "mouse,multitouch_on_demand")


import os

from kivy.resources import resource_add_path

mydir = os.path.dirname(os.path.abspath(__file__))
resource_add_path(os.path.join(mydir, "images"))

import typing as T

from kivy.core.window import Window
from kivymd.app import MDApp

from .new_models.events.view_events import (SwitchFocusedCharacter,
                                            SwitchFocusedView)
from .new_models.specific.galina import GalinaNovikova
from .new_models.specific.lumina import LuminaGale
from .new_models.specific.silvia import SilviaFerreyra
from .new_models.state.state_manager import StateManager
from .new_models.state.view_state import Views
from .views.home import Home

# Replace these with character's current info

class PatriaApp(MDApp):
    def build(self):
        self.state_manager = StateManager()
        self.state_manager.game_state.characters["lumina"] = LuminaGale()
        self.state_manager.game_state.characters["galina"] = GalinaNovikova()
        self.state_manager.game_state.characters["silvia"] = SilviaFerreyra()
        self.home = Home()
        self.home.state_manager = self.state_manager
        self.state_manager.push_event(SwitchFocusedView(new_focus=Views.CHARACTER_DETAILS))
        self.state_manager.push_event(SwitchFocusedCharacter(new_focus="lumina"))
        return self.home


def main():
    Window.size = (1200, 800)
    Window.left = 100
    Window.top = 100
    app = PatriaApp()
    app.run()
