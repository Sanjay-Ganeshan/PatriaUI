import kivy
from kivy.config import Config

from InteractiveTerminal.models.game import THE_GAME
Config.set("input", "mouse", "mouse,multitouch_on_demand")

import os
from kivy.resources import resource_add_path

mydir = os.path.dirname(os.path.abspath(__file__))
resource_add_path(os.path.join(mydir, "images"))

from kivymd.app import MDApp

from kivy.core.window import Window

from kivymd.font_definitions import theme_font_styles
import typing as T

from .kvcomponents.character_sheet import CharacterSheet






# Replace these with character's current info

class PatriaApp(MDApp):
    def build(self):
        print(theme_font_styles)
        #for each_style in theme_font_styles:
        # self.theme_cls.font_styles[each_style][0] = "ALIENLEAGUEBOLD"
        #    print(each_style, self.theme_cls.font_styles[each_style])

        THE_GAME.set_app_instance(self)
        self.character_sheet = CharacterSheet()
        self.character_sheet.constants = THE_GAME.get_current_character()
        THE_GAME.game_log.log("Welcome!")
        print(THE_GAME.get_character(THE_GAME.get_character_id_with_name("Lumina")[0]).get_weapons())

        return self.character_sheet


if __name__ == "__main__":
    Window.size = (1200, 800)
    Window.left = 100
    Window.top = 100
    app = PatriaApp()
    app.run()
