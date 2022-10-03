from kivymd.uix.boxlayout import MDBoxLayout

from .shared.box_sized_mixin import BoxSized
from .shared.needs_character_mixin import NeedsConstants
from ..models.app_settings import BOX_HEIGHT, BOX_WIDTH, AppSettings
from .character_header import CharacterGeneralInfo
from .general_controls import GameLogAndControls
from .shared.spacer import Spacer
from .character_details import DetailsSheet
from .map.map_view import MapView
from .shared.needs_map_mixin import NeedsMap

from kivy.core.window import Window



class CenterHolder(MDBoxLayout, BoxSized, NeedsConstants, NeedsMap):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=10,
            orientation="vertical",
            **kwargs,
        )

        self.details = DetailsSheet()
        self.mapv = MapView()
        self.empty = Spacer(box_width=BOX_WIDTH, box_height=10)

        self.box_init()
        self.constants_init()
        self.map_init()

        self.possible_views = [self.details, self.mapv]
        self.which_view = 0

        self.add_widget(self.possible_views[self.which_view])

    def switch_view(self) -> None:
        self.remove_widget(self.possible_views[self.which_view])
        self.which_view += 1
        self.which_view %= len(self.possible_views)
        self.add_widget(self.possible_views[self.which_view])

class CharacterSheet(MDBoxLayout, BoxSized, NeedsConstants, NeedsMap):
    """
    All character info
    """

    def __init__(self, **kwargs):
        super().__init__(
            size_hint=(1.0, 1.0),
            box_width=BOX_WIDTH,
            box_height=BOX_HEIGHT,
            orientation="vertical",
            **kwargs,
        )
        self.box_init()
        self.constants_init()
        self.map_init()

        # General info
        self.character = CharacterGeneralInfo()

        self.details = CenterHolder()

        self.game_log_window = GameLogAndControls()

        self.rest = Spacer(
            box_width=BOX_WIDTH,
            box_height=(
                BOX_HEIGHT
                - sum(
                    [
                        self.character.box_height,
                        self.game_log_window.box_height,
                        self.details.box_height,
                    ]
                )
            ),
        )

        self.add_widget(self.character)
        self.add_widget(self.details)
        self.add_widget(self.rest)
        self.add_widget(self.game_log_window)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, "text")
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(
            on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up
        )

    def _keyboard_closed(self):
        print("My keyboard have been closed!")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "h":
            AppSettings.TooltipsEnabled = not AppSettings.TooltipsEnabled
            # Return True to accept the key. Otherwise, it will be used by
            # the system.
            return True

        # print('The key', keycode, 'have been pressed')
        # print(' - text is %r' % text)
        # print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == "escape":
            keyboard.release()

        return False

    def _on_keyboard_up(self, keyboard, keycode):
        return False
