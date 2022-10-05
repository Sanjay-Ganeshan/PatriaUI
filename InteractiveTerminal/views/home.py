# The main page, regardless of contents
from kivymd.uix.boxlayout import MDBoxLayout


from .shared.box_sized_mixin import BoxSized
from .shared.listens_for_state_changes import ListenForStateChanges

from .page.header import Header
from .page.footer import Footer
from .page.body import Body

from ..new_models.state.app_settings import BOX_HEIGHT, BOX_WIDTH, AppSettings
from ..new_models.state.view_state import ViewState
from ..new_models.state.state_manager import StateManager
from ..new_models.events.ev_base import GameOrViewEvent

from kivy.properties import ObjectProperty

from kivy.core.window import Window




class Home(MDBoxLayout, BoxSized, ListenForStateChanges):
    """
    The full screen's worth of content
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
        self.listener_init()

        self.header = Header()
        self.body = Body()
        self.footer = Footer()

        self.add_widget(self.header)
        self.add_widget(self.body)
        self.add_widget(self.footer)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, "text")
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(
            on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up
        )


    def listener(self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager) -> None:
        pass

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

        # If we hit escape, release the keyboard
        if keycode[1] == "escape":
            keyboard.release()

        return False

    def _on_keyboard_up(self, keyboard, keycode):
        return False
